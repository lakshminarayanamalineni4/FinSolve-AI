from app.services.chunking.factory import get_chunker
from app.services.ingestion.types import NormalizedDocument


def main():

    document = NormalizedDocument(
        name="test.md",
        source_path="resources/data/finance/test.md",
        content=(
            "# Financial Report\n\n"
            "Revenue increased significantly during the quarter.\n\n"
            "Operating expenses were reduced through better "
            "resource allocation.\n\n"
            "The company expects continued growth next quarter."
        ),
        file_type="md",
        department="finance",
        required_permission="read_finance",
    )

    chunker = get_chunker(document.file_type)

    chunks = chunker.chunk(
        document,
        document_id=1,
    )

    print(f"Generated {len(chunks)} chunks")

    for chunk in chunks:
        print("\n--- CHUNK ---")
        print(f"Index: {chunk.chunk_index}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Department: {chunk.department}")
        print(f"Permission: {chunk.required_permission}")
        print(f"Length: {len(chunk.content)}")
        print(chunk.content)


if __name__ == "__main__":
    main()

# uv run python -m app.scripts.test_chunking