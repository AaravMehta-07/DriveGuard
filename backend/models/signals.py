from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base, UUIDMixin, TimestampMixin, SyntheticMixin

class TrafficSignalJunction(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'traffic_signal_junctions'
    """
    A junction controlled by traffic signals.
    """
    geom = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    
    approaches = relationship("SignalApproach", back_populates="junction")

class SignalApproach(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'signal_approaches'
    """
    An approach to a signal junction.
    """
    junction_id = Column(ForeignKey('traffic_signal_junctions.id'), nullable=False, index=True)
    geom = Column(Geometry('LINESTRING', srid=4326), nullable=False)
    
    junction = relationship("TrafficSignalJunction", back_populates="approaches")

class SignalStopLine(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'signal_stop_lines'
    """
    The stop line geometry for a signal.
    """
    approach_id = Column(ForeignKey('signal_approaches.id'), nullable=False, index=True)
    geom = Column(Geometry('LINESTRING', srid=4326), nullable=False)

class SignalMovement(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'signal_movements'
    """
    Allowed movements from an approach (e.g., straight, left, right).
    """
    approach_id = Column(ForeignKey('signal_approaches.id'), nullable=False, index=True)
    movement_type = Column(String, nullable=False)
