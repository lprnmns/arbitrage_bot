"""Application configuration loaded via environment variables."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_DB_PATH = Path(__file__).resolve().parents[3] / "db" / "arbitrage.db"


class Settings(BaseSettings):
    """Centralized app configuration."""

    app_name: str = Field(default="Arbitrage Backend")
    environment: str = Field(default="development")
    database_url: str = Field(
        default=f"sqlite:///{_DEFAULT_DB_PATH.as_posix()}",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    ws_broadcast_interval_ms: int = Field(default=1000)

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
