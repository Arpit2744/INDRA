from backend.app.agents.vision_agent import VisionAgent


class FakeVLM:
    def analyze_image(self, image_path: str, prompt: str) -> str:
        assert image_path.endswith(".jpg")
        return "Visible oil leakage detected near the compressor housing."


def test_vision_agent_returns_observation():
    agent = VisionAgent(vlm=FakeVLM())

    result = agent.run("compressor.jpg")

    assert "oil leakage" in result["observation"]
    assert result["image"] == "compressor.jpg"