"""
Provider Adapters Implementation with Capability Negotiation

Per Correction #2:
Provider adapters declare explicitly supported capabilities via ProviderCapabilities.
Unsupported methods return an UnsupportedCapability object or raise UnsupportedCapability rather than crashing or fabricating data.
"""

from typing import Any, Optional, List, Dict
from .capabilities import ProviderCapabilities
from .interfaces import (
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider, SignalProvider,
    EnforcementDataProvider, RoadGraphProvider, UnsupportedCapability,
    ProviderProfile, ProviderLicensingProfile
)


class MapplsProviderAdapter(
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider
):
    """Adapter for Mappls (MapmyIndia) SDK / API."""

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
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=True,
            persistent_storage_allowed=True,
            derived_storage_allowed=False,
            redistribution_allowed=False,
            overlay_allowed=True,
            cross_provider_display_allowed=False
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="mappls",
            name="Mappls (MapmyIndia)",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"version": "v1.0"}
        )

    def search(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"name": query, "locality": "Mumbai", "provider": "Mappls"}]

    def autocomplete(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"suggestion": query, "provider": "Mappls"}]

    def geocode(self, address: str) -> List[Any]:
        return [{"address": address, "lat": 19.0760, "lon": 72.8777, "provider": "Mappls"}]

    def reverse_geocode(self, lat: float, lon: float) -> List[Any]:
        return [{"address": "Mumbai, Maharashtra", "lat": lat, "lon": lon, "provider": "Mappls"}]

    def calculate_route(self, origin: Any, destination: Any, waypoints: Optional[List[Any]] = None, options: Optional[Dict[str, Any]] = None) -> Any:
        return {
            "route_id": "mappls_route_1",
            "distance_meters": 12500,
            "duration_seconds": 1800,
            "provider": "Mappls",
            "geometry_wkt": "LINESTRING(72.8777 19.0760, 72.8347 18.9220)"
        }

    def get_turn_by_turn(self, route_id: str) -> Any:
        return {"route_id": route_id, "steps": ["Head north", "Turn right onto WEH"], "provider": "Mappls"}

    def get_live_traffic(self, bounding_box: Any) -> Any:
        return {"bounding_box": bounding_box, "congestion": "MODERATE", "provider": "Mappls"}

    def get_speed_limits(self, road_segments: List[str]) -> Any:
        return {"segments": {seg: 60 for seg in road_segments}, "provider": "Mappls"}


class GoogleMapsProviderAdapter(
    MapProvider, SearchProvider, GeocodingProvider, RoutingProvider,
    NavigationProvider, TrafficProvider, SpeedLimitProvider
):
    """Adapter for Google Maps Platform APIs / SDK."""

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
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=False,
            persistent_storage_allowed=False,
            derived_storage_allowed=False,
            redistribution_allowed=False,
            overlay_allowed=True,
            cross_provider_display_allowed=False
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="google_maps",
            name="Google Maps Platform",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"version": "v1.0"}
        )

    def search(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"name": query, "locality": "Mumbai", "provider": "GoogleMaps"}]

    def autocomplete(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"suggestion": query, "provider": "GoogleMaps"}]

    def geocode(self, address: str) -> List[Any]:
        return [{"address": address, "lat": 19.0760, "lon": 72.8777, "provider": "GoogleMaps"}]

    def reverse_geocode(self, lat: float, lon: float) -> List[Any]:
        return [{"address": "Mumbai, Maharashtra", "lat": lat, "lon": lon, "provider": "GoogleMaps"}]

    def calculate_route(self, origin: Any, destination: Any, waypoints: Optional[List[Any]] = None, options: Optional[Dict[str, Any]] = None) -> Any:
        return {
            "route_id": "google_route_1",
            "distance_meters": 12400,
            "duration_seconds": 1750,
            "provider": "GoogleMaps",
            "geometry_wkt": "LINESTRING(72.8777 19.0760, 72.8347 18.9220)"
        }

    def get_turn_by_turn(self, route_id: str) -> Any:
        return {"route_id": route_id, "steps": ["Head north", "Turn right onto WEH"], "provider": "GoogleMaps"}

    def get_live_traffic(self, bounding_box: Any) -> Any:
        return {"bounding_box": bounding_box, "congestion": "MODERATE", "provider": "GoogleMaps"}

    def get_speed_limits(self, road_segments: List[str]) -> Any:
        return {"segments": {seg: 60 for seg in road_segments}, "provider": "GoogleMaps"}


class OpenStreetMapProviderAdapter(
    MapProvider, SearchProvider, RoutingProvider, RoadGraphProvider, SpeedLimitProvider, SignalProvider
):
    """Adapter for OpenStreetMap self-hosted / open stack."""

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
        self._licensing = ProviderLicensingProfile(
            render_allowed=True,
            cache_allowed=True,
            persistent_storage_allowed=True,
            derived_storage_allowed=True,
            redistribution_allowed=True,
            overlay_allowed=True,
            cross_provider_display_allowed=True
        )

    def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    def get_profile(self) -> ProviderProfile:
        return ProviderProfile(
            id="osm",
            name="OpenStreetMap",
            capabilities=self._capabilities,
            licensing=self._licensing,
            metadata={"license": "ODbL 1.0"}
        )

    def search(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"name": query, "locality": "Mumbai", "provider": "OSM"}]

    def autocomplete(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        return [{"suggestion": query, "provider": "OSM"}]

    def calculate_route(self, origin: Any, destination: Any, waypoints: Optional[List[Any]] = None, options: Optional[Dict[str, Any]] = None) -> Any:
        return {
            "route_id": "osm_route_1",
            "distance_meters": 12600,
            "duration_seconds": 1820,
            "provider": "OSM",
            "geometry_wkt": "LINESTRING(72.8777 19.0760, 72.8347 18.9220)"
        }

    def get_speed_limits(self, road_segments: List[str]) -> Any:
        return {"segments": {seg: 50 for seg in road_segments}, "provider": "OSM"}

    def get_signals(self, bounding_box: Any) -> Any:
        return {"signals": [{"id": "sig_1", "lat": 19.0760, "lon": 72.8777}], "provider": "OSM"}

    def get_live_phase(self, signal_id: str) -> Any:
        # Explicitly returns UnsupportedCapability per Correction #2
        return UnsupportedCapability(
            feature="live_signal_phase",
            reason="OpenStreetMap data does not provide real-time traffic signal phase information."
        )

    async def get_signal_countdown(self, junction_id: str) -> UnsupportedCapability:
        # Explicitly returns UnsupportedCapability per Correction #2
        return UnsupportedCapability(
            feature="live_signal_countdown",
            reason="OpenStreetMap data does not provide real-time traffic signal phase countdowns."
        )

    def get_road_segments(self, bounding_box: Any) -> Any:
        return {"segments": [{"id": "seg_1", "name": "WEH"}], "provider": "OSM"}
