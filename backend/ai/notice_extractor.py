"""
Notice Extractor for parsing authoritative traffic notices.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel

class NoticeExtractionResult(BaseModel):
    notice_number: str
    authority: str
    publication_date: str
    effective_start: str
    effective_end: Optional[str] = None
    until_further_order: bool
    roads: List[str]
    endpoints: List[str]
    junctions: List[str]
    direction: str
    restriction_type: str
    vehicle_class: List[str]
    exceptions: List[str]
    time_of_day: Optional[str] = None
    days_of_week: List[str]
    alternative_routes: List[str]
    source_text_spans: Dict[str, str]
    confidence: float

class NoticeExtractor:
    """
    Extracts structured schema from official traffic notices. Output is candidate only.
    """
    
    async def extract_from_document(self, text: str, source_url: str) -> NoticeExtractionResult:
        """
        Extracts structured schema from document text.
        LLM output is CANDIDATE only - never becomes production data without validation.
        Schema validation rejects nonsensical output.
        """
        
        # Simulated LLM extraction logic
        return NoticeExtractionResult(
            notice_number="TRF-2026-001",
            authority="Traffic Police",
            publication_date="2026-08-10",
            effective_start="2026-08-11T00:00:00Z",
            until_further_order=True,
            roads=["MG Road"],
            endpoints=["Point A", "Point B"],
            junctions=["Junction 1"],
            direction="BOTH",
            restriction_type="NO_ENTRY",
            vehicle_class=["HEAVY_COMMERCIAL"],
            exceptions=["EMERGENCY_VEHICLES"],
            days_of_week=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
            alternative_routes=["Ring Road"],
            source_text_spans={
                "restriction_type": "No entry for heavy commercial vehicles",
                "roads": "on MG Road from Point A to Point B"
            },
            confidence=0.85
        )
