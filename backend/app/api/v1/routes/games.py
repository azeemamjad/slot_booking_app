from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.game_service import GameService
from app.schemas.game import GameCreate, GameUpdate, GameOut, GameDeleteResponse
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_game_read_permission,
    require_game_create_permission,
    require_game_update_permission,
    require_game_delete_permission
)
from app.schemas.user import UserOut

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/", response_model=List[GameOut])
async def get_games(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_read_permission)
):
    """Get all games with pagination (Authenticated users only)."""
    game_service = GameService(db)
    return await game_service.get_games(skip=skip, limit=limit)


@router.get("/{game_id}", response_model=GameOut)
async def get_game(
    game_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_read_permission)
):
    """Get a specific game by ID (Authenticated users only)."""
    game_service = GameService(db)
    return await game_service.get_game_by_id(game_id)


@router.post("/", response_model=GameOut, status_code=status.HTTP_201_CREATED)
async def create_game(
    game_data: GameCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_create_permission)
):
    """Create a new game (Admin only)."""
    game_service = GameService(db)
    return await game_service.create_game(game_data)


@router.put("/{game_id}", response_model=GameOut)
async def update_game(
    game_id: int, 
    game_data: GameUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_update_permission)
):
    """Update an existing game (Admin only)."""
    game_service = GameService(db)
    return await game_service.update_game(game_id, game_data)


@router.delete("/{game_id}", response_model=GameDeleteResponse)
async def delete_game(
    game_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_delete_permission)
):
    """Delete a game (Admin only)."""
    game_service = GameService(db)
    return await game_service.delete_game(game_id)


@router.get("/available/", response_model=List[GameOut])
async def get_games_with_available_slots(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(require_game_read_permission)
):
    """Get games that have available slots (Authenticated users only)."""
    game_service = GameService(db)
    return await game_service.get_games_with_available_slots(skip=skip, limit=limit)
