# tests/test_grades.py — Testes do módulo de notas

import pytest

from src.scraper.grades import (
    Grade,
    calculate_average,
    group_grades_by_discipline,
    _safe_float,
)
from src.storage.queries import save_grades


class TestCalculateAverage:
    """Testes para cálculo de média."""

    def test_weighted_average(self):
        grades = [
            Grade(discipline_name="X", type="mapa", value=8.0, weight=0.4),
            Grade(discipline_name="X", type="prova", value=6.0, weight=0.6),
        ]
        # (8*0.4 + 6*0.6) / (0.4+0.6) = 6.8
        assert calculate_average(grades) == 6.8

    def test_simple_average(self):
        grades = [
            Grade(discipline_name="X", type="mapa", value=8.0),
            Grade(discipline_name="X", type="prova", value=6.0),
        ]
        assert calculate_average(grades) == 7.0

    def test_empty_grades(self):
        assert calculate_average([]) is None

    def test_none_values_ignored(self):
        grades = [
            Grade(discipline_name="X", type="mapa", value=8.0),
            Grade(discipline_name="X", type="prova", value=None),
        ]
        assert calculate_average(grades) == 8.0


class TestGroupGrades:
    """Testes para agrupamento por disciplina."""

    def test_group_by_discipline(self):
        grades = [
            Grade(discipline_name="A", type="mapa", value=8.0),
            Grade(discipline_name="A", type="prova", value=7.0),
            Grade(discipline_name="B", type="mapa", value=9.0),
        ]
        grouped = group_grades_by_discipline(grades)

        assert len(grouped) == 2
        assert len(grouped["A"]) == 2
        assert len(grouped["B"]) == 1


class TestSafeFloat:
    """Testes para conversão segura de float."""

    @pytest.mark.parametrize("input_val,expected", [
        (8.5, 8.5),
        ("7.0", 7.0),
        ("abc", None),
        (None, None),
        (0, 0.0),
    ])
    def test_safe_float(self, input_val, expected):
        assert _safe_float(input_val) == expected


class TestSaveGrades:
    """Testes para persistência de notas."""

    def test_save_new_grades(self, db_connection):
        grades = [
            Grade(discipline_name="ANÁLISE E PROJETO ORIENTADO A OBJETOS",
                  discipline_code="EGRAD_GRAD_080_0026", type="mapa", value=8.5),
            Grade(discipline_name="MENTALIDADE CRIATIVA E EMPREENDEDORA",
                  discipline_code="EGRAD_GRAD_080_0523", type="prova", value=7.0),
        ]
        new_items, updated = save_grades(grades, conn=db_connection)

        assert len(new_items) == 2
        assert len(updated) == 0

    def test_detect_grade_update(self, db_connection):
        grades_v1 = [Grade(discipline_name="Teste", type="mapa", value=7.0)]
        new1, upd1 = save_grades(grades_v1, conn=db_connection)
        assert len(new1) == 1
        assert len(upd1) == 0

        grades_v2 = [Grade(discipline_name="Teste", type="mapa", value=8.5)]
        new2, upd2 = save_grades(grades_v2, conn=db_connection)
        assert len(new2) == 0
        assert len(upd2) == 1
        assert upd2[0][1] == 7.0  # valor antigo
