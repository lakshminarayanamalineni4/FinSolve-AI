from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalResult:
    point_id: str
    score: float
    document_id: int
    chunk_index: int
    department: str
    required_permission: str
    content: str