from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ------------------ Base ------------------ #
class SlotBase(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = 2
    game_id: int


# ------------------ Create ------------------ #
class SlotCreate(SlotBase):
    pass


# ------------------ Update ------------------ #
class SlotUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None
    game_id: Optional[int] = None


# ------------------ Response ------------------ #
class SlotOut(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    capacity: int
    slots_booked_count: int
    is_full: bool
    game_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ------------------ Delete Response ------------------ #
class SlotDeleteResponse(BaseModel):
    message: str
