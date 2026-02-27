# src/storage/queries.py — Queries reutilizáveis e detecção de mudanças

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from src.scraper.deadlines import Deadline, Announcement
from src.scraper.grades import Grade
from src.storage.database import get_connection

logger = logging.getLogger(__name__)


# ── Disciplinas ──────────────────────────────────────────────────────────


def upsert_discipline(name: str, code: str | None = None, semester: str | None = None,
                      conn: sqlite3.Connection | None = None) -> int:
    """Insere ou atualiza uma disciplina. Retorna o ID.

    Usa SELECT + INSERT para lidar com NULL em semester
    (SQLite trata NULL como distinto em UNIQUE constraints).
    """
    c = conn or get_connection()

    # Buscar existente (tratando NULL como igual)
    if semester is None:
        row = c.execute(
            "SELECT id FROM disciplines WHERE name = ? AND semester IS NULL",
            (name,),
        ).fetchone()
    else:
        row = c.execute(
            "SELECT id FROM disciplines WHERE name = ? AND semester = ?",
            (name, semester),
        ).fetchone()

    if row:
        # Atualizar code se necessário
        disc_id = row[0]
        if code:
            c.execute("UPDATE disciplines SET code = ? WHERE id = ?", (code, disc_id))
            c.commit()
        return disc_id

    # Inserir nova
    cursor = c.execute(
        "INSERT INTO disciplines (name, code, semester) VALUES (?, ?, ?)",
        (name, code, semester),
    )
    c.commit()
    return cursor.lastrowid


def get_discipline_id(name: str, conn: sqlite3.Connection | None = None) -> int | None:
    """Busca o ID de uma disciplina pelo nome."""
    c = conn or get_connection()
    row = c.execute("SELECT id FROM disciplines WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None


# ── Prazos / Deadlines ──────────────────────────────────────────────────


@dataclass
class ChangeReport:
    """Relatório de mudanças detectadas."""
    new_deadlines: list[Deadline]
    new_grades: list[Grade]
    updated_grades: list[tuple[Grade, float | None]]  # (grade, old_value)
    new_announcements: list[Announcement]

    @property
    def has_changes(self) -> bool:
        return bool(self.new_deadlines or self.new_grades or self.updated_grades or self.new_announcements)

    @property
    def total_changes(self) -> int:
        return len(self.new_deadlines) + len(self.new_grades) + len(self.updated_grades) + len(self.new_announcements)


def save_deadlines(deadlines: list[Deadline],
                   conn: sqlite3.Connection | None = None) -> list[Deadline]:
    """Salva prazos no banco, retornando os que são novos.

    Returns:
        Lista de deadlines que foram inseridos (novos)
    """
    c = conn or get_connection()
    new_items = []

    for dl in deadlines:
        if not dl.due_date:
            continue

        # Garantir que a disciplina existe
        disc_id = upsert_discipline(dl.discipline_name, dl.discipline_code, conn=c)

        # Tentar inserir — se já existe (UNIQUE conflict), ignora
        cursor = c.execute(
            """
            INSERT OR IGNORE INTO deadlines (discipline_id, type, title, due_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (disc_id, dl.type, dl.title, dl.due_date.isoformat(), dl.status),
        )

        if cursor.rowcount > 0:
            new_items.append(dl)
            logger.info("Novo prazo: [%s] %s — %s", dl.type.upper(), dl.discipline_name,
                        dl.due_date.strftime("%d/%m/%Y"))

    c.commit()
    if new_items:
        logger.info("%d novos prazos salvos", len(new_items))
    else:
        logger.info("Nenhum prazo novo")
    return new_items


def get_upcoming_deadlines(days: int = 7,
                           only_unnotified: bool = False,
                           conn: sqlite3.Connection | None = None) -> list[dict]:
    """Busca prazos que vencem nos próximos N dias.

    Args:
        days: Janela de dias à frente
        only_unnotified: Se True, filtra apenas prazos ainda não notificados

    Returns:
        Lista de dicts com dados do prazo
    """
    c = conn or get_connection()
    query = """
        SELECT d.*, disc.name as discipline_name
        FROM deadlines d
        JOIN disciplines disc ON d.discipline_id = disc.id
        WHERE d.status = 'pendente'
          AND d.due_date <= datetime('now', ? || ' days')
          AND d.due_date >= datetime('now')
    """
    if only_unnotified:
        query += "  AND d.notified = 0\n"
    query += "ORDER BY d.due_date ASC"

    rows = c.execute(query, (str(days),)).fetchall()
    return [dict(row) for row in rows]


def mark_deadline_notified(deadline_id: int,
                           conn: sqlite3.Connection | None = None) -> None:
    """Marca um prazo como notificado."""
    c = conn or get_connection()
    c.execute("UPDATE deadlines SET notified = 1 WHERE id = ?", (deadline_id,))
    c.commit()


# ── Notas / Grades ───────────────────────────────────────────────────────


def save_grades(grades: list[Grade],
                conn: sqlite3.Connection | None = None) -> tuple[list[Grade], list[tuple[Grade, float | None]]]:
    """Salva notas no banco, detectando novidades e atualizações.

    Returns:
        (novas, atualizadas) — notas novas e notas que mudaram de valor
    """
    c = conn or get_connection()
    new_items = []
    updated_items = []

    for grade in grades:
        if grade.value is None:
            continue

        disc_id = upsert_discipline(grade.discipline_name, grade.discipline_code, conn=c)

        # Verificar se já existe
        existing = c.execute(
            "SELECT id, value FROM grades WHERE discipline_id = ? AND type = ?",
            (disc_id, grade.type),
        ).fetchone()

        if existing is None:
            # Nova nota
            c.execute(
                """
                INSERT INTO grades (discipline_id, type, value, weight, recorded_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (disc_id, grade.type, grade.value, grade.weight,
                 grade.recorded_at.isoformat() if grade.recorded_at else None),
            )
            new_items.append(grade)
            logger.info("Nova nota: [%s] %s = %.1f",
                        grade.type.upper(), grade.discipline_name, grade.value)
        elif existing["value"] != grade.value:
            # Nota atualizada
            old_value = existing["value"]
            c.execute(
                "UPDATE grades SET value = ?, recorded_at = ? WHERE id = ?",
                (grade.value,
                 grade.recorded_at.isoformat() if grade.recorded_at else None,
                 existing["id"]),
            )
            updated_items.append((grade, old_value))
            logger.info("Nota atualizada: [%s] %s = %.1f → %.1f",
                        grade.type.upper(), grade.discipline_name, old_value or 0, grade.value)

    c.commit()
    return new_items, updated_items


def get_all_grades(conn: sqlite3.Connection | None = None) -> list[dict]:
    """Busca todas as notas com nome da disciplina."""
    c = conn or get_connection()
    rows = c.execute(
        """
        SELECT g.*, disc.name as discipline_name
        FROM grades g
        JOIN disciplines disc ON g.discipline_id = disc.id
        ORDER BY disc.name, g.type
        """,
    ).fetchall()
    return [dict(row) for row in rows]


# ── Scrape Log ───────────────────────────────────────────────────────────


def log_scrape_start(conn: sqlite3.Connection | None = None) -> int:
    """Registra o início de um scrape. Retorna o ID do registro."""
    c = conn or get_connection()
    cursor = c.execute(
        "INSERT INTO scrape_log (started_at, status) VALUES (?, 'running')",
        (datetime.now().isoformat(),),
    )
    c.commit()
    return cursor.lastrowid


def log_scrape_end(log_id: int, status: str, items_found: int = 0,
                   error_message: str | None = None,
                   conn: sqlite3.Connection | None = None) -> None:
    """Registra o fim de um scrape."""
    c = conn or get_connection()
    c.execute(
        """
        UPDATE scrape_log
        SET finished_at = ?, status = ?, items_found = ?, error_message = ?
        WHERE id = ?
        """,
        (datetime.now().isoformat(), status, items_found, error_message, log_id),
    )
    c.commit()


# ── Avisos / Announcements ───────────────────────────────────────────────

def save_announcements(announcements: list[Announcement],
                       conn: sqlite3.Connection | None = None) -> list[Announcement]:
    """Salva avisos no banco, retornando os novos."""
    c = conn or get_connection()
    new_items = []

    for ann in announcements:
        cursor = c.execute(
            """
            INSERT OR IGNORE INTO announcements (id, sender_name, text, category, sent_at, is_read, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (ann.id, ann.sender_name, ann.text, ann.category,
             ann.sent_at.isoformat() if ann.sent_at else None,
             1 if ann.is_read else 0, ann.status),
        )

        if cursor.rowcount > 0:
            new_items.append(ann)
            logger.info("Novo aviso: %s — %s (do ID: %d)", ann.category, ann.sender_name, ann.id)

    c.commit()
    return new_items


def get_recent_announcements(limit: int = 10,
                              conn: sqlite3.Connection | None = None) -> list[dict]:
    """Busca os avisos mais recentes."""
    c = conn or get_connection()
    rows = c.execute(
        """
        SELECT * FROM announcements
        ORDER BY sent_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


# ── Detecção de Mudanças (orquestração) ─────────────────────────────────


def detect_and_save_changes(
    deadlines: list[Deadline],
    grades: list[Grade],
    announcements: list[Announcement] | None = None,
    conn: sqlite3.Connection | None = None,
) -> ChangeReport:
    """Salva dados novos e retorna relatório de mudanças.

    Uso principal: após cada scrape, chamar esta função para saber
    o que mudou e precisa ser notificado.
    """
    announcements = announcements or []
    new_deadlines = save_deadlines(deadlines, conn)
    new_grades, updated_grades = save_grades(grades, conn)
    new_announcements = save_announcements(announcements, conn)

    report = ChangeReport(
        new_deadlines=new_deadlines,
        new_grades=new_grades,
        updated_grades=updated_grades,
        new_announcements=new_announcements,
    )

    if report.has_changes:
        logger.info("Mudanças detectadas: %d novos prazos, %d novas notas, %d notas atualizadas, %d novos avisos",
                    len(new_deadlines), len(new_grades), len(updated_grades), len(new_announcements))
    else:
        logger.info("Nenhuma mudança detectada")

    return report
