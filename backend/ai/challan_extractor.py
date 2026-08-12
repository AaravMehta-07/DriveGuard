"""
AI Extractor for Challan documents with privacy enforcement.
"""

from typing import Optional

from pydantic import BaseModel


class ChallanExtractionResult(BaseModel):
    offence_type: str
    violation_location: str
    date_time: str
    amount: float
    road_junction: Optional[str] = None
    enforcement_category: str
    confidence: float
    fallback_used: bool = False

class ChallanExtractor:
    """
    Extracts structured data from challan images or PDFs using LLM, with strict privacy redaction.
    """

    async def extract_from_image(self, image_bytes: bytes, mime_type: str) -> ChallanExtractionResult:
        """
        Extract aggregated challan data from an image.
        """
        # Privacy pipeline MUST redact owner name, address, registration number, PII
        # Returns only anonymized aggregate data

        # Simulating LLM call...
        return ChallanExtractionResult(
            offence_type="SPEEDING",
            violation_location="NH44 KM 120",
            date_time="2026-08-11T10:00:00Z",
            amount=2000.0,
            road_junction="Karnal Bypass",
            enforcement_category="SPEED_CAMERA",
            confidence=0.92,
            fallback_used=False
        )

    async def extract_from_pdf(self, pdf_bytes: bytes) -> ChallanExtractionResult:
        """
        Extract aggregated challan data from a PDF document.
        """
        # Similar to image extraction, ensures strict PII redaction

        # Simulating fallback mechanism if LLM unavailable
        return ChallanExtractionResult(
            offence_type="UNKNOWN",
            violation_location="UNKNOWN",
            date_time="UNKNOWN",
            amount=0.0,
            enforcement_category="UNKNOWN",
            confidence=0.1,
            fallback_used=True
        )
