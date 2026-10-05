from app.services.context.models import Context
from app.services.retrieval.models import RetrievalResult


class ContextBuilder:
    def build(
        self,
        results: list[RetrievalResult],
    ) -> Context:
        context_sections = []

        for result in results:
            context_sections.append(
                (
                    f"[Document {result.document_id}, "
                    f"Chunk {result.chunk_index}]\n"
                    f"{result.content}"
                )
            )

        context_text = "\n\n".join(context_sections)

        return Context(
            text=context_text,
            sources=list(results),
        )