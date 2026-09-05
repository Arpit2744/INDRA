from backend.app.validation.validator import InvestigationValidator


def test_valid_investigation_passes_validation():
    validator = InvestigationValidator()

    result = validator.validate(
        analysis="Possible bearing degradation.",
        recommendation="Schedule inspection.",
        evidence=["SOP evidence", "Image evidence"],
    )

    assert result["status"] == "validated"
    assert result["evidence_count"] == 2


def test_investigation_without_evidence_needs_review():
    validator = InvestigationValidator()

    result = validator.validate(
        analysis="Possible failure.",
        recommendation="Inspect equipment.",
        evidence=[],
    )

    assert result["status"] == "needs_review"