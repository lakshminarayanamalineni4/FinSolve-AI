from app.services.vector.qdrant import (
    COLLECTION_NAME,
    VECTOR_SIZE,
    QdrantService,
)


def main() -> None:
    service = QdrantService()

    service.create_collection()

    collection = service.client.get_collection(
        COLLECTION_NAME
    )

    print(f"Collection: {COLLECTION_NAME}")
    print(f"Status: {collection.status}")
    print(f"Vector size: {collection.config.params.vectors.size}")
    print(f"Distance: {collection.config.params.vectors.distance}")

    print("\nPayload indexes:")

    payload_indexes = (
        collection.payload_schema
        if hasattr(collection, "payload_schema")
        else {}
    )

    for field_name in (
        "document_id",
        "department",
        "required_permission",
    ):
        print(f"- {field_name}")


if __name__ == "__main__":
    main()