"""Configuration endpoints."""

from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_config_service
from app.schemas.config import ConfigResponse, ConfigUpdateRequest, HLRuntimeConfig
from app.services.config_service import ConfigService
from app.services.hl_market_data import NETWORK_TO_URL
from app.services.status_tracker import StatusTracker

router = APIRouter()


def _to_response(config: HLRuntimeConfig) -> ConfigResponse:
    return ConfigResponse(
        network=config.network,
        api_base_url=NETWORK_TO_URL[config.network],
        fees=config.fees,
    )


@router.get("/config", response_model=ConfigResponse)
def get_config(config_service: ConfigService = Depends(get_config_service)) -> ConfigResponse:
    config = config_service.get_hl_config()
    return _to_response(config)


@router.put("/config", response_model=ConfigResponse)
def update_config(
    update: ConfigUpdateRequest,
    request: Request,
    config_service: ConfigService = Depends(get_config_service),
) -> ConfigResponse:
    new_config = HLRuntimeConfig(**update.model_dump())
    saved = config_service.update(new_config)
    status_tracker: StatusTracker = request.app.state.status_tracker
    status_tracker.set_hl_env(saved.network.value)
    return _to_response(saved)
