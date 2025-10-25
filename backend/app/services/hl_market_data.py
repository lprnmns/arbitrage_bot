"""Hyperliquid Info WS ingestion + persistence."""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Dict, List, Optional

from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.types import L2BookMsg, Trade, TradesMsg
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.market import Tick, Trade as TradeModel
from app.schemas.config import HLNetwork, HLRuntimeConfig
from app.services.log_store import LogStore
from app.services.status_tracker import StatusTracker

log = logging.getLogger("hl.marketdata")


NETWORK_TO_URL: Dict[HLNetwork, str] = {
    HLNetwork.MAINNET: constants.MAINNET_API_URL,
    HLNetwork.TESTNET: constants.TESTNET_API_URL,
}


def _l2_to_tick(msg: L2BookMsg) -> Optional[Dict]:
    bids, asks = msg["data"]["levels"]
    if not bids or not asks:
        return None
    best_bid = float(bids[0]["px"])
    best_bid_size = float(bids[0]["sz"])
    best_ask = float(asks[0]["px"])
    best_ask_size = float(asks[0]["sz"])
    mid = (best_bid + best_ask) / 2 if (best_bid + best_ask) else 0
    spread_bps = ((best_ask - best_bid) / mid * 10_000) if mid else 0
    ts_ns = int(msg["data"]["time"]) * 1_000_000
    return {
        "symbol": msg["data"]["coin"],
        "ts_ns": ts_ns,
        "best_bid": best_bid,
        "best_bid_size": best_bid_size,
        "best_ask": best_ask,
        "best_ask_size": best_ask_size,
        "spread_bps": spread_bps,
    }


def _trade_to_record(trade: Trade) -> Dict:
    ts_ns = int(trade["time"]) * 1_000_000
    return {
        "symbol": trade["coin"],
        "ts_ns": ts_ns,
        "side": trade["side"],
        "price": float(trade["px"]),
        "size": float(trade["sz"]),
    }


class HLMarketDataService:
    """Owns the Info WS client and writes ticks/trades into SQLite."""

    def __init__(
        self,
        symbols: List[str],
        status_tracker: StatusTracker,
        log_store: LogStore,
        enable_ingest: bool = True,
    ) -> None:
        self._symbols = symbols
        self._status_tracker = status_tracker
        self._log_store = log_store
        self._enable = enable_ingest
        self._info: Optional[Info] = None
        self._current_network: Optional[HLNetwork] = None
        self._shutdown = threading.Event()
        self._lock = threading.RLock()

    def start(self, initial_config: HLRuntimeConfig) -> None:
        if not self._enable:
            log.info("HL ingest disabled via settings")
            return
        threading.Thread(target=self._run, args=(initial_config,), daemon=True).start()

    def stop(self) -> None:
        self._shutdown.set()
        with self._lock:
            if self._info:
                try:
                    self._info.disconnect_websocket()
                    log.info("Disconnected HL info WS (env=%s)", self._current_network.value if self._current_network else "?")
                except Exception:
                    pass
        self._status_tracker.set_backend_ws_status(False)

    def handle_config_update(self, config: HLRuntimeConfig) -> None:
        if not self._enable:
            return
        with self._lock:
            if self._current_network == config.network:
                return
        self._log_store.append(f"HL config changed -> reloading ({config.network.value})")
        self._status_tracker.set_backend_ws_status(False)
        threading.Thread(target=self._connect, args=(config,), daemon=True).start()

    def _run(self, initial_config: HLRuntimeConfig) -> None:
        self._connect(initial_config)
        while not self._shutdown.wait(5):
            continue

    def _connect(self, config: HLRuntimeConfig) -> None:
        with self._lock:
            try:
                if self._info:
                    self._info.disconnect_websocket()
            except Exception:
                pass
            try:
                base_url = NETWORK_TO_URL.get(config.network, constants.MAINNET_API_URL)
                self._info = Info(base_url=base_url, timeout=10)
                self._current_network = config.network
                self._status_tracker.set_backend_ws_status(True)
                self._status_tracker.set_hl_env(config.network.value)
                self._log_store.append(f"Connected to HL info WS (env: {config.network.value})")
                log.info("Connected to HL info WS (env=%s)", config.network.value)
            except Exception as exc:  # pragma: no cover - network failure path
                log.exception("Failed to start HL Info client: %s", exc)
                self._status_tracker.set_backend_ws_status(False)
                time.sleep(5)
                return

        self._subscribe_streams()

    def _subscribe_streams(self) -> None:
        info = self._info
        if info is None:
            return
        for symbol in self._symbols:
            info.subscribe({"type": "l2Book", "coin": symbol}, self._handle_l2)
            info.subscribe({"type": "trades", "coin": symbol}, self._handle_trades)

    def _with_session(self, fn: Callable[[Session], None]) -> None:
        session: Session = SessionLocal()
        try:
            fn(session)
            session.commit()
        except SQLAlchemyError as exc:
            session.rollback()
            log.exception("DB error persisting HL data: %s", exc)
            self._log_store.append(f"DB error persisting HL data: {exc}", level="ERROR")
            self._status_tracker.set_db_status(False)
        finally:
            session.close()

    def _handle_l2(self, msg: L2BookMsg) -> None:
        payload = _l2_to_tick(msg)
        if payload is None:
            return
        payload.update({"venue": "HL", "source": "hl_ws"})

        def persist(session: Session) -> None:
            tick = Tick(**payload)
            session.add(tick)
            self._status_tracker.set_db_status(True)

        self._with_session(persist)
        self._status_tracker.record_tick_event(payload["ts_ns"])

    def _handle_trades(self, msg: TradesMsg) -> None:
        trades = msg["data"]
        if not trades:
            return
        records = [_trade_to_record(trade) for trade in trades]

        def persist(session: Session) -> None:
            for record in records:
                trade = TradeModel(**record, venue="HL", source="hl_ws")
                session.add(trade)
            self._status_tracker.set_db_status(True)

        self._with_session(persist)
        self._status_tracker.record_trade_event(records[0]["ts_ns"])
