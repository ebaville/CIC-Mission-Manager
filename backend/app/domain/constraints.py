"""
domain/constraints.py – Operational constraint domain objects.

Constraint sets are attached to mission phases.  Evaluation logic lives in
services/phase_manager.py; these objects are pure descriptors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.core.enums import RelativeFrame


@dataclass
class KeepOutZone:
    """Spherical keep-out zone centred on the target.

    Attributes:
        radius_m : Radius of the exclusion sphere [m].
        frame    : Frame in which the centre is expressed.
        label    : Human-readable label for reporting.
    """

    radius_m: float
    frame: RelativeFrame = RelativeFrame.QSW
    label: str = "KeepOutZone"


@dataclass
class ApproachCorridor:
    """Conical approach corridor towards the target.

    Attributes:
        half_angle_rad : Half-cone angle [rad].
        axis_frame     : Frame of the corridor axis.
        axis           : Unit vector defining the corridor axis [3,].
        label          : Human-readable label.
    """

    half_angle_rad: float
    axis_frame: RelativeFrame = RelativeFrame.LOS
    axis: list[float] = field(default_factory=lambda: [0.0, 0.0, 1.0])
    label: str = "ApproachCorridor"


@dataclass
class ConstraintSet:
    """Collection of operational constraints active during a mission phase.

    Attributes:
        keep_out_zones   : List of keep-out zones.
        approach_corridors: List of approach corridors.
        max_range_m      : Maximum allowed range to target [m] (None = unlimited).
        min_range_m      : Minimum allowed range to target [m] (None = no minimum).
        max_relative_speed_mps: Maximum allowed relative speed [m/s] (None = unlimited).
    """

    keep_out_zones: list[KeepOutZone] = field(default_factory=list)
    approach_corridors: list[ApproachCorridor] = field(default_factory=list)
    max_range_m: Optional[float] = None
    min_range_m: Optional[float] = None
    max_relative_speed_mps: Optional[float] = None
