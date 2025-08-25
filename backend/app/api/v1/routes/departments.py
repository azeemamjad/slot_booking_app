from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.department_service import DepartmentService
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut, DepartmentDeleteResponse
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_department_read_permission,
    require_department_create_permission,
    require_department_update_permission,
    require_department_delete_permission
)
from app.schemas.user import UserOut

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=List[DepartmentOut])
async def get_departments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_department_read_permission)
):
    """Get all departments with pagination (Authenticated users only)."""
    department_service = DepartmentService(db)
    return await department_service.get_departments(skip=skip, limit=limit)


@router.get("/{department_id}", response_model=DepartmentOut)
async def get_department(
    department_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_department_read_permission)
):
    """Get a specific department by ID (Authenticated users only)."""
    department_service = DepartmentService(db)
    return await department_service.get_department_by_id(department_id)


@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_department_create_permission)
):
    """Create a new department (Admin only)."""
    department_service = DepartmentService(db)
    return await department_service.create_department(department_data)


@router.put("/{department_id}", response_model=DepartmentOut)
async def update_department(
    department_id: int, 
    department_data: DepartmentUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_department_update_permission)
):
    """Update an existing department (Admin only)."""
    department_service = DepartmentService(db)
    return await department_service.update_department(department_id, department_data)


@router.delete("/{department_id}", response_model=DepartmentDeleteResponse)
async def delete_department(
    department_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_department_delete_permission)
):
    """Delete a department (Admin only)."""
    department_service = DepartmentService(db)
    return await department_service.delete_department(department_id)
