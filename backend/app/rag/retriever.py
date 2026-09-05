from backend.app.core.embedding import MockEmbeddingProvider
from backend.app.models.evidence import Evidence
from backend.app.rag.vector_store import InMemoryVectorStore


class Retriever:
    def __init__(
        self,
        embedding_provider: MockEmbeddingProvider,
        vector_store: InMemoryVectorStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Evidence]:
        query_vector = self.embedding_provider.embed([query])[0]

        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )

        evidence = []

        for result in results:
            evidence.append(
                Evidence(
                    source=result["metadata"].get(
                        "source",
                        "unknown",
                    ),
                    content=result["text"],
                    metadata=result["metadata"],
                    relevance=result["score"],
                )
            )

        return evidence