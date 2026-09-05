import pytest

from backend.app.core.llm import LocalLLMProvider


@pytest.mark.integration
def test_local_llm_can_generate():
    provider = LocalLLMProvider(
        model="qwen2.5:3b",
    )

    response = provider.generate(
        "Explain in one sentence why an industrial compressor may overheat."
    )

    assert isinstance(response, str)
    assert len(response.strip()) > 0