from fastapi import APIRouter

from app.evaludation.aggregate import aggregate_traces


router = APIRouter(prefix="/eval", tags=["evaluation"])


@router.get("/summary")
async def evaluation_summary() -> dict:
    return aggregate_traces()
