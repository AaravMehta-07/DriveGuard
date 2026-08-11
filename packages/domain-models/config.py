"""Config models."""
from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime
from .compliance import CompliancePolicyVersion
from .alerts import AlertPolicyVersion


class MapMatchPolicyVersion(BaseModel):
    """Configuration version for map matching policy."""
    version: str
    effective_from: datetime
    parameters: Dict[str, Any]
