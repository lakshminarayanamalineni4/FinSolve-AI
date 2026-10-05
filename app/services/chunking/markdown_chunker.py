import re

from app.services.chunking.base import DocumentChunker
from app.services.chunking.models import DocumentChunk
from app.services.ingestion.types import NormalizedDocument


class MarkdownChunker(DocumentChunker):

    def chunk(
        self,
        document: NormalizedDocument,
        document_id: int,
    ) -> list[DocumentChunk]:

        sections = re.split(
            r"(?=^#{1,6}\s+)",
            document.content,
            flags=re.MULTILINE,
        )

        chunks: list[DocumentChunk] = []

        for section in sections:
            section = section.strip()

            if not section:
                continue

            section_document = NormalizedDocument(
                name=document.name,
                source_path=document.source_path,
                content=section,
                file_type=document.file_type,
                department=document.department,
                required_permission=document.required_permission,
            )

            chunks.extend(
                super().chunk(
                    section_document,
                    document_id,
                )
            )

        for index, chunk in enumerate(chunks):
            chunk.chunk_index = index

        return chunks