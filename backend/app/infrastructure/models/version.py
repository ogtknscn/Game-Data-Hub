"""
Version/Commit model
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Text, JSON
from app.infrastructure.models.base import BaseModel


class VersionModel(BaseModel):
    """Version/Commit ORM model"""
    __tablename__ = "versions"
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True, index=True)
    message = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    changes = Column(JSON, nullable=False)  # {cell_id: {old_value, new_value}}

