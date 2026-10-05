import csv
from pathlib import Path

from app.services.ingestion.types import LoadedDocument


class CSVLoader:
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

        for file_path in self.data_dir.rglob("*.csv"):
            content = self._read_csv(file_path)

            documents.append(
                LoadedDocument(
                    name=file_path.name,
                    source_path=str(file_path),
                    content=content,
                )
            )

        return documents

    @staticmethod
    def _read_csv(file_path: Path) -> str:
        rows: list[str] = []
        # CSV looks roughly like:
        # employee_id,name,department,attendance
        # 101,John,Engineering,95%
        # 102,Sarah,HR,98%
        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:
            reader = csv.DictReader(file)
            # csv.DictReader gives us each row as:
            # {
            #     "employee_id": "101",
            #     "name": "John",
            #     "department": "Engineering",
            #     "attendance": "95%"
            # }

            for row in reader:
                row_text = " | ".join(
                    f"{key}: {value}"
                    for key, value in row.items()
                )

                rows.append(row_text)

            # employee_id: 101 | name: John | department: Engineering | attendance: 95%

        return "\n".join(rows)