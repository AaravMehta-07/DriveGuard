"""Tests for compliance engine."""
import pytest
from datetime import datetime
from backend.compliance.engine import ComplianceEngine

@pytest.mark.asyncio
async def test_maneuver_validation():
    engine = ComplianceEngine(geo_query_service=None)
    dt = datetime(2026, 8, 11, 10, 0)
    
    # Without geo_service, should return UNCERTAIN
    res = await engine.validate_maneuver("j1", "s1", "s2", "PRIVATE_CAR", dt)
    assert res.status == "UNCERTAIN"
    
    class MockGeo:
        class MockDB:
            def text(self, q): return q
            async def execute(self, q, p=None):
                class MockResult:
                    def mappings(self):
                        class MockMappings:
                            def all(self):
                                return [{"restriction_type": "NO_RIGHT_TURN", "vehicle_types": ["PRIVATE_CAR"]}]
                        return MockMappings()
                return MockResult()
        _db = MockDB()
        
    engine = ComplianceEngine(geo_query_service=MockGeo())
    res = await engine.validate_maneuver("j1", "s1", "s2", "PRIVATE_CAR", dt)
    assert res.status == "PROHIBITED"
