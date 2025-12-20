from fastapi import APIRouter

from app.evaluation.aggregate import aggregate_traces


router = APIRouter(prefix="/eval", tags=["evaluation"])


@router.get("/summary")
async def evaluation_summary() -> dict:
    return aggregate_traces()
