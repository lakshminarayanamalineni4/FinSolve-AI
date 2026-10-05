from qdrant_client import QdrantClient


COLLECTION_NAME = "finsolve_chunks"


def main() -> None:
    client = QdrantClient(path="./qdrant_data")

    collection = client.get_collection(COLLECTION_NAME)

    print("Collection configuration:")
    print(f"Name: {COLLECTION_NAME}")
    print(f"Status: {collection.status}")
    print(f"Vector size: {collection.config.params.vectors.size}")
    print(f"Distance: {collection.config.params.vectors.distance}")


if __name__ == "__main__":
    main()