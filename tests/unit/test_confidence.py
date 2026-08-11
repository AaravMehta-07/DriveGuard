"""Tests for confidence scoring."""
import pytest
from packages.domain_models.sources import SourceConfidenceLevel

def calculate_confidence(sources):
    score = 0
    for source in sources:
        if source == SourceConfidenceLevel.OFFICIAL_AUTHORITY:
            score += 90
        elif source == SourceConfidenceLevel.MULTI_SOURCE_CONFIRMED:
            score += 70
        elif source == SourceConfidenceLevel.MULTIPLE_COMMUNITY_REPORTS:
            score += 50
        elif source == SourceConfidenceLevel.SINGLE_COMMUNITY_REPORT:
            score += 20
        elif source == SourceConfidenceLevel.OSM:
            score += 30
    return min(100, score)

def test_single_official():
    assert calculate_confidence([SourceConfidenceLevel.OFFICIAL_AUTHORITY]) == 90

def test_single_community():
    assert calculate_confidence([SourceConfidenceLevel.SINGLE_COMMUNITY_REPORT]) == 20

def test_multiple_community_plus_osm():
    score = calculate_confidence([SourceConfidenceLevel.MULTIPLE_COMMUNITY_REPORTS, SourceConfidenceLevel.OSM])
    assert score == 80
