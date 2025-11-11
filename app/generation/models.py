from typing import Any
from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    """
    GenerationRequest defines the structure for a text generation request.
    """

    query: str = Field(..., description="The input query for generation", min_length=1)
    context_size: int = Field(
        3, description="The number of retrieved contexts to consider", ge=1
    )
    model_name: str | None = "mock-llm"


class GenerateAnswer(BaseModel):
    """
    GenerateAnswer defines the structure for the generated answer from the model.
    """

    text: str
    used_contexts: list[dict[str, Any]]


class GenerationResponse(BaseModel):
    """
    GenerationResponse defines the structure for the response of a generation request.
    it contains the original query and the generated answer by the llm.
    """

    query: str
    answer: GenerateAnswer
