"""
Project response schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectResponse(BaseModel):
    """Project response"""
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

