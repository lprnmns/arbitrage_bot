"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import redis
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import engine
from app.schemas.config import HLRuntimeConfig
from app.services.config_service import ConfigService
from app.services.hl_market_data import HLMarketDataService
from app.services.log_store import LogStore
from app.services.status_tracker import StatusTracker

settings = get_settings()


def _get_sqlite_dir() -> Optional[Path]:
    url = make_url(settings.database_url)
    if url.drivername != "sqlite" or not url.database:
        return None
    return Path(url.database).expanduser().resolve().parent


db_dir = _get_sqlite_dir()
status_tracker = StatusTracker(build=settings.build_version)
log_store = LogStore()
hl_service = HLMarketDataService(
    symbols=settings.hl_symbols,
    status_tracker=status_tracker,
    log_store=log_store,
    enable_ingest=settings.enable_market_data_ingest,
)
config_service = ConfigService(Path(settings.config_file_path))
config_service.subscribe(hl_service.handle_config_update)


def _check_db() -> bool:
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def _check_redis() -> bool:
    try:
        client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=1)
        client.ping()
        return True
    except Exception:
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    if db_dir:
        db_dir.mkdir(parents=True, exist_ok=True)
    app.state.config_service = config_service
    app.state.status_tracker = status_tracker
    app.state.log_store = log_store

    status_tracker.set_db_status(_check_db())
    status_tracker.set_redis_status(_check_redis())
    initial_config: HLRuntimeConfig = config_service.get_hl_config()
    hl_service.start(initial_config)
    yield
    hl_service.stop()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)
