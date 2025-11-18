"""
Data repository implementation
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.domain.entities.cell import Row, Cell
from app.domain.interfaces.repositories import IDataRepository
from app.infrastructure.models.cell import RowModel, CellModel
from app.infrastructure.repositories.base_repository import BaseRepository


class DataRepository(BaseRepository[RowModel, Row], IDataRepository):
    """Data repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, RowModel, Row)
    
    async def get_rows_by_table_id(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Row]:
        """Get rows by table ID - O(n) where n is limit"""
        stmt = select(RowModel).where(
            RowModel.table_id == table_id
        ).options(
            selectinload(RowModel.cells)
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    async def get_row_by_id(self, row_id: int) -> Optional[Row]:
        """Get row by ID - O(1)"""
        model = await self.session.get(RowModel, row_id)
        if model:
            # Load cells
            await self.session.refresh(model, ["cells"])
            return self._to_domain(model)
        return None
    
    async def create_row(self, row: Row) -> Row:
        """Create a new row with cells - O(n) where n is number of cells"""
        model = self._to_model(row)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        
        # Create cells with proper row_id
        for column_id, cell in row.cells.items():
            cell_model = CellModel(
                row_id=model.id,
                column_id=column_id,
                value=str(cell.value) if cell.value is not None else None
            )
            self.session.add(cell_model)
            # Update cell entity with row_id
            cell.row_id = model.id
        
        await self.session.flush()
        await self.session.refresh(model, ["cells"])
        return self._to_domain(model)
    
    async def update_row(self, row: Row) -> Row:
        """Update row and its cells - O(n) where n is number of cells"""
        model = await self.session.get(RowModel, row.id)
        if not model:
            raise ValueError(f"Row with ID {row.id} not found")
        
        # Load existing cells
        await self.session.refresh(model, ["cells"])
        
        # Update or create cells
        for column_id, cell in row.cells.items():
            # Find existing cell
            existing_cell = None
            for cell_model in model.cells:
                if cell_model.column_id == column_id:
                    existing_cell = cell_model
                    break
            
            if existing_cell:
                # Update existing cell
                existing_cell.value = str(cell.value) if cell.value is not None else None
            else:
                # Create new cell
                cell_model = CellModel(
                    row_id=row.id,
                    column_id=column_id,
                    value=str(cell.value) if cell.value is not None else None
                )
                self.session.add(cell_model)
        
        await self.session.flush()
        await self.session.refresh(model, ["cells"])
        return self._to_domain(model)
    
    async def delete_row(self, row_id: int) -> bool:
        """Delete row by ID - O(1)"""
        return await self.delete(row_id)
    
    async def get_cell_by_id(self, cell_id: int) -> Optional[Cell]:
        """Get cell by ID - O(1)"""
        model = await self.session.get(CellModel, cell_id)
        if model:
            return self._cell_to_domain(model)
        return None
    
    async def update_cell(self, cell: Cell) -> Cell:
        """Update cell value - O(1)"""
        model = await self.session.get(CellModel, cell.id)
        if not model:
            raise ValueError(f"Cell with ID {cell.id} not found")
        
        model.value = str(cell.value) if cell.value is not None else None
        await self.session.flush()
        await self.session.refresh(model)
        return self._cell_to_domain(model)
    
    def _to_domain(self, model: RowModel) -> Row:
        """Convert model to domain entity"""
        cells_dict = {}
        if model.cells:
            for cell_model in model.cells:
                cells_dict[cell_model.column_id] = self._cell_to_domain(cell_model)
        
        return Row(
            id=model.id,
            table_id=model.table_id,
            cells=cells_dict,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, domain: Row) -> RowModel:
        """Convert domain entity to model"""
        return RowModel(
            id=domain.id,
            table_id=domain.table_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def _update_model_from_domain(self, model: RowModel, domain: Row):
        """Update model from domain entity"""
        model.updated_at = domain.updated_at
    
    def _cell_to_domain(self, model: CellModel) -> Cell:
        """Convert cell model to domain entity"""
        # Parse value based on column type (simplified - actual parsing in service layer)
        value = model.value
        return Cell(
            id=model.id,
            row_id=model.row_id,
            column_id=model.column_id,
            value=value,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

