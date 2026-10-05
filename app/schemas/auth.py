from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    user_id: int
    username: str
    role_id: int
    role: str