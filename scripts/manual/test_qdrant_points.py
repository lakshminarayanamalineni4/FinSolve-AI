import time

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.services.chunking.factory import get_chunker
from app.services.chunking.models import DocumentChunk
from app.services.embeddings.qwen import QwenEmbeddingService
from app.services.ingestion.loaders.csv_loader import CSVLoader
from app.services.ingestion.loaders.markdown_loader import MarkdownLoader
from app.services.ingestion.normalizer import DocumentNormalizer
from app.services.vector.qdrant_client import generate_point_id


COLLECTION_NAME = "finsolve_chunks"
BATCH_SIZE = 25


def load_chunks() -> list[DocumentChunk]:
    """Load and chunk all source documents using the Phase 3 pipeline."""

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

    all_chunks: list[DocumentChunk] = []

    for document_id, document in enumerate(
        normalized_documents,
        start=1,
    ):
        chunker = get_chunker(document.file_type)

        chunks = chunker.chunk(
            document,
            document_id=document_id,
        )

        all_chunks.extend(chunks)

    return all_chunks


def create_points(
    embedded_chunks,
) -> list[PointStruct]:
    """Convert embedded chunks into Qdrant points."""

    points: list[PointStruct] = []

    for embedded_chunk in embedded_chunks:
        chunk = embedded_chunk.chunk

        point_id = generate_point_id(
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
        )

        points.append(
            PointStruct(
                id=point_id,
                vector=embedded_chunk.embedding,
                payload={
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "department": chunk.department,
                    "required_permission": chunk.required_permission,
                    "content": chunk.content,
                },
            )
        )

    return points


def main() -> None:
    # --------------------------------------------------
    # 1. Load all chunks
    # --------------------------------------------------

    chunks = load_chunks()

    total_chunks = len(chunks)
    total_batches = (
        total_chunks + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print(f"Total chunks available: {total_chunks}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {total_batches}")
    print()

    # --------------------------------------------------
    # 2. Initialize services
    # --------------------------------------------------

    embedding_service = QwenEmbeddingService()

    client = QdrantClient(
        path="./qdrant_data"
    )

    # --------------------------------------------------
    # 3. Process batches
    # --------------------------------------------------

    total_start_time = time.perf_counter()

    processed_chunks = 0

    for batch_number, start_index in enumerate(
        range(0, total_chunks, BATCH_SIZE),
        start=1,
    ):
        batch = chunks[
            start_index:start_index + BATCH_SIZE
        ]

        print(
            f"Batch {batch_number}/{total_batches} "
            f"({len(batch)} chunks)"
        )

        batch_start_time = time.perf_counter()

        # Generate embeddings for this batch
        embedded_chunks = (
            embedding_service.embed_chunks(batch)
        )

        embedding_time = (
            time.perf_counter()
            - batch_start_time
        )

        # Convert embeddings into Qdrant points
        points = create_points(
            embedded_chunks
        )

        # Store this batch in Qdrant
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        batch_time = (
            time.perf_counter()
            - batch_start_time
        )

        processed_chunks += len(batch)

        progress = (
            processed_chunks / total_chunks
        ) * 100

        total_elapsed = (
            time.perf_counter()
            - total_start_time
        )

        average_per_chunk = (
            total_elapsed / processed_chunks
        )

        remaining_chunks = (
            total_chunks - processed_chunks
        )

        estimated_remaining = (
            remaining_chunks
            * average_per_chunk
        )

        print(
            f"  Embedded: {processed_chunks}/{total_chunks}"
        )

        print(
            f"  Progress: {progress:.1f}%"
        )

        print(
            f"  Embedding time: "
            f"{embedding_time:.2f}s"
        )

        print(
            f"  Batch time: "
            f"{batch_time:.2f}s"
        )

        print(
            f"  Total elapsed: "
            f"{total_elapsed:.2f}s"
        )

        print(
            f"  Estimated remaining: "
            f"{estimated_remaining:.1f}s"
        )

        print("-" * 60)

    # --------------------------------------------------
    # 4. Final verification
    # --------------------------------------------------

    collection_info = client.get_collection(
        COLLECTION_NAME
    )

    total_time = (
        time.perf_counter()
        - total_start_time
    )

    print()
    print("=" * 60)
    print("Qdrant ingestion completed successfully.")
    print("=" * 60)
    print(f"Chunks processed: {processed_chunks}")
    print(
        f"Qdrant points stored: "
        f"{collection_info.points_count}"
    )
    print(
        f"Total time: "
        f"{total_time:.2f}s"
    )
    print(
        f"Average time per chunk: "
        f"{total_time / processed_chunks:.2f}s"
    )


if __name__ == "__main__":
    main()
