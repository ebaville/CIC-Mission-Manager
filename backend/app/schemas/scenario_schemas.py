"""
schemas/scenario_schemas.py – Pydantic schemas for scenario creation and validation.

All schemas explicitly declare units and frames.
All enumerations reference core/enums.py (never redeclared here).
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.core.enums import (
    DragMode,
    GuidanceLawType,
    MissionPhaseType,
    RelativeFrame,
    RelativeModelMode,
)


# ---------------------------------------------------------------------------
# Orbital state schemas
# ---------------------------------------------------------------------------

class AbsoluteOrbitalStateSchema(BaseModel):
    """Cartesian ECI state at scenario epoch.

    Units: metres for position, metres/second for velocity.
    Frame: ECI J2000.
    """

    r_eci_m: list[float] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ECI position vector [m], 3 elements.",
    )
    v_eci_mps: list[float] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ECI velocity vector [m/s], 3 elements.",
    )

    @field_validator("r_eci_m", "v_eci_mps")
    @classmethod
    def validate_three_vector(cls, v: list[float]) -> list[float]:
        if len(v) != 3:
            raise ValueError("Vector must have exactly 3 elements.")
        return v


# ---------------------------------------------------------------------------
# Vehicle schema
# ---------------------------------------------------------------------------

class VehicleSchema(BaseModel):
    """Vehicle (spacecraft) specification."""

    vehicle_id: str
    name: str
    mass_kg: float = Field(..., gt=0, description="Vehicle wet mass [kg].")
    initial_abs_state: AbsoluteOrbitalStateSchema
    drag_area_m2: float = Field(default=1.0, gt=0)
    drag_coeff: float = Field(default=2.2, gt=0)


# ---------------------------------------------------------------------------
# Perturbation config schema
# ---------------------------------------------------------------------------

class PerturbationConfigSchema(BaseModel):
    """Perturbation model configuration for a mission phase."""

    use_j2: bool = True
    use_differential_drag: bool = False
    drag_mode: DragMode = DragMode.NONE


# ---------------------------------------------------------------------------
# Mission phase schema
# ---------------------------------------------------------------------------

class MissionPhaseSchema(BaseModel):
    """Mission phase specification."""

    phase_id: str
    name: str
    phase_type: MissionPhaseType
    duration_s: float = Field(..., gt=0, description="Phase duration [s].")
    relative_model: RelativeModelMode = RelativeModelMode.KGD_QNS_J2
    guidance_law: Optional[GuidanceLawType] = None
    output_frame: RelativeFrame = RelativeFrame.QSW
    perturbation_config: PerturbationConfigSchema = Field(
        default_factory=PerturbationConfigSchema
    )
    notes: str = ""


# ---------------------------------------------------------------------------
# Scenario schema
# ---------------------------------------------------------------------------

class ScenarioCreateSchema(BaseModel):
    """Request body for scenario creation."""

    name: str
    description: str = ""
    chief: VehicleSchema
    deputy: VehicleSchema
    phases: list[MissionPhaseSchema] = Field(..., min_length=1)
    time_step_s: float = Field(default=10.0, gt=0, description="Simulation time step [s].")


class ScenarioResponseSchema(BaseModel):
    """Response body after scenario creation or retrieval."""

    scenario_id: str
    name: str
    description: str
    total_duration_s: float
    phase_count: int
    is_simulated: bool = False
