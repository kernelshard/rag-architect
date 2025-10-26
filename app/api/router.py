import time
from typing import Any

from fastapi import APIRouter

from app.core import start_time

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/ping", summary="Liveness / simple healthcheck")
async def ping() -> dict[str, Any]:
    uptime = start_time - time.time()
    return {"status": "ok", "message": "pong", "uptime_seconds": round(uptime, 2)}
