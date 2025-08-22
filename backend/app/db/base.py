from app.models.base import Base  # Our Declarative Base
from app.models.user import User
from app.models.department import Department
from app.models.slot import Slot
from app.models.game import Game
from app.models.booking import Booking

# This ensures Alembic sees all models when running migrations
__all__ = ["Base", "User", "Department", "Slot", "Game", "Booking"]
