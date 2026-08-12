from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class ReviewQueue(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'review_queues'
    """
    Queue for human review of community reports, enforcement changes, etc.
    """
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False) # UUID stored as string to refer to multiple tables
    status = Column(String, nullable=False, default='pending')

    decisions = relationship("AdminDecision", back_populates="review")

class AdminDecision(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'admin_decisions'
    """
    Decisions made by administrators on review items.
    """
    review_id = Column(ForeignKey('review_queues.id'), nullable=False, index=True)
    admin_id = Column(ForeignKey('users.id'), nullable=False)
    decision = Column(String, nullable=False) # e.g., 'approved', 'rejected'
    notes = Column(String, nullable=True)

    review = relationship("ReviewQueue", back_populates="decisions")

class AuditLog(Base, UUIDMixin):
    __tablename__ = 'audit_logs'
    """
    Comprehensive audit log for all critical changes in the system.
    """
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    actor_id = Column(String, nullable=False, index=True)
    actor_type = Column(String, nullable=False)
    before_json = Column(JSON, nullable=True)
    after_json = Column(JSON, nullable=True)
    source = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
