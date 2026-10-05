from collections import Counter

from app.services.chunking.models import DocumentChunk


class ChunkValidationError(ValueError):
    """Raised when generated chunks fail validation."""


def validate_chunks(
    chunks: list[DocumentChunk],
    expected_document_id: int,
    expected_department: str,
    expected_permission: str,
) -> None:

    if not chunks:
        raise ChunkValidationError(
            "No chunks were generated."
        )

    for chunk in chunks:

        # 1. Content validation
        if not chunk.content.strip():
            raise ChunkValidationError(
                f"Chunk {chunk.chunk_index} has empty content."
            )

        # 2. Document validation
        if chunk.document_id != expected_document_id:
            raise ChunkValidationError(
                f"Chunk {chunk.chunk_index} belongs to "
                f"document {chunk.document_id}, expected "
                f"{expected_document_id}."
            )

        # 3. Department validation
        if chunk.department != expected_department:
            raise ChunkValidationError(
                f"Chunk {chunk.chunk_index} has incorrect "
                f"department: {chunk.department}."
            )

        # 4. Permission validation
        if chunk.required_permission != expected_permission:
            raise ChunkValidationError(
                f"Chunk {chunk.chunk_index} has incorrect "
                f"permission: {chunk.required_permission}."
            )

    # 5. Chunk indexes must be sequential
    indexes = [chunk.chunk_index for chunk in chunks]

    expected_indexes = list(range(len(chunks)))

    if indexes != expected_indexes:
        raise ChunkValidationError(
            f"Chunk indexes are invalid: {indexes}"
        )

    # 6. Detect exact duplicate content
    content_counts = Counter(
        chunk.content for chunk in chunks
    )

    duplicates = [
        content
        for content, count in content_counts.items()
        if count > 1
    ]

    if duplicates:
        raise ChunkValidationError(
            "Duplicate chunk content detected."
        )

def validate_chunk_sizes(
    chunks: list[DocumentChunk],
    max_size: int = 800,
) -> None:

    oversized_chunks = [
        chunk
        for chunk in chunks
        if len(chunk.content) > max_size
    ]

    if oversized_chunks:
        print(
            f"Warning: {len(oversized_chunks)} "
            f"chunks exceed the target size of {max_size}."
        )