from dataclasses import dataclass

from app.services.retrieval.models import RetrievalResult


@dataclass(frozen=True)
class Context:
    text: str
    sources: list[RetrievalResult]