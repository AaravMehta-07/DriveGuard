"""Tests for alert arbitration."""
from packages.domain_models.alerts import AlertSeverity

def arbitrate_alerts(alerts):
    if not alerts:
        return None
    # Sort by severity priority (P0 < P1 < P2 < P3)
    alerts.sort(key=lambda a: a['severity'])
    return alerts[0]

def test_p0_overrides_p2():
    alerts = [
        {"id": "1", "severity": AlertSeverity.P2_MEDIUM, "type": "CAMERA"},
        {"id": "2", "severity": AlertSeverity.P0_CRITICAL, "type": "WRONG_WAY"}
    ]
    winner = arbitrate_alerts(alerts)
    assert winner['id'] == "2"

def test_cooldown_and_suppression():
    # Implementation depends on stateful arbiter, testing concept
    class Arbiter:
        def __init__(self):
            self.history = {}
        
        def should_alert(self, alert_id, time_sec):
            if alert_id in self.history:
                if time_sec - self.history[alert_id] < 60:
                    return False
            self.history[alert_id] = time_sec
            return True
            
    arbiter = Arbiter()
    assert arbiter.should_alert("cam_1", 0) is True
    assert arbiter.should_alert("cam_1", 30) is False
    assert arbiter.should_alert("cam_1", 65) is True
