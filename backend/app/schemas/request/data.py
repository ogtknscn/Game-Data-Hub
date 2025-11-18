"""
Data request schemas
"""
from pydantic import BaseModel
from typing import Any, Dict, Optional


class UpdateCellRequest(BaseModel):
    """Update cell request"""
    cell_id: int
    value: Any


class CreateRowRequest(BaseModel):
    """Create row request"""
    table_id: int
    cells: Dict[str, Any]  # column_name -> value


class UpdateRowRequest(BaseModel):
    """Update row request"""
    row_id: int
    cells: Dict[str, Any]  # column_name -> value

