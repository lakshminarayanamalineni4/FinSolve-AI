from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_permission import DocumentPermission
from app.models.permission import Permission
from app.services.ingestion.types import NormalizedDocument


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        document: NormalizedDocument,
    ) -> Document:

        existing_document = self.db.scalar(
            select(Document).where(
                Document.source_path == document.source_path
            )
        )

        if existing_document:
            return existing_document

        permission = self.db.scalar(
            select(Permission).where(
                Permission.name == document.required_permission
            )
        )

        if permission is None:
            raise ValueError(
                f"Permission not found: "
                f"{document.required_permission}"
            )

        db_document = Document(
            name=document.name,
            source_path=document.source_path,
            file_type=document.file_type,
            department=document.department,
            is_active=True,
        )

        self.db.add(db_document)
        self.db.flush()

        document_permission = DocumentPermission(
            document_id=db_document.id,
            permission_id=permission.id,
        )

        self.db.add(document_permission)

        return db_document