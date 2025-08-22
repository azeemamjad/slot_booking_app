from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Login request schema - user can login with either email or username."""
    email: Optional[str] = Field(None, description="User email")
    username: Optional[str] = Field(None, description="Username")
    password: str = Field(..., min_length=1, description="User password")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LogoutResponse(BaseModel):
    """Logout response schema."""
    message: str


class TokenData(BaseModel):
    """Token data schema for internal use."""
    user_id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
