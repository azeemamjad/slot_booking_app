from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserOut
from app.models.user import UserRole


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    """Dependency to get current authenticated user."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    return await auth_service.get_current_user(token)


async def get_current_active_user(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    """Dependency to get current active user."""
    # Add any additional checks for active status if needed
    # For example, check if user is not disabled, etc.
    return current_user


async def get_current_admin_user(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    """Dependency to get current admin user."""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def require_auth():
    """Decorator to require authentication for routes."""
    return Depends(get_current_user)


def require_admin():
    """Decorator to require admin role for routes."""
    return Depends(get_current_admin_user)
