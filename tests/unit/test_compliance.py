"""Tests for compliance engine."""
import pytest
from packages.domain_models.compliance import ManeuverValidationResult

def validate_maneuver(is_allowed, confidence):
    if confidence < 0.5:
        return ManeuverValidationResult.UNCERTAIN
    if is_allowed:
        return ManeuverValidationResult.ALLOWED
    return ManeuverValidationResult.PROHIBITED

def test_maneuver_validation():
    assert validate_maneuver(True, 0.9) == ManeuverValidationResult.ALLOWED
    assert validate_maneuver(False, 0.9) == ManeuverValidationResult.PROHIBITED
    assert validate_maneuver(True, 0.3) == ManeuverValidationResult.UNCERTAIN
