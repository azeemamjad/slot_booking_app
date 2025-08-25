from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserDeleteResponse, UserRole
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_user_read_permission,
    require_user_create_permission,
    require_user_update_permission,
    require_user_delete_permission,
    Permission
)
from app.core.ownership import require_user_ownership

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_create_permission)
):
    """Get all users with pagination (Admin only)."""
    user_service = UserService(db)
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_read_permission)
):
    """Get a specific user by ID (Users can only view their own profile, admins can view any)."""
    # Check ownership
    require_user_ownership(current_user, user_id)
    
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_create_permission)
):
    """Create a new user (Admin only - for creating users on behalf of others)."""
    user_service = UserService(db)
    return await user_service.create_user(user_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_update_permission)
):
    """Update an existing user (Users can only update their own profile, admins can update any)."""
    # Check ownership
    require_user_ownership(current_user, user_id)
    
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_delete_permission)
):
    """Delete a user (Admin only)."""
    user_service = UserService(db)
    return await user_service.delete_user(user_id)


@router.get("/department/{department_id}", response_model=List[UserOut])
async def get_users_by_department(
    department_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_user_read_permission)
):
    """Get all users in a specific department (Authenticated users only)."""
    user_service = UserService(db)
    return await user_service.get_users_by_department(department_id, skip=skip, limit=limit)
