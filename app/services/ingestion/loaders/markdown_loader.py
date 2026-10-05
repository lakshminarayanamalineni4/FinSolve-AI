from pathlib import Path

from app.services.ingestion.types import LoadedDocument


class MarkdownLoader:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory does not exist: {self.data_dir}"
            )

        if not self.data_dir.is_dir():
            raise NotADirectoryError(
                f"Expected a directory: {self.data_dir}"
            )

    def load(self) -> list[LoadedDocument]:
        documents: list[LoadedDocument] = []

        for file_path in self.data_dir.rglob("*.md"): # find all Markdown documents regardless of department folder
            content = file_path.read_text(encoding="utf-8")

            documents.append(
                LoadedDocument(
                    name=file_path.name,
                    source_path=str(file_path),
                    content=content,
                )
            )

        return documents