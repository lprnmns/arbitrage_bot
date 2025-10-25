"""Root API router."""

from fastapi import APIRouter

from app.api.routes import config, health, logs, markets, metrics, ws

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(config.router, tags=["config"])
api_router.include_router(markets.router, tags=["markets"])
api_router.include_router(metrics.router, tags=["metrics"])
api_router.include_router(ws.router, tags=["ws"])
api_router.include_router(logs.router, tags=["logs"])
