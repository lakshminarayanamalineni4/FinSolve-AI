from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
    )

    documents = relationship(
        "Document",
        secondary="document_permissions",
        back_populates="permissions",
    )