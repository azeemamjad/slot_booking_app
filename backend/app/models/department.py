from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="department")

    @property
    def slot_booked(self) -> int:
        """Calculate total slots booked by all users in this department."""
        return sum(len(user.slots) for user in self.users)
