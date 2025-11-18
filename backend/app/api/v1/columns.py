"""
Columns API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.schemas.request.table import CreateColumnRequest
from app.schemas.response.table import ColumnResponse
from app.application.services.table_service import TableService
from app.infrastructure.repositories.table_repository import TableRepository
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.infrastructure.repositories.column_repository import ColumnRepository
from app.application.mappers.domain_mapper import DomainMapper

router = APIRouter()


@router.post("/tables/{table_id}/columns", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
async def create_column(
    table_id: int,
    request: CreateColumnRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new column for a table"""
    try:
        table_repo = TableRepository(db)
        project_repo = ProjectRepository(db)
        column_repo = ColumnRepository(db)
        table_service = TableService(table_repo, project_repo)
        
        # Create column domain entity
        column = await table_service.create_column(
            table_id=table_id,
            name=request.name,
            data_type=request.data_type,
            is_required=request.is_required,
            default_value=request.default_value,
            enum_values=request.enum_values,
            reference_table_id=request.reference_table_id,
            order=request.order
        )
        
        # Get max order if order not provided
        if column.order == 0:
            existing_columns = await column_repo.get_by_table_id(table_id)
            if existing_columns:
                max_order = max(c.order for c in existing_columns)
                column.order = max_order + 1
            else:
                column.order = 1
        
        # Create column in database
        created_column = await column_repo.create(column)
        
        return ColumnResponse(**DomainMapper.column_to_dict(created_column))
    except Exception as e:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create column: {str(e)}"
        )


@router.get("/tables/{table_id}/columns", response_model=List[ColumnResponse])
async def get_columns_by_table(
    table_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all columns for a table"""
    column_repo = ColumnRepository(db)
    columns = await column_repo.get_by_table_id(table_id)
    
    return [ColumnResponse(**DomainMapper.column_to_dict(col)) for col in columns]


@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column(
    column_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a column"""
    try:
        column_repo = ColumnRepository(db)
        success = await column_repo.delete(column_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Column not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete column: {str(e)}"
        )

