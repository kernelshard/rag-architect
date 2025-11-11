import asyncio

from app.core.logging import get_logger
from app.generation.models import GenerateAnswer, GenerationRequest, GenerationResponse

from app.core.interfaces import BaseRetriever


logger = get_logger(__name__)


async def generate_anwer(
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
    retrieved_chunks = await retriever.retrieve(req.query, req.context_size)
    """
    e.g: retrieved_chunks = [
        {"doc_id": "1", "content": "Document content 1", "metadata": {"source": "source1"}},
        {"doc_id": "2", "content": "Document content 2", "metadata": {"source": "source2"}},
        ...
    ]
    """

    await asyncio.sleep(0.1)  # simulate llm latency

    # e.g context = [
    #     {"doc_id": "1", "content": "Document content 1", "metadata": {"source": "source1"}},
    #     {"doc_id": "2", "content": "Document content 2", "metadata": {"source": "source2"}},
    #     ...
    # ]
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
