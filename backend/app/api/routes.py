from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.agents.document_agent import DocumentAgent
from backend.app.agents.investigation_agent import InvestigationAgent
from backend.app.agents.vision_agent import VisionAgent
from backend.app.core.approval import ApprovalService
from backend.app.core.llm import LocalLLMProvider
from backend.app.core.run_store import RunStore
from backend.app.models.evidence import Evidence
from backend.app.orchestrator.graph import build_investigation_graph
from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.keyword_retriever import KeywordRetriever


router = APIRouter()

run_store = RunStore()
approval_service = ApprovalService()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "system": "INDRA",
        "mode": "local",
    }


@router.post("/investigate")
def investigate():
    """
    Run the complete INDRA investigation workflow.

    Document Agent
        -> Vision Agent
        -> Investigation Agent
        -> Validation
        -> Human Approval
    """

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

    # Store the complete investigation state.
    run_id = run_store.create(result)

    return {
        "run_id": run_id,
        **result,
    }


@router.post("/approve/{run_id}")
def approve(run_id: str):
    """
    Approve a pending investigation.
    """

    try:
        state = run_store.get(run_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Run '{run_id}' not found.",
        )

    try:
        # ApprovalService already assigns
        # approved_by = supervisor internally.
        approval = approval_service.approve(state)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    run_store.update(
        run_id,
        {
            "approval": approval,
        },
    )

    audit_events = list(
        state.get("audit_events", [])
    )

    audit_events.append(
        {
            "stage": "human_approval",
            "status": "approved",
            "details": {
                "approved_by": "supervisor",
            },
        }
    )

    run_store.update(
        run_id,
        {
            "audit_events": audit_events,
        },
    )

    return {
        "run_id": run_id,
        "status": "approved",
        "approval": approval,
    }


@router.post("/reject/{run_id}")
def reject(run_id: str):
    """
    Reject a pending investigation.
    """

    try:
        state = run_store.get(run_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Run '{run_id}' not found.",
        )

    try:
        # ApprovalService does not accept rejected_by.
        approval = approval_service.reject(state)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    run_store.update(
        run_id,
        {
            "approval": approval,
        },
    )

    audit_events = list(
        state.get("audit_events", [])
    )

    audit_events.append(
        {
            "stage": "human_approval",
            "status": "rejected",
            "details": {
                "rejected_by": "supervisor",
            },
        }
    )

    run_store.update(
        run_id,
        {
            "audit_events": audit_events,
        },
    )

    return {
        "run_id": run_id,
        "status": "rejected",
        "approval": approval,
    }


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    """
    Retrieve the complete investigation state.
    """

    try:
        state = run_store.get(run_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Run '{run_id}' not found.",
        )

    return {
        "run_id": run_id,
        "run": state,
    }


@router.get("/audit/{run_id}")
def get_audit(run_id: str):
    """
    Retrieve the audit trail for an investigation.
    """

    try:
        state = run_store.get(run_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Run '{run_id}' not found.",
        )

    return {
        "run_id": run_id,
        "events": state.get(
            "audit_events",
            [],
        ),
    }


class FakeVLM:
    """
    CPU-development VLM substitute.

    The production deployment can replace this
    provider with a local open-weight VLM without
    changing the Vision Agent interface.
    """

    def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> str:
        return (
            "Visible oil leakage detected near "
            "the compressor housing."
        )