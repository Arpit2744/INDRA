from backend.app.models.state import InvestigationState


def test_investigation_state_stores_request():
    state = InvestigationState(
        request="Investigate abnormal compressor temperature."
    )

    assert state.request == "Investigate abnormal compressor temperature."
    assert state.evidence == []
    assert state.agent_outputs == []


def test_investigation_state_can_store_evidence():
    state = InvestigationState(
        request="Investigate compressor C-101."
    )

    evidence = {
        "source": "manual.pdf",
        "content": "Temperature limit is 85°C."
    }

    state.evidence.append(evidence)

    assert len(state.evidence) == 1