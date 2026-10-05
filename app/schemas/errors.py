from pydantic import BaseModel


class AccessDeniedResponse(BaseModel):
    error: str
    message: str
    required_permission: str