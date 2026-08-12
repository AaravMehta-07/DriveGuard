from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class DataSource(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'data_sources'
    """
    Data source providers and licensing metadata.
    """
    name = Column(String, nullable=False, unique=True)
    provider = Column(String, nullable=False)

    # Licensing / Provenance fields per correction #3
    render_allowed = Column(Boolean, nullable=False, default=False)
    cache_allowed = Column(Boolean, nullable=False, default=False)
    persistent_storage_allowed = Column(Boolean, nullable=False, default=False)
    derived_storage_allowed = Column(Boolean, nullable=False, default=False)
    redistribution_allowed = Column(Boolean, nullable=False, default=False)
    overlay_allowed = Column(Boolean, nullable=False, default=False)
    cross_provider_display_allowed = Column(Boolean, nullable=False, default=False)

    documents = relationship("SourceDocument", back_populates="source")

class SourceDocument(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'source_documents'
    """
    Documents imported from data sources.
    """
    source_id = Column(ForeignKey('data_sources.id'), nullable=False, index=True)
    document_identifier = Column(String, nullable=False, index=True)

    source = relationship("DataSource", back_populates="documents")
    versions = relationship("SourceDocumentVersion", back_populates="document")

class SourceDocumentVersion(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'source_document_versions'
    """
    Version tracking for source documents.
    """
    document_id = Column(ForeignKey('source_documents.id'), nullable=False, index=True)
    version_hash = Column(String, nullable=False)

    document = relationship("SourceDocument", back_populates="versions")
