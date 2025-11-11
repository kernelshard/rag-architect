from fastapi import APIRouter, status, Depends

from app.core.interfaces import BaseRetriever
from app.core.logging import get_logger
from app.generation.deps import get_retriever
from app.generation.models import GenerationRequest, GenerationResponse
from app.generation.service import generate_anwer

logger = get_logger(__name__)

router = APIRouter(prefix="/generation", tags=["generation"])


@router.post(
    "/generate",
    response_model=GenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate answer based on query and retrieved contexts",
)
async def generate_endpoint(
    req: GenerationRequest, retriever: BaseRetriever = Depends(get_retriever)
):
    logger.info(
        "Received generation request", query=req.query, context_size=req.context_size
    )
    return await generate_anwer(req, retriever)
