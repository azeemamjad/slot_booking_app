from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.booking import Booking, BookingStatus
from app.models.slot import Slot
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut, BookingDeleteResponse


class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_bookings(self, skip: int = 0, limit: int = 100) -> List[BookingOut]:
        """Get all bookings with pagination."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        bookings = result.scalars().all()
        
        return [BookingOut.from_orm(booking) for booking in bookings]

    async def get_booking_by_id(self, booking_id: int) -> BookingOut:
        """Get a specific booking by ID."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).where(Booking.id == booking_id)
        
        result = await self.db.execute(query)
        booking = result.scalars().first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        return BookingOut.from_orm(booking)

    async def get_bookings_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[BookingOut]:
        """Get all bookings for a specific user."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).where(Booking.user_id == user_id).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        bookings = result.scalars().all()
        
        return [BookingOut.from_orm(booking) for booking in bookings]

    async def get_bookings_by_slot(self, slot_id: int, skip: int = 0, limit: int = 100) -> List[BookingOut]:
        """Get all bookings for a specific slot."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).where(Booking.slot_id == slot_id).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        bookings = result.scalars().all()
        
        return [BookingOut.from_orm(booking) for booking in bookings]

    async def get_bookings_by_status(self, status: BookingStatus, skip: int = 0, limit: int = 100) -> List[BookingOut]:
        """Get all bookings with a specific status."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).where(Booking.status == status).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        bookings = result.scalars().all()
        
        return [BookingOut.from_orm(booking) for booking in bookings]

    async def get_user_active_bookings(self, user_id: int, skip: int = 0, limit: int = 100) -> List[BookingOut]:
        """Get active (confirmed) bookings for a specific user."""
        query = select(Booking).options(
            selectinload(Booking.user),
            selectinload(Booking.slot).selectinload(Slot.game)
        ).where(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.CONFIRMED
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        bookings = result.scalars().all()
        
        return [BookingOut.from_orm(booking) for booking in bookings]

    async def create_booking(self, booking_data: BookingCreate) -> BookingOut:
        """Create a new booking."""
        # Validate that the user exists
        user_query = select(User).where(User.id == booking_data.user_id)
        user_result = await self.db.execute(user_query)
        user = user_result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate that the slot exists
        slot_query = select(Slot).options(
            selectinload(Slot.bookings)
        ).where(Slot.id == booking_data.slot_id)
        slot_result = await self.db.execute(slot_query)
        slot = slot_result.scalars().first()
        
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )
        
        # Check if slot is full
        if slot.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot is already full"
            )
        
        # Check if user already has a booking for this slot
        existing_booking_query = select(Booking).where(
            Booking.user_id == booking_data.user_id,
            Booking.slot_id == booking_data.slot_id,
            Booking.status == BookingStatus.CONFIRMED
        )
        existing_booking_result = await self.db.execute(existing_booking_query)
        existing_booking = existing_booking_result.scalars().first()
        
        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a booking for this slot"
            )
        
        # Create booking object
        booking = Booking(
            user_id=booking_data.user_id,
            slot_id=booking_data.slot_id,
            status=booking_data.status
        )
        
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        
        # Load relationships for response
        await self.db.refresh(booking, ["user", "slot"])
        await self.db.refresh(booking.slot, ["game"])
        
        return BookingOut.from_orm(booking)

    async def update_booking(self, booking_id: int, booking_data: BookingUpdate) -> BookingOut:
        """Update an existing booking."""
        # Get the booking
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.db.execute(query)
        booking = result.scalars().first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        # Update status if provided
        if booking_data.status is not None:
            booking.status = booking_data.status
        
        await self.db.commit()
        await self.db.refresh(booking)
        
        # Load relationships for response
        await self.db.refresh(booking, ["user", "slot"])
        await self.db.refresh(booking.slot, ["game"])
        
        return BookingOut.from_orm(booking)

    async def cancel_booking(self, booking_id: int) -> BookingOut:
        """Cancel a booking (set status to cancelled)."""
        # Get the booking
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.db.execute(query)
        booking = result.scalars().first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        # Check if booking is already cancelled
        if booking.status == BookingStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking is already cancelled"
            )
        
        # Cancel the booking
        booking.status = BookingStatus.CANCELLED
        
        await self.db.commit()
        await self.db.refresh(booking)
        
        # Load relationships for response
        await self.db.refresh(booking, ["user", "slot"])
        await self.db.refresh(booking.slot, ["game"])
        
        return BookingOut.from_orm(booking)

    async def confirm_booking(self, booking_id: int) -> BookingOut:
        """Confirm a pending booking."""
        # Get the booking
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.db.execute(query)
        booking = result.scalars().first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        # Check if booking is already confirmed
        if booking.status == BookingStatus.CONFIRMED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking is already confirmed"
            )
        
        # Check if slot is still available
        slot_query = select(Slot).options(
            selectinload(Slot.bookings)
        ).where(Slot.id == booking.slot_id)
        slot_result = await self.db.execute(slot_query)
        slot = slot_result.scalars().first()
        
        if slot.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot is now full, cannot confirm booking"
            )
        
        # Confirm the booking
        booking.status = BookingStatus.CONFIRMED
        
        await self.db.commit()
        await self.db.refresh(booking)
        
        # Load relationships for response
        await self.db.refresh(booking, ["user", "slot"])
        await self.db.refresh(booking.slot, ["game"])
        
        return BookingOut.from_orm(booking)

    async def delete_booking(self, booking_id: int) -> BookingDeleteResponse:
        """Delete a booking."""
        # Get the booking
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.db.execute(query)
        booking = result.scalars().first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        await self.db.delete(booking)
        await self.db.commit()
        
        return BookingDeleteResponse(message="Booking deleted successfully")

    async def reset_current_day_bookings(self) -> dict:
        """Reset all bookings for the current day (Admin only)."""
        from datetime import datetime, timezone
        
        # Get current date in UTC
        current_date = datetime.now(timezone.utc).date()
        
        # Find all bookings for slots that are on the current day
        query = select(Booking).options(
            selectinload(Booking.slot)
        ).join(Slot).where(
            func.date(Slot.start_time) == current_date
        )
        
        result = await self.db.execute(query)
        current_day_bookings = result.scalars().all()
        
        if not current_day_bookings:
            return {
                "message": "No bookings found for today",
                "deleted_count": 0,
                "date": current_date.isoformat()
            }
        
        # Delete all current day bookings
        for booking in current_day_bookings:
            await self.db.delete(booking)
        
        await self.db.commit()
        
        return {
            "message": f"Successfully reset {len(current_day_bookings)} bookings for today",
            "deleted_count": len(current_day_bookings),
            "date": current_date.isoformat()
        }
