# src/scraper/deadlines.py — Extração de prazos, disciplinas e plano de estudo
#
# Formato real da API (confirmado via inventario_com_payloads.json):
#
# GET /disciplina/afazer → {"somaTotal": 70}  (SÓ o total, não lista!)
# GET /disciplina/curricular/true → [{nmDisciplina, cdDisciplina, cdShortname, ano, semestre, ...}]
# GET /disciplina/matriculados → mesma estrutura de curricular
# GET /plano-estudo/disciplinas-usuario → [{dhInicial, dhFinal, nmDisciplina, dsPlanoDeEstudoTipoEvento, tpCor}]
# GET /atendimento?aba=AVISO → [{id, nmDestinatario, ultimoTexto, dtTexto, nmCategoria, ...}]

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

from src.scraper import endpoints
from src.scraper.client import StudeoClient

logger = logging.getLogger(__name__)


# ── Modelos ──────────────────────────────────────────────────────────────

@dataclass
class Discipline:
    """Disciplina real do Studeo."""

    id_disciplina: int
    name: str                    # nmDisciplina
    code: str = ""               # cdDisciplina
    shortname: str = ""          # cdShortname
    year: int = 0                # ano
    semester: int = 0            # semestre (51, 52, 99=especial)
    is_curricular: bool = False  # flCurricular
    is_active: bool = True       # flAtivo
    enrollment_type: str = ""    # tpMatricula
    detail_type: str = ""        # tpDetalhe
    raw_data: dict = field(default_factory=dict, repr=False)


@dataclass
class StudyEvent:
    """Evento do plano de estudo."""

    discipline_name: str         # nmDisciplina
    shortname: str = ""          # cdShortname
    event_type: str = ""         # dsPlanoDeEstudoTipoEvento ("Aula")
    sub_type: str = ""           # dsPlanoDeEstudoSubTipoEvento ("AULA")
    alert_type: str = ""         # dsPlanoDeEstudoTipoAlerta
    color: str = ""              # tpCor ("success", "warning", etc.)
    start_at: datetime | None = None  # dhInicial (timestamp ms)
    end_at: datetime | None = None    # dhFinal (timestamp ms)
    raw_data: dict = field(default_factory=dict, repr=False)


@dataclass
class Announcement:
    """Aviso/comunicado do mediador."""

    id: int
    sender_name: str = ""        # nmDestinatario
    text: str = ""               # ultimoTexto (HTML)
    category: str = ""           # nmCategoria
    sent_at: datetime | None = None  # dtTexto (timestamp ms)
    is_read: bool = False        # nLida (0 ou 1)
    status: str = ""             # nmConversaStatus
    raw_data: dict = field(default_factory=dict, repr=False)


# Para compatibilidade com storage/queries.py
@dataclass
class Deadline:
    """Representação unificada para o banco de dados."""

    discipline_name: str
    discipline_code: str | None = None
    type: str = ""
    title: str = ""
    due_date: datetime | None = None
    status: str = "pendente"
    raw_data: dict = field(default_factory=dict, repr=False)


# ── Fetchers ─────────────────────────────────────────────────────────────


def fetch_afazer_count(client: StudeoClient) -> int:
    """Busca o total de atividades pendentes.

    Response real: {"somaTotal": 70}
    NOTA: Este endpoint retorna SÓ a contagem, não a lista de atividades.

    Returns:
        Total de itens pendentes
    """
    logger.info("Buscando contagem de atividades pendentes...")
    response = client.get(endpoints.DISCIPLINAS_AFAZER)

    if response.status_code == 204:
        return 0

    data = response.json()
    total = data.get("somaTotal", 0)
    logger.info("Total de itens pendentes: %d", total)
    return total


def fetch_disciplines(client: StudeoClient, curricular: bool = True) -> list[Discipline]:
    """Busca disciplinas do aluno.

    Response real (array):
    [{
        "tpMatricula": "Matriculado",
        "tpDetalhe": "Curricular",
        "idDisciplina": 766981,
        "nmDisciplina": "ANÁLISE E PROJETO ORIENTADO A OBJETOS",
        "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026",
        "flAtivo": true,
        "dhLiberar": null,
        "ano": 2026,
        "semestre": 51,
        "cdDisciplina": "EGRAD_GRAD_080_0026",
        "cdTurma": "26_EGRAD_ADSIS5E-51",
        "flCurricular": true,
        "flDestaque": false,
        "flDigital": false
    }]

    Args:
        curricular: True para curriculares, False para não-curriculares

    Returns:
        Lista de Discipline
    """
    path = endpoints.DISCIPLINAS_CURRICULARES.format(curricular=str(curricular).lower())
    logger.info("Buscando disciplinas (curricular=%s)...", curricular)

    response = client.get(path)

    if response.status_code == 204:
        logger.info("Nenhuma disciplina encontrada (204)")
        return []

    data = response.json()
    items = data if isinstance(data, list) else [data]

    disciplines = []
    for item in items:
        try:
            disc = Discipline(
                id_disciplina=item.get("idDisciplina", 0),
                name=item.get("nmDisciplina", ""),
                code=item.get("cdDisciplina", ""),
                shortname=item.get("cdShortname", ""),
                year=item.get("ano", 0),
                semester=item.get("semestre", 0),
                is_curricular=item.get("flCurricular", False),
                is_active=item.get("flAtivo", True),
                enrollment_type=item.get("tpMatricula", ""),
                detail_type=item.get("tpDetalhe", ""),
                raw_data=item,
            )
            disciplines.append(disc)
        except Exception as e:
            logger.warning("Erro ao parsear disciplina: %s", e)

    logger.info("Encontradas %d disciplinas", len(disciplines))
    return disciplines


def fetch_all_disciplines(client: StudeoClient) -> list[Discipline]:
    """Busca todas as disciplinas (curriculares + não-curriculares)."""
    curricular = fetch_disciplines(client, curricular=True)
    non_curricular = fetch_disciplines(client, curricular=False)
    return curricular + non_curricular


def fetch_study_plan(client: StudeoClient) -> list[StudyEvent]:
    """Busca o plano de estudo (eventos agendados).

    Response real (array):
    [{
        "dhInicial": 1771930800000,
        "dhFinal": 1771988340000,
        "dsPlanoDeEstudoTipoEvento": "Aula",
        "dsPlanoDeEstudoSubTipoEvento": "AULA",
        "dsPlanoDeEstudoTipoAlerta": "Aula",
        "tpCor": "success",
        "nmDisciplina": "MENTALIDADE CRIATIVA E EMPREENDEDORA",
        "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523"
    }]

    Returns:
        Lista de StudyEvent
    """
    logger.info("Buscando plano de estudo...")

    response = client.get(endpoints.PLANO_ESTUDO_DISCIPLINAS)

    if response.status_code == 204:
        logger.info("Nenhum evento no plano de estudo (204)")
        return []

    data = response.json()
    items = data if isinstance(data, list) else [data]

    events = []
    for item in items:
        try:
            event = StudyEvent(
                discipline_name=item.get("nmDisciplina", ""),
                shortname=item.get("cdShortname", ""),
                event_type=item.get("dsPlanoDeEstudoTipoEvento", ""),
                sub_type=item.get("dsPlanoDeEstudoSubTipoEvento", ""),
                alert_type=item.get("dsPlanoDeEstudoTipoAlerta", ""),
                color=item.get("tpCor", ""),
                start_at=_timestamp_to_datetime(item.get("dhInicial")),
                end_at=_timestamp_to_datetime(item.get("dhFinal")),
                raw_data=item,
            )
            events.append(event)
        except Exception as e:
            logger.warning("Erro ao parsear evento do plano: %s", e)

    logger.info("Encontrados %d eventos no plano de estudo", len(events))
    return events


def fetch_announcements(client: StudeoClient, page_size: int = 7) -> list[Announcement]:
    """Busca avisos/comunicados do mediador.

    Response real (array):
    [{
        "id": 5021782,
        "nmDestinatario": "ELAINE IGNACIO MOREIRA",
        "ultimoTexto": "<p>Olá, estudante!...</p>",
        "dtTexto": 1772110628180,
        "nLida": 1,
        "aba": "AVISO",
        "nmCategoria": "Santander Top Espanha 2026",
        "nmConversaStatus": "Em andamento",
        ...
    }]
    """
    logger.info("Buscando avisos/comunicados...")

    response = client.get(
        endpoints.ATENDIMENTO_LISTA,
        params={
            "aba": "AVISO",
            "mediador": "false",
            "novasPrimeiro": "true",
            "pageOffset": str(page_size),
            "startIndex": "0",
        },
    )

    if response.status_code == 204:
        return []

    data = response.json()
    items = data if isinstance(data, list) else [data]

    announcements = []
    for item in items:
        try:
            ann = Announcement(
                id=item.get("id", 0),
                sender_name=item.get("nmDestinatario", ""),
                text=item.get("ultimoTexto", ""),
                category=item.get("nmCategoria", ""),
                sent_at=_timestamp_to_datetime(item.get("dtTexto")),
                is_read=item.get("nLida", 0) == 1,
                status=item.get("nmConversaStatus", ""),
                raw_data=item,
            )
            announcements.append(ann)
        except Exception as e:
            logger.warning("Erro ao parsear aviso: %s", e)

    logger.info("Encontrados %d avisos", len(announcements))
    return announcements


def fetch_unread_count(client: StudeoClient) -> int:
    """Busca a quantidade de mensagens não lidas.

    Response real: [{"situacao": "COMUNICADO", "qtdMensagem": 5}]
    """
    response = client.get(endpoints.MENSAGENS_NAO_LIDAS)

    if response.status_code == 204:
        return 0

    data = response.json()
    if isinstance(data, list) and data:
        return data[0].get("qtdMensagem", 0)
    return 0


# Compatibilidade com o fluxo existente (scheduler/queries usam Deadline)
def fetch_deadlines(client: StudeoClient) -> list[Deadline]:
    """Busca prazos — converte eventos do plano de estudo em Deadlines.

    Como /disciplina/afazer retorna apenas {somaTotal}, usamos
    o plano de estudo como fonte de eventos com datas.
    """
    events = fetch_study_plan(client)
    deadlines = []

    for event in events:
        if event.end_at:
            deadlines.append(Deadline(
                discipline_name=event.discipline_name,
                discipline_code=event.shortname,
                type=event.sub_type.lower() if event.sub_type else event.event_type.lower(),
                title=f"{event.event_type} — {event.discipline_name}",
                due_date=event.end_at,
                status="pendente",
                raw_data=event.raw_data,
            ))

    logger.info("Convertidos %d eventos em deadlines", len(deadlines))
    return deadlines


# ── Helpers ──────────────────────────────────────────────────────────────


def _timestamp_to_datetime(ts: int | None) -> datetime | None:
    """Converte timestamp em milissegundos para datetime."""
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(ts / 1000)
    except (ValueError, TypeError, OSError):
        return None
