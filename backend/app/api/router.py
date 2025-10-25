"""Root API router."""

from fastapi import APIRouter

from app.api.routes import health, ws

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(ws.router, tags=["ws"])
