import json
import math
from typing import Any

from app.core.interfaces import BaseVectorSearchRepository
import sqlite3


class SQLiteVectorRepo(BaseVectorSearchRepository):
    def __init__(self, db_path: str = "var/vector_store.sqlite"):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        """
        Initialize the SQLite database and create necessary tables.

        create table embeddings if it does not exist.
        with columns:
        - doc_id: TEXT PRIMARY KEY
        - vector: TEXT NOT NULL
        - metadata: TEXT
        """
        with self._conn() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                      doc_id TEXT PRIMARY KEY,
                      vector TEXT NOT NULL,
                      metadata TEXT
            )
            """)
            c.commit()

    async def store_embedding(
        self, doc_id: str, vector: list[float], metadata: dict[str, Any] | None = None
    ) -> None:
        """
        Store an embedding in the database.

        :param self: The instance of the repository.
        :type self: SQLiteVectorRepo
        :param doc_id: document identifier
        :type doc_id: str
        :param vector: Embedding vector as a list of floats
        :type vector: list[float]
        :param metadata: Additional information associated with the embedding
        :type metadata: dict[str, Any] | None
        """
        with self._conn() as c:
            c.execute(
                "INSERT OR REPLACE INTO embeddings (doc_id, vector, metadata) VALUES (?, ?, ?)",
                (doc_id, json.dumps(vector), json.dumps(metadata or {})),
            )
            c.commit()

    async def query(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
        include_metadata: bool = True,
    ) -> list:
        """
        Query the database for the top_k most similar embeddings to the query_vector.
        :param self: The instance of the repository.
        :type self: SQLiteVectorRepo
        :param query_vector: The embedding vector to query against
        :type query_vector: list[float]
        :param top_k: Number of top similar embeddings to return
        :type top_k: int
        :param filters: Optional filters to apply on metadata
        :type filters: dict[str, Any] | None
        :param include_metadata: Whether to include metadata in the results
        :type include_metadata: bool
        :return: List of tuples (doc_id, similarity_score, metadata)
        :rtype: list[tuple[str, float, dict[str, Any] | None]]
        """

        def cosine(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))
            return (
                0.0 if norm_a == 0 or norm_b == 0 else dot_product / (norm_a * norm_b)
            )

        rows = []

        with self._conn() as c:
            # Retrieve all embeddings and compute similarity
            for doc_id, v, m in c.execute(
                "SELECT doc_id, vector, metadata FROM embeddings"
            ):
                vec = json.loads(v)
                metadata = json.loads(m) if m else {}

                if filters:
                    if not all(metadata.get(k) == v for k, v in filters.items()):
                        continue
                rows.append(
                    {
                        "doc_id": doc_id,
                        "score": round(cosine(query_vector, vec), 3),
                        "metadata": metadata if include_metadata else {},
                    }
                )
        rows.sort(
            key=lambda x: x["score"], reverse=True
        )  # Sort by similarity descending, cause higher is better
        rows = rows[:top_k]
        return rows
