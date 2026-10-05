from qdrant_client import QdrantClient

COLLECTION_NAME = "finsolve_chunks"

# These are the IDs from our original 5-point experiment.
EXPERIMENTAL_POINT_IDS = [1, 2, 3, 4, 5]


def main() -> None:
    client = QdrantClient(
        path="./qdrant_data"
    )

    print("Removing experimental points...")

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=EXPERIMENTAL_POINT_IDS,
    )

    collection_info = client.get_collection(
        COLLECTION_NAME
    )

    print(
        f"Points remaining: "
        f"{collection_info.points_count}"
    )


if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.clean_qdrant_collection