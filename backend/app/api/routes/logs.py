"""WebSocket endpoint streaming log lines."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.log_store import LogStore

router = APIRouter()


async def stream_logs(websocket: WebSocket, store: LogStore) -> None:
    await websocket.accept()
    cursor = 0
    try:
        while True:
            entries, cursor = store.read_since(cursor)
            for entry in entries:
                await websocket.send_json(entry)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return


@router.websocket("/ws/logs")
async def logs_ws(websocket: WebSocket):
    store: LogStore = websocket.app.state.log_store
    await stream_logs(websocket, store)
