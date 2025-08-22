from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserDeleteResponse
from app.core.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_admin_user)
):
    """Get all users with pagination (Admin only)."""
    user_service = UserService(db)
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Get a specific user by ID (Users can only view their own profile, admins can view any)."""
    # Users can only view their own profile, admins can view any
    if current_user.role.value != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this user"
        )
    
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_admin_user)
):
    """Create a new user (Admin only)."""
    user_service = UserService(db)
    return await user_service.create_user(user_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Update an existing user (Users can only update their own profile, admins can update any)."""
    # Users can only update their own profile, admins can update any
    if current_user.role.value != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user"
        )
    
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_admin_user)
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
    current_user: UserOut = Depends(get_current_user)
):
    """Get all users in a specific department (Authenticated users only)."""
    user_service = UserService(db)
    return await user_service.get_users_by_department(department_id, skip=skip, limit=limit)
