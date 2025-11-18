"""
Version repository implementation
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.version import Version
from app.domain.interfaces.repositories import IVersionRepository
from app.infrastructure.models.version import VersionModel
from app.infrastructure.repositories.base_repository import BaseRepository


class VersionRepository(BaseRepository[VersionModel, Version], IVersionRepository):
    """Version repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, VersionModel, Version)
    
    async def get_by_project_id(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Version]:
        """Get versions by project ID - O(n) where n is limit"""
        stmt = select(VersionModel).where(
            VersionModel.project_id == project_id
        ).order_by(VersionModel.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    async def get_by_table_id(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Version]:
        """Get versions by table ID - O(n) where n is limit"""
        stmt = select(VersionModel).where(
            VersionModel.table_id == table_id
        ).order_by(VersionModel.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    def _to_domain(self, model: VersionModel) -> Version:
        """Convert model to domain entity"""
        return Version(
            id=model.id,
            project_id=model.project_id,
            table_id=model.table_id,
            message=model.message,
            author_id=model.author_id,
            changes=model.changes or {},
            created_at=model.created_at
        )
    
    def _to_model(self, domain: Version) -> VersionModel:
        """Convert domain entity to model"""
        return VersionModel(
            id=domain.id,
            project_id=domain.project_id,
            table_id=domain.table_id,
            message=domain.message,
            author_id=domain.author_id,
            changes=domain.changes,
            created_at=domain.created_at
        )
    
    def _update_model_from_domain(self, model: VersionModel, domain: Version):
        """Update model from domain entity"""
        model.message = domain.message
        model.changes = domain.changes

