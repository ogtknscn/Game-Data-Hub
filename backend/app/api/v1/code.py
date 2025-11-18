"""
Code generation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.infrastructure.repositories.table_repository import TableRepository
from app.infrastructure.repositories.data_repository import DataRepository
from app.application.services.code_generation_service import CodeGenerationService
from app.application.mappers.domain_mapper import DomainMapper

router = APIRouter()


@router.get("/tables/{table_id}/generate")
async def generate_code(
    table_id: int,
    format: str = Query(..., description="Code format: unity, unreal, json"),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate code for a table"""
    try:
        table_repo = TableRepository(db)
        data_repo = DataRepository(db)
        
        # Get table
        table = await table_repo.get_by_id(table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found"
            )
        
        # Get table data
        rows = await data_repo.get_rows_by_table_id(table_id, skip=0, limit=1000)
        
        # Prepare data for code generation
        table_data = {
            "name": table.name,
            "rows": [DomainMapper.row_to_dict(row, table.columns) for row in rows]
        }
        
        schema = {
            "columns": [DomainMapper.column_to_dict(col) for col in table.columns]
        }
        
        # Generate code
        code_service = CodeGenerationService()
        code = code_service.generate_code(format, table_data, schema)
        
        # Determine file extension and MIME type
        file_ext = "cs" if format == "unity" else "json" if format == "json" else "json"
        mime_type = "text/plain" if format == "unity" else "application/json"
        
        filename = f"{table.name}.{file_ext}"
        
        return Response(
            content=code,
            media_type=mime_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate code: {str(e)}"
        )

