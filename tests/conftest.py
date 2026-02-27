# tests/conftest.py — Fixtures compartilhadas para testes

import sqlite3
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from src.storage.database import init_db
from src.storage import models


@pytest.fixture
def db_connection(tmp_path):
    """Banco SQLite em memória para testes."""
    db_path = tmp_path / "test.db"
    conn = init_db(str(db_path))
    yield conn
    conn.close()


@pytest.fixture
def mock_studeo_client():
    """Cliente HTTP mockado."""
    client = MagicMock()
    client.base_url = "https://studeoapi.unicesumar.edu.br"
    client.is_authenticated = True
    client.token = "fake-token-123"
    return client


# ── Respostas mockadas da API ────────────────────────────────────────────


@pytest.fixture
def mock_auth_response():
    """Resposta mockada do endpoint de login."""
    return {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.token",
        "userId": 12345,
        "nome": "Estudante Teste",
    }


@pytest.fixture
def mock_deadlines_response():
    """Resposta mockada do endpoint de atividades pendentes."""
    now = datetime.now()
    return [
        {
            "nomeDisciplina": "Algoritmos e Programação",
            "codigoDisciplina": "ALG001",
            "tipoAtividade": "MAPA",
            "titulo": "MAPA - Material de Avaliação Prática",
            "dataFim": (now + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "pendente",
        },
        {
            "nomeDisciplina": "Banco de Dados",
            "codigoDisciplina": "BD001",
            "tipoAtividade": "Fórum",
            "titulo": "Fórum de Discussão - Normalização",
            "dataFim": (now + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "pendente",
        },
        {
            "nomeDisciplina": "Engenharia de Software",
            "codigoDisciplina": "ES001",
            "tipoAtividade": "Prova",
            "titulo": "Prova Objetiva",
            "dataFim": (now + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "pendente",
        },
    ]


@pytest.fixture
def mock_grades_response():
    """Resposta mockada do endpoint de notas/disciplinas."""
    return [
        {
            "nomeDisciplina": "Algoritmos e Programação",
            "codigoDisciplina": "ALG001",
            "notas": [
                {"tipo": "MAPA", "valor": 8.5, "peso": 0.4},
                {"tipo": "Prova", "valor": 7.0, "peso": 0.6},
            ],
        },
        {
            "nomeDisciplina": "Banco de Dados",
            "codigoDisciplina": "BD001",
            "notas": [
                {"tipo": "MAPA", "valor": 9.0, "peso": 0.4},
            ],
        },
        {
            "nomeDisciplina": "Engenharia de Software",
            "codigoDisciplina": "ES001",
            "nota": 6.5,
        },
    ]
