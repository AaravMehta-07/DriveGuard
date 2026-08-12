"""
Abuse Detector for identifying malicious reporting behavior.
"""

from enum import Enum
from typing import Any, Dict, List


class AbuseFlag(str, Enum):
    GPS_SPOOFING = "GPS_SPOOFING"
    MASS_REPORTS = "MASS_REPORTS"
    COORDINATE_PATTERN = "COORDINATE_PATTERN"
    ACCOUNT_ABUSE = "ACCOUNT_ABUSE"

class AbuseDetector:
    """
    Detects abusive behavior from reporters.
    """

    async def check_report_for_abuse(self, report: Dict[str, Any], reporter: Dict[str, Any], recent_history: List[Dict[str, Any]]) -> List[AbuseFlag]:
        """
        Check an incoming report and reporter history for abuse patterns.
        """
        flags = []

        # GPS spoofing detection: speed > 300km/h or coordinates not on road
        speed_kmh = report.get("speed_from_last_report_kmh", 0)
        if speed_kmh > 300:
            flags.append(AbuseFlag.GPS_SPOOFING)

        if not report.get("is_on_road", True):
            flags.append(AbuseFlag.GPS_SPOOFING)

        # Mass report detection: >10 in 1 hour
        reports_last_hour = len([r for r in recent_history if r.get("age_hours", 0) <= 1])
        if reports_last_hour > 10:
            flags.append(AbuseFlag.MASS_REPORTS)

        # Account abuse: new account + high report volume
        is_new = reporter.get("account_age_days", 0) < 7
        if is_new and len(recent_history) > 20:
            flags.append(AbuseFlag.ACCOUNT_ABUSE)

        # Coordinate suspicious patterns (simplified check for perfect grid/same road)
        if report.get("matches_suspicious_pattern", False):
            flags.append(AbuseFlag.COORDINATE_PATTERN)

        return flags

    async def check_confirmation_for_abuse(self, confirmation: Dict[str, Any], user: Dict[str, Any]) -> List[AbuseFlag]:
        """
        Check if a user is abusively confirming/rejecting reports.
        """
        flags = []
        if user.get("rapid_confirmations_flag", False):
            flags.append(AbuseFlag.MASS_REPORTS)
        return flags
