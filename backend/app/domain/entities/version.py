"""
Version domain entity
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Version:
    """Version/Commit domain entity"""
    id: Optional[int] = None
    project_id: int = 0
    table_id: Optional[int] = None
    message: str = ""
    author_id: int = 0
    changes: Dict[str, Any] = None  # Cell changes: {cell_id: {old_value, new_value}}
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate version"""
        if not self.message:
            raise ValueError("Version message cannot be empty")
        if self.project_id <= 0:
            raise ValueError("Version must belong to a project")
        if self.author_id <= 0:
            raise ValueError("Version must have an author")
        if self.changes is None:
            self.changes = {}
    
    def add_change(self, cell_id: int, old_value: Any, new_value: Any):
        """Add a cell change to this version"""
        self.changes[str(cell_id)] = {
            "old_value": old_value,
            "new_value": new_value
        }

