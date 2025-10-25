"""Manage runtime configuration stored in config/default.yaml."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable, Optional

import yaml

from app.schemas.config import HLRuntimeConfig


class ConfigService:
    """Loads, caches, and persists runtime configuration."""

    def __init__(self, config_path: Path, on_change: Optional[Callable[[HLRuntimeConfig], None]] = None) -> None:
        self._config_path = config_path
        self._lock = threading.RLock()
        self._hl_config = self._load_file()
        self._subscribers: list[Callable[[HLRuntimeConfig], None]] = []
        if on_change:
            self._subscribers.append(on_change)

    def _load_file(self) -> HLRuntimeConfig:
        if not self._config_path.exists():
            return HLRuntimeConfig()
        with self._config_path.open("r", encoding="utf-8") as fp:
            raw = yaml.safe_load(fp) or {}
        hl_raw = raw.get("hl", {})
        return HLRuntimeConfig(**hl_raw)

    def _persist(self) -> None:
        """Write latest config back to disk (merging with existing file)."""
        if self._config_path.exists():
            with self._config_path.open("r", encoding="utf-8") as fp:
                raw = yaml.safe_load(fp) or {}
        else:
            raw = {}
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
        raw["hl"] = self._hl_config.model_dump(mode="json")
        with self._config_path.open("w", encoding="utf-8") as fp:
            yaml.safe_dump(raw, fp, allow_unicode=True, sort_keys=False)

    def get_hl_config(self) -> HLRuntimeConfig:
        with self._lock:
            return HLRuntimeConfig(**self._hl_config.model_dump())

    def update(self, new_config: HLRuntimeConfig) -> HLRuntimeConfig:
        with self._lock:
            self._hl_config = new_config
            self._persist()
            subscribers = list(self._subscribers)
        for callback in subscribers:
            callback(self.get_hl_config())
        return self.get_hl_config()

    def subscribe(self, callback: Callable[[HLRuntimeConfig], None]) -> None:
        with self._lock:
            self._subscribers.append(callback)
