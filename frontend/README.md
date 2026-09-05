# INDRA Frontend

Dependency-free single-page demo for the existing FastAPI backend.

Copy `index.html` to `frontend/index.html`.

Replace `backend/app/main.py` with:

```python
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
```

Run from the repository root:

```cmd
uvicorn backend.app.main:app --reload
```

Open:

http://127.0.0.1:8000/

No npm/React/Node dependency is required.
