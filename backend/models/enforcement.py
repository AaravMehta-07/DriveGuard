from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class EnforcementPoint(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'enforcement_points'
    """
    Point-based enforcement (e.g., speed cameras, red light cameras).
    """
    geom = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    point_type = Column(String, nullable=False) # e.g., speed_camera, red_light_camera

    # road_level fields per correction #23
    road_level = Column(Integer, nullable=True)
    level_confidence = Column(Float, nullable=True)
    structure_type = Column(String, nullable=True) # bridge/tunnel/surface/elevated

    observations = relationship("EnforcementObservation", back_populates="point")

class EnforcementZone(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'enforcement_zones'
    """
    Area-based enforcement (e.g., no parking zones).
    """
    geom = Column(Geometry('POLYGON', srid=4326), nullable=False, index=True)
    zone_type = Column(String, nullable=False) # e.g., no_parking, low_emission

class EnforcementObservation(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'enforcement_observations'
    """
    User or automated observations of enforcement points.
    """
    point_id = Column(ForeignKey('enforcement_points.id'), nullable=False, index=True)
    observed_status = Column(String, nullable=False) # e.g., active, removed
    confidence = Column(Float, default=1.0)

    point = relationship("EnforcementPoint", back_populates="observations")
