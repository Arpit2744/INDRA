from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from backend.app.agents.document_agent import DocumentAgent
from backend.app.agents.investigation_agent import InvestigationAgent
from backend.app.agents.vision_agent import VisionAgent
from backend.app.core.audit import AuditLogger
from backend.app.validation.validator import InvestigationValidator


class GraphState(TypedDict, total=False):
    request: str
    document: str
    image: str

    document_result: dict[str, Any]
    vision_result: dict[str, Any]
    investigation_result: dict[str, Any]

    evidence: list[Any]

    validation: dict[str, Any]
    approval: dict[str, Any]

    final_output: dict[str, Any] | None

    agent_outputs: list[dict[str, Any]]
    audit_events: list[dict[str, Any]]


class InvestigationGraph:
    def __init__(
        self,
        document_agent: DocumentAgent,
        vision_agent: VisionAgent,
        investigation_agent: InvestigationAgent,
    ):
        self.document_agent = document_agent
        self.vision_agent = vision_agent
        self.investigation_agent = investigation_agent

        self.validator = InvestigationValidator()
        self.audit = AuditLogger()

    def _record_stage(
        self,
        state: GraphState,
        stage: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        outputs = list(state.get("agent_outputs", []))

        outputs.append(
            {
                "stage": stage,
                "status": status,
            }
        )

        self.audit.log(
            stage=stage,
            status=status,
            details=details or {},
        )

        return outputs

    def _audit_events(self) -> list[dict[str, Any]]:
        return self.audit.all()

    def document_node(self, state: GraphState):
        result = self.document_agent.run(
            state["request"]
        )

        outputs = self._record_stage(
            state,
            stage="document_agent",
            status="completed",
        )

        return {
            "document_result": result,
            "agent_outputs": outputs,
            "audit_events": self._audit_events(),
        }

    def vision_node(self, state: GraphState):
        image = state.get("image")

        if not image:
            result = {
                "image": None,
                "observation": "No image provided.",
            }

            status = "skipped"
        else:
            result = self.vision_agent.run(image)
            status = "completed"

        outputs = self._record_stage(
            state,
            stage="vision_agent",
            status=status,
        )

        return {
            "vision_result": result,
            "agent_outputs": outputs,
            "audit_events": self._audit_events(),
        }

    def investigation_node(self, state: GraphState):
        document_result = state.get(
            "document_result",
            {},
        )
        vision_result = state.get(
            "vision_result",
            {},
        )

        evidence: list[Any] = []

        for item in document_result.get(
            "evidence",
            [],
        ):
            if hasattr(item, "content"):
                evidence.append(item.content)
            else:
                evidence.append(str(item))

        observation = vision_result.get(
            "observation"
        )

        if observation:
            evidence.append(observation)

        result = self.investigation_agent.run(
            problem=state["request"],
            evidence=evidence,
        )

        outputs = self._record_stage(
            state,
            stage="investigation_agent",
            status="completed",
            details={
                "evidence_count": len(evidence),
            },
        )

        return {
            "investigation_result": result,
            "evidence": evidence,
            "agent_outputs": outputs,
            "audit_events": self._audit_events(),
        }

    def validate_node(self, state: GraphState):
        investigation = state.get(
            "investigation_result",
            {},
        )

        evidence = state.get(
            "evidence",
            [],
        )

        validation = self.validator.validate(
            analysis=investigation.get(
                "analysis",
                "",
            ),
            recommendation=investigation.get(
                "recommendation",
                "",
            ),
            evidence=evidence,
        )

        outputs = self._record_stage(
            state,
            stage="validation",
            status=validation["status"],
            details={
                "evidence_count": validation[
                    "evidence_count"
                ],
            },
        )

        return {
            "validation": validation,
            "agent_outputs": outputs,
            "audit_events": self._audit_events(),
        }

    def approval_node(self, state: GraphState):
        validation = state.get(
            "validation",
            {},
        )

        status = (
            "pending"
            if validation.get("status")
            == "validated"
            else "blocked"
        )

        approval = {
            "status": status,
            "required": True,
        }

        outputs = self._record_stage(
            state,
            stage="human_approval",
            status=status,
        )

        return {
            "approval": approval,
            "final_output": state.get(
                "investigation_result"
            ),
            "agent_outputs": outputs,
            "audit_events": self._audit_events(),
        }


def build_investigation_graph(
    document_agent,
    vision_agent,
    investigation_agent,
):
    system = InvestigationGraph(
        document_agent=document_agent,
        vision_agent=vision_agent,
        investigation_agent=investigation_agent,
    )

    graph = StateGraph(GraphState)

    graph.add_node(
        "document_agent",
        system.document_node,
    )

    graph.add_node(
        "vision_agent",
        system.vision_node,
    )

    graph.add_node(
        "investigation_agent",
        system.investigation_node,
    )

    graph.add_node(
        "validate",
        system.validate_node,
    )

    graph.add_node(
        "approval",
        system.approval_node,
    )

    graph.add_edge(
        START,
        "document_agent",
    )

    graph.add_edge(
        "document_agent",
        "vision_agent",
    )

    graph.add_edge(
        "vision_agent",
        "investigation_agent",
    )

    graph.add_edge(
        "investigation_agent",
        "validate",
    )

    graph.add_edge(
        "validate",
        "approval",
    )

    graph.add_edge(
        "approval",
        END,
    )

    return graph.compile()