"""
Service interfaces
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.project import Project
from app.domain.entities.table import Table
from app.domain.entities.cell import Row, Cell
from app.domain.entities.version import Version


class IAuthService(ABC):
    """Authentication service interface"""
    
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token"""
        pass
    
    @abstractmethod
    async def register(self, username: str, email: str, password: str) -> dict:
        """Register new user"""
        pass


class IProjectService(ABC):
    """Project service interface"""
    
    @abstractmethod
    async def create_project(self, name: str, description: Optional[str], owner_id: int) -> Project:
        """Create a new project"""
        pass
    
    @abstractmethod
    async def get_project(self, project_id: int, user_id: int) -> Optional[Project]:
        """Get project by ID with authorization check"""
        pass


class ITableService(ABC):
    """Table service interface"""
    
    @abstractmethod
    async def create_table(self, project_id: int, name: str, description: Optional[str]) -> Table:
        """Create a new table"""
        pass
    
    @abstractmethod
    async def add_column(self, table_id: int, column: 'Column') -> 'Column':
        """Add column to table"""
        pass


class IDataService(ABC):
    """Data service interface"""
    
    @abstractmethod
    async def update_cell_value(self, cell_id: int, new_value: any, user_id: int) -> Cell:
        """Update cell value with validation"""
        pass
    
    @abstractmethod
    async def get_table_data(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Row]:
        """Get table data (rows)"""
        pass


class IVersionService(ABC):
    """Version service interface"""
    
    @abstractmethod
    async def create_commit(self, project_id: int, table_id: Optional[int], message: str, author_id: int, changes: dict) -> Version:
        """Create a new version/commit"""
        pass
    
    @abstractmethod
    async def get_diff(self, version_id: int) -> dict:
        """Get diff for a version"""
        pass
    
    @abstractmethod
    async def rollback(self, version_id: int, user_id: int) -> bool:
        """Rollback to a version"""
        pass

