# src/main.py — Entry point do Bot-Studeo

from __future__ import annotations

import logging
import signal
import sys

from src.config import get_settings
from src.storage.database import init_db, close_db
from src.scheduler import create_scheduler, run_scrape
from src.integrations.telegram_bot import create_telegram_app

from pathlib import Path

# ── Logging ──────────────────────────────────────────────────────────────

# Garantir que o diretório de dados existe para o log
Path("data").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/bot-studeo.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("bot-studeo")


def main() -> None:
    """Inicializa e roda o Bot-Studeo."""

    logger.info("🎓 Bot-Studeo — Iniciando...")

    # 1. Carregar configurações
    settings = get_settings()
    settings.ensure_dirs()

    # 2. Inicializar banco de dados
    init_db(settings.db_path)
    logger.info("Banco de dados pronto: %s", settings.db_path)

    # 3. Configurar bot Telegram
    telegram_app = create_telegram_app()
    if telegram_app:
        logger.info("Bot Telegram ativo")
    else:
        logger.info("Bot Telegram desativado (token não configurado)")

    # 4. Executar primeiro scrape imediato
    logger.info("Executando primeiro scrape...")
    run_scrape(telegram_app)

    # 5. Iniciar scheduler
    scheduler = create_scheduler(telegram_app)
    scheduler.start()
    logger.info("Scheduler iniciado com %d jobs", len(scheduler.get_jobs()))

    # 6. Manter o processo vivo
    if telegram_app:
        # Se o Telegram está ativo, usa o polling dele (bloqueia)
        logger.info("Iniciando polling do Telegram (Ctrl+C para parar)...")
        telegram_app.run_polling(drop_pending_updates=True)
    else:
        # Sem Telegram, espera sinal de interrupção
        logger.info("Rodando em modo headless (Ctrl+C para parar)...")

        def signal_handler(sig, frame):
            logger.info("Sinal recebido, encerrando...")
            scheduler.shutdown(wait=False)
            close_db()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            # Bloqueia indefinidamente até receber um sinal
            signal.pause()
        except AttributeError:
            # Windows não tem signal.pause() — usar loop simples
            import time
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                pass

    # Cleanup
    scheduler.shutdown(wait=False)
    close_db()
    logger.info("🎓 Bot-Studeo encerrado.")


if __name__ == "__main__":
    main()
