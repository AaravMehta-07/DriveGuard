from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class ChallanUpload(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'challan_uploads'
    """
    Traffic violation challans uploaded by users for tracking/analysis.
    """
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    vehicle_id = Column(ForeignKey('vehicles.id'), nullable=True, index=True)
    status = Column(String, nullable=False, default='processing')
    parsed_data = Column(JSON, nullable=True)

    events = relationship("ChallanEvent", back_populates="upload")

class ChallanEvent(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'challan_events'
    """
    Specific violation events parsed from a challan.
    """
    upload_id = Column(ForeignKey('challan_uploads.id'), nullable=False, index=True)
    violation_type = Column(String, nullable=False)
    penalty_amount = Column(String, nullable=True)

    upload = relationship("ChallanUpload", back_populates="events")
