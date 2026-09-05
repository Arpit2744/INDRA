import pytest

from backend.app.agents.document_agent import DocumentAgent
from backend.app.agents.investigation_agent import (
    InvestigationAgent,
)
from backend.app.agents.vision_agent import VisionAgent
from backend.app.core.llm import LocalLLMProvider
from backend.app.models.evidence import Evidence
from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.keyword_retriever import KeywordRetriever
from backend.app.orchestrator.graph import (
    build_investigation_graph,
)


class FakeVLM:
    def analyze_image(self, image_path, prompt):
        return (
            "Visible oil leakage detected near compressor housing."
        )


@pytest.mark.integration
def test_end_to_end_investigation_graph():

    path = "data/demo/compressor_sop.txt"

    loader = DocumentLoader()
    text = loader.load(path)

    evidence = Evidence(
        source=path,
        content=text,
    )

    retriever = KeywordRetriever([evidence])

    llm = LocalLLMProvider(
        model="qwen2.5:3b",
    )

    document_agent = DocumentAgent(
        retriever=retriever,
        llm=llm,
    )

    vision_agent = VisionAgent(
        vlm=FakeVLM(),
    )

    investigation_agent = InvestigationAgent(
        llm=llm,
    )

    graph = build_investigation_graph(
        document_agent=document_agent,
        vision_agent=vision_agent,
        investigation_agent=investigation_agent,
    )

    result = graph.invoke(
        {
            "request": (
                "Investigate abnormal compressor "
                "C-101 condition."
            ),
            "image": "compressor.jpg",
            "agent_outputs": [],
        }
    )

    assert result["document_result"]["answer"]
    assert result["vision_result"]["observation"]
    assert result["investigation_result"]["analysis"]

    assert result["validation"]["status"] == "validated"
    assert result["approval"]["status"] == "pending"

    assert len(result["evidence"]) >= 2