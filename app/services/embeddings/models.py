from dataclasses import dataclass

from app.services.chunking.models import DocumentChunk


@dataclass
class EmbeddedChunk:
    chunk: DocumentChunk
    embedding: list[float]
