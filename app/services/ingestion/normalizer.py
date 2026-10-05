from pathlib import Path

from app.services.ingestion.constants import (
    ALLOWED_DEPARTMENTS,
    DEPARTMENT_PERMISSION_MAP,
)
from app.services.ingestion.types import LoadedDocument, NormalizedDocument


class DocumentNormalizer:

    def normalize(
        self,
        document: LoadedDocument,
    ) -> NormalizedDocument:

        path = Path(document.source_path) # get the path of the document to extract file type and department

        file_type = path.suffix.lower().lstrip(".") # get the file type from the file extension (e.g., "md" or "csv")
        department = path.parent.name.lower() # get the department from the parent folder name (e.g., "finance" or "hr")

        if department not in ALLOWED_DEPARTMENTS:
            raise ValueError(
                f"Unsupported department '{department}' "
                f"for document: {document.source_path}"
            )

        required_permission = DEPARTMENT_PERMISSION_MAP.get(department)

        return NormalizedDocument(
            name=document.name,
            source_path=document.source_path,
            content=document.content,
            file_type=file_type,
            department=department,
            required_permission=required_permission,
        )