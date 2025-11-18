"""
Versions API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.schemas.request.version import CreateCommitRequest
from app.schemas.response.version import VersionResponse, DiffResponse
from app.application.services.version_service import VersionService
from app.infrastructure.repositories.version_repository import VersionRepository
from app.infrastructure.repositories.data_repository import DataRepository

router = APIRouter()


@router.post("/commit", response_model=VersionResponse, status_code=status.HTTP_201_CREATED)
async def create_commit(
    request: CreateCommitRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new version/commit"""
    version_repo = VersionRepository(db)
    data_repo = DataRepository(db)
    version_service = VersionService(version_repo, data_repo)
    
    version = await version_service.create_commit(
        project_id=request.project_id,
        table_id=request.table_id,
        message=request.message,
        author_id=current_user.id,
        changes=request.changes
    )
    
    return VersionResponse(
        id=version.id,
        project_id=version.project_id,
        table_id=version.table_id,
        message=version.message,
        author_id=version.author_id,
        changes=version.changes,
        created_at=version.created_at
    )


@router.get("/project/{project_id}", response_model=List[VersionResponse])
async def get_versions_by_project(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get versions by project ID"""
    version_repo = VersionRepository(db)
    versions = await version_repo.get_by_project_id(project_id, skip, limit)
    
    return [
        VersionResponse(
            id=v.id,
            project_id=v.project_id,
            table_id=v.table_id,
            message=v.message,
            author_id=v.author_id,
            changes=v.changes,
            created_at=v.created_at
        )
        for v in versions
    ]


@router.get("/{version_id}/diff", response_model=DiffResponse)
async def get_diff(
    version_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get diff for a version"""
    version_repo = VersionRepository(db)
    data_repo = DataRepository(db)
    version_service = VersionService(version_repo, data_repo)
    
    diff_data = await version_service.get_diff(version_id)
    
    return DiffResponse(**diff_data)


@router.post("/{version_id}/rollback", status_code=status.HTTP_200_OK)
async def rollback_version(
    version_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Rollback to a version"""
    version_repo = VersionRepository(db)
    data_repo = DataRepository(db)
    version_service = VersionService(version_repo, data_repo)
    
    success = await version_service.rollback(version_id, current_user.id)
    
    if success:
        return {"message": "Rollback successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rollback failed"
        )

