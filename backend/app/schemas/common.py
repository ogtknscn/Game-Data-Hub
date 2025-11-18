"""
Common schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str


class SuccessResponse(BaseModel):
    """Success response schema"""
    message: str


class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = 0
    limit: int = 100

