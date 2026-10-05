from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.chunking.models import DocumentChunk
from app.services.embeddings.models import EmbeddedChunk


class QwenEmbeddingService:

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.embedding_model
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:

        texts = [chunk.content for chunk in chunks]

        embeddings = self.embed_documents(texts)

        return [
            EmbeddedChunk(
                chunk=chunk,
                embedding=embedding,
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]