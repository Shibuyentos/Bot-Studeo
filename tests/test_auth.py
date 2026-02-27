# tests/test_auth.py — Testes do módulo de autenticação

from unittest.mock import MagicMock

import pytest

from src.scraper.auth import login, AuthenticationError, AuthInfo


class TestLogin:
    """Testes para a função login()."""

    def test_login_success_token_in_body(self, mock_studeo_client):
        """Login com token no body da response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "token": "eyJhbGciOiJSUzI1NiJ9.fake",
            "refreshToken": "eyJhbGciOiJSUzI1NiJ9.fake_refresh",
        }
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.cookies = {}
        mock_studeo_client.post.return_value = mock_response

        # Mock user info
        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {
            "cdUsuario": "25050325-5",
            "nmUsuario": "Kauann Gabriel Shibuya",
            "dsEmail": "test@email.com",
            "cpf": "80070107939",
            "cursoList": [{"nmCurso": "ADS", "cdCurso": "EGRAD_ADSIS"}],
        }
        mock_studeo_client.get.return_value = mock_user_resp

        result = login(mock_studeo_client, "80070107939", "senha123")

        assert isinstance(result, AuthInfo)
        assert result.token == "eyJhbGciOiJSUzI1NiJ9.fake"
        assert result.refresh_token == "eyJhbGciOiJSUzI1NiJ9.fake_refresh"
        assert result.user_name == "Kauann Gabriel Shibuya"
        assert result.curso == "ADS"
        mock_studeo_client.set_token.assert_called_once()

    def test_login_token_in_header(self, mock_studeo_client):
        """Login com token no header Authorization."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        mock_response.headers = {"Authorization": "Bearer token-from-header"}
        mock_response.cookies = {}
        mock_studeo_client.post.return_value = mock_response

        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {"nmUsuario": "Test"}
        mock_studeo_client.get.return_value = mock_user_resp

        result = login(mock_studeo_client, "80070107939", "senha123")

        assert result.token == "token-from-header"

    def test_login_no_token(self, mock_studeo_client):
        """Login sem token em nenhuma fonte deve levantar AuthenticationError."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.cookies = {}
        mock_studeo_client.post.return_value = mock_response

        with pytest.raises(AuthenticationError, match="Token não encontrado"):
            login(mock_studeo_client, "80070107939", "senha_errada")

    def test_login_network_error(self, mock_studeo_client):
        """Erro de rede deve ser encapsulado em AuthenticationError."""
        mock_studeo_client.post.side_effect = ConnectionError("Connection refused")

        with pytest.raises(AuthenticationError, match="Falha no login"):
            login(mock_studeo_client, "80070107939", "senha123")

    def test_login_payload_format(self, mock_studeo_client):
        """Payload deve usar os campos reais: username e password."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "t"}
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.cookies = {}
        mock_studeo_client.post.return_value = mock_response

        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {}
        mock_studeo_client.get.return_value = mock_user_resp

        login(mock_studeo_client, "80070107939", "Renann1.")

        # Verificar que o payload usa os campos corretos
        call_args = mock_studeo_client.post.call_args
        payload = call_args[1].get("json") or call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("json")
        assert payload is not None
        assert payload["username"] == "80070107939"
        assert payload["password"] == "Renann1."
