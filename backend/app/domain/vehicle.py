"""
domain/vehicle.py – Vehicle and Target domain objects.

Defines the spacecraft (chaser deputy and target chief) as pure data containers.
All physical quantities are in SI units.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from app.domain.states import AbsoluteOrbitalState, AttitudeState


@dataclass
class Vehicle:
    """Generic spacecraft representation.

    Attributes:
        vehicle_id        : Unique string identifier.
        name              : Human-readable label.
        mass_kg           : Spacecraft wet mass [kg].
        inertia_tensor_kgm2: Inertia tensor in body frame [kg·m²], shape (3, 3).
        initial_abs_state : Initial absolute orbital state in ECI [m, m/s].
        initial_att_state : Initial attitude state (optional).
        drag_area_m2      : Reference area for atmospheric drag [m²].
        drag_coeff        : Drag coefficient Cd [-].
        srp_area_m2       : Reference area for solar radiation pressure [m²].
        srp_coeff         : SRP coefficient Cr [-].
        docking_axis_body : Unit vector of docking axis in body frame (optional).
    """

    vehicle_id: str
    name: str
    mass_kg: float
    initial_abs_state: AbsoluteOrbitalState
    inertia_tensor_kgm2: NDArray[np.float64] = field(
        default_factory=lambda: np.eye(3, dtype=np.float64)
    )
    initial_att_state: Optional[AttitudeState] = None
    drag_area_m2: float = 1.0
    drag_coeff: float = 2.2
    srp_area_m2: float = 1.0
    srp_coeff: float = 1.5
    docking_axis_body: Optional[NDArray[np.float64]] = None

    def __post_init__(self) -> None:
        if self.mass_kg <= 0.0:
            raise ValueError("Vehicle mass must be positive.")
        self.inertia_tensor_kgm2 = np.asarray(
            self.inertia_tensor_kgm2, dtype=np.float64
        )
        if self.inertia_tensor_kgm2.shape != (3, 3):
            raise ValueError("Inertia tensor must be 3×3.")


@dataclass
class Target(Vehicle):
    """Target spacecraft (chief / non-manoeuvring reference).

    Extends Vehicle with a flag indicating that this is the reference orbit
    around which relative dynamics are computed.
    """

    is_reference: bool = True
