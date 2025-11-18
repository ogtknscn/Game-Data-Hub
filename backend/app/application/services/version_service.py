"""
Version service
"""
from typing import Optional, Dict, Any
from app.domain.entities.version import Version
from app.domain.interfaces.services import IVersionService
from app.domain.interfaces.repositories import IVersionRepository, IDataRepository
from app.core.exceptions import NotFoundError, ForbiddenError


class VersionService(IVersionService):
    """Version service implementation"""
    
    def __init__(self, version_repository: IVersionRepository, data_repository: IDataRepository):
        self.version_repository = version_repository
        self.data_repository = data_repository
    
    async def create_commit(
        self,
        project_id: int,
        table_id: Optional[int],
        message: str,
        author_id: int,
        changes: dict
    ) -> Version:
        """Create a new version/commit"""
        version = Version(
            project_id=project_id,
            table_id=table_id,
            message=message,
            author_id=author_id,
            changes=changes
        )
        return await self.version_repository.create(version)
    
    async def get_diff(self, version_id: int) -> Dict[str, Any]:
        """Get diff for a version"""
        version = await self.version_repository.get_by_id(version_id)
        if not version:
            raise NotFoundError("Version", str(version_id))
        
        return {
            "version_id": version.id,
            "message": version.message,
            "changes": version.changes,
            "created_at": version.created_at.isoformat() if version.created_at else None
        }
    
    async def rollback(self, version_id: int, user_id: int) -> bool:
        """Rollback to a version"""
        version = await self.version_repository.get_by_id(version_id)
        if not version:
            raise NotFoundError("Version", str(version_id))
        
        # Check authorization (simplified)
        if version.author_id != user_id:
            raise ForbiddenError("You can only rollback your own versions")
        
        # Apply rollback - restore old values
        for cell_id_str, change_data in version.changes.items():
            cell_id = int(cell_id_str)
            old_value = change_data.get("old_value")
            
            # Get cell and restore old value
            cell = await self.data_repository.get_cell_by_id(cell_id)
            if cell:
                cell.update_value(old_value)
                await self.data_repository.update_cell(cell)
        
        return True

