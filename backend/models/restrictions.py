from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, ForeignKey, String

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class TurnRestriction(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'turn_restrictions'
    """
    Restrictions on turns from one segment to another.
    """
    from_segment_id = Column(ForeignKey('road_segments.id'), nullable=False, index=True)
    to_segment_id = Column(ForeignKey('road_segments.id'), nullable=False, index=True)
    restriction_type = Column(String, nullable=False) # e.g. no_left_turn, no_u_turn

class AccessRestriction(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'access_restrictions'
    """
    Access restrictions for specific vehicle types or times.
    """
    geom = Column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    vehicle_type = Column(String, nullable=True)
    access_type = Column(String, nullable=False) # e.g., no_entry, private

class TemporaryRestriction(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'temporary_restrictions'
    """
    Temporary closures or restrictions (e.g., construction).
    """
    geom = Column(Geometry('LINESTRING', srid=4326), nullable=False, index=True)
    restriction_type = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
