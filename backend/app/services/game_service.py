from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate, GameOut, GameDeleteResponse


class GameService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_games(self, skip: int = 0, limit: int = 100) -> List[GameOut]:
        """Get all games with pagination."""
        query = select(Game).options(
            selectinload(Game.slots)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        games = result.scalars().all()
        
        return [GameOut.from_orm(game) for game in games]

    async def get_game_by_id(self, game_id: int) -> GameOut:
        """Get a specific game by ID."""
        query = select(Game).options(
            selectinload(Game.slots)
        ).where(Game.id == game_id)
        
        result = await self.db.execute(query)
        game = result.scalars().first()
        
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        return GameOut.from_orm(game)

    async def get_game_by_title(self, title: str) -> Optional[Game]:
        """Get game by title (for internal use)."""
        query = select(Game).where(Game.title == title)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_game(self, game_data: GameCreate) -> GameOut:
        """Create a new game."""
        # Check if title already exists
        existing_game = await self.get_game_by_title(game_data.title)
        if existing_game:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game with this title already exists"
            )
        
        # Create game object
        game = Game(
            title=game_data.title,
            description=game_data.description,
            background=game_data.background
        )
        
        self.db.add(game)
        await self.db.commit()
        await self.db.refresh(game)
        
        # Load relationships for response
        await self.db.refresh(game, ["slots"])
        
        return GameOut.from_orm(game)

    async def update_game(self, game_id: int, game_data: GameUpdate) -> GameOut:
        """Update an existing game."""
        # Get the game
        query = select(Game).where(Game.id == game_id)
        result = await self.db.execute(query)
        game = result.scalars().first()
        
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Check if new title conflicts with existing game
        if game_data.title and game_data.title != game.title:
            existing_game = await self.get_game_by_title(game_data.title)
            if existing_game:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Game with this title already exists"
                )
        
        # Update fields
        if game_data.title is not None:
            game.title = game_data.title
        if game_data.description is not None:
            game.description = game_data.description
        if game_data.background is not None:
            game.background = game_data.background
        
        await self.db.commit()
        await self.db.refresh(game)
        
        # Load relationships for response
        await self.db.refresh(game, ["slots"])
        
        return GameOut.from_orm(game)

    async def delete_game(self, game_id: int) -> GameDeleteResponse:
        """Delete a game."""
        # Get the game
        query = select(Game).options(
            selectinload(Game.slots)
        ).where(Game.id == game_id)
        result = await self.db.execute(query)
        game = result.scalars().first()
        
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Check if game has slots
        if game.slots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete game with existing slots. Please delete slots first."
            )
        
        await self.db.delete(game)
        await self.db.commit()
        
        return GameDeleteResponse(message="Game deleted successfully")

    async def get_games_with_available_slots(self, skip: int = 0, limit: int = 100) -> List[GameOut]:
        """Get games that have available slots."""
        query = select(Game).options(
            selectinload(Game.slots)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        games = result.scalars().all()
        
        # Filter games with available slots
        games_with_available_slots = [
            game for game in games 
            if any(not slot.is_full for slot in game.slots)
        ]
        
        return [GameOut.from_orm(game) for game in games_with_available_slots]
