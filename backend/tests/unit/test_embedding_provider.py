from backend.app.core.embedding import MockEmbeddingProvider


def test_mock_embedding_provider_can_be_created():
    provider = MockEmbeddingProvider(dimension=8)

    assert provider.dimension == 8


def test_mock_embedding_provider_returns_vectors():
    provider = MockEmbeddingProvider(dimension=8)

    embeddings = provider.embed(
        [
            "Compressor temperature is high.",
            "Bearing inspection is required.",
        ]
    )

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 8
    assert len(embeddings[1]) == 8


def test_mock_embedding_provider_is_deterministic():
    provider = MockEmbeddingProvider(dimension=8)

    first = provider.embed(["compressor"])
    second = provider.embed(["compressor"])

    assert first == second