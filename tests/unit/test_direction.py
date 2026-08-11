"""Tests for direction math."""
import pytest


def get_heading_diff(h1, h2):
    diff = abs(h1 - h2)
    return min(diff, 360 - diff)


def test_same_direction():
    assert get_heading_diff(10, 10) == 0
    assert get_heading_diff(350, 10) == 20
    assert get_heading_diff(10, 350) == 20


def test_opposite_direction():
    assert get_heading_diff(0, 180) == 180
    assert get_heading_diff(90, 270) == 180


def test_tolerance():
    tolerance = 60
    assert get_heading_diff(0, 45) <= tolerance
    assert get_heading_diff(0, 135) > tolerance
