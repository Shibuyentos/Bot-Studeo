# src/scheduler.py — Agendamento de tarefas com APScheduler

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config import get_settings
from src.scraper.auth import login, AuthenticationError
from src.scraper.client import StudeoClient
from src.scraper.deadlines import fetch_deadlines, fetch_announcements
from src.scraper.grades import fetch_grades
from src.storage.queries import (
    detect_and_save_changes,
    get_upcoming_deadlines,
    mark_deadline_notified,
    log_scrape_start,
    log_scrape_end,
)

logger = logging.getLogger(__name__)


def run_scrape(telegram_app=None) -> None:
    """Executa um ciclo completo de scraping.

    1. Autentica no Studeo
    2. Busca prazos e notas
    3. Salva no banco e detecta mudanças
    4. Envia notificações se houver novidades
    """
    settings = get_settings()
    log_id = log_scrape_start()

    logger.info("═══ Iniciando scrape às %s ═══", datetime.now().strftime("%d/%m/%Y %H:%M"))

    try:
        with StudeoClient() as client:
            # 1. Autenticar
            username = settings.studeo_ra or settings.studeo_cpf
            if not username or not settings.studeo_senha:
                raise AuthenticationError("RA/CPF ou senha não configurados no .env")

            auth_info = login(client, username, settings.studeo_senha)
            logger.info("Autenticado como: %s", auth_info.user_name or "N/A")

            # 2. Buscar dados
            deadlines = fetch_deadlines(client)
            grades = fetch_grades(client)
            announcements = fetch_announcements(client)

            total_items = len(deadlines) + len(grades) + len(announcements)
            logger.info("Dados coletados: %d prazos, %d notas, %d avisos", len(deadlines), len(grades), len(announcements))

            # 3. Salvar e detectar mudanças
            report = detect_and_save_changes(deadlines, grades, announcements)

            # 4. Notificar via Telegram
            if telegram_app and report.has_changes:
                from src.integrations.telegram_bot import notify_changes
                try:
                    asyncio.get_event_loop().run_until_complete(
                        notify_changes(telegram_app, report)
                    )
                except RuntimeError:
                    # Se já está dentro de um event loop
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(notify_changes(telegram_app, report))
                    loop.close()

            log_scrape_end(log_id, status="success", items_found=total_items)
            logger.info("═══ Scrape concluído: %d itens, %d mudanças ═══",
                        total_items, report.total_changes)

    except AuthenticationError as e:
        logger.error("Falha de autenticação: %s", e)
        log_scrape_end(log_id, status="auth_failed", error_message=str(e))

    except Exception as e:
        logger.error("Erro no scrape: %s", e, exc_info=True)
        log_scrape_end(log_id, status="error", error_message=str(e))


def check_upcoming_deadlines(telegram_app=None) -> None:
    """Verifica prazos se aproximando e notifica.

    Notifica em: 7 dias, 3 dias, 1 dia, HOJE.
    Usa only_unnotified=True para não re-notificar prazos já enviados.
    Após notificar, marca cada prazo com notified=1.
    """
    logger.info("Verificando prazos próximos...")

    for days in [7, 3, 1, 0]:
        deadlines = get_upcoming_deadlines(days=days, only_unnotified=True)
        if deadlines and telegram_app:
            from src.integrations.telegram_bot import notify_upcoming_deadlines
            try:
                asyncio.get_event_loop().run_until_complete(
                    notify_upcoming_deadlines(telegram_app, deadlines)
                )
            except RuntimeError:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(
                    notify_upcoming_deadlines(telegram_app, deadlines)
                )
                loop.close()

            # Marcar prazos como notificados para não repetir
            for dl in deadlines:
                mark_deadline_notified(dl["id"])
            logger.info("%d prazos marcados como notificados", len(deadlines))

            break  # Notifica apenas o nível mais urgente


def create_scheduler(telegram_app=None) -> BackgroundScheduler:
    """Cria e configura o scheduler com os jobs.

    Jobs:
    1. Scraping a cada N horas (padrão: 6h)
    2. Verificação de prazos a cada N horas (padrão: 12h)

    Returns:
        BackgroundScheduler configurado (ainda não iniciado)
    """
    settings = get_settings()
    scheduler = BackgroundScheduler()

    # Job 1: Scraping periódico
    scheduler.add_job(
        run_scrape,
        trigger=IntervalTrigger(hours=settings.scrape_interval_hours),
        kwargs={"telegram_app": telegram_app},
        id="scrape_job",
        name=f"Scraping a cada {settings.scrape_interval_hours}h",
        replace_existing=True,
    )

    # Job 2: Verificação de prazos
    scheduler.add_job(
        check_upcoming_deadlines,
        trigger=IntervalTrigger(hours=settings.deadline_check_interval_hours),
        kwargs={"telegram_app": telegram_app},
        id="deadline_check_job",
        name=f"Check prazos a cada {settings.deadline_check_interval_hours}h",
        replace_existing=True,
    )

    logger.info(
        "Scheduler configurado: scrape=%dh, check_deadlines=%dh",
        settings.scrape_interval_hours,
        settings.deadline_check_interval_hours,
    )

    return scheduler
