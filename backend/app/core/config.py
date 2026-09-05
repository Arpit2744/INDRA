import os


class Settings:
    APP_NAME = os.getenv("INDRA_APP_NAME", "INDRA")
    MODEL_BACKEND = os.getenv("INDRA_MODEL_BACKEND", "ollama")
    MODEL_DEVICE = os.getenv("INDRA_MODEL_DEVICE", "cpu")

    LLM_MODEL = os.getenv(
        "INDRA_LLM_MODEL",
        "qwen2.5:7b",
    )

    VLM_MODEL = os.getenv(
        "INDRA_VLM_MODEL",
        "qwen2.5vl:7b",
    )


settings = Settings()