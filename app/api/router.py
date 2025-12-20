import time
from typing import Any

from fastapi import APIRouter

from app.core import start_time
from app.retrieval.api import router as retrival_router
from app.ingestion.api import router as ingestion_router
from app.generation.api import router as generation_router
from app.evaluation.api import router as evaluation_router


router = APIRouter(prefix="/api/v1", tags=["api"])


@router.get("/ping", summary="Liveness / simple healthcheck")
async def ping() -> dict[str, Any]:
    uptime = time.time() - start_time
    return {"status": "ok", "message": "pong", "uptime_seconds": round(uptime, 2)}


# Attach domain routers here
router.include_router(retrival_router)
router.include_router(ingestion_router)
router.include_router(generation_router)
router.include_router(evaluation_router)
