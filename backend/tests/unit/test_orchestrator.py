from backend.app.orchestrator.graph import build_investigation_graph


def test_investigation_graph_runs():

    graph = build_investigation_graph()

    state = {
        "request": "Investigate abnormal compressor condition.",
        "evidence": [],
        "agent_outputs": [],
        "validation": {},
        "approval": {},
        "final_output": None,
    }

    result = graph.invoke(state)

    assert result is not None
    assert result["request"] == (
        "Investigate abnormal compressor condition."
    )