"""Response shapes for market summary endpoint."""

from typing import List, Optional

from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    symbol: str
    best_bid: Optional[float]
    best_ask: Optional[float]
    best_bid_size: Optional[float]
    best_ask_size: Optional[float]
    spread_bps: Optional[float]
    trades_last_min: int


class MarketSummaryResponse(BaseModel):
    markets: List[MarketSnapshot]
