from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

from app.models.slot import Slot
from app.models.game import Game
from app.schemas.slot import SlotCreate, SlotUpdate, SlotOut, SlotDeleteResponse


class SlotService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_slots(self, skip: int = 0, limit: int = 100) -> List[SlotOut]:
        """Get all slots with pagination."""
        query = select(Slot).options(
            selectinload(Slot.game),
            selectinload(Slot.bookings)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        slots = result.scalars().all()
        
        return [SlotOut.from_orm(slot) for slot in slots]

    async def get_slot_by_id(self, slot_id: int) -> SlotOut:
        """Get a specific slot by ID."""
        query = select(Slot).options(
            selectinload(Slot.game),
            selectinload(Slot.bookings)
        ).where(Slot.id == slot_id)
        
        result = await self.db.execute(query)
        slot = result.scalars().first()
        
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )
        
        return SlotOut.from_orm(slot)

    async def get_slots_by_game(self, game_id: int, skip: int = 0, limit: int = 100) -> List[SlotOut]:
        """Get all slots for a specific game."""
        query = select(Slot).options(
            selectinload(Slot.game),
            selectinload(Slot.bookings)
        ).where(Slot.game_id == game_id).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        slots = result.scalars().all()
        
        return [SlotOut.from_orm(slot) for slot in slots]

    async def get_available_slots(self, skip: int = 0, limit: int = 100) -> List[SlotOut]:
        """Get all slots that are not full."""
        query = select(Slot).options(
            selectinload(Slot.game),
            selectinload(Slot.bookings)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        slots = result.scalars().all()
        
        # Filter slots that are not full
        available_slots = [slot for slot in slots if not slot.is_full]
        
        return [SlotOut.from_orm(slot) for slot in available_slots]

    async def get_slots_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[SlotOut]:
        """Get slots within a specific date range."""
        query = select(Slot).options(
            selectinload(Slot.game),
            selectinload(Slot.bookings)
        ).where(
            Slot.start_time >= start_date,
            Slot.end_time <= end_date
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        slots = result.scalars().all()
        
        return [SlotOut.from_orm(slot) for slot in slots]

    async def create_slot(self, slot_data: SlotCreate) -> SlotOut:
        """Create a new slot."""
        # Validate that the game exists
        game_query = select(Game).where(Game.id == slot_data.game_id)
        game_result = await self.db.execute(game_query)
        game = game_result.scalars().first()
        
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Validate time logic
        if slot_data.start_time >= slot_data.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time must be before end time"
            )
        
        # Check for overlapping slots for the same game
        overlapping_query = select(Slot).where(
            Slot.game_id == slot_data.game_id,
            Slot.start_time < slot_data.end_time,
            Slot.end_time > slot_data.start_time
        )
        overlapping_result = await self.db.execute(overlapping_query)
        overlapping_slots = overlapping_result.scalars().all()
        
        if overlapping_slots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot time overlaps with existing slots for this game"
            )
        
        # Create slot object
        slot = Slot(
            start_time=slot_data.start_time,
            end_time=slot_data.end_time,
            capacity=slot_data.capacity,
            game_id=slot_data.game_id
        )
        
        self.db.add(slot)
        await self.db.commit()
        await self.db.refresh(slot)
        
        # Load relationships for response
        await self.db.refresh(slot, ["game", "bookings"])
        
        return SlotOut.from_orm(slot)

    async def update_slot(self, slot_id: int, slot_data: SlotUpdate) -> SlotOut:
        """Update an existing slot."""
        # Get the slot with relationships
        query = select(Slot).options(
            selectinload(Slot.bookings)
        ).where(Slot.id == slot_id)
        result = await self.db.execute(query)
        slot = result.scalars().first()
        
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )
        
        # Check if slot has bookings and prevent certain updates
        if slot.bookings and (slot_data.start_time is not None or slot_data.end_time is not None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot modify time of slot with existing bookings"
            )
        
        # Validate game exists if changing game_id
        if slot_data.game_id is not None and slot_data.game_id != slot.game_id:
            game_query = select(Game).where(Game.id == slot_data.game_id)
            game_result = await self.db.execute(game_query)
            game = game_result.scalars().first()
            
            if not game:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Game not found"
                )
        
        # Validate time logic if updating times
        if slot_data.start_time is not None and slot_data.end_time is not None:
            if slot_data.start_time >= slot_data.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start time must be before end time"
                )
        elif slot_data.start_time is not None:
            if slot_data.start_time >= slot.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start time must be before end time"
                )
        elif slot_data.end_time is not None:
            if slot.start_time >= slot_data.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start time must be before end time"
                )
        
        # Check for overlapping slots if updating times or game
        if (slot_data.start_time is not None or slot_data.end_time is not None or slot_data.game_id is not None):
            start_time = slot_data.start_time if slot_data.start_time is not None else slot.start_time
            end_time = slot_data.end_time if slot_data.end_time is not None else slot.end_time
            game_id = slot_data.game_id if slot_data.game_id is not None else slot.game_id
            
            overlapping_query = select(Slot).where(
                Slot.id != slot_id,
                Slot.game_id == game_id,
                Slot.start_time < end_time,
                Slot.end_time > start_time
            )
            overlapping_result = await self.db.execute(overlapping_query)
            overlapping_slots = overlapping_result.scalars().all()
            
            if overlapping_slots:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slot time overlaps with existing slots for this game"
                )
        
        # Update fields
        if slot_data.start_time is not None:
            slot.start_time = slot_data.start_time
        if slot_data.end_time is not None:
            slot.end_time = slot_data.end_time
        if slot_data.capacity is not None:
            slot.capacity = slot_data.capacity
        if slot_data.game_id is not None:
            slot.game_id = slot_data.game_id
        
        await self.db.commit()
        await self.db.refresh(slot)
        
        # Load relationships for response
        await self.db.refresh(slot, ["game", "bookings"])
        
        return SlotOut.from_orm(slot)

    async def delete_slot(self, slot_id: int) -> SlotDeleteResponse:
        """Delete a slot."""
        # Get the slot
        query = select(Slot).options(
            selectinload(Slot.bookings)
        ).where(Slot.id == slot_id)
        result = await self.db.execute(query)
        slot = result.scalars().first()
        
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )
        
        # Check if slot has bookings
        if slot.bookings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete slot with existing bookings. Please cancel bookings first."
            )
        
        await self.db.delete(slot)
        await self.db.commit()
        
        return SlotDeleteResponse(message="Slot deleted successfully")
