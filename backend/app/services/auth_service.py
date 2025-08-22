from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, LogoutResponse, TokenData
from app.schemas.user import UserOut
from app.core.security import verify_password, create_access_token, decode_access_token
from app.core.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, login_data: LoginRequest) -> Optional[User]:
        """Authenticate user with email/username and password."""
        # Find user by email or username
        if login_data.email:
            query = select(User).where(User.email == login_data.email)
        else:
            query = select(User).where(User.username == login_data.username)
        
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        if not user:
            return None
        
        # Verify password
        if not verify_password(login_data.password, user.password):
            return None
        
        return user

    async def login(self, login_data: LoginRequest) -> TokenResponse:
        """Login user and return JWT token."""
        user = await self.authenticate_user(login_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        }
        
        access_token = create_access_token(
            data=token_data, 
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        )

    async def logout(self) -> LogoutResponse:
        """Logout user (client-side token invalidation)."""
        # In a stateless JWT system, logout is typically handled client-side
        # by removing the token. For additional security, you could implement
        # a token blacklist in Redis or database.
        return LogoutResponse(message="Successfully logged out")

    async def get_current_user(self, token: str) -> UserOut:
        """Get current user from JWT token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Decode token
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get user from database
        query = select(User).options(
            selectinload(User.department),
            selectinload(User.bookings)
        ).where(User.id == int(user_id))
        
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        if user is None:
            raise credentials_exception
        
        return UserOut.from_orm(user)

    async def get_current_active_user(self, token: str) -> UserOut:
        """Get current active user from JWT token."""
        user = await self.get_current_user(token)
        # Add any additional checks for active status if needed
        # For example, check if user is not disabled, etc.
        return user

    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify JWT token and return token data."""
        payload = decode_access_token(token)
        if payload is None:
            return None
        
        return TokenData(
            user_id=int(payload.get("sub")),
            email=payload.get("email"),
            username=payload.get("username"),
            role=payload.get("role")
        )
