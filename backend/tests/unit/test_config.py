from backend.app.core.config import settings


def test_default_model_backend_is_ollama():
    assert settings.MODEL_BACKEND == "ollama"


def test_default_device_is_cpu():
    assert settings.MODEL_DEVICE == "cpu"


def test_llm_model_is_configured():
    assert settings.LLM_MODEL


def test_vlm_model_is_configured():
    assert settings.VLM_MODEL