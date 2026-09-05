from .interfaces import VLMProvider


class LocalVLMProvider(VLMProvider):
    def __init__(self, model: str):
        self.model = model

    def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "Local VLM runtime is not connected yet."
        )