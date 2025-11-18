"""
Repository interfaces
Abstract interfaces following Dependency Inversion Principle
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar
from app.domain.entities.project import Project
from app.domain.entities.table import Table, Column
from app.domain.entities.cell import Row, Cell
from app.domain.entities.version import Version

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Generic repository interface"""
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create new entity"""
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update existing entity"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete entity by ID"""
        pass


class IProjectRepository(IRepository[Project]):
    """Project repository interface"""
    
    @abstractmethod
    async def get_by_owner_id(self, owner_id: int) -> List[Project]:
        """Get projects by owner ID"""
        pass


class ITableRepository(IRepository[Table]):
    """Table repository interface"""
    
    @abstractmethod
    async def get_by_project_id(self, project_id: int) -> List[Table]:
        """Get tables by project ID"""
        pass
    
    @abstractmethod
    async def get_columns_by_table_id(self, table_id: int) -> List[Column]:
        """Get columns by table ID"""
        pass


class IDataRepository(IRepository[Row]):
    """Data repository interface"""
    
    @abstractmethod
    async def get_rows_by_table_id(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Row]:
        """Get rows by table ID"""
        pass
    
    @abstractmethod
    async def get_cell_by_id(self, cell_id: int) -> Optional[Cell]:
        """Get cell by ID"""
        pass
    
    @abstractmethod
    async def update_cell(self, cell: Cell) -> Cell:
        """Update cell value"""
        pass


class IVersionRepository(IRepository[Version]):
    """Version repository interface"""
    
    @abstractmethod
    async def get_by_project_id(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Version]:
        """Get versions by project ID"""
        pass
    
    @abstractmethod
    async def get_by_table_id(self, table_id: int, skip: int = 0, limit: int = 100) -> List[Version]:
        """Get versions by table ID"""
        pass

