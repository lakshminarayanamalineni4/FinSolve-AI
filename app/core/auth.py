from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password
from app.models.user import User

from app.schemas.auth import AuthenticatedUser

security = HTTPBasic()


def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
    db=Depends(get_db),
):
    username = credentials.username
    password = credentials.password

    user = db.scalar(
        select(User)
        .where(User.username == username)
    )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return AuthenticatedUser(
        user_id=user.id,
        username=user.username,
        role_id=user.role_id,
        role=user.role.name,
    )