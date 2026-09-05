import hashlib

from .interfaces import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimension: int = 8):
        if dimension <= 0:
            raise ValueError("dimension must be greater than zero")

        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []

        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()

            vector = [
                digest[index % len(digest)] / 255.0
                for index in range(self.dimension)
            ]

            embeddings.append(vector)

        return embeddings