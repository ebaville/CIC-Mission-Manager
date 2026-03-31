"""
domain/scenario.py – Scenario and MissionPhase domain objects.

A Scenario is the top-level user abstraction.
It contains an ordered list of MissionPhases; each phase specifies which
physics models, guidance laws, sensors, and constraints are active.

No framework logic lives here.  All values are SI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import uuid

from app.core.enums import (
    DragMode,
    GuidanceLawType,
    MissionPhaseType,
    RelativeFrame,
    RelativeModelMode,
)
from app.domain.constraints import ConstraintSet
from app.domain.sensor import Sensor
from app.domain.vehicle import Target, Vehicle


@dataclass
class PerturbationConfig:
    """Perturbation model configuration for a mission phase.

    Attributes:
        use_j2              : Include J2 zonal harmonic in propagation.
        use_differential_drag: Include differential drag in relative STM.
        drag_mode           : Drag modelling approach (requires use_differential_drag).
        use_srp             : Include solar radiation pressure.
    """

    use_j2: bool = True
    use_differential_drag: bool = False
    drag_mode: DragMode = DragMode.NONE
    use_srp: bool = False


@dataclass
class MissionPhase:
    """A single phase of a proximity operations mission.

    A phase is the fundamental unit of scenario structure.  Different phases
    may use different guidance laws, relative frames, sensors, and constraints.

    Attributes:
        phase_id          : Unique identifier string.
        name              : Human-readable name.
        phase_type        : High-level phase type label.
        duration_s        : Phase duration [s].
        relative_model    : Relative dynamics model to use.
        guidance_law      : Guidance law type active in this phase.
        active_sensors    : List of sensors active in this phase.
        constraints       : Operational constraints active in this phase.
        perturbation_config: Perturbation model configuration.
        output_frame      : Primary output frame for relative state reporting.
        notes             : Free-text description.
    """

    phase_id: str
    name: str
    phase_type: MissionPhaseType
    duration_s: float
    relative_model: RelativeModelMode = RelativeModelMode.KGD_QNS_J2
    guidance_law: Optional[GuidanceLawType] = None
    active_sensors: list[Sensor] = field(default_factory=list)
    constraints: ConstraintSet = field(default_factory=ConstraintSet)
    perturbation_config: PerturbationConfig = field(default_factory=PerturbationConfig)
    output_frame: RelativeFrame = RelativeFrame.QSW
    notes: str = ""

    def __post_init__(self) -> None:
        if self.duration_s <= 0.0:
            raise ValueError("Phase duration must be positive.")


@dataclass
class Scenario:
    """Top-level mission scenario.

    A Scenario ties together the vehicles, phases, and ground stations into
    a single simulation specification.

    Attributes:
        scenario_id   : Unique identifier (auto-generated if not provided).
        name          : Human-readable scenario name.
        description   : Free-text description.
        chief         : Target / chief spacecraft.
        deputy        : Chaser / deputy spacecraft.
        phases        : Ordered list of mission phases.
        ground_stations: List of ground stations for visibility analysis.
        time_step_s   : Simulation integration time step [s].
        created_at_iso: ISO-8601 creation timestamp string.
    """

    name: str
    chief: Target
    deputy: Vehicle
    phases: list[MissionPhase] = field(default_factory=list)
    ground_stations: list = field(default_factory=list)
    time_step_s: float = 10.0
    description: str = ""
    created_at_iso: str = ""
    scenario_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.time_step_s <= 0.0:
            raise ValueError("Simulation time step must be positive.")

    @property
    def total_duration_s(self) -> float:
        """Sum of all phase durations [s]."""
        return sum(p.duration_s for p in self.phases)
