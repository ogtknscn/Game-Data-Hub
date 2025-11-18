"""
Cell domain entity
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class Cell:
    """Cell domain entity - represents a single data point"""
    id: Optional[int] = None
    row_id: int = 0
    column_id: int = 0
    value: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate cell"""
        # Allow row_id=0 for cells that will be assigned to a row later
        if self.row_id < 0:
            raise ValueError("Cell row_id cannot be negative")
        if self.column_id <= 0:
            raise ValueError("Cell must belong to a column")
    
    def update_value(self, new_value: Any):
        """Update cell value"""
        self.value = new_value
        self.updated_at = datetime.utcnow()


@dataclass
class Row:
    """Row domain entity - represents a data row"""
    id: Optional[int] = None
    table_id: int = 0
    cells: dict = None  # column_id -> Cell mapping
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize cells dict if None"""
        if self.cells is None:
            self.cells = {}
        # Allow table_id=0 for rows that will be assigned to a table later
        if self.table_id < 0:
            raise ValueError("Row table_id cannot be negative")
    
    def get_cell_value(self, column_id: int) -> Optional[Any]:
        """Get cell value by column ID"""
        cell = self.cells.get(column_id)
        return cell.value if cell else None
    
    def set_cell_value(self, column_id: int, value: Any):
        """Set cell value by column ID"""
        if column_id in self.cells:
            self.cells[column_id].update_value(value)
        else:
            self.cells[column_id] = Cell(
                row_id=self.id or 0,
                column_id=column_id,
                value=value
            )

