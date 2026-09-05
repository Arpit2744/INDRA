import pytest

from backend.app.core.vlm import LocalVLMProvider


@pytest.mark.integration
def test_local_vlm_can_analyze_image():
    provider = LocalVLMProvider(
        model="qwen2.5vl:3b",
    )

    result = provider.analyze_image(
        image_path="data/demo/compressor.jpg",
        prompt="Describe visible abnormalities in this industrial equipment image.",
    )

    assert isinstance(result, str)
    assert len(result.strip()) > 0