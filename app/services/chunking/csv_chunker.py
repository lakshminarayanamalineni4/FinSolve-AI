from app.services.chunking.models import DocumentChunk
from app.services.ingestion.types import NormalizedDocument


class CSVChunker:
    def __init__(
        self,
        chunk_size: int = 800,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        self.chunk_size = chunk_size

    def chunk(
        self,
        document: NormalizedDocument,
        document_id: int,
    ) -> list[DocumentChunk]:

        rows = [
            row.strip()
            for row in document.content.splitlines()
            if row.strip()
        ]

        chunks: list[DocumentChunk] = []
        current_rows: list[str] = []
        current_size = 0

        for row in rows:

            row_size = len(row)

            if (
                current_rows
                and current_size + row_size + 1 > self.chunk_size
            ):
                chunks.append(
                    self._create_chunk(
                        current_rows,
                        document,
                        document_id,
                        len(chunks),
                    )
                )

                current_rows = []
                current_size = 0

            current_rows.append(row)
            current_size += row_size + 1

        if current_rows:
            chunks.append(
                self._create_chunk(
                    current_rows,
                    document,
                    document_id,
                    len(chunks),
                )
            )

        return chunks

    @staticmethod
    def _create_chunk(
        rows: list[str],
        document: NormalizedDocument,
        document_id: int,
        chunk_index: int,
    ) -> DocumentChunk:

        return DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            content="\n".join(rows),
            department=document.department,
            required_permission=document.required_permission,
        )