from app.services.retrieval.models import RetrievalResult


class SourceAttributor:
    """Builds application-controlled source references."""

    def build(self, sources: list[RetrievalResult]) -> list[str]:
        """Return human-readable references for retrieved sources."""

        return [
            f"Document {source.document_id}, Chunk {source.chunk_index}"
            for source in sources
        ]