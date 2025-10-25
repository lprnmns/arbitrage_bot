"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.engine import make_url

from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()


def _get_sqlite_dir() -> Path | None:
    """Return directory for sqlite DBs if used."""
    url = make_url(settings.database_url)
    if url.drivername != "sqlite" or not url.database:
        return None
    return Path(url.database).expanduser().resolve().parent


db_dir = _get_sqlite_dir()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Prepare directories before serving requests."""
    if db_dir:
        db_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)
