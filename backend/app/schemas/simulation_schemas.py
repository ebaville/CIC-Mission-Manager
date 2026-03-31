"""
schemas/simulation_schemas.py – Pydantic schemas for simulation requests and results.

All array fields carry explicit unit and frame annotations.
NumPy arrays are never serialised raw; they are converted to typed lists.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field

from app.core.enums import ExportFormat, RelativeFrame


# ---------------------------------------------------------------------------
# Simulation request
# ---------------------------------------------------------------------------

class SimulateRequest(BaseModel):
    """Request body for launching a simulation."""

    scenario_id: str
    time_step_s: Optional[float] = Field(
        default=None,
        gt=0,
        description="Override simulation time step [s]. Uses scenario default if None.",
    )


# ---------------------------------------------------------------------------
# ROE state snapshot
# ---------------------------------------------------------------------------

class QnsRoeStateSchema(BaseModel):
    """Serialised QNS ROE state.

    Units: delta_a is dimensionless; delta_lambda, delta_ix, delta_iy are in radians.
    """

    delta_a: float
    delta_lambda: float
    delta_ex: float
    delta_ey: float
    delta_ix: float
    delta_iy: float
    chief_a_m: float = Field(..., description="Chief semi-major axis used to normalise delta_a [m].")
    epoch_s: float


# ---------------------------------------------------------------------------
# Cartesian relative state snapshot
# ---------------------------------------------------------------------------

class RelativeCartesianStateSchema(BaseModel):
    """Serialised relative Cartesian state.

    Units: metres and metres/second.
    """

    rho_m: list[float] = Field(..., description="Relative position [m], 3 elements.")
    rho_dot_mps: list[float] = Field(..., description="Relative velocity [m/s], 3 elements.")
    frame: RelativeFrame
    epoch_s: float


# ---------------------------------------------------------------------------
# Simulation results response
# ---------------------------------------------------------------------------

class SimulationResultsSchema(BaseModel):
    """Response body for simulation results retrieval."""

    scenario_id: str
    step_count: int
    start_epoch_s: float
    end_epoch_s: float
    roe_time_series: list[QnsRoeStateSchema]
    qsw_time_series: list[RelativeCartesianStateSchema]


# ---------------------------------------------------------------------------
# Export request
# ---------------------------------------------------------------------------

class ExportRequest(BaseModel):
    """Request body for result export."""

    format: ExportFormat = ExportFormat.CSV
    output_path: Optional[str] = Field(
        default=None,
        description="Server-side output path. If None, returns file as download.",
    )
