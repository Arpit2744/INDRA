from typing import Any


class VisionAgent:
    def __init__(self, vlm: Any):
        self.vlm = vlm

    def run(self, image_path: str) -> dict[str, Any]:
        observation = self.vlm.analyze_image(
            image_path,
            (
                "Inspect this industrial equipment image. "
                "Identify visible abnormalities relevant to "
                "maintenance investigation."
            ),
        )

        return {
            "image": image_path,
            "observation": observation,
        }