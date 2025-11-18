"""
Table request schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class CreateTableRequest(BaseModel):
    """Create table request"""
    name: str
    description: Optional[str] = None
    project_id: int


class CreateColumnRequest(BaseModel):
    """Create column request"""
    name: str
    data_type: str  # string, integer, float, boolean, enum, reference
    is_required: bool = False
    default_value: Optional[str] = None
    enum_values: Optional[List[str]] = None
    reference_table_id: Optional[int] = None
    order: int = 0


class UpdateTableSchemaRequest(BaseModel):
    """Update table schema request"""
    columns: List[Dict[str, Any]]

