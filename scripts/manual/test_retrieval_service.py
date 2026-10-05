from qdrant_client import QdrantClient

from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.query.processor import QueryProcessor
from app.services.retrieval.service import RetrievalService


COLLECTION_NAME = "finsolve_chunks"


def main() -> None:
    client = QdrantClient(path="./qdrant_data")

    embedding_service = QwenEmbeddingService()
    query_processor = QueryProcessor()

    retrieval_service = RetrievalService(
        client=client,
        embedding_service=embedding_service,
    )

    query = query_processor.process(
        "What is the finance department responsible for?"
    )

    results = retrieval_service.retrieve(
        query=query,
        limit=5,
    )

    print(f"Query: {query.processed}")
    print(f"Results: {len(results)}")

    for rank, result in enumerate(results, start=1):
        print()
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Point ID: {result.point_id}")
        print(f"Document ID: {result.document_id}")
        print(f"Chunk Index: {result.chunk_index}")
        print(f"Department: {result.department}")
        print(f"Permission: {result.required_permission}")
        print(f"Content:\n{result.content}")


if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.test_retrieval_service