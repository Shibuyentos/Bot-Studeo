# src/config.py — Configurações centralizadas via pydantic-settings

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do Bot-Studeo carregadas de variáveis de ambiente / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Studeo ---
    studeo_cpf: str = ""
    studeo_ra: str = ""
    studeo_senha: str = ""
    studeo_base_url: str = "https://studeoapi.unicesumar.edu.br"

    # --- Banco de dados ---
    database_url: str = "sqlite:///data/studeo.db"

    # --- Telegram ---
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # --- Scheduler ---
    scrape_interval_hours: int = 6
    deadline_check_interval_hours: int = 12

    # --- Caminhos ---
    data_dir: Path = Path("data")
    materials_dir: Path = Path("data/materials")

    @property
    def db_path(self) -> Path:
        """Extrai o caminho do arquivo SQLite da DATABASE_URL."""
        url = self.database_url
        if url.startswith("sqlite:///"):
            return Path(url.replace("sqlite:///", ""))
        return Path("data/studeo.db")

    def ensure_dirs(self) -> None:
        """Cria diretórios de dados se não existem."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.materials_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Retorna instância singleton das configurações."""
    return Settings()
