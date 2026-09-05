from dataclasses import dataclass, field
from uuid import uuid4
from typing import Any


@dataclass
class Evidence:
    source: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    relevance: float | None = None
    id: str = field(default_factory=lambda: str(uuid4()))