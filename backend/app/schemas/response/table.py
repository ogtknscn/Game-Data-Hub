"""
Table response schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ColumnResponse(BaseModel):
    """Column response"""
    id: int
    table_id: int
    name: str
    data_type: str
    is_required: bool
    default_value: Optional[str]
    enum_values: Optional[List[str]]
    reference_table_id: Optional[int]
    order: int


class TableResponse(BaseModel):
    """Table response"""
    id: int
    project_id: int
    name: str
    description: Optional[str]
    columns: List[ColumnResponse]
    created_at: datetime
    updated_at: datetime


class TableDataResponse(BaseModel):
    """Table data response"""
    table_id: int
    rows: List[Dict[str, Any]]  # List of row data

