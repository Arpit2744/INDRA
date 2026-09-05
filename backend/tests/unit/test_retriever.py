from backend.app.core.embedding import MockEmbeddingProvider
from backend.app.rag.retriever import Retriever
from backend.app.rag.vector_store import InMemoryVectorStore


def test_retriever_returns_relevant_evidence():
    embeddings = MockEmbeddingProvider(dimension=8)
    store = InMemoryVectorStore()

    text = "Compressor C-101 maximum operating temperature is 85 C."

    vector = embeddings.embed([text])[0]

    store.add(
        vector=vector,
        text=text,
        metadata={
            "source": "compressor_sop.pdf",
            "page": 4,
        },
    )

    retriever = Retriever(
        embedding_provider=embeddings,
        vector_store=store,
    )

    results = retriever.retrieve(
        "Compressor C-101 maximum operating temperature"
    )

    assert len(results) == 1
    assert results[0].content == text
    assert results[0].metadata["source"] == "compressor_sop.pdf"

def test_retriever_respects_top_k():
    embeddings = MockEmbeddingProvider(dimension=8)
    store = InMemoryVectorStore()

    texts = [
        "Compressor temperature information.",
        "Compressor vibration information.",
        "Compressor maintenance information.",
    ]

    vectors = embeddings.embed(texts)

    for text, vector in zip(texts, vectors):
        store.add(
            vector=vector,
            text=text,
            metadata={"source": text},
        )

    retriever = Retriever(
        embedding_provider=embeddings,
        vector_store=store,
    )

    results = retriever.retrieve(
        "Compressor information",
        top_k=2,
    )

    assert len(results) == 2