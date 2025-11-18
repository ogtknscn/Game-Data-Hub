"""
Row and Cell models
"""
from sqlalchemy import Column, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.infrastructure.models.base import BaseModel


class RowModel(BaseModel):
    """Row ORM model"""
    __tablename__ = "rows"
    
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)
    
    # Relationships
    table = relationship("TableModel", back_populates="rows")
    cells = relationship("CellModel", back_populates="row", cascade="all, delete-orphan")


class CellModel(BaseModel):
    """Cell ORM model"""
    __tablename__ = "cells"
    
    row_id = Column(Integer, ForeignKey("rows.id"), nullable=False, index=True)
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=False, index=True)
    value = Column(Text, nullable=True)  # Store as text, parse based on column type
    
    # Relationships
    row = relationship("RowModel", back_populates="cells")
    column = relationship("ColumnModel")

