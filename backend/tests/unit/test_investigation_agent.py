from backend.app.agents.investigation_agent import InvestigationAgent


class FakeLLM:
    def generate(self, prompt: str, context=None):
        return (
            "Likely cause: bearing degradation. "
            "Recommendation: schedule bearing inspection."
        )


def test_investigation_agent_combines_evidence():
    agent = InvestigationAgent(llm=FakeLLM())

    result = agent.run(
        problem="Investigate abnormal compressor condition.",
        evidence=[
            "SOP: temperature above 85 C requires inspection.",
            "Image: visible oil leakage near housing.",
        ],
    )

    assert "bearing degradation" in result["analysis"]
    assert "inspection" in result["recommendation"].lower()