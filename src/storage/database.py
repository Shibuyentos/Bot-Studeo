# src/storage/database.py — Conexão e setup do SQLite

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from src.storage.models import DDL_STATEMENTS

logger = logging.getLogger(__name__)

_connection: sqlite3.Connection | None = None


def init_db(db_path: str | Path = "data/studeo.db") -> sqlite3.Connection:
    """Inicializa o banco de dados: cria o arquivo e as tabelas.

    Args:
        db_path: Caminho para o arquivo SQLite

    Returns:
        Conexão ativa com o banco
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # retorna dict-like ao invés de tuple
    conn.execute("PRAGMA journal_mode=WAL")  # performance
    conn.execute("PRAGMA foreign_keys=ON")

    # Criar tabelas
    for ddl in DDL_STATEMENTS:
        conn.execute(ddl)
    conn.commit()

    logger.info("Banco de dados inicializado: %s", db_path)

    global _connection
    _connection = conn
    return conn


def get_connection() -> sqlite3.Connection:
    """Retorna a conexão ativa, ou cria uma nova."""
    global _connection
    if _connection is None:
        return init_db()
    return _connection


def close_db() -> None:
    """Fecha a conexão com o banco."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        logger.info("Conexão com o banco fechada")
