"""Application configuration loaded via environment variables."""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_PATH = Path(__file__).resolve().parents[3]
_DEFAULT_DB_PATH = _BASE_PATH / "db" / "arbitrage.db"
_DEFAULT_CONFIG_PATH = _BASE_PATH / "config" / "default.yaml"


class Settings(BaseSettings):
    """Centralized app configuration."""

    app_name: str = Field(default="Arbitrage Backend")
    environment: str = Field(default="development")
    database_url: str = Field(default=f"sqlite:///{_DEFAULT_DB_PATH.as_posix()}", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    ws_broadcast_interval_ms: int = Field(default=1000)
    config_file_path: str = Field(default=_DEFAULT_CONFIG_PATH.as_posix(), alias="CONFIG_FILE_PATH")
    hl_symbols: List[str] = Field(default_factory=lambda: ["HYPE", "SOL", "BTC"])
    build_version: str = Field(default="dev", alias="BUILD_VERSION")
    enable_market_data_ingest: bool = Field(default=True, alias="ENABLE_MARKET_DATA_INGEST")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
