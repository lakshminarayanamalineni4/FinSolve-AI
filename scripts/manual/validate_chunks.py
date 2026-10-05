from app.services.chunking.factory import get_chunker
from app.services.chunking.validator import (
    validate_chunk_sizes,
    validate_chunks,
)
from app.services.ingestion.loaders.csv_loader import CSVLoader
from app.services.ingestion.loaders.markdown_loader import MarkdownLoader
from app.services.ingestion.normalizer import DocumentNormalizer


def main():

    markdown_loader = MarkdownLoader("resources/data")
    csv_loader = CSVLoader("resources/data")

    loaded_documents = (
        markdown_loader.load()
        + csv_loader.load()
    )

    normalizer = DocumentNormalizer()

    normalized_documents = [
        normalizer.normalize(document)
        for document in loaded_documents
    ]

    total_chunks = 0

    for document_id, document in enumerate(
        normalized_documents,
        start=1,
    ):

        chunker = get_chunker(document.file_type)

        chunks = chunker.chunk(
            document,
            document_id=document_id,
        )

        validate_chunks(
            chunks,
            expected_document_id=document_id,
            expected_department=document.department,
            expected_permission=document.required_permission,
        )

        validate_chunk_sizes(chunks)

        total_chunks += len(chunks)

        print(
            f"✓ {document.name}: "
            f"{len(chunks)} chunks"
        )

    print()
    print(
        f"Chunk validation successful. "
        f"Total chunks: {total_chunks}"
    )


if __name__ == "__main__":
    main()

# uv run python -m app.scripts.validate_chunks