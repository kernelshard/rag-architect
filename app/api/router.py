from fastapi import APIRouter

from core import start_time

import time

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/ping", summary="Liveness / simple healthcheck")
async def pint():
    uptime = time.time()
    return {"status": "ok", "message": "pong", "uptime_seconds": round(uptime, 2)}
