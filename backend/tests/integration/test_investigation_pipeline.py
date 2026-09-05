import pytest

from backend.app.agents.document_agent import DocumentAgent
from backend.app.agents.investigation_agent import InvestigationAgent
from backend.app.agents.vision_agent import VisionAgent
from backend.app.core.llm import LocalLLMProvider
from backend.app.models.evidence import Evidence
from backend.app.rag.keyword_retriever import KeywordRetriever


class FakeVLM:
    def analyze_image(self, image_path: str, prompt: str) -> str:
        return (
            "Visible oil leakage is present near the compressor housing."
        )


@pytest.mark.integration
def test_full_investigation_pipeline():

    # --- Document Agent ---
    document = Evidence(
        source="compressor_sop.txt",
        content=(
            "Compressor C-101 normal operating temperature is "
            "75 C to 85 C. Above 85 C requires maintenance inspection. "
            "Check cooling, lubrication and bearing condition."
        ),
    )

    retriever = KeywordRetriever([document])

    llm = LocalLLMProvider(
        model="qwen2.5:3b",
    )

    document_agent = DocumentAgent(
        retriever=retriever,
        llm=llm,
    )

    document_result = document_agent.run(
        "What should be checked when compressor temperature exceeds 85 C?"
    )

    assert document_result["evidence"]

    # --- Vision Agent ---
    vision_agent = VisionAgent(vlm=FakeVLM())

    vision_result = vision_agent.run(
        "compressor.jpg"
    )

    assert vision_result["observation"]

    # --- Investigation Agent ---
    investigation_agent = InvestigationAgent(
        llm=llm,
    )

    evidence = [
        item.content
        for item in document_result["evidence"]
    ]

    evidence.append(
        vision_result["observation"]
    )

    result = investigation_agent.run(
        problem=(
            "Investigate abnormal compressor C-101 condition."
        ),
        evidence=evidence,
    )

    assert result["analysis"]
    assert result["recommendation"]
    assert len(result["evidence"]) >= 2