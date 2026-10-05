from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    original: str
    processed: str