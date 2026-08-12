from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class IngestionJob(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'ingestion_jobs'
    """
    Configuration for data ingestion pipelines.
    """
    source_id = Column(ForeignKey('data_sources.id'), nullable=False, index=True)
    job_name = Column(String, nullable=False)
    schedule = Column(String, nullable=True) # e.g. cron

    runs = relationship("IngestionRun", back_populates="job")

class IngestionRun(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'ingestion_runs'
    """
    A single execution of an ingestion job.
    """
    job_id = Column(ForeignKey('ingestion_jobs.id'), nullable=False, index=True)
    status = Column(String, nullable=False, default='pending')
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)

    job = relationship("IngestionJob", back_populates="runs")
