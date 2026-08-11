"""
Provider Capability Contract Tests

Per Correction #2:
Verifies that:
- Every provider adapter explicitly declares supported capabilities via ProviderCapabilities
- Unsupported methods return an UnsupportedCapability instance rather than crashing or fabricating data
- Provider capabilities match expected configurations for Mappls, Google, and OSM adapters
"""

import pytest
from packages.provider-contracts.capabilities import ProviderCapabilities
from packages.provider-contracts.interfaces import UnsupportedCapability
from packages.provider-contracts.adapters import (
    MapplsProviderAdapter,
    GoogleMapsProviderAdapter,
    OpenStreetMapProviderAdapter
)


def test_mappls_provider_capabilities():
    adapter = MapplsProviderAdapter(api_key="test_key", client_id="cid", client_secret="secret")
    caps = adapter.get_capabilities()

    assert isinstance(caps, ProviderCapabilities)
    assert caps.map_rendering is True
    assert caps.search is True
    assert caps.route_calculation is True
    assert caps.turn_by_turn_navigation is True
    assert caps.live_traffic is True
    assert caps.offline_maps is True
    assert caps.traffic_signals is False
    assert caps.live_signal_countdown is False


def test_google_maps_provider_capabilities():
    adapter = GoogleMapsProviderAdapter(api_key="test_key")
    caps = adapter.get_capabilities()

    assert isinstance(caps, ProviderCapabilities)
    assert caps.map_rendering is True
    assert caps.search is True
    assert caps.route_calculation is True
    assert caps.turn_by_turn_navigation is True
    assert caps.offline_maps is False  # Google Maps SDK prohibits caching offline maps per terms
    assert caps.traffic_signals is False


def test_osm_provider_capabilities():
    adapter = OpenStreetMapProviderAdapter(endpoint_url="http://localhost:5000")
    caps = adapter.get_capabilities()

    assert isinstance(caps, ProviderCapabilities)
    assert caps.map_rendering is True
    assert caps.route_calculation is True
    assert caps.traffic_signals is True
    assert caps.custom_route_injection is True
    assert caps.turn_by_turn_navigation is False


@pytest.mark.asyncio
async def test_unsupported_capability_return():
    adapter = OpenStreetMapProviderAdapter(endpoint_url="http://localhost:5000")
    result = await adapter.get_signal_countdown("junction_123")

    assert isinstance(result, UnsupportedCapability)
    assert result.feature == "live_signal_countdown"
    assert "OpenStreetMap" in result.reason
