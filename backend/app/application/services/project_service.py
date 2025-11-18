"""
Project service
"""
from typing import Optional
from app.domain.entities.project import Project
from app.domain.interfaces.services import IProjectService
from app.domain.interfaces.repositories import IProjectRepository
from app.core.exceptions import NotFoundError, ForbiddenError


class ProjectService(IProjectService):
    """Project service implementation"""
    
    def __init__(self, repository: IProjectRepository):
        self.repository = repository
    
    async def create_project(self, name: str, description: Optional[str], owner_id: int) -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id
        )
        return await self.repository.create(project)
    
    async def get_project(self, project_id: int, user_id: int) -> Optional[Project]:
        """Get project by ID with authorization check"""
        project = await self.repository.get_by_id(project_id)
        
        if not project:
            raise NotFoundError("Project", str(project_id))
        
        # Check authorization (owner only for now)
        if project.owner_id != user_id:
            raise ForbiddenError("You don't have access to this project")
        
        return project

