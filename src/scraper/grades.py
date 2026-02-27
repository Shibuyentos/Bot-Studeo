# src/scraper/grades.py — Extração de notas
#
# Formato real da API (confirmado via inventario_com_payloads.json):
#
# NÃO existe um endpoint dedicado de "notas/boletim" no tráfego capturado.
# O endpoint /aluno/disciplina/curricular/true retorna as disciplinas,
# mas NÃO traz notas dentro do JSON.
#
# Possíveis fontes de notas (a investigar):
# - Pode haver um endpoint por disciplina (ex: /disciplina/{id}/notas)
# - O scraper Selenium original pegava de um modal "Atividades" na UI
# - POST /questionario/afazer/ pode conter resultados de questionários
#
# Por enquanto, este módulo mantém a estrutura preparada para quando
# o endpoint de notas for descoberto.

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

from src.scraper import endpoints
from src.scraper.client import StudeoClient

logger = logging.getLogger(__name__)


@dataclass
class Grade:
    """Representa uma nota de avaliação."""

    discipline_name: str
    discipline_code: str | None = None
    type: str = ""           # "mapa", "prova", "forum", "substitutiva"
    value: float | None = None  # 0.0 a 10.0
    weight: float | None = None  # Peso na média
    recorded_at: datetime | None = None
    raw_data: dict = field(default_factory=dict, repr=False)


def fetch_grades(client: StudeoClient) -> list[Grade]:
    """Busca notas do aluno.

    NOTA: O endpoint específico de notas/boletim não foi encontrado
    no tráfego capturado. Este módulo retorna lista vazia até que
    o endpoint correto seja identificado.

    Para descobrir o endpoint:
    1. Abrir DevTools (F12) → Network → Fetch/XHR
    2. No Studeo, ir em "Meu Curso" → "Boletim"
    3. Observar qual endpoint é chamado
    4. Anotar a URL e o formato do JSON de resposta

    Returns:
        Lista de Grade (vazia até o endpoint ser descoberto)
    """
    logger.info("Buscando notas... (endpoint ainda não mapeado)")

    # TODO: Quando o endpoint de notas for descoberto, implementar aqui.
    # Possível caminho: navegar em "Boletim" no Studeo com DevTools aberto
    # e capturar o endpoint que traz as notas.

    return []


def calculate_average(grades: list[Grade]) -> float | None:
    """Calcula a média ponderada das notas.

    Se não houver pesos, calcula média simples.

    Returns:
        Média ou None se não houver notas
    """
    valid_grades = [g for g in grades if g.value is not None]
    if not valid_grades:
        return None

    has_weights = all(g.weight is not None for g in valid_grades)

    if has_weights:
        total_weight = sum(g.weight for g in valid_grades)
        if total_weight == 0:
            return None
        weighted_sum = sum(g.value * g.weight for g in valid_grades)
        return round(weighted_sum / total_weight, 2)
    else:
        return round(sum(g.value for g in valid_grades) / len(valid_grades), 2)


def group_grades_by_discipline(grades: list[Grade]) -> dict[str, list[Grade]]:
    """Agrupa notas por disciplina."""
    grouped: dict[str, list[Grade]] = {}
    for grade in grades:
        key = grade.discipline_name
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(grade)
    return grouped


def _safe_float(value) -> float | None:
    """Converte para float de forma segura."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
