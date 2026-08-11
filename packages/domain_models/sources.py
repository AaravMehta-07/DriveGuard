"""Source and licensing models."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    AUTHORITY = "AUTHORITY"
    PROVIDER = "PROVIDER"
    COMMUNITY = "COMMUNITY"
    OSM = "OSM"
    SENSOR_DERIVED = "SENSOR_DERIVED"
    UNKNOWN = "UNKNOWN"


class SourceConfidenceLevel(str, Enum):
    OFFICIAL_AUTHORITY = "OFFICIAL_AUTHORITY"
    LICENSED_PROVIDER = "LICENSED_PROVIDER"
    FIELD_VERIFIED = "FIELD_VERIFIED"
    MULTI_SOURCE_CONFIRMED = "MULTI_SOURCE_CONFIRMED"
    OSM = "OSM"
    MULTIPLE_COMMUNITY_REPORTS = "MULTIPLE_COMMUNITY_REPORTS"
    SINGLE_COMMUNITY_REPORT = "SINGLE_COMMUNITY_REPORT"
    UNKNOWN = "UNKNOWN"


class DataSource(BaseModel):
    """A source of data with its licensing permissions."""
    id: str
    name: str
    type: SourceType
    render_allowed: bool = False
    cache_allowed: bool = False
    persistent_storage_allowed: bool = False
    derived_storage_allowed: bool = False
    redistribution_allowed: bool = False
    overlay_allowed: bool = False
    cross_provider_display_allowed: bool = False


class SourceReference(BaseModel):
    """Reference to a specific data source for a given entity."""
    source_id: str
    original_id: Optional[str] = None
    confidence_level: SourceConfidenceLevel = SourceConfidenceLevel.UNKNOWN
    version: Optional[str] = None
