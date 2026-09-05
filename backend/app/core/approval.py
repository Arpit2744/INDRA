from typing import Any


class ApprovalService:
    def approve(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        approval = dict(state.get("approval", {}))

        if approval.get("status") != "pending":
            raise ValueError(
                "Only pending approvals can be approved."
            )

        approval["status"] = "approved"
        approval["approved_by"] = "supervisor"

        return approval

    def reject(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        approval = dict(state.get("approval", {}))

        if approval.get("status") != "pending":
            raise ValueError(
                "Only pending approvals can be rejected."
            )

        approval["status"] = "rejected"

        return approval