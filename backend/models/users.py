from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'users'
    """
    User model for DriveGuard V3.
    """
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    vehicles = relationship("Vehicle", back_populates="user")

class UserPreferences(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'user_preferences'
    """
    Stores individual user preferences for the app and navigation routing.
    """
    user_id = Column(ForeignKey('users.id'), unique=True, nullable=False)
    preferences = Column(JSON, default={}, nullable=False)

    user = relationship("User", back_populates="preferences")

class Vehicle(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'vehicles'
    """
    Stores user vehicles for personalized routing.
    """
    user_id = Column(ForeignKey('users.id'), nullable=False)
    license_plate = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=False) # e.g., 'car', 'bike', 'truck'

    user = relationship("User", back_populates="vehicles")
