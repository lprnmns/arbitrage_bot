"""Background worker placeholder."""

import asyncio
import json
import logging
import signal
from typing import Any

import redis.asyncio as redis

from app.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


class WorkerService:
    """Periodic heartbeat publisher to redis."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._shutdown = asyncio.Event()
        self._redis: redis.Redis | None = None

    async def start(self) -> None:
        self._redis = redis.from_url(self.settings.redis_url, decode_responses=True)
        logger.info("Worker connected to redis")
        while not self._shutdown.is_set():
            payload: dict[str, Any] = {"channel": "worker-heartbeat", "status": "idle"}
            await self._redis.publish("worker-heartbeat", json.dumps(payload))
            await asyncio.sleep(self.settings.heartbeat_interval_sec)

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()
        self._shutdown.set()


async def main() -> None:
    service = WorkerService()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(service.close()))

    await service.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker shutdown requested")
