"""Trace Generator for Synthetic City."""
from datetime import datetime, timedelta
from typing import Any, Dict, List


class TraceGenerator:
    """Generates GPS traces for testing various scenarios."""

    def _create_sample(self, lat, lon, speed, heading, time_offset_sec) -> Dict[str, Any]:
        base_time = datetime(2026, 1, 1, 10, 0, 0)
        ts = base_time + timedelta(seconds=time_offset_sec)
        return {
            "latitude": lat,
            "longitude": lon,
            "speed": speed,
            "heading": heading,
            "accuracy": 5.0,
            "timestamp": ts.isoformat(),
            "synthetic": True
        }

    def generate_highway_pass(self) -> List[Dict[str, Any]]:
        """Trace driving north on highway past cameras (0 heading)."""
        trace = []
        lat = 12.960
        lon = 77.594
        for i in range(120):
            lat += 0.0001
            trace.append(self._create_sample(lat, lon, 60, 0, i))
        return trace

    def generate_opposite_direction(self) -> List[Dict[str, Any]]:
        """Trace driving south past north-facing camera."""
        trace = []
        lat = 12.980
        lon = 77.594
        for i in range(120):
            lat -= 0.0001
            trace.append(self._create_sample(lat, lon, 60, 180, i))
        return trace

    def generate_flyover_pass(self) -> List[Dict[str, Any]]:
        """Trace on flyover (should avoid surface camera)."""
        trace = []
        lat = 12.970
        lon = 77.595
        for i in range(60):
            lat += 0.0001
            sample = self._create_sample(lat, lon, 50, 0, i)
            sample["altitude"] = 900 # Elevated
            trace.append(sample)
        return trace

    def generate_restricted_turn(self) -> List[Dict[str, Any]]:
        """Trace approaching no-left junction."""
        return [self._create_sample(12.974, 77.595, 30, 90, i) for i in range(10)]

    def generate_speed_transition(self) -> List[Dict[str, Any]]:
        """Trace crossing 60->40 zone."""
        trace = []
        for i in range(10):
            trace.append(self._create_sample(12.976, 77.596, 60, 0, i))
        for i in range(10, 20):
            trace.append(self._create_sample(12.977, 77.596, 40, 0, i))
        return trace

    def generate_stationary_near_camera(self) -> List[Dict[str, Any]]:
        """5 minutes stopped near a camera."""
        return [self._create_sample(12.971, 77.594, 0, 0, i) for i in range(300)]

    def generate_gps_drift(self) -> List[Dict[str, Any]]:
        """Trace with oscillating GPS accuracy."""
        trace = []
        for i in range(60):
            acc = 5.0 + (i % 10) * 5
            sample = self._create_sample(12.970, 77.594, 40, 0, i)
            sample["accuracy"] = acc
            trace.append(sample)
        return trace
