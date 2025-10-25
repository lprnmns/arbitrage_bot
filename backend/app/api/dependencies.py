"""Common dependency helpers."""

from fastapi import Request

from app.services.config_service import ConfigService


def get_config_service(request: Request) -> ConfigService:
    return request.app.state.config_service
