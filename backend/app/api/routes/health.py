"""Health check route."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    """Return basic liveness data."""
    return {"status": "ok"}
