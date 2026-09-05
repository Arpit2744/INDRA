from backend.app.core.vlm import LocalVLMProvider


def test_local_vlm_provider_can_be_created():
    provider = LocalVLMProvider(
        model="qwen2.5-vl:7b"
    )

    assert provider.model == "qwen2.5-vl:7b"


def test_local_vlm_provider_implements_analyze_image():
    provider = LocalVLMProvider(
        model="qwen2.5-vl:7b"
    )

    assert hasattr(provider, "analyze_image")