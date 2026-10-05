from qdrant_client import QdrantClient

from app.services.context.builder import ContextBuilder
from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.query.processor import QueryProcessor
from app.services.retrieval.service import RetrievalService


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

    context_builder = ContextBuilder()

    context = context_builder.build(results)

    print("=" * 80)
    print("GENERATED CONTEXT")
    print("=" * 80)
    print(context.text)

    print()
    print("=" * 80)
    print("SOURCE COUNT")
    print("=" * 80)
    print(len(context.sources))


if __name__ == "__main__":
    main()