import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import router as api_router
from app.models.ml_monitor import ml_monitor
from app.monitoring.drift import drift_analyzer
from app.security.audit import audit_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager: initialize baseline model & reference data on startup.
    """
    try:
        baseline_meta = ml_monitor.train_baseline()
        drift_analyzer.set_reference_data(ml_monitor.reference_data)
        audit_logger.record_event(
            actor="SYSTEM_INIT",
            action="SERVICE_STARTUP",
            target_version=ml_monitor.current_version,
            outcome="SUCCESS",
            details={
                "app_name": settings.APP_NAME,
                "app_version": settings.APP_VERSION,
                "metrics": baseline_meta["metrics"]
            }
        )
    except Exception as e:
        print(f"Warning during startup baseline init: {e}")
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Request Size / Sanitization Middleware (SR-04, TC-13)
@app.middleware("http")
async def sanitize_and_limit_middleware(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 5 * 1024 * 1024:
        return JSONResponse(
            status_code=413,
            content={"detail": "Payload too large. Maximum allowable request size is 5MB."}
        )
    response = await call_next(request)
    return response

# Include API Router
app.include_router(api_router)

# Mount Dashboard Directory
dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
if os.path.exists(dashboard_dir):
    app.mount("/static", StaticFiles(directory=dashboard_dir), name="static")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False, tags=["UI Dashboard"])
def serve_dashboard():
    index_path = os.path.join(dashboard_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Self-Monitoring MLOps Dashboard Loading...</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
