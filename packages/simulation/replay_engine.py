"""GPS Replay Engine for testing."""
import json
import asyncio
from typing import List, Optional, AsyncGenerator, Dict, Any
from datetime import datetime, timedelta
import random
from packages.domain_models.location import RawLocationSample


class GPSReplayEngine:
    """Replays GPS traces with noise and dropout simulation."""

    def __init__(self):
        self.trace: List[Dict[str, Any]] = []
        self.playback_speed: float = 1.0
        self.is_paused: bool = False
        self.noise_config = {
            "accuracy_degradation": 5.0,  # meters
            "heading_jitter": 0.0,        # degrees
            "speed_noise": 0.0            # km/h
        }
        self.dropout_config = {
            "active": False,
            "duration": 0,
            "start_index": -1
        }
        self.current_index = 0

    def load_json_trace(self, file_path: str):
        """Load a trace from a JSON file."""
        with open(file_path, 'r') as f:
            self.trace = json.load(f)
        self.current_index = 0

    def load_synthetic_trace(self, trace: List[Dict[str, Any]]):
        """Load a trace generated synthetically."""
        self.trace = trace
        self.current_index = 0

    def set_playback_speed(self, speed: float):
        """Set playback speed (e.g., 0.5x to 10x)."""
        self.playback_speed = max(0.1, min(10.0, speed))

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def jump_to(self, index: int):
        if 0 <= index < len(self.trace):
            self.current_index = index

    def set_noise(self, accuracy_degradation: float = 5.0, heading_jitter: float = 0.0, speed_noise: float = 0.0):
        self.noise_config = {
            "accuracy_degradation": accuracy_degradation,
            "heading_jitter": heading_jitter,
            "speed_noise": speed_noise
        }

    def simulate_dropout(self, duration_seconds: int, start_index: int = None):
        """Simulate a GPS dropout (e.g., in a tunnel)."""
        self.dropout_config = {
            "active": True,
            "duration": duration_seconds,
            "start_index": start_index if start_index is not None else self.current_index
        }

    def _apply_noise(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply configured noise to a GPS sample."""
        noisy = dict(sample)
        if "accuracy" in noisy:
            noisy["accuracy"] += random.uniform(0, self.noise_config["accuracy_degradation"])
        if "heading" in noisy and self.noise_config["heading_jitter"] > 0:
            noisy["heading"] = (noisy["heading"] + random.uniform(-self.noise_config["heading_jitter"], self.noise_config["heading_jitter"])) % 360
        if "speed" in noisy and self.noise_config["speed_noise"] > 0:
            noisy["speed"] = max(0, noisy["speed"] + random.uniform(-self.noise_config["speed_noise"], self.noise_config["speed_noise"]))
        return noisy

    async def stream(self) -> AsyncGenerator[RawLocationSample, None]:
        """Stream the GPS trace as RawLocationSample objects."""
        last_timestamp = None
        dropout_end_time = None

        while self.current_index < len(self.trace):
            while self.is_paused:
                await asyncio.sleep(0.1)

            sample_dict = self.trace[self.current_index]
            current_timestamp = datetime.fromisoformat(sample_dict["timestamp"])

            if self.dropout_config["active"] and self.current_index == self.dropout_config["start_index"]:
                dropout_end_time = current_timestamp + timedelta(seconds=self.dropout_config["duration"])
                self.dropout_config["active"] = False

            if dropout_end_time and current_timestamp < dropout_end_time:
                # Skip sample due to dropout
                self.current_index += 1
                continue
            
            dropout_end_time = None # Dropout over

            if last_timestamp:
                delta = (current_timestamp - last_timestamp).total_seconds()
                sleep_time = delta / self.playback_speed
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            noisy_dict = self._apply_noise(sample_dict)
            
            sample = RawLocationSample(
                latitude=noisy_dict["latitude"],
                longitude=noisy_dict["longitude"],
                altitude=noisy_dict.get("altitude"),
                accuracy=noisy_dict.get("accuracy", 10.0),
                heading=noisy_dict.get("heading"),
                speed=noisy_dict.get("speed"),
                timestamp=current_timestamp,
                provider="replay_engine"
            )
            
            yield sample
            
            last_timestamp = current_timestamp
            self.current_index += 1
