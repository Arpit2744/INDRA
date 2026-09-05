import pytest

from backend.app.core.approval import ApprovalService


def test_pending_request_can_be_approved():
    service = ApprovalService()

    result = service.approve(
        {
            "approval": {
                "status": "pending",
            }
        }
    )

    assert result["status"] == "approved"
    assert result["approved_by"] == "supervisor"


def test_pending_request_can_be_rejected():
    service = ApprovalService()

    result = service.reject(
        {
            "approval": {
                "status": "pending",
            }
        }
    )

    assert result["status"] == "rejected"


def test_non_pending_request_cannot_be_approved():
    service = ApprovalService()

    with pytest.raises(ValueError):
        service.approve(
            {
                "approval": {
                    "status": "approved",
                }
            }
        )