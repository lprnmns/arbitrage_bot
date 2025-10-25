"""Metrics endpoints."""

from fastapi import APIRouter, Request

from app.services.status_tracker import StatusTracker

router = APIRouter()


@router.get("/metrics/health")
def metrics_health(request: Request) -> dict:
    tracker: StatusTracker = request.app.state.status_tracker
    snapshot = tracker.snapshot()
    return {
        "ts": snapshot.ts,
        "build": snapshot.build,
        "hl_env": snapshot.hl_env,
        "hl_ws_ok": snapshot.backend_ws_ok,
        "redis_ok": snapshot.redis_ok,
        "db_ok": snapshot.db_ok,
        "msgs_1m": snapshot.msgs_1m,
        "last_tick_ts": snapshot.last_tick_ts,
        "uptime_s": snapshot.uptime_s,
    }
