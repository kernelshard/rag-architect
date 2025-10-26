import time
from typing import Any

from fastapi import APIRouter

from app.core import start_time

router = APIRouter(prefix="/api/v1", tags=["api"])


@router.get("/ping", summary="Liveness / simple healthcheck")
async def ping() -> dict[str, Any]:
    uptime = time.time() - start_time
    return {"status": "ok", "message": "pong", "uptime_seconds": round(uptime, 2)}
