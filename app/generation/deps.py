from app.core.interfaces import BaseRetriever
from app.retrieval.models import RetrievalRequest
from app.retrieval.service import retrieve_documents
from app.core.repositories import global_vector_repo


class RetrievalAdapter(BaseRetriever):
    """
    Adapter to wrap retrieval logic behind a common interface.
    This is because - different retrieval implementations may have different method signatures.
    """

    async def retrieve(
        self, query: str, top_k: int, include_metadata: bool = True
    ) -> list[dict]:
        request = RetrievalRequest(query=query, top_k=top_k, filters=None)
        reponse = await retrieve_documents(request, global_vector_repo)
        # It converts [RetrievedChunk, ...] to [dict, ...] cause GenerateAnswer.used_contexts expects list[dict]
        # e.g: response = RetrievalResponse(results=[RetrievedChunk(...), ...])
        # so after conversion res becomes:
        # [{"doc_id": "1", "content": "Document content 1", "metadata": {"source": "source1"}}, ...]
        res = [r.model_dump() for r in reponse.results]
        return res


# make a singleton instance for easy import
_retriever = RetrievalAdapter()


def get_retriever() -> BaseRetriever:
    """
    Returns the global retriever instance.
    """
    return _retriever
