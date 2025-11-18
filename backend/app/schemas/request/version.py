"""
Version request schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class CreateCommitRequest(BaseModel):
    """Create commit request"""
    project_id: int
    table_id: Optional[int] = None
    message: str
    changes: Dict[str, Any]  # cell_id -> {old_value, new_value}

