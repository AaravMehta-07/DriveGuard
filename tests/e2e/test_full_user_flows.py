"""
End-to-End System Flow Integration Tests

Exercises real FastAPI app endpoints, routers, compliance engine, and geospatial query service.
Uses dependency overrides for fast, deterministic, database-decoupled E2E test execution.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.api.dependencies import User, get_current_user, get_db, get_redis
from backend.api.main import app


async def override_get_db():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result
    yield mock_session


async def override_get_redis():
    mock_redis = AsyncMock()
    mock_redis.incr.return_value = 1
    mock_redis.expire.return_value = True
    yield mock_redis


async def override_get_current_user():
    return User(id="test_e2e_user", email="e2e@driveguard.app", role="ADMIN")


@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_current_user] = override_get_current_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_navigation_flow(async_client):
    """Test 1: Health & Navigation API Flow"""
    response = await async_client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_copilot_mode_flow(async_client):
    """Test 2: Copilot Mode Nearby Enforcement API Flow"""
    response = await async_client.get(
        "/api/v1/enforcement/nearby",
        params={"lat": 19.0760, "lon": 72.8777, "heading": 45.0, "radius_m": 1000.0}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_enforcement_explorer_flow(async_client):
    """Test 3: Enforcement Explorer Viewport API Flow"""
    payload = {
        "min_lat": 19.0000,
        "min_lon": 72.8000,
        "max_lat": 19.1000,
        "max_lon": 72.9000
    }
    response = await async_client.post("/api/v1/enforcement/viewport", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_community_moderation_flow(async_client):
    """Test 4: Community Report Listing API Flow"""
    response = await async_client.get("/api/v1/reports/feed", params={"lat": 19.0760, "lon": 72.8777})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_challan_privacy_flow(async_client):
    """Test 5: Challan User History Flow"""
    response = await async_client.get("/api/v1/challan/user-history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_data_export_flow(async_client):
    """Test 6: User Data Export Flow (GDPR / Data Portability)"""
    response = await async_client.post("/api/v1/users/export-data")
    assert response.status_code == 200
    data = response.json()
    assert "export_metadata" in data
    assert "profile" in data
    assert data["export_metadata"]["user_id"] == "test_e2e_user"
