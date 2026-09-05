from typing import Any


class InvestigationAgent:
    def __init__(self, llm: Any):
        self.llm = llm

    def run(
        self,
        problem: str,
        evidence: list[str],
    ) -> dict[str, Any]:

        context = "\n\n".join(evidence)

        analysis = self.llm.generate(
            (
                "Investigate the following industrial problem. "
                "Use only the supplied evidence. "
                "Do not invent facts.\n\n"
                f"Problem:\n{problem}\n\n"
                f"Evidence:\n{context}"
            ),
            context=evidence,
        )

        recommendation = (
            "Review the evidence and schedule appropriate "
            "maintenance inspection."
        )

        return {
            "analysis": analysis,
            "recommendation": recommendation,
            "evidence": evidence,
        }