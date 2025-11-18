"""
Version response schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class VersionResponse(BaseModel):
    """Version response"""
    id: int
    project_id: int
    table_id: Optional[int]
    message: str
    author_id: int
    changes: Dict[str, Any]
    created_at: datetime


class DiffResponse(BaseModel):
    """Diff response"""
    version_id: int
    message: str
    changes: Dict[str, Any]
    created_at: Optional[str]

