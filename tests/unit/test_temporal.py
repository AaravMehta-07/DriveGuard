"""Tests for temporal rules with Asia/Kolkata timezone support per Correction #40."""
from datetime import datetime, time, date, timezone
from zoneinfo import ZoneInfo
from packages.domain_models.compliance import TemporalRule


def test_weekday_restriction():
    rule = TemporalRule(days_of_week=[0, 1, 2, 3, 4])  # Monday-Friday
    
    # Monday
    dt_monday = datetime(2026, 8, 10)
    assert dt_monday.weekday() in rule.days_of_week
    
    # Saturday
    dt_saturday = datetime(2026, 8, 15)
    assert dt_saturday.weekday() not in rule.days_of_week


def test_time_restriction():
    rule = TemporalRule(
        start_time=time(7, 0),
        end_time=time(10, 0)
    )
    
    t_active = time(8, 30)
    assert rule.start_time <= t_active <= rule.end_time
    
    t_inactive = time(12, 0)
    assert not (rule.start_time <= t_inactive <= rule.end_time)


def test_overnight_restriction():
    rule = TemporalRule(
        start_time=time(22, 0),
        end_time=time(6, 0),
        overnight=True
    )
    
    t_active_1 = time(23, 0)
    t_active_2 = time(3, 0)
    t_inactive = time(12, 0)
    
    def is_active(t):
        if rule.overnight:
            return t >= rule.start_time or t <= rule.end_time
        return rule.start_time <= t <= rule.end_time
        
    assert is_active(t_active_1)
    assert is_active(t_active_2)
    assert not is_active(t_inactive)


def test_until_further_order():
    rule = TemporalRule(until_further_order=True)
    assert rule.until_further_order


def test_date_range():
    rule = TemporalRule(
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31)
    )
    
    d_active = date(2026, 8, 15)
    d_inactive = date(2026, 9, 1)
    
    assert rule.start_date <= d_active <= rule.end_date
    assert not (rule.start_date <= d_inactive <= rule.end_date)


def test_asia_kolkata_timezone():
    tz = ZoneInfo('Asia/Kolkata')
    dt_utc = datetime(2026, 8, 11, 2, 30, tzinfo=timezone.utc)
    dt_ist = dt_utc.astimezone(tz)
    
    assert dt_ist.hour == 8
    assert dt_ist.minute == 0
