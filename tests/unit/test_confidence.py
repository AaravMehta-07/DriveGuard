"""Tests for confidence scoring."""
import pytest
from packages.domain_models.sources import SourceConfidenceLevel
from backend.compliance.confidence import SourceConfidenceEngine

def test_single_official():
    engine = SourceConfidenceEngine()
    # OFFICIAL_AUTHORITY base is 1.0. With dir_accuracy 1.0, score = 1.0 * (0.8 + 0.2*1.0) = 1.0
    score = engine.calculate_confidence(["OFFICIAL_AUTHORITY"], 1, 0, 0, 1.0)
    assert score == 1.0

def test_single_community():
    engine = SourceConfidenceEngine()
    # SINGLE_COMMUNITY_REPORT base is 0.2. score = 0.2 * 1.0 = 0.2
    score = engine.calculate_confidence(["SINGLE_COMMUNITY_REPORT"], 1, 0, 0, 1.0)
    assert pytest.approx(score) == 0.2

def test_multiple_community_plus_osm():
    engine = SourceConfidenceEngine()
    # OSM is 0.65, MULTIPLE is 0.5. Max is 0.65. Cross-source bonus +0.1 = 0.75.
    score = engine.calculate_confidence(["MULTIPLE_COMMUNITY_REPORTS", "OSM"], 2, 0, 0, 1.0)
    assert pytest.approx(score) == 0.75
