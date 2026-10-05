from uuid import NAMESPACE_URL, UUID, uuid5


def generate_point_id(
    document_id: int,
    chunk_index: int,
) -> UUID:
    """
    Generate a deterministic Qdrant point ID
    for a document chunk.
    """

    return uuid5(
        NAMESPACE_URL,
        f"{document_id}:{chunk_index}",
    )
