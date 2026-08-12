"""Tests for speed warning logic."""

class SpeedAlerter:
    def __init__(self):
        self.hysteresis_threshold = 2
        self.is_warning_active = False

    def evaluate(self, current_speed, speed_limit, has_camera=False):
        if current_speed <= speed_limit:
            self.is_warning_active = False
            return "NO_WARNING"

        over_speed = current_speed - speed_limit

        # Hysteresis for single GPS spike could be implemented with historical smoothing,
        # here we simulate the output based on current state and threshold.

        if over_speed <= 5:
            self.is_warning_active = True
            return "SUBTLE_WARNING"
        elif over_speed <= 15:
            self.is_warning_active = True
            return "STRONG_WARNING"
        else:
            self.is_warning_active = True
            return "SEVERE_WARNING_VOICE_HAPTIC"

def test_below_limit():
    alerter = SpeedAlerter()
    assert alerter.evaluate(50, 60) == "NO_WARNING"

def test_at_limit():
    alerter = SpeedAlerter()
    assert alerter.evaluate(60, 60) == "NO_WARNING"

def test_slight_overspeed():
    alerter = SpeedAlerter()
    assert alerter.evaluate(65, 60) == "SUBTLE_WARNING"

def test_severe_overspeed():
    alerter = SpeedAlerter()
    assert alerter.evaluate(85, 60) == "SEVERE_WARNING_VOICE_HAPTIC"

def test_no_camera_warns():
    alerter = SpeedAlerter()
    assert alerter.evaluate(70, 60, has_camera=False) == "STRONG_WARNING"
