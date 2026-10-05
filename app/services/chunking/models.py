from dataclasses import dataclass

@dataclass
class DocumentChunk:
    document_id: int
    chunk_index: int
    content: str
    department: str
    required_permission: str