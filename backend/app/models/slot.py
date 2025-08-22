from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, default=2)

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship("Game", back_populates="slots")

    bookings = relationship("Booking", back_populates="slot", cascade="all, delete-orphan")

    @property
    def slots_booked_count(self) -> int:
        return len(self.bookings)

    @property
    def is_full(self) -> bool:
        return self.slots_booked_count >= self.capacity
