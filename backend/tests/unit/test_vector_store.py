from backend.app.rag.vector_store import InMemoryVectorStore


def test_vector_store_can_add_and_search():
    store = InMemoryVectorStore()

    store.add(
        vector=[1.0, 0.0, 0.0],
        text="Compressor temperature limit is 85 C.",
        metadata={"source": "compressor_sop.pdf"},
    )

    results = store.search(
        query_vector=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == "Compressor temperature limit is 85 C."
    assert results[0]["metadata"]["source"] == "compressor_sop.pdf"

def test_vector_store_returns_most_similar_first():
    store = InMemoryVectorStore()

    store.add(
        vector=[1.0, 0.0, 0.0],
        text="Temperature information",
        metadata={"source": "temperature.pdf"},
    )

    store.add(
        vector=[0.0, 1.0, 0.0],
        text="Lubrication information",
        metadata={"source": "lubrication.pdf"},
    )

    results = store.search(
        query_vector=[0.9, 0.1, 0.0],
        top_k=2,
    )

    assert results[0]["text"] == "Temperature information"