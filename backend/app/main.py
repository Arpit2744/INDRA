from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from backend.app.api.routes import router


app = FastAPI(
    title="INDRA",
    version="0.1.0",
)

app.include_router(router)

FRONTEND_PATH = Path(__file__).resolve().parents[2] / "frontend" / "index.html"


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_PATH)