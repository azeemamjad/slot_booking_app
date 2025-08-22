from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserDeleteResponse
from app.core.security import get_password_hash, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserOut]:
        """Get all users with pagination."""
        query = select(User).options(
            selectinload(User.department),
            selectinload(User.bookings)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return [UserOut.from_orm(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserOut:
        """Get a specific user by ID."""
        query = select(User).options(
            selectinload(User.department),
            selectinload(User.bookings)
        ).where(User.id == user_id)
        
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserOut.from_orm(user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (for internal use)."""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username (for internal use)."""
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user_data: UserCreate) -> UserOut:
        """Create a new user."""
        # Check if email already exists
        if user_data.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check if username already exists
        if user_data.username:
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user object
        user = User(
            email=user_data.email,
            username=user_data.username,
            password=hashed_password,
            description=user_data.description,
            profile_picture=user_data.profile_picture,
            role=UserRole(user_data.role.value),
            department_id=user_data.department_id
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        # Load relationships for response
        await self.db.refresh(user, ["department", "bookings"])
        
        return UserOut.from_orm(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserOut:
        """Update an existing user."""
        # Get the user
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if email already exists (if being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check if username already exists (if being updated)
        if user_data.username and user_data.username != user.username:
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
        
        if "role" in update_data:
            update_data["role"] = UserRole(update_data["role"].value)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        # Load relationships for response
        await self.db.refresh(user, ["department", "bookings"])
        
        return UserOut.from_orm(user)

    async def delete_user(self, user_id: int) -> UserDeleteResponse:
        """Delete a user."""
        # Get the user
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete the user
        await self.db.delete(user)
        await self.db.commit()
        
        return UserDeleteResponse(message="User deleted successfully")

    async def get_users_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[UserOut]:
        """Get all users in a specific department."""
        query = select(User).options(
            selectinload(User.department),
            selectinload(User.bookings)
        ).where(User.department_id == department_id).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return [UserOut.from_orm(user) for user in users]

    async def get_users_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[UserOut]:
        """Get all users with a specific role."""
        query = select(User).options(
            selectinload(User.department),
            selectinload(User.bookings)
        ).where(User.role == role).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return [UserOut.from_orm(user) for user in users]
