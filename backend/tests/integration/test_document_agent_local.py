from pathlib import Path

import pytest

from backend.app.agents.document_agent import DocumentAgent
from backend.app.core.llm import LocalLLMProvider
from backend.app.models.evidence import Evidence
from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.keyword_retriever import KeywordRetriever


@pytest.mark.integration
def test_document_agent_can_answer_from_local_document():

    path = Path("data/demo/compressor_sop.txt")

    loader = DocumentLoader()
    text = loader.load(path)

    evidence = Evidence(
        source=str(path),
        content=text,
    )

    retriever = KeywordRetriever([evidence])

    llm = LocalLLMProvider(
        model="qwen2.5:3b",
    )

    agent = DocumentAgent(
        retriever=retriever,
        llm=llm,
    )

    result = agent.run(
        "What is the normal operating temperature for compressor C-101?"
    )

    assert result["answer"]
    assert len(result["evidence"]) == 1
    assert "85" in result["answer"]