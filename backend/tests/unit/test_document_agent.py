from backend.app.agents.document_agent import DocumentAgent
from backend.app.models.evidence import Evidence


class FakeRetriever:
    def retrieve(self, query: str, top_k: int = 5):
        return [
            Evidence(
                source="compressor_sop.pdf",
                content="Maximum operating temperature is 85 C.",
                relevance=0.95,
            )
        ]


class FakeLLM:
    def generate(self, prompt: str, context=None):
        assert context is not None
        assert "Maximum operating temperature is 85 C." in context[0]

        return "The maximum operating temperature is 85 C."


def test_document_agent_returns_answer_and_evidence():
    agent = DocumentAgent(
        retriever=FakeRetriever(),
        llm=FakeLLM(),
    )

    result = agent.run(
        "What is the maximum operating temperature?"
    )

    assert result["answer"] == (
        "The maximum operating temperature is 85 C."
    )
    assert len(result["evidence"]) == 1
    assert result["evidence"][0].source == "compressor_sop.pdf"