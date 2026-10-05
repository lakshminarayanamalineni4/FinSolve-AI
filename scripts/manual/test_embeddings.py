from sentence_transformers import util

from app.services.chunking.factory import get_chunker
from app.services.chunking.validator import (
    validate_chunk_sizes,
    validate_chunks,
)
from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.ingestion.loaders.csv_loader import CSVLoader
from app.services.ingestion.loaders.markdown_loader import MarkdownLoader
from app.services.ingestion.normalizer import DocumentNormalizer


def get_validated_chunks():
    markdown_loader = MarkdownLoader("resources/data")
    csv_loader = CSVLoader("resources/data")

    loaded_documents = markdown_loader.load() + csv_loader.load()
    normalizer = DocumentNormalizer()

    all_chunks = []

    for document_id, document in enumerate(
        [normalizer.normalize(doc) for doc in loaded_documents],
        start=1,
    ):
        chunker = get_chunker(document.file_type)
        chunks = chunker.chunk(document, document_id=document_id)

        validate_chunks(
            chunks,
            expected_document_id=document_id,
            expected_department=document.department,
            expected_permission=document.required_permission,
        )
        validate_chunk_sizes(chunks)
        all_chunks.extend(chunks)

    return all_chunks


def main():
    chunks = get_validated_chunks()
    test_chunks = chunks[:10]
    service = QwenEmbeddingService()

    embedded_chunks = service.embed_chunks(test_chunks)

    print(f"Chunks: {len(chunks)}")
    print(f"Embedded chunks: {len(embedded_chunks)}")

    for item in embedded_chunks[:5]:
        print(
            f"document_id={item.chunk.document_id}, "
            f"chunk_index={item.chunk.chunk_index}, "
            f"department={item.chunk.department}, "
            f"permission={item.chunk.required_permission}, "
            f"dimensions={len(item.embedding)}"
        )

    query = "How much did the company spend on marketing?"
    query_embedding = service.embed_query(query)

    similarities = util.cos_sim(
        query_embedding,
        [chunk.embedding for chunk in embedded_chunks],
    )

    for index, score in enumerate(similarities[0]):
        print(f"Text {index}: {score.item():.4f}")

    assert len(embedded_chunks) == len(test_chunks)

    for original, embedded in zip(test_chunks, embedded_chunks):

        assert embedded.chunk is original

        assert embedded.chunk.content == original.content

        assert len(embedded.embedding) == 1024

        assert embedded.chunk.department == original.department

        assert (
            embedded.chunk.required_permission
            == original.required_permission
        )

if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.test_embeddings
