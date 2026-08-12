from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class RoadSegment(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'road_segments'
    """
    Base definition of a road segment.
    """
    geom = Column(Geometry('LINESTRING', srid=4326), nullable=False, index=True)
    name = Column(String, nullable=True)
    highway_type = Column(String, nullable=True) # e.g., motorway, primary, residential

    levels = relationship("RoadSegmentLevel", back_populates="segment")

class RoadSegmentLevel(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'road_segment_levels'
    """
    Detailed level data for segments (elevated vs surface).
    """
    segment_id = Column(ForeignKey('road_segments.id'), nullable=False, index=True)
    level = Column(Integer, nullable=False, default=0) # 0=surface, 1=bridge, -1=tunnel

    segment = relationship("RoadSegment", back_populates="levels")

class SpeedLimit(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'speed_limits'
    """
    Defined speed limits for segments or areas.
    """
    segment_id = Column(ForeignKey('road_segments.id'), nullable=True, index=True)
    geom = Column(Geometry('LINESTRING', srid=4326), nullable=True, index=True)
    max_speed = Column(Float, nullable=False) # km/h
    vehicle_type = Column(String, nullable=True) # If applicable

class SpeedLimitObservation(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'speed_limit_observations'
    """
    Observed speed limits (e.g. from users/cameras).
    """
    geom = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    observed_speed = Column(Float, nullable=False)
    source_id = Column(String, nullable=True)
