# src/scraper/client.py — Cliente HTTP base para o Studeo

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from src.scraper import endpoints

logger = logging.getLogger(__name__)


class StudeoClient:
    """Cliente HTTP para comunicação com a API do Studeo.

    Encapsula httpx.Client com:
    - Base URL fixa
    - Gerenciamento de token (Authorization header)
    - Rate limiting (intervalo mínimo entre requests)
    - Retry automático com re-auth em 401
    """

    MIN_REQUEST_INTERVAL = 2.0  # segundos entre requests (rate limiting)

    def __init__(self, base_url: str | None = None, timeout: float = 30.0) -> None:
        self.base_url = base_url or endpoints.BASE_URL
        self._token: str | None = None
        self._refresh_token: str | None = None
        self._last_request_time: float = 0
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "Origin": "https://studeo.unicesumar.edu.br",
            },
            follow_redirects=True,
        )
        logger.info("StudeoClient inicializado — base_url=%s", self.base_url)

    # ── Token ────────────────────────────────────────────────────────────

    @property
    def token(self) -> str | None:
        return self._token

    def set_token(self, token: str, refresh_token: str | None = None) -> None:
        """Define o token de autenticação e atualiza o header."""
        self._token = token
        if refresh_token:
            self._refresh_token = refresh_token
        self._client.headers["Authorization"] = token
        logger.debug("Token configurado: [%s...] (tamanho: %d)", token[:10], len(token))

    def clear_token(self) -> None:
        """Remove o token de autenticação."""
        self._token = None
        self._refresh_token = None
        self._client.headers.pop("Authorization", None)

    @property
    def is_authenticated(self) -> bool:
        return self._token is not None

    # ── Rate limiting ────────────────────────────────────────────────────

    def _wait_rate_limit(self) -> None:
        """Respeita o intervalo mínimo entre requests."""
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self.MIN_REQUEST_INTERVAL:
            sleep_time = self.MIN_REQUEST_INTERVAL - elapsed
            logger.debug("Rate limit: aguardando %.1fs", sleep_time)
            time.sleep(sleep_time)

    # ── Requests ─────────────────────────────────────────────────────────

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        retry_on_401: bool = True,
    ) -> httpx.Response:
        """Faz um request HTTP com rate limiting e tratamento de erros.

        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Caminho do endpoint (ex: /auth-api-controller/auth/token/create)
            params: Query parameters
            json: Body JSON
            data: Body form-encoded
            headers: Headers adicionais
            retry_on_401: Se True, tenta re-autenticar e refazer em caso de 401

        Returns:
            httpx.Response

        Raises:
            httpx.HTTPStatusError: Para status codes 4xx/5xx (exceto 401 com retry)
        """
        self._wait_rate_limit()
        self._last_request_time = time.monotonic()

        logger.info("%s %s", method.upper(), path)

        response = self._client.request(
            method=method,
            url=path,
            params=params,
            json=json,
            data=data,
            headers=headers,
        )

        logger.debug("Response: %d %s", response.status_code, response.reason_phrase)
        if response.status_code == 401:
            logger.debug("Header enviado: %s", dict(self._client.headers).get("authorization", "NENHUM"))

        # 401 → tentar re-auth (se não for o próprio request de login)
        if response.status_code == 401 and retry_on_401:
            logger.warning("401 Unauthorized — tentando renovar token...")
            if self._try_renew_token():
                return self.request(
                    method, path,
                    params=params, json=json, data=data, headers=headers,
                    retry_on_401=False,  # evitar loop infinito
                )

        response.raise_for_status()
        return response

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    # ── Token renewal ────────────────────────────────────────────────────

    def _try_renew_token(self) -> bool:
        """Tenta renovar o token via endpoint de renew."""
        if not self._refresh_token:
            logger.warning("Sem refresh_token disponível para renovação")
            return False
        try:
            payload = {"refreshToken": self._refresh_token}
            response = self._client.post(endpoints.AUTH_TOKEN_RENEW, json=payload)
            if response.status_code == 200:
                data = response.json()
                new_token = data.get("token") or data.get("access_token")
                new_refresh = data.get("refreshToken")
                if new_token:
                    self.set_token(new_token, new_refresh)
                    logger.info("Token renovado com sucesso")
                    return True
            logger.warning("Falha ao renovar token: status %d", response.status_code)
        except Exception as e:
            logger.error("Erro ao renovar token: %s", e)
        return False

    # ── Lifecycle ────────────────────────────────────────────────────────

    def close(self) -> None:
        """Fecha o cliente HTTP."""
        self._client.close()
        logger.info("StudeoClient fechado")

    def __enter__(self) -> StudeoClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
