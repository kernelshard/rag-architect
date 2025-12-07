from app.core.constants import GeneratorBackend
from app.core.interfaces import BaseGenerator, BaseRetriever
from app.generation.adapters.dryrun_adapter import DryRunGenerator
from app.generation.adapters.ollama_adapter import OllamaGenerator
from app.generation.mock_generator import MockGenerator
from app.retrieval.models import RetrievalRequest
from app.retrieval.service import retrieve_documents
from app.core.repositories import global_vector_repo
from app.core.config import settings


class RetrievalAdapter(BaseRetriever):
    """
    Adapter to wrap retrieval logic behind a common interface.
    This is because - different retrieval implementations may have different method signatures.
    """

    async def retrieve(
        self, query: str, top_k: int, include_metadata: bool = True
    ) -> list[dict]:
        request = RetrievalRequest(query=query, top_k=top_k, filters=None)
        response = await retrieve_documents(request, global_vector_repo)
        # It converts [RetrievedChunk, ...] to [dict, ...] cause GenerateAnswer.used_contexts expects list[dict]
        # e.g: response = RetrievalResponse(results=[RetrievedChunk(...), ...])
        # so after conversion res becomes:
        # [{"doc_id": "1", "content": "Document content 1", "metadata": {"source": "source1"}}, ...]
        res = [r.model_dump() for r in response.results]
        return res


# make a singleton instance for easy import
_retriever = RetrievalAdapter()


def get_retriever() -> BaseRetriever:
    """
    Returns the global retriever instance.
    """
    return _retriever


async def get_generator(
    use_real: bool = settings.USE_REAL_GENERATOR,
    backend: GeneratorBackend = settings.GENERATOR_BACKEND,
):
    """
    Returns a generator instance based on configuration.
    """
    # Precedence: if use_real=False → always Mock
    generator: BaseGenerator
    if not use_real:
        generator = MockGenerator()
    else:
        match backend:
            case GeneratorBackend.Mock:
                generator = MockGenerator()
            case GeneratorBackend.DryRun:
                generator = DryRunGenerator()
            case GeneratorBackend.OPENAI:
                generator = OllamaGenerator()
            case GeneratorBackend.Ollama:
                generator = OllamaGenerator()
            case _:
                generator = OllamaGenerator()  # Default to OllamaGenerator for now
    yield generator
