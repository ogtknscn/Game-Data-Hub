"""
Data API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.schemas.request.data import UpdateCellRequest, CreateRowRequest, UpdateRowRequest
from app.schemas.response.table import TableDataResponse
from app.application.services.data_service import DataService
from app.infrastructure.repositories.data_repository import DataRepository
from app.infrastructure.repositories.table_repository import TableRepository
from app.application.mappers.domain_mapper import DomainMapper

router = APIRouter()


@router.get("/table/{table_id}", response_model=TableDataResponse)
async def get_table_data(
    table_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get table data (rows)"""
    data_repo = DataRepository(db)
    table_repo = TableRepository(db)
    data_service = DataService(data_repo, table_repo)
    
    rows = await data_service.get_table_data(table_id, skip, limit)
    
    # Get table columns for mapping
    table = await table_repo.get_by_id(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    rows_data = [DomainMapper.row_to_dict(row, table.columns) for row in rows]
    
    return TableDataResponse(table_id=table_id, rows=rows_data)


@router.post("/rows", status_code=status.HTTP_201_CREATED)
async def create_row(
    request: CreateRowRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new row"""
    try:
        data_repo = DataRepository(db)
        table_repo = TableRepository(db)
        data_service = DataService(data_repo, table_repo)
        
        row = await data_service.create_row(
            table_id=request.table_id,
            cells=request.cells
        )
        
        # Get table columns for mapping
        table = await table_repo.get_by_id(request.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        
        row_dict = DomainMapper.row_to_dict(row, table.columns)
        return row_dict
    except Exception as e:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create row: {str(e)}"
        )


@router.patch("/rows/{row_id}", status_code=status.HTTP_200_OK)
async def update_row(
    row_id: int,
    request: UpdateRowRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update row cells"""
    try:
        data_repo = DataRepository(db)
        table_repo = TableRepository(db)
        data_service = DataService(data_repo, table_repo)
        
        row = await data_service.update_row(
            row_id=row_id,
            cells=request.cells
        )
        
        # Get table columns for mapping
        table = await table_repo.get_by_id(row.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        
        row_dict = DomainMapper.row_to_dict(row, table.columns)
        return row_dict
    except Exception as e:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update row: {str(e)}"
        )


@router.delete("/rows/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_row(
    row_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a row"""
    try:
        data_repo = DataRepository(db)
        success = await data_repo.delete_row(row_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Row not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete row: {str(e)}"
        )


@router.patch("/cell", status_code=status.HTTP_200_OK)
async def update_cell(
    request: UpdateCellRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update cell value"""
    try:
        data_repo = DataRepository(db)
        table_repo = TableRepository(db)
        data_service = DataService(data_repo, table_repo)
        
        cell = await data_service.update_cell_value(
            cell_id=request.cell_id,
            new_value=request.value,
            user_id=current_user.id
        )
        
        return {"cell_id": cell.id, "value": cell.value, "message": "Cell updated successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update cell: {str(e)}"
        )

