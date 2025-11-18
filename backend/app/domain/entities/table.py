"""
Table domain entity
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Table:
    """Table domain entity"""
    id: Optional[int] = None
    project_id: int = 0
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    columns: List['Column'] = None
    
    def __post_init__(self):
        """Initialize columns list if None"""
        if self.columns is None:
            self.columns = []
        if not self.name:
            raise ValueError("Table name cannot be empty")
        if self.project_id <= 0:
            raise ValueError("Table must belong to a project")


@dataclass
class Column:
    """Column domain entity"""
    id: Optional[int] = None
    table_id: int = 0
    name: str = ""
    data_type: str = "string"  # string, integer, float, boolean, enum, reference
    is_required: bool = False
    default_value: Optional[str] = None
    enum_values: Optional[List[str]] = None
    reference_table_id: Optional[int] = None
    order: int = 0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate column"""
        if not self.name:
            raise ValueError("Column name cannot be empty")
        valid_types = ["string", "integer", "float", "boolean", "enum", "reference"]
        if self.data_type not in valid_types:
            raise ValueError(f"Invalid data type: {self.data_type}")
        if self.data_type == "enum" and not self.enum_values:
            raise ValueError("Enum type requires enum_values")
        if self.data_type == "reference" and not self.reference_table_id:
            raise ValueError("Reference type requires reference_table_id")

