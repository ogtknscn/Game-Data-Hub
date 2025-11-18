"""
Authentication request schemas
"""
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Register request"""
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Login request"""
    username: str
    password: str

