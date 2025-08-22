from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    normal = "normal"


# ------------------ Base ------------------ #
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    description: Optional[str] = None
    profile_picture: Optional[str] = None
    role: UserRole = UserRole.normal
    department_id: int


# ------------------ Create ------------------ #
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


# ------------------ Update ------------------ #
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[UserRole] = None
    department_id: Optional[int] = None


# ------------------ Response ------------------ #
class UserOut(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    description: Optional[str] = None
    profile_picture: Optional[str] = None
    role: UserRole
    department_id: int
    slot_booked: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ------------------ Delete Response ------------------ #
class UserDeleteResponse(BaseModel):
    message: str
