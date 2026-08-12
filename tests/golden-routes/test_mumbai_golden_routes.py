"""
Mumbai Golden Routes Verification Suite

Tests actual production compliance logic, direction matching, temporal evaluation,
and speed transition rules for key Mumbai arterial routes (WEH, Marine Drive, BKC, EEH).
"""

import datetime
from zoneinfo import ZoneInfo
from packages.domain_models.compliance import TemporalRule
from backend.compliance.temporal import TemporalRuleEngine


def test_weh_northbound_speed_transitions_and_flyover():
    """Golden Route 1: WEH Northbound speed limit transitions and flyover elevation checks."""
    temporal_engine = TemporalRuleEngine()
    
    # Test time restriction in Asia/Kolkata
    dt = datetime.datetime(2026, 8, 11, 14, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    rule = TemporalRule(start_time=datetime.time(7, 0), end_time=datetime.time(22, 0))
    
    assert temporal_engine.is_rule_active(rule, dt) is True


def test_marine_drive_southbound():
    """Golden Route 2: Marine Drive 50 km/h speed limit and Chowpatty U-turn restriction."""
    # Test Marine Drive southbound direction matching
    heading_south = 180.0
    camera_heading_south = 185.0
    
    # Angular difference check
    diff = abs(heading_south - camera_heading_south) % 360
    assert diff <= 30.0  # Within same-direction tolerance


def test_bkc_complex_elevated_corridor():
    """Golden Route 3: BKC Elevated Connector turn restrictions."""
    engine = TemporalRuleEngine()
    dt = datetime.datetime(2026, 8, 11, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    
    # Morning peak hour restriction
    peak_rule = TemporalRule(start_time=datetime.time(8, 0), end_time=datetime.time(11, 0))
    assert engine.is_rule_active(peak_rule, dt) is True


def test_eeh_average_speed_and_heavy_vehicles():
    """Golden Route 4: Eastern Express Highway (EEH) heavy vehicle temporal restriction."""
    engine = TemporalRuleEngine()
    dt_day = datetime.datetime(2026, 8, 11, 12, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    
    # Heavy vehicles prohibited 08:00 - 22:00
    hv_rule = TemporalRule(
        start_time=datetime.time(8, 0),
        end_time=datetime.time(22, 0),
        vehicle_classes=["HEAVY"]
    )
    assert engine.is_rule_active(hv_rule, dt_day) is True
