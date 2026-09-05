from dataclasses import dataclass, field
from typing import Any

from .evidence import Evidence


@dataclass
class InvestigationState:
    request: str
    evidence: list[Evidence | dict[str, Any]] = field(default_factory=list)
    agent_outputs: list[dict[str, Any]] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=dict)
    approval: dict[str, Any] = field(default_factory=dict)
    final_output: dict[str, Any] | None = None