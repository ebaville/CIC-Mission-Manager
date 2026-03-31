"""
api/v1/reference.py – Reference data API routes.

Routes:
  GET /api/v1/reference/frames  – List available reference frames.
  GET /api/v1/reference/models  – List available physics models.

These are read-only, no-side-effect informational endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.core.enums import RelativeFrame, RelativeModelMode

router = APIRouter(prefix="/reference", tags=["reference"])


@router.get(
    "/frames",
    response_model=dict,
    summary="List available reference frames.",
)
def get_frames() -> dict:
    """Return available inertial and local orbital frames with descriptions."""
    return {
        "inertial_frames": ["ECI_J2000"],
        "relative_frames": [f.value for f in RelativeFrame],
    }


@router.get(
    "/models",
    response_model=dict,
    summary="List available physics models.",
)
def get_models() -> dict:
    """Return available relative dynamics models."""
    return {
        "relative_models": [m.value for m in RelativeModelMode],
        "default_relative_model": RelativeModelMode.KGD_QNS_J2.value,
    }
