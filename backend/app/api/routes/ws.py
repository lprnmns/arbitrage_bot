"""WebSocket placeholder endpoint for future HL streams."""

import asyncio
from datetime import datetime
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


class ConnectionManager:
    """Minimal WebSocket manager for mock broadcasts."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, payload: dict) -> None:
        for ws in list(self.active_connections):
            try:
                await ws.send_json(payload)
            except RuntimeError:
                self.disconnect(ws)


manager = ConnectionManager()


@router.websocket("/ws/stream")
async def stream_placeholder(websocket: WebSocket) -> None:
    """
    Accept WebSocket connections and emit mock heartbeat payloads.

    Actual HL market data wiring happens in later phases once endpoints are approved.
    """

    await manager.connect(websocket)
    try:
        while True:
            await manager.broadcast(
                {
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "status": "placeholder",
                }
            )
            await asyncio.sleep(settings.ws_broadcast_interval_ms / 1000)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
