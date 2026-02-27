# tests/test_deadlines.py — Testes do módulo de prazos/disciplinas

from datetime import datetime

import pytest

from src.scraper.deadlines import (
    Discipline,
    StudyEvent,
    Announcement,
    Deadline,
    _timestamp_to_datetime,
)
from src.storage.queries import save_deadlines


class TestTimestampConversion:
    """Testes para conversão de timestamp Java (ms) → datetime."""

    def test_valid_timestamp(self):
        # 2026-02-26T20:55:21 (approx)
        result = _timestamp_to_datetime(1772150121841)
        assert result is not None
        assert result.year == 2026

    def test_none_input(self):
        assert _timestamp_to_datetime(None) is None

    def test_zero(self):
        result = _timestamp_to_datetime(0)
        assert result is not None  # epoch


class TestDisciplineParsing:
    """Testes para parsing de disciplinas — formato real."""

    def test_parse_curricular(self):
        raw = {
            "tpMatricula": "Matriculado",
            "tpDetalhe": "Curricular",
            "idDisciplina": 766981,
            "nmDisciplina": "ANÁLISE E PROJETO ORIENTADO A OBJETOS",
            "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026",
            "flAtivo": True,
            "dhLiberar": None,
            "ano": 2026,
            "semestre": 51,
            "cdDisciplina": "EGRAD_GRAD_080_0026",
            "flCurricular": True,
        }
        disc = Discipline(
            id_disciplina=raw["idDisciplina"],
            name=raw["nmDisciplina"],
            code=raw.get("cdDisciplina", ""),
            shortname=raw.get("cdShortname", ""),
            year=raw.get("ano", 0),
            semester=raw.get("semestre", 0),
            is_curricular=raw.get("flCurricular", False),
            is_active=raw.get("flAtivo", True),
        )
        assert disc.name == "ANÁLISE E PROJETO ORIENTADO A OBJETOS"
        assert disc.code == "EGRAD_GRAD_080_0026"
        assert disc.year == 2026
        assert disc.semester == 51
        assert disc.is_curricular is True

    def test_parse_non_curricular(self):
        raw = {
            "idDisciplina": 312376,
            "nmDisciplina": "GIRO EAD",
            "cdDisciplina": "7158",
            "semestre": 99,
            "flCurricular": False,
        }
        disc = Discipline(
            id_disciplina=raw["idDisciplina"],
            name=raw["nmDisciplina"],
            code=raw.get("cdDisciplina", ""),
            semester=raw.get("semestre", 0),
            is_curricular=raw.get("flCurricular", False),
        )
        assert disc.is_curricular is False
        assert disc.semester == 99  # "especial"


class TestStudyEventParsing:
    """Testes para parsing de eventos do plano de estudo."""

    def test_parse_study_event(self):
        raw = {
            "dhInicial": 1771930800000,
            "dhFinal": 1771988340000,
            "dsPlanoDeEstudoTipoEvento": "Aula",
            "dsPlanoDeEstudoSubTipoEvento": "AULA",
            "dsPlanoDeEstudoTipoAlerta": "Aula",
            "tpCor": "success",
            "nmDisciplina": "MENTALIDADE CRIATIVA E EMPREENDEDORA",
            "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523",
        }
        event = StudyEvent(
            discipline_name=raw["nmDisciplina"],
            shortname=raw.get("cdShortname", ""),
            event_type=raw.get("dsPlanoDeEstudoTipoEvento", ""),
            sub_type=raw.get("dsPlanoDeEstudoSubTipoEvento", ""),
            color=raw.get("tpCor", ""),
            start_at=_timestamp_to_datetime(raw.get("dhInicial")),
            end_at=_timestamp_to_datetime(raw.get("dhFinal")),
        )
        assert event.discipline_name == "MENTALIDADE CRIATIVA E EMPREENDEDORA"
        assert event.event_type == "Aula"
        assert event.start_at is not None
        assert event.end_at is not None
        assert event.start_at < event.end_at


class TestAnnouncementParsing:
    """Testes para parsing de avisos."""

    def test_parse_announcement(self):
        raw = {
            "id": 5021782,
            "nmDestinatario": "ELAINE IGNACIO MOREIRA",
            "ultimoTexto": "<p>Olá, estudante!</p>",
            "dtTexto": 1772110628180,
            "nLida": 1,
            "aba": "AVISO",
            "nmCategoria": "Santander Top Espanha 2026",
            "nmConversaStatus": "Em andamento",
        }
        ann = Announcement(
            id=raw["id"],
            sender_name=raw.get("nmDestinatario", ""),
            text=raw.get("ultimoTexto", ""),
            category=raw.get("nmCategoria", ""),
            sent_at=_timestamp_to_datetime(raw.get("dtTexto")),
            is_read=raw.get("nLida", 0) == 1,
            status=raw.get("nmConversaStatus", ""),
        )
        assert ann.id == 5021782
        assert ann.is_read is True
        assert ann.category == "Santander Top Espanha 2026"
        assert ann.sent_at is not None


class TestDeadlineConversion:
    """Testes para conversão de eventos em Deadlines (compatibilidade com banco)."""

    def test_study_event_to_deadline(self):
        event = StudyEvent(
            discipline_name="MENTALIDADE CRIATIVA E EMPREENDEDORA",
            shortname="2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523",
            event_type="Aula",
            sub_type="AULA",
            end_at=datetime(2026, 2, 25, 23, 59),
        )
        deadline = Deadline(
            discipline_name=event.discipline_name,
            discipline_code=event.shortname,
            type=event.sub_type.lower(),
            title=f"{event.event_type} — {event.discipline_name}",
            due_date=event.end_at,
            status="pendente",
        )
        assert deadline.type == "aula"
        assert deadline.due_date == datetime(2026, 2, 25, 23, 59)


class TestSaveDeadlines:
    """Testes para persistência de deadlines."""

    def test_save_new_deadlines(self, db_connection):
        deadlines = [
            Deadline(
                discipline_name="ANÁLISE E PROJETO ORIENTADO A OBJETOS",
                discipline_code="EGRAD_GRAD_080_0026",
                type="aula",
                title="Aula — ANÁLISE E PROJETO ORIENTADO A OBJETOS",
                due_date=datetime(2026, 3, 5, 23, 59),
            ),
            Deadline(
                discipline_name="MENTALIDADE CRIATIVA E EMPREENDEDORA",
                discipline_code="EGRAD_GRAD_080_0523",
                type="aula",
                title="Aula — MENTALIDADE CRIATIVA E EMPREENDEDORA",
                due_date=datetime(2026, 3, 1, 23, 59),
            ),
        ]
        new_items = save_deadlines(deadlines, conn=db_connection)
        assert len(new_items) == 2

    def test_save_duplicate_deadlines(self, db_connection):
        deadlines = [
            Deadline(
                discipline_name="ANÁLISE E PROJETO ORIENTADO A OBJETOS",
                discipline_code="EGRAD_GRAD_080_0026",
                type="aula",
                title="Aula — ANÁLISE E PROJETO ORIENTADO A OBJETOS",
                due_date=datetime(2026, 3, 5, 23, 59),
            ),
        ]
        # Primeira vez: novo
        new_first = save_deadlines(deadlines, conn=db_connection)
        assert len(new_first) == 1

        # Segunda vez: duplicado
        new_second = save_deadlines(deadlines, conn=db_connection)
        assert len(new_second) == 0
