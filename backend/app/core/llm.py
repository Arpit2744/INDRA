from typing import Any

from .interfaces import LLMProvider


class LocalLLMProvider(LLMProvider):
    def __init__(self, model: str):
        self.model = model

    def generate(
        self,
        prompt: str,
        context: list[str] | None = None,
    ) -> str:
        raise NotImplementedError(
            "Local LLM runtime is not connected yet."
        )