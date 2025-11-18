"""
Data service
"""
from typing import List, Any, Dict
from app.domain.entities.cell import Row, Cell
from app.domain.interfaces.services import IDataService
from app.domain.interfaces.repositories import IDataRepository, ITableRepository
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.value_objects.data_types import DataType, DataTypeDefinition


class DataService(IDataService):
    """Data service implementation"""
    
    def __init__(self, data_repository: IDataRepository, table_repository: ITableRepository):
        self.data_repository = data_repository
        self.table_repository = table_repository
    
    async def update_cell_value(self, cell_id: int, new_value: Any, user_id: int) -> Cell:
        """Update cell value with validation"""
        # Get cell
        cell = await self.data_repository.get_cell_by_id(cell_id)
        if not cell:
            raise NotFoundError("Cell", str(cell_id))
        
        # Get column for validation (simplified - would need column repository)
        # For now, basic validation
        if new_value is not None and not isinstance(new_value, (str, int, float, bool)):
            raise ValidationError("Invalid cell value type")
        
        # Update cell
        cell.update_value(new_value)
        return await self.data_repository.update_cell(cell)
    
    async def get_table_data(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Row]:
        """Get table data (rows)"""
        # Verify table exists
        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise NotFoundError("Table", str(table_id))
        
        return await self.data_repository.get_rows_by_table_id(table_id, skip, limit)
    
    async def create_row(self, table_id: int, cells: Dict[str, Any]) -> Row:
        """Create a new row with cells"""
        # Verify table exists
        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise NotFoundError("Table", str(table_id))
        
        # Create row
        row = Row(table_id=table_id)
        
        # Create cells for each column
        for column in table.columns:
            value = cells.get(column.name)
            
            # Use default value if not provided
            if value is None and column.default_value is not None:
                value = column.default_value
            
            # Validate required columns
            if column.is_required and value is None:
                raise ValidationError(f"Column '{column.name}' is required")
            
            # Create cell (row_id will be set after row is created)
            # Temporarily set row_id to 0 to pass validation
            cell = Cell(
                row_id=0,  # Will be set after row is created
                column_id=column.id,
                value=value
            )
            row.cells[column.id] = cell
        
        return await self.data_repository.create_row(row)
    
    async def update_row(self, row_id: int, cells: Dict[str, Any]) -> Row:
        """Update row cells"""
        # Get row
        row = await self.data_repository.get_row_by_id(row_id)
        if not row:
            raise NotFoundError("Row", str(row_id))
        
        # Get table for column info
        table = await self.table_repository.get_by_id(row.table_id)
        if not table:
            raise NotFoundError("Table", str(row.table_id))
        
        # Update cells
        for column in table.columns:
            if column.name in cells:
                value = cells[column.name]
                
                # Validate required columns
                if column.is_required and value is None:
                    raise ValidationError(f"Column '{column.name}' is required")
                
                # Get or create cell
                if column.id in row.cells:
                    cell = row.cells[column.id]
                    cell.update_value(value)
                else:
                    cell = Cell(
                        row_id=row_id,
                        column_id=column.id,
                        value=value
                    )
                    row.cells[column.id] = cell
        
        return await self.data_repository.update_row(row)

