from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict, total=False):
    request: str
    evidence: list[Any]
    agent_outputs: list[dict[str, Any]]
    validation: dict[str, Any]
    approval: dict[str, Any]
    final_output: dict[str, Any] | None


def build_investigation_graph():
    graph = StateGraph(GraphState)

    def understand(state: GraphState):
        outputs = list(state.get("agent_outputs", []))

        outputs.append({
            "stage": "understand",
            "status": "completed",
        })

        return {
            "agent_outputs": outputs,
        }

    def validate(state: GraphState):
        outputs = list(state.get("agent_outputs", []))

        outputs.append({
            "stage": "validate",
            "status": "completed",
        })

        return {
            "agent_outputs": outputs,
            "validation": {
                "status": "validated",
            },
        }

    def approval(state: GraphState):
        outputs = list(state.get("agent_outputs", []))

        outputs.append({
            "stage": "approval",
            "status": "pending",
        })

        return {
            "agent_outputs": outputs,
            "approval": {
                "status": "pending",
            },
        }

    graph.add_node("understand", understand)
    graph.add_node("validate", validate)
    graph.add_node("approval", approval)

    graph.add_edge(START, "understand")
    graph.add_edge("understand", "validate")
    graph.add_edge("validate", "approval")
    graph.add_edge("approval", END)

    return graph.compile()