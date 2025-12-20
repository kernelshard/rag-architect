import time
from app.core.logging import get_logger
from app.core.metrics import (
    APP_NAME,
    APP_PROMPT_BUILD_SECONDS,
    APP_GENERATION_LATENCY_SECONDS,
)
from app.evaluation.recall import recall_at_k
from app.generation.models import GenerateAnswer, GenerationRequest, GenerationResponse
from app.generation.prompt_builder import build_prompt

from app.core.interfaces import BaseGenerator, BaseRetriever
from app.evaluation.trace_writer import write_trace


logger = get_logger(__name__)


async def generate_answer(
    req: GenerationRequest,
    retriever: BaseRetriever,
    generator: BaseGenerator,
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
    """
    logger.debug(f"Retrieved {len(retrieved_chunks)} chunks")

    # prompt build metrics
    t0 = time.monotonic()
    prompt = build_prompt(req.query, retrieved_chunks)
    APP_PROMPT_BUILD_SECONDS.labels(app_name=APP_NAME).observe(time.monotonic() - t0)

    # Generation latency metrics
    t1 = time.monotonic()
    answer_text = await generator.generate(prompt=prompt)
    APP_GENERATION_LATENCY_SECONDS.labels(app_name=APP_NAME).observe(
        time.monotonic() - t1
    )

    logger.info(f"Generated answer for query='{req.query}'")

    # Write trace for the generation
    recall_k = None
    if req.expected_doc_ids:
        recall_k = recall_at_k(
            retrieved_ids=[chunk["doc_id"] for chunk in retrieved_chunks],
            relevant_ids=set(req.expected_doc_ids),
            k=req.context_size,
        )
        logger.info(
            f"Recall@{req.context_size} for query='{req.query}': {recall_k:.2f}"
        )
    write_trace(
        query=req.query,
        retrieved_ids=[chunk["doc_id"] for chunk in retrieved_chunks],
        answer_text=answer_text,
        recall_k=recall_k,
        faithfulness=None,
    )

    return GenerationResponse(
        query=req.query,
        answer=GenerateAnswer(
            text=answer_text,
            used_context=retrieved_chunks,
            recall_at_k=recall_k,
        ),
    )
