from typing import Any
from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    query: str = Field(
        ..., min_length=1, description="User's natural language search query"
    )
    top_k: int = Field(5, gt=0, le=50, description="Number of top results to retrieve")
    filters: dict[str, Any] | None = Field(
        None,
        description="Optional metadata filter to restrict search resources (e.g. tag=value, tag ...",
    )
    include_metadata: bool = Field(
        default=True, description="Whether to include metadata in the retrieval results"
    )

    model_config = {"extra": "ignore"}


class RetrievedChunk(BaseModel):
    """
    A single Document chunk retrieved from the vector search.
    """

    doc_id: str = Field(..., description="ID of the document chunk")
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized similarity score")
    metadata: dict[str, Any] | None = Field(
        None, description="Optional metadata related to the chunk"
    )


class RetrievalResponse(BaseModel):
    """Response model for retrieval results."""

    query: str = Field(..., description="Original search query")
    results: list[RetrievedChunk] = Field(
        ...,
        description="Top-k retrieved & ranked document chunks relevant to the query",
    )

    model_config = {"extra": "ignore"}
