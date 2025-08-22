from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, LogoutResponse
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login user and get access token."""
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    db: AsyncSession = Depends(get_db)
):
    """Logout user."""
    auth_service = AuthService(db)
    return await auth_service.logout()


@router.get("/me", response_model=UserOut)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user information."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    return await auth_service.get_current_user(token)


@router.get("/verify")
async def verify_token(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Verify JWT token validity."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    
    token_data = auth_service.verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "valid": True,
        "user_id": token_data.user_id,
        "email": token_data.email,
        "username": token_data.username,
        "role": token_data.role
    }
