"""Pydantic models for runtime configuration exposed to the UI."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class HLNetwork(str, Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"


class FeeConfig(BaseModel):
    spot_fee_bps: Optional[float] = Field(default=None, ge=0)
    perp_fee_bps: Optional[float] = Field(default=None, ge=0)


class HLRuntimeConfig(BaseModel):
    network: HLNetwork = HLNetwork.MAINNET
    fees: FeeConfig = Field(default_factory=FeeConfig)


class ConfigResponse(BaseModel):
    network: HLNetwork
    api_base_url: str
    fees: FeeConfig


class ConfigUpdateRequest(BaseModel):
    network: HLNetwork
    fees: FeeConfig
