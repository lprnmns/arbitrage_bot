"""WebSocket streams."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.config import get_settings
from app.services.status_tracker import StatusTracker

router = APIRouter()
settings = get_settings()


@router.websocket("/ws/stream")
async def heartbeat_stream(websocket: WebSocket) -> None:
    """Emit heartbeat payloads for the Latency HUD."""
    await websocket.accept()
    tracker: StatusTracker = websocket.app.state.status_tracker
    try:
        while True:
            snapshot = tracker.snapshot()
            payload = {
                "ts": snapshot.ts,
                "mode": snapshot.mode,
                "backend_ws_ok": snapshot.backend_ws_ok,
                "redis_ok": snapshot.redis_ok,
                "db_ok": snapshot.db_ok,
                "hl_env": snapshot.hl_env,
                "latency_mock_ms": snapshot.latency_mock_ms,
                "build": snapshot.build,
                "msgs_1m": snapshot.msgs_1m,
                "last_tick_ts": snapshot.last_tick_ts,
                "uptime_s": snapshot.uptime_s,
            }
            payload.update(snapshot.extra)
            await websocket.send_json(payload)
            await asyncio.sleep(settings.ws_broadcast_interval_ms / 1000)
    except WebSocketDisconnect:
        return
