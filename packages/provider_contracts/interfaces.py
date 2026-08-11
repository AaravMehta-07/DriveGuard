"""Provider interfaces."""
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from pydantic import BaseModel
from .capabilities import ProviderCapabilities


class UnsupportedCapability(Exception):
    """Raised or returned when a provider does not support an operation."""
    def __init__(self, feature: str = "", reason: str = ""):
        self.feature = feature
        self.reason = reason
        super().__init__(f"Capability '{feature}' is unsupported: {reason}")


class ProviderLicensingProfile(BaseModel):
    """Licensing flags for a provider."""
    render_allowed: bool
    cache_allowed: bool
    persistent_storage_allowed: bool
    derived_storage_allowed: bool
    redistribution_allowed: bool
    overlay_allowed: bool
    cross_provider_display_allowed: bool


class ProviderProfile(BaseModel):
    """Profile of a provider including its capabilities and licensing."""
    id: str
    name: str
    capabilities: ProviderCapabilities
    licensing: ProviderLicensingProfile
    metadata: Dict[str, Any]


class MapProvider(ABC):
    @abstractmethod
    def get_profile(self) -> ProviderProfile:
        pass


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        pass

    @abstractmethod
    def autocomplete(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        pass


class GeocodingProvider(ABC):
    @abstractmethod
    def geocode(self, address: str) -> List[Any]:
        pass

    @abstractmethod
    def reverse_geocode(self, lat: float, lon: float) -> List[Any]:
        pass


class RoutingProvider(ABC):
    @abstractmethod
    def calculate_route(self, origin: Any, destination: Any, waypoints: Optional[List[Any]] = None, options: Optional[Dict[str, Any]] = None) -> Any:
        pass


class NavigationProvider(ABC):
    @abstractmethod
    def get_turn_by_turn(self, route_id: str) -> Any:
        pass


class TrafficProvider(ABC):
    @abstractmethod
    def get_live_traffic(self, bounding_box: Any) -> Any:
        pass


class SpeedLimitProvider(ABC):
    @abstractmethod
    def get_speed_limits(self, road_segments: List[str]) -> Any:
        pass


class SignalProvider(ABC):
    @abstractmethod
    def get_signals(self, bounding_box: Any) -> Any:
        pass

    @abstractmethod
    def get_live_phase(self, signal_id: str) -> Any:
        pass


class EnforcementDataProvider(ABC):
    @abstractmethod
    def get_enforcement_points(self, bounding_box: Any) -> Any:
        pass


class RoadGraphProvider(ABC):
    @abstractmethod
    def get_road_segments(self, bounding_box: Any) -> Any:
        pass
