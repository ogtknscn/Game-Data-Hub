"""
Project request schemas
"""
from pydantic import BaseModel
from typing import Optional


class CreateProjectRequest(BaseModel):
    """Create project request"""
    name: str
    description: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    """Update project request"""
    name: Optional[str] = None
    description: Optional[str] = None

