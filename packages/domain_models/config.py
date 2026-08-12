"""Config models."""
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel


class MapMatchPolicyVersion(BaseModel):
    """Configuration version for map matching policy."""
    version: str
    effective_from: datetime
    parameters: Dict[str, Any]
