"""
Tables API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.schemas.request.table import CreateTableRequest, CreateColumnRequest
from app.schemas.response.table import TableResponse, ColumnResponse
from app.application.services.table_service import TableService
from app.infrastructure.repositories.table_repository import TableRepository
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.application.mappers.domain_mapper import DomainMapper

router = APIRouter()


@router.post("", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
async def create_table(
    request: CreateTableRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new table"""
    try:
        table_repo = TableRepository(db)
        project_repo = ProjectRepository(db)
        table_service = TableService(table_repo, project_repo)
        
        table = await table_service.create_table(
            project_id=request.project_id,
            name=request.name,
            description=request.description
        )
        
        return TableResponse(**DomainMapper.table_to_dict(table))
    except Exception as e:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create table: {str(e)}"
        )


@router.get("/project/{project_id}", response_model=List[TableResponse])
async def get_tables_by_project(
    project_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all tables for a project"""
    table_repo = TableRepository(db)
    tables = await table_repo.get_by_project_id(project_id)
    
    return [TableResponse(**DomainMapper.table_to_dict(t)) for t in tables]


@router.get("/{table_id}", response_model=TableResponse)
async def get_table(
    table_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get table by ID"""
    try:
        table_repo = TableRepository(db)
        table = await table_repo.get_by_id(table_id)
        
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        
        return TableResponse(**DomainMapper.table_to_dict(table))
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get table: {str(e)}"
        )

