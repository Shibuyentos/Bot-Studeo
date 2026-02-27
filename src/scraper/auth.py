# src/scraper/auth.py — Autenticação no Studeo
#
# Formato real da API (confirmado via inventario_com_payloads.json):
# - POST /auth/token/create: body {"username": "CPF", "password": "SENHA"}
#   Response: token provavelmente no header (res_payloads vazio no HAR)
# - POST /auth/token/renew: body {"refreshToken": "JWT"}
#   Response: {"token": "JWT", "refreshToken": "JWT"}
# - GET /usuario/info-login: Response com {id, cdUsuario, nmUsuario, dsEmail, cpf, cursoList}

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
import re

from src.scraper import endpoints
from src.scraper.client import StudeoClient

logger = logging.getLogger(__name__)


@dataclass
class AuthInfo:
    """Informações sobre a sessão autenticada."""

    token: str
    refresh_token: str | None = None
    user_id: str | None = None
    user_name: str | None = None
    email: str | None = None
    cpf: str | None = None
    curso: str | None = None


def login(client: StudeoClient, cpf: str, senha: str) -> AuthInfo:
    """Autentica no Studeo e retorna informações da sessão.

    O Studeo usa JWT (RS256). O endpoint /auth/token/create
    recebe {"username": "CPF", "password": "senha"}.

    O token pode vir:
    1. No body da response (campo "token")
    2. No header Authorization da response
    3. Em um cookie de sessão

    Args:
        client: Instância do StudeoClient
        cpf: CPF do aluno (sem formatação)
        senha: Senha do Studeo

    Returns:
        AuthInfo com token e dados do usuário

    Raises:
        AuthenticationError: Se o login falhar
    """
    logger.info("Iniciando login para CPF=***%s", cpf[-4:] if len(cpf) >= 4 else "****")

    # Formato confirmado: {"username": "CPF", "password": "senha"}
    payload = {
        "username": cpf,
        "password": senha,
    }

    try:
        response = client.post(
            endpoints.AUTH_TOKEN_CREATE,
            json=payload,
            retry_on_401=False,
        )

        # Tentar extrair token de múltiplas fontes
        token = None
        refresh_token = None

        # 1. Tentar do body (pode ser vazio no HAR por ser HTTPOnly)
        data = {}
        try:
            data = response.json()
            token = data.get("token")
            refresh_token = data.get("refreshToken")
        except Exception:
            pass

        # 2. Tentar via Regex no plain text (API as vezes devolve só "eyJh...")
        if not token:
            # Padrão básico de JWT: tres partes em base64url separadas por ponto
            jwt_pattern = re.compile(r'(eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)')
            matches = jwt_pattern.findall(response.text)
            if matches:
                 # Assumimos que o primeiro é o token, o segundo (se existir) é o refresh
                 token = matches[0]
                 if len(matches) > 1:
                     refresh_token = matches[1]

        # 3. Tentar do header Authorization
        if not token:
            auth_header = response.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]

        # 4. Tentar de outros headers comuns
        if not token:
            token = response.headers.get("X-Auth-Token") or response.headers.get("Token")

        # 5. Tentar do cookie
        if not token:
            for cookie_name in ["token", "auth_token", "JSESSIONID"]:
                if cookie_name in response.cookies:
                    token = response.cookies[cookie_name]
                    break

        if not token:
            logger.error(
                "Token não encontrado. Response status: %d, headers: %s, body keys: %s",
                response.status_code,
                dict(response.headers),
                list(data.keys()) if data else "empty",
            )
            logger.error("DUMP COMPLETO DO BODY: %s", response.text)
            raise AuthenticationError(
                f"Token não encontrado na resposta (status {response.status_code}). "
                f"Body keys: {list(data.keys()) if data else 'vazio'}. "
                "Verifique com DevTools de onde o frontend extrai o token."
            )

        # Configurar o token no cliente
        client.set_token(token, refresh_token)

        # Buscar info do usuário
        user_info = _fetch_user_info(client)

        auth_info = AuthInfo(
            token=token,
            refresh_token=refresh_token,
            user_id=user_info.get("cdUsuario"),
            user_name=user_info.get("nmUsuario"),
            email=user_info.get("dsEmail"),
            cpf=user_info.get("cpf"),
            curso=_extract_curso(user_info),
        )

        logger.info("Login bem-sucedido! Usuário: %s (%s)",
                     auth_info.user_name, auth_info.curso)
        return auth_info

    except Exception as e:
        if isinstance(e, AuthenticationError):
            raise
        raise AuthenticationError(f"Falha no login: {e}") from e


def _fetch_user_info(client: StudeoClient) -> dict:
    """Busca informações do usuário logado.

    Response real:
    {
        "id": 2494641,
        "cdUsuario": "25050325-5",
        "nmUsuario": "Kauann Gabriel Shibuya",
        "dsEmail": "RA250503255@EAD.CESUMAR.BR",
        "dhUltimoAcesso": 1772150120322,
        "nmPerfil": "ALUNO",
        "cpf": "80070107939",
        "unidadeAssociada": {...},
        "cursoList": [{"nmCurso": "...", "cdCurso": "..."}]
    }
    """
    try:
        response = client.get(endpoints.USUARIO_INFO_LOGIN)
        return response.json()
    except Exception as e:
        logger.warning("Não foi possível buscar info do usuário: %s", e)
        return {}


def _extract_curso(user_info: dict) -> str | None:
    """Extrai o nome do curso da lista de cursos."""
    curso_list = user_info.get("cursoList", [])
    if curso_list and isinstance(curso_list, list):
        return curso_list[0].get("nmCurso")
    return None


def renew_token(client: StudeoClient, refresh_token: str) -> AuthInfo | None:
    """Renova o token usando o refresh token.

    Request: {"refreshToken": "JWT"}
    Response: {"token": "JWT", "refreshToken": "JWT"}
    """
    try:
        response = client.post(
            endpoints.AUTH_TOKEN_RENEW,
            json={"refreshToken": refresh_token},
            retry_on_401=False,
        )

        data = response.json()
        new_token = data.get("token")
        new_refresh = data.get("refreshToken")

        if new_token:
            client.set_token(new_token)
            logger.info("Token renovado com sucesso")
            return AuthInfo(token=new_token, refresh_token=new_refresh)

        logger.warning("Renew retornou sem token: %s", list(data.keys()))
        return None

    except Exception as e:
        logger.error("Erro ao renovar token: %s", e)
        return None


def get_token_info(client: StudeoClient) -> dict:
    """Consulta info do servidor (timestamp atual).

    Response real:
    {
        "datetime": "2026-02-26T20:55:21.841-0300",
        "offset": -180,
        "timezone": "-0300",
        "timezoneId": "America/Sao_Paulo",
        "timestamp": 1772150121841
    }
    """
    response = client.get(endpoints.AUTH_TOKEN_TIME_INFO, retry_on_401=False)
    return response.json()


def revoke_token(client: StudeoClient) -> bool:
    """Revoga o token atual (logout)."""
    try:
        client.post(endpoints.AUTH_TOKEN_REVOKE, retry_on_401=False)
        client.clear_token()
        logger.info("Token revogado (logout)")
        return True
    except Exception as e:
        logger.warning("Erro ao revogar token: %s", e)
        client.clear_token()
        return False


class AuthenticationError(Exception):
    """Erro de autenticação no Studeo."""
