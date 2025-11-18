"""
Projects API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.infrastructure.models.user import UserModel
from app.schemas.request.project import CreateProjectRequest, UpdateProjectRequest
from app.schemas.response.project import ProjectResponse
from app.application.services.project_service import ProjectService
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.application.mappers.domain_mapper import DomainMapper

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: CreateProjectRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new project"""
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    
    project = await project_service.create_project(
        name=request.name,
        description=request.description,
        owner_id=current_user.id
    )
    
    return ProjectResponse(**DomainMapper.project_to_dict(project))


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all projects for current user"""
    project_repo = ProjectRepository(db)
    projects = await project_repo.get_by_owner_id(current_user.id)
    
    return [ProjectResponse(**DomainMapper.project_to_dict(p)) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get project by ID"""
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    
    project = await project_service.get_project(project_id, current_user.id)
    
    return ProjectResponse(**DomainMapper.project_to_dict(project))

