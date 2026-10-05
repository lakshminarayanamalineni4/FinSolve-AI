from qdrant_client import QdrantClient

from app.core.config import settings
from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.query.models import Query
from app.services.retrieval.models import RetrievalResult


COLLECTION_NAME = "finsolve_chunks"


class RetrievalService:
    def __init__(
        self,
        client: QdrantClient,
        embedding_service: QwenEmbeddingService,
    ) -> None:
        self.client = client
        self.embedding_service = embedding_service

    def retrieve(
        self,
        query: Query,
        limit: int = 5,
        query_filter=None,
    ) -> list[RetrievalResult]:

        query_embedding = self.embedding_service.embed_query(
            query.processed
        )

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        ).points

        return [
            self._to_retrieval_result(result)
            for result in results
        ]

    @staticmethod
    def _to_retrieval_result(result) -> RetrievalResult:
        payload = result.payload or {}

        return RetrievalResult(
            point_id=str(result.id),
            score=float(result.score),
            document_id=int(payload["document_id"]),
            chunk_index=int(payload["chunk_index"]),
            department=str(payload["department"]),
            required_permission=str(
                payload["required_permission"]
            ),
            content=str(payload["content"]),
        )