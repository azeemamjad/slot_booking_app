from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ------------------ Base ------------------ #
class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    background: Optional[str] = None


# ------------------ Create ------------------ #
class GameCreate(GameBase):
    pass


# ------------------ Update ------------------ #
class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    background: Optional[str] = None


# ------------------ Response ------------------ #
class GameOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    background: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ------------------ Delete Response ------------------ #
class GameDeleteResponse(BaseModel):
    message: str
