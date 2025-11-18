"""
Project domain entity
Pure business object without infrastructure concerns
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """Project domain entity"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate entity after initialization"""
        if not self.name:
            raise ValueError("Project name cannot be empty")
    
    def update_name(self, new_name: str):
        """Update project name with validation"""
        if not new_name:
            raise ValueError("Project name cannot be empty")
        self.name = new_name
        self.updated_at = datetime.utcnow()

