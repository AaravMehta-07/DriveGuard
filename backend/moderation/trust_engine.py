"""
Reporter Trust Engine for evaluating community user trustworthiness.
"""

from enum import Enum
from typing import Dict, Any, List

class AbuseType(str, Enum):
    GPS_SPOOFING = "GPS_SPOOFING"
    MASS_REPORTS = "MASS_REPORTS"
    BRIGADING = "BRIGADING"
    DUPLICATE_ACCOUNT = "DUPLICATE_ACCOUNT"

class ReporterTrustEngine:
    """
    Engine to calculate and manage reporter trust scores and auto-promotion rules.
    """
    
    def __init__(self):
        self.MAX_REPORTS_PER_HOUR = 10
        self.MAX_REPORTS_PER_DAY = 50

    async def calculate_trust_score(self, reporter_id: str, report_stats: Dict[str, Any]) -> float:
        """
        Calculate trust score based on user history.
        
        Args:
            reporter_id: The ID of the reporter.
            report_stats: Dictionary containing total_reports, confirmed_reports,
                          rejected_reports, account_age_days, device_consistency_score.
        
        Returns:
            Float representing the trust score between 0.0 and 1.0.
        """
        total = report_stats.get("total_reports", 0)
        if total == 0:
            return 0.2  # Default for new users
            
        confirmed = report_stats.get("confirmed_reports", 0)
        rejected = report_stats.get("rejected_reports", 0)
        
        # Base ratio
        ratio = confirmed / total if total > 0 else 0.0
        
        # Penalties for rejections
        penalty = min(0.5, (rejected / total) * 1.5) if total > 0 else 0.0
        
        # Device consistency bonus
        device_bonus = report_stats.get("device_consistency_score", 0.5) * 0.1
        
        # Age bonus (up to 0.1 for 365 days)
        age_bonus = min(0.1, report_stats.get("account_age_days", 0) / 3650.0)
        
        score = (ratio * 0.8) - penalty + device_bonus + age_bonus
        return max(0.0, min(1.0, score))

    async def check_rate_limits(self, reporter_id: str, recent_reports_count: Dict[str, int]) -> bool:
        """
        Check if the reporter has exceeded rate limits.
        recent_reports_count should have 'last_hour' and 'last_day'.
        """
        if recent_reports_count.get("last_hour", 0) >= self.MAX_REPORTS_PER_HOUR:
            return False
        if recent_reports_count.get("last_day", 0) >= self.MAX_REPORTS_PER_DAY:
            return False
        return True

    async def can_auto_promote(self, report_id: str, confirmations: List[Dict[str, Any]]) -> bool:
        """
        Determine if a report can be auto-promoted to VERIFIED.
        Promotion requires: 3+ independent reporters with trust>0.5, within 100m, within 7 days, no contradictions.
        """
        # A single report is NEVER auto-promoted
        if not confirmations or len(confirmations) < 2:
            return False
            
        valid_confirmations = 0
        for conf in confirmations:
            trust = conf.get("reporter_trust", 0.0)
            distance = conf.get("distance_m", float('inf'))
            age_days = conf.get("age_days", 999)
            is_contradiction = conf.get("is_contradiction", False)
            
            if is_contradiction:
                return False  # Any contradiction blocks auto-promotion
                
            if trust > 0.5 and distance <= 100.0 and age_days <= 7:
                valid_confirmations += 1
                
        # Need original reporter + 2 valid confirmations (total 3 independent)
        return valid_confirmations >= 2
