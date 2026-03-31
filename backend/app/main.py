"""
main.py – FastAPI application entry point.

Mounts all versioned API routers.
Configures CORS for frontend access.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import scenarios as scenarios_router
from app.api.v1 import reference as reference_router

app = FastAPI(
    title="CIC Mission Manager API",
    description=(
        "Python backend for orbital proximity-operations mission scenario simulation. "
        "ROE-based relative dynamics, phase-based mission model, SIMU-CIC-compatible exports."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS – allow frontend dev server
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite default dev port
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------

app.include_router(scenarios_router.router, prefix="/api/v1")
app.include_router(reference_router.router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return application health status."""
    return {"status": "ok", "version": "0.1.0"}
