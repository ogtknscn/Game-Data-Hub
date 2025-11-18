"""
Table and Column models
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.infrastructure.models.base import BaseModel


class TableModel(BaseModel):
    """Table ORM model"""
    __tablename__ = "tables"
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    project = relationship("ProjectModel", back_populates="tables")
    columns = relationship("ColumnModel", back_populates="table", cascade="all, delete-orphan", order_by="ColumnModel.order", foreign_keys="[ColumnModel.table_id]")
    rows = relationship("RowModel", back_populates="table", cascade="all, delete-orphan")


class ColumnModel(BaseModel):
    """Column ORM model"""
    __tablename__ = "columns"
    
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    data_type = Column(String(20), nullable=False)  # string, integer, float, boolean, enum, reference
    is_required = Column(Boolean, default=False, nullable=False)
    default_value = Column(String(255), nullable=True)
    enum_values = Column(JSON, nullable=True)  # For enum type
    reference_table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)  # For reference type
    order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    table = relationship("TableModel", back_populates="columns", foreign_keys=[table_id])

