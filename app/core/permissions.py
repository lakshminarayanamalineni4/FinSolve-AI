from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import authenticate
from app.core.database import get_db
from app.models.role_permission import RolePermission
from app.models.permission import Permission
from app.models.user import User

def require_permission(permission_name: str):
    def permission_checker(
        user: dict = Depends(authenticate),
        db: Session = Depends(get_db),
    ):
        permissions = get_user_permissions(
            user.user_id,
            db,
        )

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "access_denied",
                    "message": (
                        "You do not have permission "
                        "to access this resource."
                    ),
                    "required_permission": permission_name,
                },
            )

        return user

    return permission_checker

def get_user_permissions(
    user_id: int,
    db: Session,
) -> set[str]:
    permissions = db.scalars(
        select(Permission.name)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id,
        )
        .join(
            User,
            User.role_id == RolePermission.role_id,
        )
        .where(User.id == user_id)
    ).all()

    return set(permissions)