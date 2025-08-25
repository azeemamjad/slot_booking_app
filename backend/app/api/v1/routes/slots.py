from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.services.slot_service import SlotService
from app.schemas.slot import SlotCreate, SlotUpdate, SlotOut, SlotDeleteResponse
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_slot_read_permission,
    require_slot_create_permission,
    require_slot_update_permission,
    require_slot_delete_permission
)
from app.schemas.user import UserOut

router = APIRouter(prefix="/slots", tags=["Slots"])


@router.get("/", response_model=List[SlotOut])
async def get_slots(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_read_permission)
):
    """Get all slots with pagination (Authenticated users only)."""
    slot_service = SlotService(db)
    return await slot_service.get_slots(skip=skip, limit=limit)


@router.get("/available/", response_model=List[SlotOut])
async def get_available_slots(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_read_permission)
):
    """Get all available slots (not full) (Authenticated users only)."""
    slot_service = SlotService(db)
    return await slot_service.get_available_slots(skip=skip, limit=limit)


@router.get("/game/{game_id}", response_model=List[SlotOut])
async def get_slots_by_game(
    game_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_read_permission)
):
    """Get all slots for a specific game (Authenticated users only)."""
    slot_service = SlotService(db)
    return await slot_service.get_slots_by_game(game_id, skip=skip, limit=limit)


@router.get("/date-range/", response_model=List[SlotOut])
async def get_slots_by_date_range(
    start_date: datetime = Query(..., description="Start date and time"),
    end_date: datetime = Query(..., description="End date and time"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_read_permission)
):
    """Get slots within a specific date range (Authenticated users only)."""
    slot_service = SlotService(db)
    return await slot_service.get_slots_by_date_range(start_date, end_date, skip=skip, limit=limit)


@router.get("/{slot_id}", response_model=SlotOut)
async def get_slot(
    slot_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_read_permission)
):
    """Get a specific slot by ID (Authenticated users only)."""
    slot_service = SlotService(db)
    return await slot_service.get_slot_by_id(slot_id)


@router.post("/", response_model=SlotOut, status_code=status.HTTP_201_CREATED)
async def create_slot(
    slot_data: SlotCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_create_permission)
):
    """Create a new slot (Admin only)."""
    slot_service = SlotService(db)
    return await slot_service.create_slot(slot_data)


@router.put("/{slot_id}", response_model=SlotOut)
async def update_slot(
    slot_id: int, 
    slot_data: SlotUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_update_permission)
):
    """Update an existing slot (Admin only)."""
    slot_service = SlotService(db)
    return await slot_service.update_slot(slot_id, slot_data)


@router.delete("/{slot_id}", response_model=SlotDeleteResponse)
async def delete_slot(
    slot_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_slot_delete_permission)
):
    """Delete a slot (Admin only)."""
    slot_service = SlotService(db)
    return await slot_service.delete_slot(slot_id)
