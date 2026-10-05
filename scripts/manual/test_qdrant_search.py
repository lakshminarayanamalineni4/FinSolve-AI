from qdrant_client import QdrantClient
from app.services.embeddings.qwen import QwenEmbeddingService


COLLECTION_NAME = "finsolve_chunks"

TEST_QUERIES = [
    "What does FinSolve do?",
    "What is FinSolve's company overview?",
    "How does the engineering architecture work?",
    "What is the finance department responsible for?",
    "What are the HR policies?",
]

def main() -> None:
    # Connect to the existing local Qdrant database
    client = QdrantClient(path="./qdrant_data")

    # Create the embedding service
    embedding_service = QwenEmbeddingService()

    for query in TEST_QUERIES:
        # Convert the query into a 1024-dimensional vector
        query_embedding = embedding_service.embed_query(query)

        # Search for the most semantically similar points
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=3,
            with_payload=True,
            with_vectors=False,
        ).points

        print(f"Query: {query}")
        print()
        print("Search results:")
        print("=" * 80)

        for result in results:
            print(f"Score: {result.score:.4f}")
            print(f"Point ID: {result.id}")

            payload = result.payload or {}

            print(f"Document ID: {payload.get('document_id')}")
            print(f"Chunk Index: {payload.get('chunk_index')}")
            print(f"Department: {payload.get('department')}")
            print(f"Permission: {payload.get('required_permission')}")
            print(f"Content:\n{payload.get('content')}")

            print("-" * 80)


if __name__ == "__main__":
    main()

