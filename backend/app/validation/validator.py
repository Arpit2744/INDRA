from typing import Any


class InvestigationValidator:
    def validate(
        self,
        analysis: str,
        recommendation: str,
        evidence: list[Any],
    ) -> dict[str, Any]:

        evidence_count = len(evidence)

        if not analysis.strip():
            return {
                "status": "needs_review",
                "reason": "Missing analysis.",
                "evidence_count": evidence_count,
            }

        if not recommendation.strip():
            return {
                "status": "needs_review",
                "reason": "Missing recommendation.",
                "evidence_count": evidence_count,
            }

        if evidence_count == 0:
            return {
                "status": "needs_review",
                "reason": "No supporting evidence.",
                "evidence_count": 0,
            }

        return {
            "status": "validated",
            "reason": "Required analysis, recommendation and evidence are present.",
            "evidence_count": evidence_count,
        }