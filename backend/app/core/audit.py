from datetime import datetime, timezone
from typing import Any


class AuditLogger:
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def log(
        self,
        stage: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        event = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "stage": stage,
            "status": status,
            "details": details or {},
        }

        self.events.append(event)

        return event

    def all(self) -> list[dict[str, Any]]:
        return list(self.events)