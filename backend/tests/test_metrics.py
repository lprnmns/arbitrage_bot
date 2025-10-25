"""Tests for metrics endpoints."""

import os

os.environ.setdefault("ENABLE_MARKET_DATA_INGEST", "false")

from fastapi.testclient import TestClient

from app.main import app


def test_metrics_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/metrics/health")
        assert response.status_code == 200
        payload = response.json()
        assert "build" in payload
        assert "hl_env" in payload
        assert "msgs_1m" in payload and "l2" in payload["msgs_1m"]
        assert "uptime_s" in payload
