from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, validates
import enum

from app.models.base import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    NORMAL = "normal"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)   # URL or file path
    description = Column(Text, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.NORMAL, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    department = relationship("Department", back_populates="users")

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")

    @property
    def slot_booked(self) -> int:
        return len(self.bookings)


    @validates("email", "username")
    def validate_user_identifiers(self, key, value):
        """Ensure at least one of email or username is provided."""
        if not value and not (self.email if key == "username" else self.username):
            raise ValueError("Either email or username must be provided")
        return value
