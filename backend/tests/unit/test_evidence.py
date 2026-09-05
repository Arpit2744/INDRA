from backend.app.models.evidence import Evidence


def test_evidence_contains_source_and_content():
    evidence = Evidence(
        source="compressor_manual.pdf",
        content="Maximum operating temperature is 85°C.",
    )

    assert evidence.source == "compressor_manual.pdf"
    assert evidence.content == "Maximum operating temperature is 85°C."
    assert evidence.id