from app.core.logging import get_logger
from app.generation.models import GenerateAnswer, GenerationRequest, GenerationResponse
from app.generation.prompt_builder import build_prompt

from app.core.interfaces import BaseRetriever


logger = get_logger(__name__)


async def generate_answer(
    req: GenerationRequest, retriever: BaseRetriever
) -> GenerationResponse:
    """
    generate handles the text generation process by retrieving relevant documents
    and generating an answer based on the input query and contexts.

    Args:
        req (GenerationRequest): The generation request containing the query and parameters.
        retriever (BaseRetriever): The retriever instance to fetch relevant documents.

    Returns:
        GenerationResponse: The response containing the original query and generated answer.
    """
    # retrieve top-k relevant documents based on the query
    logger.info(f"Generation started for query='{req.query}'")

    retrieved_chunks = await retriever.retrieve(req.query, req.context_size)
    """
    e.g: retrieved_chunks = [
        {"doc_id": "1", "score": 0.8, "metadata": {"source": "source1"}},
        {"doc_id": "2", "score": 0.7, "metadata": {"source": "source2"}},
        ...
    ]
    Note: Does not include original text; only doc_id and metadata.
    """
    logger.debug(f"Retrieved {len(retrieved_chunks)} chunks")

    _ = build_prompt(req.query, retrieved_chunks)

    synthesized = (
        " ".join(chunk["doc_id"] for chunk in retrieved_chunks) or "No context found."
    )

    logger.info(
        f"Generated answer for query='{req.query}' using {len(retrieved_chunks)}"
    )

    return GenerationResponse(
        query=req.query,
        answer=GenerateAnswer(
            text=f"Mock answer: {synthesized}",
            used_contexts=retrieved_chunks,
        ),
    )
