"""
Project repository implementation
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.project import Project
from app.domain.interfaces.repositories import IProjectRepository
from app.infrastructure.models.project import ProjectModel
from app.infrastructure.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[ProjectModel, Project], IProjectRepository):
    """Project repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectModel, Project)
    
    async def get_by_owner_id(self, owner_id: int) -> List[Project]:
        """Get projects by owner ID - O(n) where n is number of projects"""
        stmt = select(ProjectModel).where(ProjectModel.owner_id == owner_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    def _to_domain(self, model: ProjectModel) -> Project:
        """Convert model to domain entity"""
        return Project(
            id=model.id,
            name=model.name,
            description=model.description,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, domain: Project) -> ProjectModel:
        """Convert domain entity to model"""
        return ProjectModel(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            owner_id=domain.owner_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def _update_model_from_domain(self, model: ProjectModel, domain: Project):
        """Update model from domain entity"""
        model.name = domain.name
        model.description = domain.description
        model.updated_at = domain.updated_at

