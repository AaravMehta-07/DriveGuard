from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base, UUIDMixin, TimestampMixin, SyntheticMixin

class RouteComplianceScan(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'route_compliance_scans'
    """
    Pre-trip compliance checking for a planned route.
    """
    user_id = Column(ForeignKey('users.id'), nullable=True, index=True)
    route_geom = Column(Geometry('LINESTRING', srid=4326), nullable=False)
    status = Column(String, nullable=False, default='completed')
    
    events = relationship("RouteComplianceEvent", back_populates="scan")

class RouteComplianceEvent(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'route_compliance_events'
    """
    Identified compliance issues along a scanned route.
    """
    scan_id = Column(ForeignKey('route_compliance_scans.id'), nullable=False, index=True)
    event_type = Column(String, nullable=False) # e.g. speed_zone, restricted_access
    geom = Column(Geometry('POINT', srid=4326), nullable=False)
    details = Column(JSON, nullable=True)
    
    scan = relationship("RouteComplianceScan", back_populates="events")
