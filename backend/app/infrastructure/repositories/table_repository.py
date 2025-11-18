"""
Table repository implementation
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.domain.entities.table import Table, Column
from app.domain.interfaces.repositories import ITableRepository
from app.infrastructure.models.table import TableModel, ColumnModel
from app.infrastructure.repositories.base_repository import BaseRepository


class TableRepository(BaseRepository[TableModel, Table], ITableRepository):
    """Table repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableModel, Table)
    
    async def get_by_id(self, id: int) -> Optional[Table]:
        """Get table by ID with columns loaded - O(1) with index"""
        stmt = select(TableModel).where(TableModel.id == id).options(
            selectinload(TableModel.columns)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return self._to_domain(model)
        return None
    
    async def get_by_project_id(self, project_id: int) -> List[Table]:
        """Get tables by project ID - O(n) where n is number of tables"""
        stmt = select(TableModel).where(TableModel.project_id == project_id).options(
            selectinload(TableModel.columns)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    async def get_columns_by_table_id(self, table_id: int) -> List[Column]:
        """Get columns by table ID - O(n) where n is number of columns"""
        stmt = select(ColumnModel).where(ColumnModel.table_id == table_id).order_by(ColumnModel.order)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._column_to_domain(model) for model in models]
    
    async def _to_domain_async(self, model: TableModel) -> Table:
        """Convert model to domain entity (async version)"""
        # For newly created tables, columns will be empty
        # We avoid accessing lazy-loaded relationships in async context
        columns = []
        
        # Try to access columns if they're already loaded (e.g., from selectinload)
        try:
            # Check if columns attribute exists and is accessible
            if hasattr(model, 'columns'):
                # Use getattr to safely access
                cols = getattr(model, 'columns', None)
                if cols is not None:
                    # If it's a list/collection, convert it
                    columns = [self._column_to_domain(col) for col in cols] if cols else []
        except Exception:
            # If any error occurs, just use empty list
            columns = []
        
        return Table(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            columns=columns
        )
    
    def _to_domain(self, model: TableModel) -> Table:
        """Convert model to domain entity (sync version for queries)"""
        # For queries, columns should be preloaded with selectinload
        columns = [self._column_to_domain(col) for col in model.columns] if model.columns else []
        return Table(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            columns=columns
        )
    
    def _to_model(self, domain: Table) -> TableModel:
        """Convert domain entity to model"""
        model = TableModel(
            id=domain.id,
            project_id=domain.project_id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
        return model
    
    def _update_model_from_domain(self, model: TableModel, domain: Table):
        """Update model from domain entity"""
        model.name = domain.name
        model.description = domain.description
        model.updated_at = domain.updated_at
    
    def _column_to_domain(self, model: ColumnModel) -> Column:
        """Convert column model to domain entity"""
        return Column(
            id=model.id,
            table_id=model.table_id,
            name=model.name,
            data_type=model.data_type,
            is_required=model.is_required,
            default_value=model.default_value,
            enum_values=model.enum_values,
            reference_table_id=model.reference_table_id,
            order=model.order,
            created_at=model.created_at
        )

