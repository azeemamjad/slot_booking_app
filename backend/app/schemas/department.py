from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ------------------ Base ------------------ #
class DepartmentBase(BaseModel):
    title: str
    description: Optional[str] = None


# ------------------ Create ------------------ #
class DepartmentCreate(DepartmentBase):
    pass


# ------------------ Update ------------------ #
class DepartmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# ------------------ Response ------------------ #
class DepartmentOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    slot_booked: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ------------------ Delete Response ------------------ #
class DepartmentDeleteResponse(BaseModel):
    message: str
