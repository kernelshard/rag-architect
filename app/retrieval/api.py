from __future__ import annotations
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.logging import get_logger
from app.core.interfaces import BaseVectorSearchRepository
from app.retrieval.deps import get_vector_repo
from app.retrieval.models import RetrievalRequest, RetrievalResponse
from app.retrieval.service import retrieve_documents

logger = get_logger(__name__)


router = APIRouter(prefix="/retrieval", tags=["retrieval"])


@router.post(
    "/query",
    response_model=RetrievalResponse,
    status_code=status.HTTP_200_OK,
    summary="Query the vector store and return top-k results",
)
async def query_endpoint(
    request: RetrievalRequest,
    repo: Annotated[BaseVectorSearchRepository, Depends(get_vector_repo)],
) -> RetrievalResponse:
    """
    Converts the user query into an embedding,  performs a similarity search via
    the repository, and returns the top-k results.

    Notes:
        - Global HTTP request metrics are automatically recorded by middleware.
        - Additional domain metrics can be added later if needed.
    """
    logger.info("Retrieval request received", query=request.query, top_k=request.top_k)

    try:
        # Core processing is delegated to the service layer
        response = await retrieve_documents(request, repo)

        logger.info(
            "Retrieval completed successfully",
            query=request.query,
            results_count=len(response.results),
        )
        return response

    except HTTPException:
        # Re-raise FastAPI HTTP errors unchanged
        raise

    except Exception as exc:
        logger.exception("Unhandled error during retrieval", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during retrieval",
        )
