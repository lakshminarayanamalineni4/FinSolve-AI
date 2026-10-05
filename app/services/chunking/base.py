from app.services.chunking.models import DocumentChunk
from app.services.ingestion.types import NormalizedDocument


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        document: NormalizedDocument,
        document_id: int,
    ) -> list[DocumentChunk]:

        content = document.content.strip()

        if not content:
            return []

        chunks: list[DocumentChunk] = []

        start = 0
        chunk_index = 0

        while start < len(content):
            end = min(
                start + self.chunk_size,
                len(content),
            )

            chunk_content = content[start:end].strip()

            if chunk_content:
                chunks.append(
                    DocumentChunk(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        content=chunk_content,
                        department=document.department,
                        required_permission=document.required_permission,
                    )
                )

                chunk_index += 1

            if end >= len(content):
                break

            start = end - self.chunk_overlap

        return chunks