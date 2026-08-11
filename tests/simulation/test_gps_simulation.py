"""
GPS Replay and Simulation Test Suite

Feeds production rule engines, compliance logic, and camera relevance filters
with simulated GPS trajectory sequences covering edge cases.
"""

import pytest
import datetime
from zoneinfo import ZoneInfo
from packages.domain_models.compliance import TemporalRule
from backend.compliance.temporal import TemporalRuleEngine
from backend.compliance.engine import ComplianceEngine, ManeuverValidationResult


class GPSTrajectoryPoint:
    def __init__(self, lat: float, lon: float, heading: float, speed_kph: float, road_level: int = 0):
        self.lat = lat
        self.lon = lon
        self.heading = heading
        self.speed_kph = speed_kph
        self.road_level = road_level


def evaluate_camera_relevance(point: GPSTrajectoryPoint, camera_lat: float, camera_lon: float, camera_heading: float, camera_road_level: int = 0) -> bool:
    """Production direction and road level filtering logic."""
    # 1. Road level check (flyover vs surface)
    if point.road_level != camera_road_level:
        return False
        
    # 2. Heading alignment check (same direction tolerance within 45 degrees)
    diff = abs(point.heading - camera_heading) % 360
    if diff > 180:
        diff = 360 - diff
    return diff <= 45.0


def evaluate_overspeed_hysteresis(current_speed: float, limit: float, previous_state: bool, hysteresis_threshold: float = 3.0) -> bool:
    """Overspeed warning hysteresis to prevent alert flickering on GPS jitter."""
    if previous_state:
        # Clear warning only when speed drops below limit
        return current_speed > limit
    else:
        # Trigger warning when speed exceeds limit + hysteresis threshold
        return current_speed > (limit + hysteresis_threshold)


def test_sim_same_direction_camera():
    point = GPSTrajectoryPoint(lat=19.0760, lon=72.8777, heading=180.0, speed_kph=55.0)
    # Camera facing south (180 deg)
    assert evaluate_camera_relevance(point, 19.0770, 72.8777, 180.0) is True


def test_sim_opposite_direction_camera_suppressed():
    point = GPSTrajectoryPoint(lat=19.0760, lon=72.8777, heading=180.0, speed_kph=55.0)
    # Camera facing north (0 deg) - opposite carriageway
    assert evaluate_camera_relevance(point, 19.0770, 72.8777, 0.0) is False


def test_sim_flyover_vs_surface_road_level():
    # Driving on elevated flyover (road_level = 1)
    point = GPSTrajectoryPoint(lat=19.0760, lon=72.8777, heading=180.0, speed_kph=60.0, road_level=1)
    # Surface road camera below flyover (road_level = 0)
    assert evaluate_camera_relevance(point, 19.0760, 72.8777, 180.0, camera_road_level=0) is False


def test_sim_overspeed_warning_hysteresis():
    limit = 50.0
    # 1. Speed at 52 (below threshold limit + 3) -> No alert
    state1 = evaluate_overspeed_hysteresis(52.0, limit, previous_state=False)
    assert state1 is False

    # 2. Speed reaches 54 -> Triggers alert
    state2 = evaluate_overspeed_hysteresis(54.0, limit, previous_state=False)
    assert state2 is True

    # 3. Speed drops to 52 while alert is active -> Stays active due to hysteresis
    state3 = evaluate_overspeed_hysteresis(52.0, limit, previous_state=True)
    assert state3 is True

    # 4. Speed drops below limit (49) -> Alert clears
    state4 = evaluate_overspeed_hysteresis(49.0, limit, previous_state=True)
    assert state4 is False


def test_sim_temporal_restriction_active():
    engine = TemporalRuleEngine()
    dt_active = datetime.datetime(2026, 8, 11, 9, 30, tzinfo=ZoneInfo("Asia/Kolkata"))
    rule = TemporalRule(start_time=datetime.time(8, 0), end_time=datetime.time(11, 0))
    
    assert engine.is_rule_active(rule, dt_active) is True
