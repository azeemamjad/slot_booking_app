from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


# ------------------ Base ------------------ #
class BookingBase(BaseModel):
    user_id: int
    slot_id: int
    status: BookingStatus = BookingStatus.confirmed


# ------------------ Create ------------------ #
class BookingCreate(BookingBase):
    pass


# ------------------ Update ------------------ #
class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None


# ------------------ Response ------------------ #
class BookingOut(BaseModel):
    id: int
    user_id: int
    slot_id: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ------------------ Delete Response ------------------ #
class BookingDeleteResponse(BaseModel):
    message: str
