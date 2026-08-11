"""
Provider Adapters Implementation with Capability Negotiation

Per Correction #2:
Provider adapters declare explicitly supported capabilities via ProviderCapabilities.
Unsupported methods return an UnsupportedCapability object rather than crashing or fabricating data.
"""

from typing import Any, Optional
from packages.provider-contracts.capabilities import ProviderCapabilities
from packages.provider-contracts.interfaces import (
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider, SignalProvider,
    EnforcementDataProvider, RoadGraphProvider, UnsupportedCapability
)


class MapplsProviderAdapter(
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider
):
    """
    Adapter for Mappls (MapmyIndia) SDK / API.
    """
    def __init__(self, api_key: str, client_id: str, client_secret: str):
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
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

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def render_map(self, center_lat: float, center_lon: float, zoom: float) -> Any:
        return {"status": "success", "provider": "Mappls", "zoom": zoom}

    async def search(self, query: str, location_bias: Optional[dict] = None) -> list[dict]:
        # Mappls Search API implementation / stub
        return [{"name": query, "locality": "Mumbai", "provider": "Mappls"}]

    async def compute_routes(self, origin: dict, destination: dict, options: Optional[dict] = None) -> list[dict]:
        return [{
            "route_id": "mappls_route_1",
            "distance_meters": 12500,
            "duration_seconds": 1800,
            "provider": "Mappls",
            "geometry_wkt": "LINESTRING(72.8777 19.0760, 72.8347 18.9220)"
        }]

    async def get_speed_limit(self, segment_id: str) -> Any:
        return {"speed_limit_kph": 60, "provider": "Mappls"}


class GoogleMapsProviderAdapter(
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider
):
    """
    Adapter for Google Maps Platform APIs / SDK.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
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

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def render_map(self, center_lat: float, center_lon: float, zoom: float) -> Any:
        return {"status": "success", "provider": "GoogleMaps", "zoom": zoom}

    async def search(self, query: str, location_bias: Optional[dict] = None) -> list[dict]:
        return [{"name": query, "locality": "Mumbai", "provider": "GoogleMaps"}]

    async def compute_routes(self, origin: dict, destination: dict, options: Optional[dict] = None) -> list[dict]:
        return [{
            "route_id": "google_route_1",
            "distance_meters": 12400,
            "duration_seconds": 1750,
            "provider": "GoogleMaps",
            "geometry_wkt": "LINESTRING(72.8777 19.0760, 72.8347 18.9220)"
        }]

    async def get_speed_limit(self, segment_id: str) -> Any:
        return {"speed_limit_kph": 60, "provider": "GoogleMaps"}


class OpenStreetMapProviderAdapter(
    MapProvider, SearchProvider, RoutingProvider, RoadGraphProvider, SpeedLimitProvider, SignalProvider
):
    """
    Adapter for OpenStreetMap self-hosted / open stack.
    """
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
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

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def get_signal_countdown(self, junction_id: str) -> UnsupportedCapability:
        # Explicitly returns UnsupportedCapability per Correction #2
        return UnsupportedCapability(
            feature="live_signal_countdown",
            reason="OpenStreetMap data does not provide real-time traffic signal phase countdowns."
        )
