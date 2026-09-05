from typing import Any

from backend.app.models.evidence import Evidence


class DocumentAgent:
    def __init__(self, retriever: Any, llm: Any):
        self.retriever = retriever
        self.llm = llm

    def run(self, question: str) -> dict[str, Any]:
        evidence: list[Evidence] = self.retriever.retrieve(question)

        context = [item.content for item in evidence]

        answer = self.llm.generate(
            question,
            context=context,
        )

        return {
            "answer": answer,
            "evidence": evidence,
        }