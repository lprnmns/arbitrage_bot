"""Shared status tracker feeding heartbeat/log endpoints."""

from __future__ import annotations

import random
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class HeartbeatSnapshot:
    ts: int
    mode: str
    backend_ws_ok: bool
    redis_ok: bool
    db_ok: bool
    hl_env: str
    latency_mock_ms: int
    build: str
    msgs_1m: Dict[str, int] = field(default_factory=lambda: {"l2": 0, "trades": 0})
    last_tick_ts: Optional[str] = None
    uptime_s: int = 0
    extra: Dict[str, str] = field(default_factory=dict)


class StatusTracker:
    """Thread-safe storage for subsystem health."""

    def __init__(self, build: str) -> None:
        self._lock = threading.RLock()
        self._start_time = time.time()
        self._l2_events: deque[float] = deque()
        self._trade_events: deque[float] = deque()
        self._last_tick_iso: Optional[str] = None
        self._state = HeartbeatSnapshot(
            ts=self._now_ms(),
            mode="paper",
            backend_ws_ok=False,
            redis_ok=False,
            db_ok=False,
            hl_env="mainnet",
            latency_mock_ms=42,
            build=build,
        )

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def _event_counts(self) -> Dict[str, int]:
        cutoff = time.time() - 60
        self._prune_events(self._l2_events, cutoff)
        self._prune_events(self._trade_events, cutoff)
        return {"l2": len(self._l2_events), "trades": len(self._trade_events)}

    def _prune_events(self, events: deque[float], cutoff: float) -> None:
        while events and events[0] < cutoff:
            events.popleft()

    def _record_event(self, events: deque[float]) -> None:
        with self._lock:
            events.append(time.time())

    def _with_update(self, **kwargs) -> None:
        with self._lock:
            data = self._state.__dict__.copy()
            data.update(kwargs)
            data["ts"] = self._now_ms()
            data["latency_mock_ms"] = 30 + random.randint(0, 25)
            data["msgs_1m"] = self._event_counts()
            data["last_tick_ts"] = self._last_tick_iso
            data["uptime_s"] = int(time.time() - self._start_time)
            self._state = HeartbeatSnapshot(**data)

    def set_backend_ws_status(self, ok: bool) -> None:
        self._with_update(backend_ws_ok=ok)

    def set_redis_status(self, ok: bool) -> None:
        self._with_update(redis_ok=ok)

    def set_db_status(self, ok: bool) -> None:
        self._with_update(db_ok=ok)

    def set_hl_env(self, env: str) -> None:
        self._with_update(hl_env=env)

    def set_mode(self, mode: str) -> None:
        self._with_update(mode=mode)

    def record_tick_event(self, ts_ns: int) -> None:
        iso_ts = (
            datetime.fromtimestamp(ts_ns / 1_000_000_000, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
        with self._lock:
            self._last_tick_iso = iso_ts
        self._record_event(self._l2_events)

    def record_trade_event(self, ts_ns: int) -> None:
        self._record_event(self._trade_events)

    def snapshot(self) -> HeartbeatSnapshot:
        with self._lock:
            data = self._state.__dict__.copy()
            data["msgs_1m"] = self._event_counts()
            data["last_tick_ts"] = self._last_tick_iso
            data["uptime_s"] = int(time.time() - self._start_time)
            return HeartbeatSnapshot(**data)
