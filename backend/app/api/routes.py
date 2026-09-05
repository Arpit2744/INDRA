from pathlib import Path

from fastapi import APIRouter

from backend.app.agents.document_agent import DocumentAgent
from backend.app.agents.investigation_agent import InvestigationAgent
from backend.app.agents.vision_agent import VisionAgent
from backend.app.core.llm import LocalLLMProvider
from backend.app.models.evidence import Evidence
from backend.app.orchestrator.graph import (
    build_investigation_graph,
)
from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.keyword_retriever import KeywordRetriever


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "system": "INDRA",
        "mode": "local",
    }


@router.post("/investigate")
def investigate():
    document_path = Path(
        "data/demo/compressor_sop.txt"
    )

    loader = DocumentLoader()
    text = loader.load(document_path)

    evidence = Evidence(
        source=str(document_path),
        content=text,
    )

    retriever = KeywordRetriever(
        [evidence]
    )

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

    return graph.invoke(
        {
            "request": (
                "Investigate abnormal compressor "
                "C-101 condition."
            ),
            "image": "compressor.jpg",
            "agent_outputs": [],
        }
    )


class FakeVLM:
    def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> str:
        return (
            "Visible oil leakage detected near "
            "the compressor housing."
        )