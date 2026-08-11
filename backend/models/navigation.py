from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base, UUIDMixin, TimestampMixin, SyntheticMixin

class NavigationSession(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'navigation_sessions'
    """
    Tracks a user's active navigation session.
    """
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    start_location = Column(Geometry('POINT', srid=4326), nullable=False)
    destination = Column(Geometry('POINT', srid=4326), nullable=False)
    route_geometry = Column(Geometry('LINESTRING', srid=4326), nullable=True)
    status = Column(String, nullable=False, default='active')

    trips = relationship("Trip", back_populates="session")

class Trip(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'trips'
    """
    Represents a completed or ongoing trip within a navigation session.
    """
    session_id = Column(ForeignKey('navigation_sessions.id'), nullable=False, index=True)
    distance_meters = Column(Float, nullable=False, default=0.0)
    duration_seconds = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default='ongoing')

    session = relationship("NavigationSession", back_populates="trips")
    events = relationship("TripEvent", back_populates="trip")

class TripEvent(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'trip_events'
    """
    Events that occur during a trip (e.g., speeding, hard braking).
    """
    trip_id = Column(ForeignKey('trips.id'), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    data = Column(JSON, nullable=True)

    trip = relationship("Trip", back_populates="events")
