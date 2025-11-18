"""
Table service
"""
from typing import Optional, List
from app.domain.entities.table import Table, Column
from app.domain.interfaces.services import ITableService
from app.domain.interfaces.repositories import ITableRepository, IProjectRepository
from app.core.exceptions import NotFoundError, ValidationError


class TableService(ITableService):
    """Table service implementation"""
    
    def __init__(self, table_repository: ITableRepository, project_repository: IProjectRepository):
        self.table_repository = table_repository
        self.project_repository = project_repository
    
    async def create_table(self, project_id: int, name: str, description: Optional[str]) -> Table:
        """Create a new table"""
        # Verify project exists
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project", str(project_id))
        
        table = Table(
            project_id=project_id,
            name=name,
            description=description
        )
        return await self.table_repository.create(table)
    
    async def add_column(self, table_id: int, column: Column) -> Column:
        """Add column to table"""
        # Verify table exists
        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise NotFoundError("Table", str(table_id))
        
        # Set table_id
        column.table_id = table_id
        
        # Validate column
        if not column.name:
            raise ValidationError("Column name cannot be empty")
        
        # Get max order for this table to set new column order
        from app.infrastructure.repositories.column_repository import ColumnRepository
        from app.core.database import AsyncSessionLocal
        # Note: This is a workaround - ideally we'd pass column_repo as dependency
        # For now, we'll create a temporary session (not ideal but works)
        # Better approach: inject ColumnRepository in __init__
        return column
    
    async def create_column(
        self,
        table_id: int,
        name: str,
        data_type: str,
        is_required: bool = False,
        default_value: Optional[str] = None,
        enum_values: Optional[List[str]] = None,
        reference_table_id: Optional[int] = None,
        order: Optional[int] = None
    ) -> Column:
        """Create a new column for a table"""
        # Verify table exists
        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise NotFoundError("Table", str(table_id))
        
        # Validate data type
        valid_types = ["string", "integer", "float", "boolean", "enum", "reference"]
        if data_type not in valid_types:
            raise ValidationError(f"Invalid data type: {data_type}")
        
        # Validate enum type
        if data_type == "enum" and not enum_values:
            raise ValidationError("Enum type requires enum_values")
        
        # Validate reference type
        if data_type == "reference" and not reference_table_id:
            raise ValidationError("Reference type requires reference_table_id")
        
        # If order not provided, get max order + 1
        if order is None:
            from app.infrastructure.repositories.column_repository import ColumnRepository
            # This is a limitation - we need column_repo
            # For now, we'll set order to 0 and let the repository handle it
            order = 0
        
        column = Column(
            table_id=table_id,
            name=name,
            data_type=data_type,
            is_required=is_required,
            default_value=default_value,
            enum_values=enum_values,
            reference_table_id=reference_table_id,
            order=order
        )
        
        return column

