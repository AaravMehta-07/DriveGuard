"""Capabilities models."""
from pydantic import BaseModel


class ProviderCapabilities(BaseModel):
    """Boolean capability flags for a map/routing provider."""
    map_rendering: bool = False
    search: bool = False
    autocomplete: bool = False
    geocoding: bool = False
    reverse_geocoding: bool = False
    route_calculation: bool = False
    alternative_routes: bool = False
    turn_by_turn_navigation: bool = False
    rerouting: bool = False
    lane_guidance: bool = False
    live_traffic: bool = False
    speed_limits: bool = False
    traffic_signals: bool = False
    live_signal_phase: bool = False
    live_signal_countdown: bool = False
    provider_enforcement_data: bool = False
    offline_maps: bool = False
    offline_routing: bool = False
    offline_navigation: bool = False
    android_auto: bool = False
    carplay: bool = False
    route_avoid_segments: bool = False
    custom_waypoints: bool = False
    custom_route_injection: bool = False
