from ollama import Client

from .interfaces import LLMProvider


class LocalLLMProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.client = Client(host=host)

    def generate(
        self,
        prompt: str,
        context: list[str] | None = None,
    ) -> str:
        messages = []

        if context:
            context_text = "\n\n".join(context)

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "You are an industrial engineering assistant. "
                        "Use the supplied evidence when answering. "
                        "Do not invent facts that are not supported by "
                        "the evidence.\n\n"
                        f"Evidence:\n{context_text}"
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        return response["message"]["content"]