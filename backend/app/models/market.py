"""Market data related tables."""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer, String, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Tick(Base):
    """Order book snapshot metadata."""

    __tablename__ = "ticks"
    __table_args__ = (Index("idx_ticks_symbol_ts_ns", "symbol", "ts_ns"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    ts_ns: Mapped[int] = mapped_column(BigInteger, index=True)
    venue: Mapped[str] = mapped_column(String(32), default="HL")
    best_bid: Mapped[float] = mapped_column(Float)
    best_bid_size: Mapped[float] = mapped_column(Float)
    best_ask: Mapped[float] = mapped_column(Float)
    best_ask_size: Mapped[float] = mapped_column(Float)
    spread_bps: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(64), default="HL")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Trade(Base):
    """Recent trades stream metadata."""

    __tablename__ = "trades"
    __table_args__ = (Index("idx_trades_symbol_ts_ns", "symbol", "ts_ns"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    venue: Mapped[str] = mapped_column(String(32), default="HL")
    ts_ns: Mapped[int] = mapped_column(BigInteger, index=True)
    side: Mapped[str] = mapped_column(String(4))
    price: Mapped[float] = mapped_column(Float)
    size: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(64), default="HL")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
