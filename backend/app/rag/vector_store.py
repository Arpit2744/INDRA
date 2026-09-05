import math
from typing import Any


class InMemoryVectorStore:
    def __init__(self):
        self._items: list[dict[str, Any]] = []

    def add(
        self,
        vector: list[float],
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self._items.append(
            {
                "vector": vector,
                "text": text,
                "metadata": metadata or {},
            }
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        scored = []

        for item in self._items:
            score = self._cosine_similarity(
                query_vector,
                item["vector"],
            )

            scored.append(
                {
                    "text": item["text"],
                    "metadata": item["metadata"],
                    "score": score,
                }
            )

        scored.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored[:top_k]

    @staticmethod
    def _cosine_similarity(
        a: list[float],
        b: list[float],
    ) -> float:
        if len(a) != len(b):
            raise ValueError("Vector dimensions must match")

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)