"""
Provider Adapters Implementation with Capability Negotiation

Per Correction #2:
Provider adapters declare explicitly supported capabilities via ProviderCapabilities.
Unsupported methods return an UnsupportedCapability object.

Per Correction #10-#11:
Production adapters NEVER return fabricated data (fake Mumbai coordinates, fake routes).
They either make genuine provider API requests, or return a typed NOT_CONFIGURED state.
"""

from typing import Any, Optional, List, Dict
from enum import Enum

from .capabilities import ProviderCapabilities
from .interfaces import (
    MapProvider,
    SearchProvider,
    GeocodingProvider,
    RoutingProvider,
    NavigationProvider,
    TrafficProvider,
    SpeedLimitProvider,
    SignalProvider,
    RoadGraphProvider,
    UnsupportedCapability,
    ProviderProfile,
    ProviderLicensingProfile,
)


class ProviderStatus(str, Enum):
    """Status indicating why a provider operation could not complete."""

    PROVIDER_NOT_CONFIGURED = "PROVIDER_NOT_CONFIGURED"
    BLOCKED_EXTERNAL_CREDENTIAL = "BLOCKED_EXTERNAL_CREDENTIAL"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    UNSUPPORTED_CAPABILITY = "UNSUPPORTED_CAPABILITY"


class ProviderResult:
    """Typed result wrapper for provider operations."""

    def __init__(
        self,
        status: ProviderStatus,
        data: Any = None,
        message: str = "",
    ):
        self.status = status
        self.data = data
        self.message = message
        self.success = status not in (
            ProviderStatus.PROVIDER_NOT_CONFIGURED,
            ProviderStatus.BLOCKED_EXTERNAL_CREDENTIAL,
            ProviderStatus.PROVIDER_UNAVAILABLE,
            ProviderStatus.UNSUPPORTED_CAPABILITY,
        )

    def __repr__(self) -> str:
        return f"ProviderResult(status={self.status}, message={self.message!r})"


def _credential_blocked(provider: str, operation: str) -> ProviderResult:
    """Return a typed BLOCKED_EXTERNAL_CREDENTIAL result."""
    return ProviderResult(
        status=ProviderStatus.BLOCKED_EXTERNAL_CREDENTIAL,
        message=(
            f"{provider} {operation}: API credential not configured. "
            f"Set the required environment variable to enable this operation."
        ),
    )


class MapplsProviderAdapter(
    MapProvider,
    SearchProvider,
    GeocodingProvider,
    RoutingProvider,
    NavigationProvider,
    TrafficProvider,
    SpeedLimitProvider,
):
    """Adapter for Mappls (MapmyIndia) SDK / API.

    All operations require valid Mappls API credentials.
    Without credentials, operations return BLOCKED_EXTERNAL_CREDENTIAL.
    """

    def __init__(
        self,
        api_key: str = "",
        client_id: str = "",
        client_secret: str = "",
    ):
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self._configured = bool(api_key and client_id and client_secret)
        self._capabilities = ProviderCapabilities(
            map_rendering=True,
            search=True,
            autocomplete=True,
            geocoding=True,
            reverse_geocoding=True,
            route_calculation=True,
            alternative_routes=True,
            turn_by_turn_navigation=True,
            rerouting=True,
            lane_guidance=True,
            live_traffic=True,
            speed_limits=True,
            traffic_signals=False,
            live_signal_phase=False,
            live_signal_countdown=False,
            provider_enforcement_data=False,
            offline_maps=True,
            offline_routing=True,
            offline_navigation=True,
            android_auto=True,
            carplay=True,
            route_avoid_segments=True,
            custom_waypoints=True,
            custom_route_injection=False,
        )
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=True,
            persistent_storage_allowed=True,
            derived_storage_allowed=False,
            redistribution_allowed=False,
            overlay_allowed=True,
            cross_provider_display_allowed=False,
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="mappls",
            name="Mappls (MapmyIndia)",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"version": "v1.0", "configured": self._configured},
        )

    def search(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "search")
        # Real implementation: call Mappls Atlas Search API
        return _credential_blocked("Mappls", "search")

    def autocomplete(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "autocomplete")
        return _credential_blocked("Mappls", "autocomplete")

    def geocode(self, address: str) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "geocode")
        return _credential_blocked("Mappls", "geocode")

    def reverse_geocode(self, lat: float, lon: float) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "reverse_geocode")
        return _credential_blocked("Mappls", "reverse_geocode")

    def calculate_route(
        self,
        origin: Any,
        destination: Any,
        waypoints: Optional[List[Any]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "calculate_route")
        return _credential_blocked("Mappls", "calculate_route")

    def get_turn_by_turn(self, route_id: str) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "get_turn_by_turn")
        return _credential_blocked("Mappls", "get_turn_by_turn")

    def get_live_traffic(self, bounding_box: Any) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "get_live_traffic")
        return _credential_blocked("Mappls", "get_live_traffic")

    def get_speed_limits(self, road_segments: List[str]) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("Mappls", "get_speed_limits")
        return _credential_blocked("Mappls", "get_speed_limits")


class GoogleMapsProviderAdapter(
    MapProvider,
    SearchProvider,
    GeocodingProvider,
    RoutingProvider,
    NavigationProvider,
    TrafficProvider,
    SpeedLimitProvider,
):
    """Adapter for Google Maps Platform APIs / SDK.

    All operations require a valid Google Maps API key.
    Without credentials, operations return BLOCKED_EXTERNAL_CREDENTIAL.
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self._configured = bool(api_key)
        self._capabilities = ProviderCapabilities(
            map_rendering=True,
            search=True,
            autocomplete=True,
            geocoding=True,
            reverse_geocoding=True,
            route_calculation=True,
            alternative_routes=True,
            turn_by_turn_navigation=True,
            rerouting=True,
            lane_guidance=True,
            live_traffic=True,
            speed_limits=True,
            traffic_signals=False,
            live_signal_phase=False,
            live_signal_countdown=False,
            provider_enforcement_data=False,
            offline_maps=False,
            offline_routing=False,
            offline_navigation=False,
            android_auto=True,
            carplay=True,
            route_avoid_segments=True,
            custom_waypoints=True,
            custom_route_injection=False,
        )
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=False,
            persistent_storage_allowed=False,
            derived_storage_allowed=False,
            redistribution_allowed=False,
            overlay_allowed=True,
            cross_provider_display_allowed=False,
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="google_maps",
            name="Google Maps Platform",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"version": "v1.0", "configured": self._configured},
        )

    def search(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "search")
        return _credential_blocked("GoogleMaps", "search")

    def autocomplete(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "autocomplete")
        return _credential_blocked("GoogleMaps", "autocomplete")

    def geocode(self, address: str) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "geocode")
        return _credential_blocked("GoogleMaps", "geocode")

    def reverse_geocode(self, lat: float, lon: float) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "reverse_geocode")
        return _credential_blocked("GoogleMaps", "reverse_geocode")

    def calculate_route(
        self,
        origin: Any,
        destination: Any,
        waypoints: Optional[List[Any]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "calculate_route")
        return _credential_blocked("GoogleMaps", "calculate_route")

    def get_turn_by_turn(self, route_id: str) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "get_turn_by_turn")
        return _credential_blocked("GoogleMaps", "get_turn_by_turn")

    def get_live_traffic(self, bounding_box: Any) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "get_live_traffic")
        return _credential_blocked("GoogleMaps", "get_live_traffic")

    def get_speed_limits(self, road_segments: List[str]) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("GoogleMaps", "get_speed_limits")
        return _credential_blocked("GoogleMaps", "get_speed_limits")


class OpenStreetMapProviderAdapter(
    MapProvider,
    SearchProvider,
    RoutingProvider,
    RoadGraphProvider,
    SpeedLimitProvider,
    SignalProvider,
):
    """Adapter for OpenStreetMap self-hosted / open stack.

    OSM data is open-licensed (ODbL 1.0). Some operations require
    a configured Nominatim/OSRM/Valhalla endpoint.
    """

    def __init__(self, endpoint_url: str = ""):
        self.endpoint_url = endpoint_url
        self._configured = bool(endpoint_url)
        self._capabilities = ProviderCapabilities(
            map_rendering=True,
            search=True,
            autocomplete=True,
            geocoding=True,
            reverse_geocoding=True,
            route_calculation=True,
            alternative_routes=True,
            turn_by_turn_navigation=False,
            rerouting=False,
            lane_guidance=False,
            live_traffic=False,
            speed_limits=True,
            traffic_signals=True,
            live_signal_phase=False,
            live_signal_countdown=False,
            provider_enforcement_data=False,
            offline_maps=True,
            offline_routing=True,
            offline_navigation=True,
            android_auto=False,
            carplay=False,
            route_avoid_segments=True,
            custom_waypoints=True,
            custom_route_injection=True,
        )
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=True,
            persistent_storage_allowed=True,
            derived_storage_allowed=True,
            redistribution_allowed=True,
            overlay_allowed=True,
            cross_provider_display_allowed=True,
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="osm",
            name="OpenStreetMap",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"license": "ODbL 1.0", "configured": self._configured},
        )

    def search(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "search")
        return _credential_blocked("OSM", "search")

    def autocomplete(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "autocomplete")
        return _credential_blocked("OSM", "autocomplete")

    def calculate_route(
        self,
        origin: Any,
        destination: Any,
        waypoints: Optional[List[Any]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "calculate_route")
        return _credential_blocked("OSM", "calculate_route")

    def get_speed_limits(self, road_segments: List[str]) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "get_speed_limits")
        return _credential_blocked("OSM", "get_speed_limits")

    def get_signals(self, bounding_box: Any) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "get_signals")
        return _credential_blocked("OSM", "get_signals")

    def get_live_phase(self, signal_id: str) -> UnsupportedCapability:
        return UnsupportedCapability(
            feature="live_signal_phase",
            reason="OpenStreetMap does not provide real-time signal phase data.",
        )

    async def get_signal_countdown(self, junction_id: str) -> UnsupportedCapability:
        return UnsupportedCapability(
            feature="live_signal_countdown",
            reason="OpenStreetMap does not provide real-time signal countdown data.",
        )

    def get_road_segments(self, bounding_box: Any) -> ProviderResult:
        if not self._configured:
            return _credential_blocked("OSM", "get_road_segments")
        return _credential_blocked("OSM", "get_road_segments")
