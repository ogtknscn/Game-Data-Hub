"""
Column repository implementation
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.entities.table import Column
from app.infrastructure.models.table import ColumnModel
from app.infrastructure.repositories.base_repository import BaseRepository


class ColumnRepository(BaseRepository[ColumnModel, Column]):
    """Column repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ColumnModel, Column)
    
    async def get_by_table_id(self, table_id: int) -> List[Column]:
        """Get columns by table ID - O(n) where n is number of columns"""
        stmt = select(ColumnModel).where(ColumnModel.table_id == table_id).order_by(ColumnModel.order)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    async def delete_by_table_id(self, table_id: int) -> int:
        """Delete all columns for a table - O(n)"""
        stmt = delete(ColumnModel).where(ColumnModel.table_id == table_id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
    
    async def _to_domain_async(self, model: ColumnModel) -> Column:
        """Async version of _to_domain"""
        return self._to_domain(model)
    
    def _to_domain(self, model: ColumnModel) -> Column:
        """Convert model to domain entity"""
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
    
    def _to_model(self, domain: Column) -> ColumnModel:
        """Convert domain entity to model"""
        return ColumnModel(
            id=domain.id,
            table_id=domain.table_id,
            name=domain.name,
            data_type=domain.data_type,
            is_required=domain.is_required,
            default_value=domain.default_value,
            enum_values=domain.enum_values,
            reference_table_id=domain.reference_table_id,
            order=domain.order,
            created_at=domain.created_at
        )
    
    def _update_model_from_domain(self, model: ColumnModel, domain: Column):
        """Update model from domain entity"""
        model.name = domain.name
        model.data_type = domain.data_type
        model.is_required = domain.is_required
        model.default_value = domain.default_value
        model.enum_values = domain.enum_values
        model.reference_table_id = domain.reference_table_id
        model.order = domain.order

