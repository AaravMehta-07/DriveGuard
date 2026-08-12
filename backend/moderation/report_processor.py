"""
Report Processor for handling community reports.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProcessingResult(BaseModel):
    report_id: str
    status: str
    confidence_score: float
    queued_for_review: bool
    review_reason: Optional[str] = None
    merged_with_id: Optional[str] = None

class ReportProcessor:
    """
    Processes incoming reports, handles deduplication, and initial confidence scoring.
    """

    async def process_report(self, report: Dict[str, Any], existing_reports: List[Dict[str, Any]], reporter_trust: float, is_first_report: bool) -> ProcessingResult:
        """
        Process a new report, deduplicate, calculate confidence, and queue for review if necessary.
        """
        report_id = report.get("id", "new_report")
        report_type = report.get("type")

        # Deduplication check: existing reports within 100m, same type, within 48 hours
        for ext in existing_reports:
            if (ext.get("distance_m", float('inf')) <= 100.0 and
                ext.get("type") == report_type and
                ext.get("age_hours", 99) <= 48):

                # Merge if duplicate
                return ProcessingResult(
                    report_id=report_id,
                    status="MERGED",
                    confidence_score=ext.get("confidence_score", 0.0) + (reporter_trust * 0.1),
                    queued_for_review=False,
                    merged_with_id=ext.get("id")
                )

        initial_confidence = reporter_trust * 0.5

        queued = False
        reason = None

        if reporter_trust < 0.3:
            queued = True
            reason = "Low trust score"
        elif is_first_report:
            queued = True
            reason = "First report from user"
        elif report.get("unusual_location", False):
            queued = True
            reason = "Unusual location"
        elif report.get("contradicts_verified", False):
            queued = True
            reason = "Contradicts verified data"

        return ProcessingResult(
            report_id=report_id,
            status="QUEUED" if queued else "ACCEPTED",
            confidence_score=initial_confidence,
            queued_for_review=queued,
            review_reason=reason
        )

    async def process_confirmation(self, report_id: str, user_id: str, confirmation_type: str, current_confidence: float, user_trust: float) -> float:
        """
        Update the confidence score of a report based on a user's confirmation or rejection.
        """
        if confirmation_type == "CONFIRM":
            return min(1.0, current_confidence + (user_trust * 0.2))
        elif confirmation_type == "REJECT":
            return max(0.0, current_confidence - (user_trust * 0.3))
        return current_confidence
