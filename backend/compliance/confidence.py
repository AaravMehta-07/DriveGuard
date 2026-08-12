from typing import List

SOURCE_WEIGHTS = {
    "OFFICIAL_AUTHORITY": 1.0,
    "LICENSED_PROVIDER": 0.9,
    "FIELD_VERIFIED": 0.85,
    "MULTI_SOURCE_CONFIRMED": 0.8,
    "OSM": 0.65,
    "MULTIPLE_COMMUNITY_REPORTS": 0.5,
    "SINGLE_COMMUNITY_REPORT": 0.2,
    "UNKNOWN": 0.1
}

class SourceConfidenceEngine:
    def __init__(self, compliance_policy_version: str = "1.0"):
        self.compliance_policy_version = compliance_policy_version

    def calculate_confidence(
        self,
        sources: List[str],
        verification_count: int,
        contradiction_count: int,
        last_verified_days_ago: int,
        directional_accuracy: float
    ) -> float:
        """
        Calculates source confidence based on multiple factors.
        """
        if not sources:
            return 0.0

        base_score = max([SOURCE_WEIGHTS.get(src, 0.1) for src in sources])

        # Cross-source consistency bonus
        if len(set(sources)) >= 2:
            base_score += 0.1

        # Freshness decay
        if last_verified_days_ago > 180:
            decay_factor = min(1.0, (last_verified_days_ago - 180) * 0.001)
            base_score -= decay_factor

        # Contradiction penalty
        base_score -= contradiction_count * 0.15

        # Geographic accuracy component
        base_score = base_score * (0.8 + 0.2 * directional_accuracy)

        return max(0.0, min(1.0, base_score))

    def get_status(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "VERIFIED"
        elif confidence >= 0.5:
            return "PROBABLE"
        elif confidence >= 0.2:
            return "REPORTED"
        else:
            return "UNCERTAIN"
