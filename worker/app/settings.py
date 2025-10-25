"""Worker configuration management."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven worker settings."""

    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    heartbeat_interval_sec: int = Field(default=5)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
