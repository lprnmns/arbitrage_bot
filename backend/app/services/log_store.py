"""Simple in-memory log store to feed /ws/logs."""

from __future__ import annotations

import threading
import time
from typing import Dict, List


class LogStore:
    """Thread-safe append-only log buffer."""

    def __init__(self, max_entries: int = 500) -> None:
        self._lock = threading.RLock()
        self._entries: List[Dict[str, str]] = []
        self._max_entries = max_entries

    def append(self, message: str, level: str = "INFO") -> None:
        payload = {
            "ts": int(time.time() * 1000),
            "level": level,
            "message": message,
        }
        with self._lock:
            self._entries.append(payload)
            if len(self._entries) > self._max_entries:
                self._entries = self._entries[-self._max_entries :]

    def read_since(self, cursor: int) -> tuple[List[Dict[str, str]], int]:
        with self._lock:
            if cursor < 0:
                cursor = 0
            new_entries = self._entries[cursor:]
            next_cursor = cursor + len(new_entries)
            return list(new_entries), next_cursor
