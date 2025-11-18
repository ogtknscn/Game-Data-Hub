"""
Domain mapper utilities
Converts between domain entities and DTOs/models
"""
from typing import Dict, Any, List
from app.domain.entities.project import Project
from app.domain.entities.table import Table, Column
from app.domain.entities.cell import Row, Cell


class DomainMapper:
    """Domain mapper"""
    
    @staticmethod
    def project_to_dict(project: Project) -> Dict[str, Any]:
        """Convert project entity to dictionary"""
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "owner_id": project.owner_id,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    
    @staticmethod
    def table_to_dict(table: Table) -> Dict[str, Any]:
        """Convert table entity to dictionary"""
        return {
            "id": table.id,
            "project_id": table.project_id,
            "name": table.name,
            "description": table.description,
            "columns": [DomainMapper.column_to_dict(col) for col in table.columns],
            "created_at": table.created_at.isoformat() if table.created_at else None,
            "updated_at": table.updated_at.isoformat() if table.updated_at else None
        }
    
    @staticmethod
    def column_to_dict(column: Column) -> Dict[str, Any]:
        """Convert column entity to dictionary"""
        return {
            "id": column.id,
            "table_id": column.table_id,
            "name": column.name,
            "data_type": column.data_type,
            "is_required": column.is_required,
            "default_value": column.default_value,
            "enum_values": column.enum_values,
            "reference_table_id": column.reference_table_id,
            "order": column.order
        }
    
    @staticmethod
    def row_to_dict(row: Row, columns: List[Column]) -> Dict[str, Any]:
        """Convert row entity to dictionary"""
        data = {
            "id": row.id,
            "table_id": row.table_id,
            "cells": {}
        }
        
        # Map cells by column name for easier frontend consumption
        for column in columns:
            cell = row.cells.get(column.id)
            data["cells"][column.name] = cell.value if cell else None
        
        return data

