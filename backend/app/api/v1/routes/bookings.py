from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.booking_service import BookingService
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut, BookingDeleteResponse, BookingStatus
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_booking_read_permission,
    require_booking_create_permission,
    require_booking_update_permission,
    require_booking_delete_permission,
    require_booking_confirm_permission,
    require_booking_reset_permission
)
from app.core.ownership import require_booking_ownership
from app.schemas.user import UserOut

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=List[BookingOut])
async def get_bookings(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_delete_permission)  # Use admin-only permission
):
    """Get all bookings with pagination (Admin only)."""
    booking_service = BookingService(db)
    return await booking_service.get_bookings(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[BookingOut])
async def get_bookings_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_read_permission)
):
    """Get all bookings for a specific user (Users can only view their own bookings, admins can view any)."""
    # Check ownership
    require_booking_ownership(current_user, user_id)
    
    booking_service = BookingService(db)
    return await booking_service.get_bookings_by_user(user_id, skip=skip, limit=limit)


@router.get("/user/{user_id}/active", response_model=List[BookingOut])
async def get_user_active_bookings(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_read_permission)
):
    """Get active (confirmed) bookings for a specific user (Users can only view their own bookings, admins can view any)."""
    # Check ownership
    require_booking_ownership(current_user, user_id)
    
    booking_service = BookingService(db)
    return await booking_service.get_user_active_bookings(user_id, skip=skip, limit=limit)


@router.get("/slot/{slot_id}", response_model=List[BookingOut])
async def get_bookings_by_slot(
    slot_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_read_permission)
):
    """Get all bookings for a specific slot (Authenticated users only)."""
    booking_service = BookingService(db)
    return await booking_service.get_bookings_by_slot(slot_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[BookingOut])
async def get_bookings_by_status(
    status: BookingStatus,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_delete_permission)
):
    """Get all bookings with a specific status (Admin only)."""
    booking_service = BookingService(db)
    return await booking_service.get_bookings_by_status(status, skip=skip, limit=limit)


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_read_permission)
):
    """Get a specific booking by ID (Users can only view their own bookings, admins can view any)."""
    booking_service = BookingService(db)
    booking = await booking_service.get_booking_by_id(booking_id)
    
    # Check ownership
    require_booking_ownership(current_user, booking.user_id)
    
    return booking


@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_create_permission)
):
    """Create a new booking (Users can only create bookings for themselves, admins can create for any user)."""
    # Users can only create bookings for themselves, admins can create for any user
    if current_user.role != "admin" and booking_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users can only create bookings for themselves"
        )
    
    booking_service = BookingService(db)
    return await booking_service.create_booking(booking_data)


@router.put("/{booking_id}", response_model=BookingOut)
async def update_booking(
    booking_id: int, 
    booking_data: BookingUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_update_permission)
):
    """Update an existing booking (Users can only update their own bookings, admins can update any)."""
    booking_service = BookingService(db)
    booking = await booking_service.get_booking_by_id(booking_id)
    
    # Check ownership
    require_booking_ownership(current_user, booking.user_id)
    
    return await booking_service.update_booking(booking_id, booking_data)


@router.post("/{booking_id}/cancel", response_model=BookingOut)
async def cancel_booking(
    booking_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_update_permission)
):
    """Cancel a booking (Users can only cancel their own bookings, admins can cancel any)."""
    booking_service = BookingService(db)
    booking = await booking_service.get_booking_by_id(booking_id)
    
    # Check ownership
    require_booking_ownership(current_user, booking.user_id)
    
    return await booking_service.cancel_booking(booking_id)


@router.post("/{booking_id}/confirm", response_model=BookingOut)
async def confirm_booking(
    booking_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_confirm_permission)
):
    """Confirm a pending booking (Admin only)."""
    booking_service = BookingService(db)
    return await booking_service.confirm_booking(booking_id)


@router.delete("/{booking_id}", response_model=BookingDeleteResponse)
async def delete_booking(
    booking_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_delete_permission)
):
    """Delete a booking (Admin only)."""
    booking_service = BookingService(db)
    return await booking_service.delete_booking(booking_id)


@router.post("/reset-current-day", response_model=dict)
async def reset_current_day_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_booking_reset_permission)
):
    """Reset all bookings for the current day (Admin only)."""
    booking_service = BookingService(db)
    return await booking_service.reset_current_day_bookings()
