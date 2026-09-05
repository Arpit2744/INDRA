from backend.app.core.interfaces import (
    Agent,
    LLMProvider,
    VLMProvider,
)


def test_llm_provider_defines_generate():
    assert hasattr(LLMProvider, "generate")


def test_vlm_provider_defines_analyze_image():
    assert hasattr(VLMProvider, "analyze_image")


def test_agent_defines_run():
    assert hasattr(Agent, "run")


