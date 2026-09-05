from backend.app.core.llm import LocalLLMProvider


def test_local_llm_provider_can_be_created():
    provider = LocalLLMProvider(
        model="qwen2.5:7b"
    )

    assert provider.model == "qwen2.5:7b"


def test_local_llm_provider_implements_generate():
    provider = LocalLLMProvider(
        model="qwen2.5:7b"
    )

    assert hasattr(provider, "generate")