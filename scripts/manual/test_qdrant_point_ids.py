from app.services.vector.qdrant_client import generate_point_id


def main() -> None:
    first_id = generate_point_id(
        document_id=1,
        chunk_index=4,
    )

    second_id = generate_point_id(
        document_id=1,
        chunk_index=4,
    )

    different_id = generate_point_id(
        document_id=1,
        chunk_index=5,
    )

    print(f"First ID:     {first_id}")
    print(f"Second ID:    {second_id}")
    print(f"Different ID: {different_id}")
    print()

    print(
        f"Same chunk produces same ID: "
        f"{first_id == second_id}"
    )

    print(
        f"Different chunk produces different ID: "
        f"{first_id != different_id}"
    )


if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.test_qdrant_point_ids