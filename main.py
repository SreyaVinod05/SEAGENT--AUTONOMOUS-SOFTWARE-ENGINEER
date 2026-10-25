from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import workflow_router
from app.config import is_gemini_configured, GEMINI_MODEL

app = FastAPI(
    title="SEAGENT",
    description="Agentic AI Software Engineering Platform powered by Google Gemini and LangGraph",
    version="1.0.0",
)

# Enable CORS for local development (Vite React frontend, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Core API Routers
app.include_router(workflow_router)


@app.get("/health")
def health_check():
    """System health check and provider readiness status."""
    return {
        "status": "healthy",
        "service": "SEAGENT Backend",
        "gemini_ready": is_gemini_configured(),
        "model": GEMINI_MODEL,
    }


# Check if frontend static build exists to serve directly
dist_path = Path(__file__).resolve().parent / "frontend" / "dist"
if dist_path.exists():
    app.mount("/assets", StaticFiles(directory=dist_path / "assets"), name="assets")

    @app.get("/")
    def serve_frontend_root():
        return FileResponse(dist_path / "index.html")

    @app.get("/{full_path:path}")
    def serve_frontend_spa(full_path: str):
        target = dist_path / full_path
        if target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(dist_path / "index.html")
else:
    @app.get("/")
    def home():
        return {
            "message": "SEAGENT backend is running!",
            "docs": "/docs",
            "health": "/health",
            "gemini_ready": is_gemini_configured(),
            "model": GEMINI_MODEL,
        }