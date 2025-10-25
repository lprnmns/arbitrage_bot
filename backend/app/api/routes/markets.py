"""Market summary endpoints."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.market import Tick, Trade
from app.schemas.market_summary import MarketSnapshot, MarketSummaryResponse
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/markets/summary", response_model=MarketSummaryResponse)
def market_summary(db: Session = Depends(get_db)) -> MarketSummaryResponse:
    now = datetime.now(timezone.utc)
    one_min_ago = now - timedelta(minutes=1)
    markets = []
    for symbol in settings.hl_symbols:
        tick = (
            db.query(Tick)
            .filter(Tick.symbol == symbol)
            .order_by(Tick.recorded_at.desc())
            .first()
        )
        trade_count = (
            db.query(func.count(Trade.id))
            .filter(Trade.symbol == symbol, Trade.recorded_at >= one_min_ago)
            .scalar()
        )
        markets.append(
            MarketSnapshot(
                symbol=symbol,
                best_bid=tick.best_bid if tick else None,
                best_ask=tick.best_ask if tick else None,
                best_bid_size=tick.best_bid_size if tick else None,
                best_ask_size=tick.best_ask_size if tick else None,
                spread_bps=tick.spread_bps if tick else None,
                trades_last_min=int(trade_count or 0),
            )
        )
    return MarketSummaryResponse(markets=markets)
