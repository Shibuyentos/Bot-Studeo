# src/integrations/telegram_bot.py — Bot Telegram para notificações e comandos

from __future__ import annotations

import logging
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from src.config import get_settings
from src.scraper.client import StudeoClient
from src.scraper.auth import login
from src.scraper.deadlines import Deadline, Announcement, fetch_deadlines
from src.scraper.grades import Grade, fetch_grades, calculate_average
from src.storage.database import get_connection
from src.storage.queries import (
    detect_and_save_changes,
    get_all_grades,
    get_recent_announcements,
    get_recent_changes,
    get_upcoming_deadlines,
)

logger = logging.getLogger(__name__)

# ── Formatação de mensagens ──────────────────────────────────────────────


def format_deadline_message(deadline: Deadline | dict) -> str:
    """Formata um prazo para exibição no Telegram."""
    if isinstance(deadline, dict):
        name = deadline.get("discipline_name", "?")
        dtype = deadline.get("type", "?")
        title = deadline.get("title", "")
        due = deadline.get("due_date", "?")
        status = deadline.get("status", "pendente")
    else:
        name = deadline.discipline_name
        dtype = deadline.type
        title = deadline.title
        due = deadline.due_date.strftime("%d/%m/%Y %H:%M") if deadline.due_date else "?"
        status = deadline.status

    # Calcular dias restantes
    countdown = ""
    try:
        if isinstance(due, str):
            due_dt = datetime.fromisoformat(due)
        elif isinstance(due, datetime):
            due_dt = due
        else:
            due_dt = None

        if due_dt:
            delta = (due_dt - datetime.now()).days
            if delta < 0:
                countdown = " ⚠️ ATRASADO"
            elif delta == 0:
                countdown = " 🔴 HOJE!"
            elif delta <= 3:
                countdown = f" 🟡 {delta} dias"
            elif delta <= 7:
                countdown = f" 🟢 {delta} dias"
            else:
                countdown = f" {delta} dias"
    except Exception:
        pass

    type_emoji = {
        "mapa": "📝", "prova": "📋", "forum": "💬",
        "substitutiva": "🔄", "questionario": "❓",
    }.get(dtype, "📌")

    lines = [f"{type_emoji} *[{dtype.upper()}]* {name}{countdown}"]
    if title:
        lines.append(f"   📎 {title}")
    if isinstance(due, str) and due != "?":
        lines.append(f"   📅 {due}")
    elif isinstance(due, datetime):
        lines.append(f"   📅 {due.strftime('%d/%m/%Y %H:%M')}")

    return "\n".join(lines)


def format_grade_message(grade: Grade | dict) -> str:
    """Formata uma nota para exibição no Telegram."""
    if isinstance(grade, dict):
        name = grade.get("discipline_name", "?")
        gtype = grade.get("type", "?")
        value = grade.get("value")
    else:
        name = grade.discipline_name
        gtype = grade.type
        value = grade.value

    if value is None:
        return f"📊 *{name}* — [{gtype.upper()}]: sem nota"

    # Emoji por faixa
    if value >= 7:
        emoji = "🟢"
    elif value >= 6:
        emoji = "🟡"
    else:
        emoji = "🔴"

    return f"{emoji} *{name}* — [{gtype.upper()}]: *{value:.1f}*"


def format_announcement_message(ann: Announcement | dict) -> str:
    """Formata um aviso para exibição no Telegram."""
    if isinstance(ann, dict):
        cat = ann.get("category", "Aviso")
        sender = ann.get("sender_name", "")
        # Removemos o HTML sujo para o push
        text_preview = "📩 Novo aviso recebido (acesse o Studeo para ler completo)."
    else:
        cat = ann.category
        sender = ann.sender_name
        text_preview = "📩 Novo aviso recebido (acesse o Studeo para ler completo)."
    
    return f"📢 *{cat}*\nDe: _{sender}_\n{text_preview}"


# ── Notificações push ────────────────────────────────────────────────────


async def send_notification(app: Application, message: str) -> None:
    """Envia uma mensagem para o chat configurado."""
    settings = get_settings()
    if not settings.telegram_chat_id:
        logger.warning("TELEGRAM_CHAT_ID não configurado")
        return

    await app.bot.send_message(
        chat_id=settings.telegram_chat_id,
        text=message,
        parse_mode="Markdown",
    )


async def notify_new_grades(app: Application, grades: list[Grade]) -> None:
    """Notifica sobre notas novas."""
    if not grades:
        return

    lines = ["🎓 *NOTAS NOVAS DETECTADAS!*\n"]
    for grade in grades:
        lines.append(format_grade_message(grade))

    await send_notification(app, "\n".join(lines))


async def notify_upcoming_deadlines(app: Application, deadlines: list[dict]) -> None:
    """Notifica sobre prazos se aproximando."""
    if not deadlines:
        return

    lines = ["⏰ *PRAZOS SE APROXIMANDO!*\n"]
    for dl in deadlines:
        lines.append(format_deadline_message(dl))

    await send_notification(app, "\n".join(lines))


async def notify_changes(app: Application, report) -> None:
    """Notifica sobre todas as mudanças detectadas no último scrape."""
    if not report.has_changes:
        return

    lines = [f"🔔 *Studeo — {report.total_changes} novidade(s)!*\n"]

    if report.new_deadlines:
        lines.append("📅 *Novos Prazos:*")
        for dl in report.new_deadlines:
            lines.append(format_deadline_message(dl))
        lines.append("")

    if report.new_grades:
        lines.append("📊 *Notas Novas:*")
        for grade in report.new_grades:
            lines.append(format_grade_message(grade))
        lines.append("")

    if report.updated_grades:
        lines.append("🔄 *Notas Atualizadas:*")
        for grade, old_val in report.updated_grades:
            old = f"{old_val:.1f}" if old_val else "?"
            new = f"{grade.value:.1f}" if grade.value else "?"
            lines.append(f"  {grade.discipline_name} [{grade.type.upper()}]: {old} → {new}")
        lines.append("")

    if getattr(report, "new_announcements", None):
        lines.append("📢 *Novos Avisos:*")
        for ann in report.new_announcements:
            lines.append(format_announcement_message(ann))
            lines.append("")

    await send_notification(app, "\n".join(lines))


# ── Comandos ─────────────────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start — boas-vindas."""
    msg = (
        "🎓 *Bot-Studeo*\n\n"
        "Automação acadêmica para o Studeo (Unicesumar EAD).\n\n"
        "Digite /ajuda para ver os comandos disponíveis."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_prazos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /prazos — lista prazos pendentes."""
    deadlines = get_upcoming_deadlines(days=30)

    if not deadlines:
        await update.message.reply_text("✅ Nenhum prazo pendente nos próximos 30 dias!")
        return

    lines = [f"📅 *Prazos Pendentes ({len(deadlines)})*\n"]
    for dl in deadlines:
        lines.append(format_deadline_message(dl))

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_notas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /notas — lista notas."""
    grades = get_all_grades()

    if not grades:
        await update.message.reply_text("📊 Nenhuma nota registrada ainda.")
        return

    lines = ["📊 *Suas Notas*\n"]
    for grade in grades:
        lines.append(format_grade_message(grade))

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /status — resumo geral."""
    conn = get_connection()

    # Contar disciplinas
    disc_count = conn.execute("SELECT COUNT(*) FROM disciplines").fetchone()[0]

    # Prazos próximos
    upcoming = get_upcoming_deadlines(days=7)

    # Notas
    grades = get_all_grades()
    grade_values = [g["value"] for g in grades if g.get("value") is not None]
    avg = round(sum(grade_values) / len(grade_values), 2) if grade_values else None

    # Último scrape
    last_scrape = conn.execute(
        "SELECT * FROM scrape_log ORDER BY started_at DESC LIMIT 1"
    ).fetchone()

    lines = ["📋 *Status Geral — Bot-Studeo*\n"]
    lines.append(f"📚 Disciplinas: *{disc_count}*")
    lines.append(f"📅 Prazos próximos (7 dias): *{len(upcoming)}*")

    if avg is not None:
        emoji = "🟢" if avg >= 7 else "🟡" if avg >= 6 else "🔴"
        lines.append(f"{emoji} Média geral: *{avg:.1f}*")
    else:
        lines.append("📊 Média: _sem notas_")

    if last_scrape:
        lines.append(f"\n🤖 Último scrape: {last_scrape['started_at']}")
        lines.append(f"   Status: {last_scrape['status']}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_avisos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /avisos — lista avisos recentes."""
    announcements = get_recent_announcements(limit=10)

    if not announcements:
        await update.message.reply_text("📢 Nenhum aviso registrado ainda.")
        return

    lines = [f"📢 *Avisos Recentes ({len(announcements)})*\n"]
    for ann in announcements:
        cat = ann.get("category", "Aviso")
        sender = ann.get("sender_name", "?")
        sent_at = ann.get("sent_at", "")
        date_str = ""
        if sent_at:
            try:
                dt = datetime.fromisoformat(sent_at)
                date_str = f" — {dt.strftime('%d/%m/%Y')}"
            except Exception:
                pass
        lines.append(f"📩 *{cat}*{date_str}\n   De: _{sender}_")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_painel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /painel — dashboard agrupado por disciplina."""
    conn = get_connection()

    # Todas as disciplinas em andamento
    disc_rows = conn.execute(
        "SELECT name FROM disciplines WHERE status = 'em_andamento' ORDER BY name"
    ).fetchall()
    discipline_names = [r["name"] for r in disc_rows]

    if not discipline_names:
        await update.message.reply_text("📋 Nenhuma disciplina em andamento no momento.")
        return

    # Prazos pendentes (janela ampla de 90 dias)
    deadlines = get_upcoming_deadlines(days=90)

    # Agrupar por discipline_name
    grouped: dict[str, list[dict]] = {name: [] for name in discipline_names}
    for dl in deadlines:
        name = dl.get("discipline_name", "")
        if name in grouped:
            grouped[name].append(dl)

    # Montar mensagem
    lines = ["📋 *Painel por Disciplina*\n"]
    for name in discipline_names:
        pending = grouped[name]
        if pending:
            lines.append(f"📚 *{name}* ({len(pending)} pendência(s))")
            for dl in pending:
                lines.append(format_deadline_message(dl))
        else:
            lines.append(f"✅ *{name}* — Nenhuma pendência!")
        lines.append("")  # linha em branco entre disciplinas

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_materiais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /materiais — lista materiais/PDFs por disciplina."""
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT m.title, m.type, m.url, m.local_path, disc.name as discipline_name
        FROM materials m
        JOIN disciplines disc ON m.discipline_id = disc.id
        ORDER BY disc.name, m.title
        """
    ).fetchall()

    if not rows:
        await update.message.reply_text(
            "📂 Nenhum material registrado ainda.\n"
            "_O scraper de materiais será implementado em breve!_",
            parse_mode="Markdown",
        )
        return

    # Agrupar por disciplina
    grouped: dict[str, list] = {}
    for r in rows:
        name = r["discipline_name"]
        grouped.setdefault(name, []).append(r)

    type_emoji = {
        "pdf": "📕", "video": "🎬", "slide": "📊", "livro": "📖", "link": "🔗",
    }

    lines = [f"📂 *Materiais ({len(rows)} arquivo(s))*\n"]
    for disc_name, materials in grouped.items():
        lines.append(f"📚 *{disc_name}*")
        for mat in materials:
            emoji = type_emoji.get(mat["type"], "📄")
            title = mat["title"] or "Sem título"
            if mat["local_path"]:
                lines.append(f"  {emoji} {title} ✅ baixado")
            elif mat["url"]:
                lines.append(f"  {emoji} [{title}]({mat['url']})")
            else:
                lines.append(f"  {emoji} {title}")
        lines.append("")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_novidades(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /novidades — mostra o que apareceu nas últimas 24h."""
    # Aceita argumento opcional: /novidades 48 (últimas 48h)
    hours = 24
    if context.args:
        try:
            hours = max(1, min(int(context.args[0]), 168))  # entre 1h e 7 dias
        except ValueError:
            pass

    changes = get_recent_changes(hours=hours)
    label = changes["since_label"]
    new_deadlines = changes["new_deadlines"]
    new_grades = changes["new_grades"]
    new_announcements = changes["new_announcements"]

    total = len(new_deadlines) + len(new_grades) + len(new_announcements)

    if total == 0:
        await update.message.reply_text(
            f"✅ Nenhuma novidade nas {label}!\n"
            "_Use /atualizar para forçar um scrape agora._",
            parse_mode="Markdown",
        )
        return

    lines = [f"🔔 *Novidades — {label}* ({total} item(s))\n"]

    if new_deadlines:
        lines.append(f"📅 *Novos Prazos ({len(new_deadlines)}):*")
        for dl in new_deadlines:
            lines.append(format_deadline_message(dl))
        lines.append("")

    if new_grades:
        lines.append(f"📊 *Novas Notas ({len(new_grades)}):*")
        for g in new_grades:
            lines.append(format_grade_message(g))
        lines.append("")

    if new_announcements:
        lines.append(f"📢 *Novos Avisos ({len(new_announcements)}):*")
        for ann in new_announcements:
            lines.append(format_announcement_message(ann))
        lines.append("")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ajuda — lista todos os comandos disponíveis."""
    msg = (
        "🎓 *Bot-Studeo — Comandos*\n\n"
        "/painel — Dashboard por disciplina (pendências + livres)\n"
        "/prazos — Prazos pendentes com countdown\n"
        "/notas — Suas notas mais recentes\n"
        "/avisos — Avisos/comunicados recentes\n"
        "/novidades — O que apareceu nas últimas 24h (use /novidades 48 para 48h)\n"
        "/materiais — Materiais e PDFs das disciplinas\n"
        "/status — Resumo geral (disciplinas, média, último scrape)\n"
        "/atualizar — Força um scrape imediato\n"
        "/ajuda — Esta mensagem\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_atualizar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /atualizar — força um scrape imediato."""
    await update.message.reply_text("🔄 Iniciando scrape manual...")

    from src.scheduler import run_scrape
    try:
        run_scrape()
        await update.message.reply_text("✅ Scrape concluído! Use /prazos ou /notas para ver os dados atualizados.")
    except Exception as e:
        logger.error("Erro no scrape manual: %s", e, exc_info=True)
        await update.message.reply_text(f"❌ Erro no scrape: {e}")


# ── Setup ────────────────────────────────────────────────────────────────


def create_telegram_app() -> Application | None:
    """Cria e configura a Application do Telegram.

    Returns:
        Application configurada, ou None se o token não estiver definido
    """
    settings = get_settings()

    if not settings.telegram_bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN não configurado — bot desativado")
        return None

    app = Application.builder().token(settings.telegram_bot_token).build()

    # Registrar handlers de comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("prazos", cmd_prazos))
    app.add_handler(CommandHandler("notas", cmd_notas))
    app.add_handler(CommandHandler("avisos", cmd_avisos))
    app.add_handler(CommandHandler("novidades", cmd_novidades))
    app.add_handler(CommandHandler("painel", cmd_painel))
    app.add_handler(CommandHandler("materiais", cmd_materiais))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("atualizar", cmd_atualizar))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))

    logger.info("Bot Telegram configurado com %d comandos", 10)
    return app
