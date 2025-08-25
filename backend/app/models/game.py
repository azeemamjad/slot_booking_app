from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    background = Column(String, nullable=True)  # image/file path

    slots = relationship("Slot", back_populates="game")

    @property
    def total_slots(self) -> int:
        """Calculate total number of slots for this game."""
        return len(self.slots)

    @property
    def available_slots(self) -> int:
        """Calculate available slots (not full) for this game."""
        return sum(1 for slot in self.slots if not slot.is_full)
