# from qdrant_client import QdrantClient
# from qdrant_client.models import Filter, FieldCondition, MatchValue

# from app.services.embeddings.qwen import QwenEmbeddingService

# COLLECTION_NAME = "finsolve_chunks"


# def main() -> None:
#     client = QdrantClient(path="./qdrant_data")

#     embedding_service = QwenEmbeddingService()

#     query = "How does the engineering & general architecture work?"

#     query_embedding = embedding_service.embed_query(query)

#     # engineering_filter = Filter(
#     #     must=[
#     #         FieldCondition(
#     #             key="department",
#     #             match=MatchValue(
#     #                 value="engineering"
#     #             ),
#     #         )
#     #     ]
#     # )

#     # permission_filter = Filter(
#     #     must=[
#     #         FieldCondition(
#     #             key="required_permission",
#     #             match=MatchValue(
#     #                 value="read_engineering"
#     #             ),
#     #         )
#     #     ]
#     # )

#     permission_filter = Filter(
#         should=[
#             FieldCondition(
#                 key="required_permission",
#                 match=MatchValue(
#                     value="read_engineering"
#                 ),
#             ),
#             FieldCondition(
#                 key="required_permission",
#                 match=MatchValue(
#                     value="read_general"
#                 ),
#             ),
#         ]
#     )

#     results = client.query_points(
#         collection_name=COLLECTION_NAME,
#         query=query_embedding,
#         query_filter=permission_filter,
#         limit=10,
#         with_payload=True,
#         with_vectors=False,
#     ).points

#     print(f"Query: {query}")
#     print("Filter: required_permission = read_engineering OR required_permission = read_general")
#     print()
#     print("Search results:")
#     print("=" * 80)

#     for rank, result in enumerate(results, start=1):
#         payload = result.payload or {}

#         print(f"Rank: {rank}")
#         print(f"Score: {result.score:.4f}")
#         print(f"Point ID: {result.id}")
#         print(f"Document ID: {payload.get('document_id')}")
#         print(f"Chunk Index: {payload.get('chunk_index')}")
#         print(f"Department: {payload.get('department')}")
#         print(f"Permission: {payload.get('required_permission')}")
#         print(f"Content:\n{payload.get('content')}")
#         print("-" * 80)


# if __name__ == "__main__":
#     main()

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.services.embeddings.qwen import QwenEmbeddingService

COLLECTION_NAME = "finsolve_chunks"

ALLOWED_PERMISSIONS = [
    "read_engineering",
    "read_general",
]


def main() -> None:
    client = QdrantClient(path="./qdrant_data")

    embedding_service = QwenEmbeddingService()

    query = "What are the finance policies?"

    query_embedding = embedding_service.embed_query(query)

    permission_filter = Filter(
        should=[
            FieldCondition(
                key="required_permission",
                match=MatchValue(
                    value=permission
                ),
            )
            for permission in ALLOWED_PERMISSIONS
        ]
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=permission_filter,
        limit=10,
        with_payload=True,
        with_vectors=False,
    ).points

    print(f"Query: {query}")
    print(
        "Allowed permissions: "
        f"{ALLOWED_PERMISSIONS}"
    )
    print()
    print("Search results:")
    print("=" * 80)

    for rank, result in enumerate(results, start=1):
        payload = result.payload or {}

        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Point ID: {result.id}")
        print(f"Document ID: {payload.get('document_id')}")
        print(f"Chunk Index: {payload.get('chunk_index')}")
        print(f"Department: {payload.get('department')}")
        print(f"Permission: {payload.get('required_permission')}")
        print(f"Content:\n{payload.get('content')}")
        print("-" * 80)


if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.test_qdrant_filter