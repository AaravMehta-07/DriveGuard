from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base, UUIDMixin, TimestampMixin, SyntheticMixin

class CommunityReport(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'community_reports'
    """
    User-submitted reports for road issues (e.g., potholes, accidents).
    """
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    report_type = Column(String, nullable=False)
    geom = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    status = Column(String, nullable=False, default='active')
    
    confirmations = relationship("ReportConfirmation", back_populates="report")

class ReportConfirmation(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'report_confirmations'
    """
    Upvotes/downvotes on community reports.
    """
    report_id = Column(ForeignKey('community_reports.id'), nullable=False, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    confirmation_type = Column(String, nullable=False) # e.g., 'confirmed', 'rejected'
    
    report = relationship("CommunityReport", back_populates="confirmations")

class ReporterReputation(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'reporter_reputations'
    """
    Tracks reliability score for users submitting reports.
    """
    user_id = Column(ForeignKey('users.id'), unique=True, nullable=False)
    score = Column(Integer, nullable=False, default=100)
