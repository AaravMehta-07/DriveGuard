"""Synthetic City Generator."""
import random
from datetime import datetime
from typing import Any, Dict

from packages.domain_models.compliance import ComplianceRule, RuleType, TemporalRule
from packages.domain_models.enforcement import (
    ActiveStatus,
    Carriageway,
    EnforcementPoint,
    EnforcementType,
    FixedOrMobile,
    StructureType,
    VerificationStatus,
)
from packages.domain_models.signals import TrafficSignalJunction


class SyntheticCityGenerator:
    """Generates a deterministic synthetic test city."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.data = {
            "enforcement_points": [],
            "compliance_rules": [],
            "signals": [],
            "metadata": {"synthetic": True}
        }

    def generate(self) -> Dict[str, Any]:
        """Generate the complete city."""
        self._generate_highway()
        self._generate_surface_road()
        self._generate_cameras()
        self._generate_signals()
        self._generate_rules()
        return self.data

    def _generate_highway(self):
        """Generate north-south highway (60 kph)."""
        rule = ComplianceRule(
            id="rule_hw_speed",
            rule_type=RuleType.SPEED_LIMIT,
            description="60 kph limit on highway",
            metadata={"synthetic": True, "speed_limit": 60}
        )
        self.data["compliance_rules"].append(rule)

    def _generate_surface_road(self):
        """Generate east-west surface road (50 kph)."""
        rule = ComplianceRule(
            id="rule_surface_speed",
            rule_type=RuleType.SPEED_LIMIT,
            description="50 kph limit on surface road",
            metadata={"synthetic": True, "speed_limit": 50}
        )
        self.data["compliance_rules"].append(rule)

    def _generate_cameras(self):
        """Generate test speed cameras."""
        cameras = [
            EnforcementPoint(
                id="cam_highway_north",
                type=EnforcementType.FIXED_SPEED,
                verification_status=VerificationStatus.VERIFIED,
                active_status=ActiveStatus.ACTIVE,
                fixed_or_mobile=FixedOrMobile.FIXED,
                latitude=12.971,
                longitude=77.594,
                heading=0, # North
                structure_type=StructureType.SURFACE,
                carriageway=Carriageway.MAIN,
                speed_limit=60,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                metadata={"synthetic": True}
            ),
            EnforcementPoint(
                id="cam_highway_south",
                type=EnforcementType.FIXED_SPEED,
                verification_status=VerificationStatus.VERIFIED,
                active_status=ActiveStatus.ACTIVE,
                fixed_or_mobile=FixedOrMobile.FIXED,
                latitude=12.972,
                longitude=77.594,
                heading=180, # South
                structure_type=StructureType.SURFACE,
                carriageway=Carriageway.MAIN,
                speed_limit=60,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                metadata={"synthetic": True}
            ),
            EnforcementPoint(
                id="cam_under_flyover",
                type=EnforcementType.RED_LIGHT,
                verification_status=VerificationStatus.VERIFIED,
                active_status=ActiveStatus.ACTIVE,
                fixed_or_mobile=FixedOrMobile.FIXED,
                latitude=12.975,
                longitude=77.595,
                structure_type=StructureType.SURFACE, # Under flyover
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                metadata={"synthetic": True, "note": "Camera is under flyover"}
            ),
             EnforcementPoint(
                id="cam_service_road",
                type=EnforcementType.FIXED_SPEED,
                verification_status=VerificationStatus.VERIFIED,
                active_status=ActiveStatus.ACTIVE,
                fixed_or_mobile=FixedOrMobile.FIXED,
                latitude=12.978,
                longitude=77.596,
                structure_type=StructureType.SURFACE,
                carriageway=Carriageway.SERVICE,
                speed_limit=40,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                metadata={"synthetic": True}
            )
        ]
        self.data["enforcement_points"].extend(cameras)

    def _generate_signals(self):
        """Generate traffic signals."""
        signals = [
            TrafficSignalJunction(
                id="sig_1",
                latitude=12.975,
                longitude=77.595,
                has_red_light_camera=True,
                metadata={"synthetic": True}
            )
        ]
        self.data["signals"].extend(signals)

    def _generate_rules(self):
        """Generate turn and temporal restrictions."""
        # Timed no-entry
        rule_timed = ComplianceRule(
            id="rule_timed_no_entry",
            rule_type=RuleType.NO_ENTRY,
            temporal_rules=[
                TemporalRule(
                    start_time=datetime.strptime("07:00", "%H:%M").time(),
                    end_time=datetime.strptime("10:00", "%H:%M").time()
                )
            ],
            metadata={"synthetic": True}
        )
        self.data["compliance_rules"].append(rule_timed)
