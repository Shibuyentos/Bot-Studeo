# src/storage/models.py — Modelos de dados e DDL do SQLite

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

# ── DDL — Criação das tabelas ────────────────────────────────────────────

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS disciplines (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT NOT NULL,
        code            TEXT,
        semester        TEXT,
        status          TEXT DEFAULT 'em_andamento',
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(name, semester)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS deadlines (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        discipline_id   INTEGER REFERENCES disciplines(id),
        type            TEXT NOT NULL,
        title           TEXT,
        due_date        TIMESTAMP NOT NULL,
        status          TEXT DEFAULT 'pendente',
        discovered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notified        INTEGER DEFAULT 0,
        UNIQUE(discipline_id, type, title, due_date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS grades (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        discipline_id   INTEGER REFERENCES disciplines(id),
        type            TEXT NOT NULL,
        value           REAL,
        weight          REAL,
        recorded_at     TIMESTAMP,
        discovered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(discipline_id, type)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS materials (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        discipline_id   INTEGER REFERENCES disciplines(id),
        title           TEXT,
        type            TEXT,
        url             TEXT,
        local_path      TEXT,
        downloaded_at   TIMESTAMP,
        UNIQUE(discipline_id, url)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS announcements (
        id              INTEGER PRIMARY KEY,
        sender_name     TEXT,
        text            TEXT,
        category        TEXT,
        sent_at         TIMESTAMP,
        is_read         INTEGER DEFAULT 0,
        status          TEXT,
        discovered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notified        INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS scrape_log (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at      TIMESTAMP NOT NULL,
        finished_at     TIMESTAMP,
        status          TEXT NOT NULL,
        items_found     INTEGER DEFAULT 0,
        error_message   TEXT
    )
    """,
]

# ── Dataclasses ──────────────────────────────────────────────────────────


@dataclass
class Discipline:
    id: int | None = None
    name: str = ""
    code: str | None = None
    semester: str | None = None
    status: str = "em_andamento"
    created_at: datetime | None = None


@dataclass
class DeadlineRecord:
    id: int | None = None
    discipline_id: int | None = None
    type: str = ""
    title: str = ""
    due_date: datetime | None = None
    status: str = "pendente"
    discovered_at: datetime | None = None
    notified: bool = False


@dataclass
class GradeRecord:
    id: int | None = None
    discipline_id: int | None = None
    type: str = ""
    value: float | None = None
    weight: float | None = None
    recorded_at: datetime | None = None
    discovered_at: datetime | None = None


@dataclass
class ScrapeLogRecord:
    id: int | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    status: str = ""
    items_found: int = 0
    error_message: str | None = None


@dataclass
class AnnouncementRecord:
    id: int | None = None
    sender_name: str = ""
    text: str = ""
    category: str = ""
    sent_at: datetime | None = None
    is_read: bool = False
    status: str = ""
    discovered_at: datetime | None = None
    notified: bool = False


@dataclass
class AnnouncementRecord:
    id: int | None = None
    sender_name: str = ""
    text: str = ""
    category: str = ""
    sent_at: datetime | None = None
    is_read: bool = False
    status: str = ""
    discovered_at: datetime | None = None
    notified: bool = False
