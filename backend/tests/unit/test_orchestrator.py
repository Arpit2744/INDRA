from backend.app.orchestrator.graph import (
    build_investigation_graph,
)


class FakeEvidence:
    def __init__(self, content: str):
        self.content = content


class FakeDocumentAgent:
    def run(self, request):
        return {
            "answer": "Temperature limit is 85 C.",
            "evidence": [
                FakeEvidence(
                    "Temperature limit is 85 C."
                )
            ],
        }


class FakeVisionAgent:
    def run(self, image):
        return {
            "image": image,
            "observation": (
                "Visible oil leakage detected."
            ),
        }


class FakeInvestigationAgent:
    def run(self, problem, evidence):
        assert problem
        assert len(evidence) >= 2

        return {
            "analysis": (
                "Possible bearing degradation."
            ),
            "recommendation": (
                "Schedule bearing inspection."
            ),
            "evidence": evidence,
        }


def test_investigation_graph_runs():
    graph = build_investigation_graph(
        document_agent=FakeDocumentAgent(),
        vision_agent=FakeVisionAgent(),
        investigation_agent=FakeInvestigationAgent(),
    )

    result = graph.invoke(
        {
            "request": (
                "Investigate compressor C-101."
            ),
            "image": "compressor.jpg",
            "agent_outputs": [],
        }
    )

    assert result["document_result"]
    assert result["vision_result"]
    assert result["investigation_result"]

    assert result["validation"]["status"] == (
        "validated"
    )

    assert result["approval"]["status"] == (
        "pending"
    )

    assert len(result["evidence"]) >= 2

    stages = [
        event["stage"]
        for event in result["agent_outputs"]
    ]

    assert stages == [
        "document_agent",
        "vision_agent",
        "investigation_agent",
        "validation",
        "human_approval",
    ]

    assert len(result["audit_events"]) >= 5