"""
Authentication response schemas
"""
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response"""
    id: int
    username: str
    email: str

