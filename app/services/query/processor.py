import re

from app.services.query.models import Query


class QueryValidationError(ValueError):
    """Raised when a user query is invalid."""


class QueryProcessor:
    def process(self, query: str) -> Query:
        if not isinstance(query, str):
            raise QueryValidationError(
                "Query must be a string."
            )

        if not query.strip():
            raise QueryValidationError(
                "Query cannot be empty."
            )

        processed_query = re.sub(
            r"\s+",
            " ",
            query.strip(),
        )

        return Query(
            original=query,
            processed=processed_query,
        )