import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class UUIDMixin:
    """Provides a UUID primary key for models."""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

class TimestampMixin:
    """Provides created_at and updated_at timestamp columns."""
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class SyntheticMixin:
    """Provides a synthetic flag to distinguish real data from synthetic/test data."""
    synthetic = Column(Boolean, default=False, nullable=False, server_default='false')
