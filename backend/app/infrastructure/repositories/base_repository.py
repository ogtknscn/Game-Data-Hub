"""
Generic base repository implementation
DRY principle - reduces code duplication
"""
from typing import Optional, List, TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.domain.interfaces.repositories import IRepository
from app.infrastructure.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)
D = TypeVar('D')  # Domain entity type


class BaseRepository(Generic[T, D], IRepository[D]):
    """
    Generic repository implementation
    Provides common CRUD operations
    """
    
    def __init__(self, session: AsyncSession, model: Type[T], domain_entity: Type[D]):
        self.session = session
        self.model = model
        self.domain_entity = domain_entity
    
    async def get_by_id(self, id: int) -> Optional[D]:
        """Get entity by ID - O(1) with index"""
        result = await self.session.get(self.model, id)
        if result:
            return self._to_domain(result)
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[D]:
        """Get all entities - O(n) where n is limit"""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        return [self._to_domain(entity) for entity in entities]
    
    async def create(self, entity: D) -> D:
        """Create new entity - O(1)"""
        model_instance = self._to_model(entity)
        self.session.add(model_instance)
        await self.session.flush()
        await self.session.refresh(model_instance)
        # Refresh relationships if needed
        return await self._to_domain_async(model_instance)
    
    async def _to_domain_async(self, model: T) -> D:
        """Async version of _to_domain - can be overridden"""
        return self._to_domain(model)
    
    async def update(self, entity: D) -> D:
        """Update existing entity - O(1)"""
        if not hasattr(entity, 'id') or not entity.id:
            raise ValueError("Entity must have an ID to update")
        
        model_instance = await self.session.get(self.model, entity.id)
        if not model_instance:
            raise ValueError(f"Entity with ID {entity.id} not found")
        
        # Update model from domain entity
        self._update_model_from_domain(model_instance, entity)
        await self.session.flush()
        await self.session.refresh(model_instance)
        return self._to_domain(model_instance)
    
    async def delete(self, id: int) -> bool:
        """Delete entity by ID - O(1)"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0
    
    def _to_domain(self, model: T) -> D:
        """Convert model to domain entity - must be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement _to_domain")
    
    def _to_model(self, domain: D) -> T:
        """Convert domain entity to model - must be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement _to_model")
    
    def _update_model_from_domain(self, model: T, domain: D):
        """Update model from domain entity - must be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement _update_model_from_domain")

