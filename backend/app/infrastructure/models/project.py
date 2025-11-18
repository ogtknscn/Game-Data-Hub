"""
Project model
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.models.base import BaseModel


class ProjectModel(BaseModel):
    """Project ORM model"""
    __tablename__ = "projects"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationships
    tables = relationship("TableModel", back_populates="project", cascade="all, delete-orphan")

