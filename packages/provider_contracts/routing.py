"""Routing contracts."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RouteLegalityResult(str, Enum):
    COMPLIANT = "COMPLIANT"
    UNCERTAIN = "UNCERTAIN"
    PROHIBITED = "PROHIBITED"


class RouteCandidate(BaseModel):
    """A candidate route proposed by a routing engine."""
    id: str
    geometry: str = Field(..., description="WKT or GeoJSON LineString")
    segments: List[str] = Field(default_factory=list)
    duration_seconds: float
    distance_meters: float
    provider_id: str


class RouteComplianceGateResult(BaseModel):
    """Result of passing a route candidate through the compliance gate."""
    route_id: str
    legality: RouteLegalityResult
    violations: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[Dict[str, Any]] = Field(default_factory=list)


class ComplianceAwareRoutingCoordinator(ABC):
    """Interface for a coordinator that ensures routes comply with domain rules."""

    @abstractmethod
    def evaluate_route_candidates(self, candidates: List[RouteCandidate]) -> List[RouteComplianceGateResult]:
        """Evaluate a list of route candidates for compliance."""
        pass

    @abstractmethod
    def get_compliant_route(self, origin: Any, destination: Any, waypoints: Optional[List[Any]] = None) -> RouteCandidate:
        """Calculate and return a fully compliant route."""
        pass
