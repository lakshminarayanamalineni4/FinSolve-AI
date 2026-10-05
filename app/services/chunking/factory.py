from app.services.chunking.base import DocumentChunker
from app.services.chunking.csv_chunker import CSVChunker
from app.services.chunking.markdown_chunker import MarkdownChunker


def get_chunker(file_type: str):

    normalized_type = file_type.lower().strip()

    if normalized_type in {"md", "markdown"}:
        return MarkdownChunker()

    if normalized_type == "csv":
        return CSVChunker()

    raise ValueError(
        f"Unsupported file type for chunking: {file_type}"
    )