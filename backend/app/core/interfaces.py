from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: list[str] | None = None,
    ) -> str:
        """Generate text using a local or compatible LLM."""
        raise NotImplementedError


class VLMProvider(ABC):

    @abstractmethod
    def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> str:
        """Analyze an image using a local or compatible VLM."""
        raise NotImplementedError


class Agent(ABC):

    @abstractmethod
    def run(
        self,
        state: Any,
    ) -> Any:
        """Execute the agent against the investigation state."""
        raise NotImplementedError