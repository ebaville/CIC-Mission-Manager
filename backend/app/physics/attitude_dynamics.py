"""
physics/attitude_dynamics.py – Attitude propagation and pointing laws.

Provides:
  AttitudePropagator      – Integrates quaternion kinematics + Euler equations.
  AttitudeLaw             – Abstract pointing law interface.
  TargetPointingLaw       – Nadir / target tracking pointing law.
  SunPointingLaw          – Sun-pointing law for power modes.
  DockingAxisAlignmentLaw – Aligns docking axis to approach corridor.

Governing equations:

  Quaternion kinematics:
    dq/dt = 0.5 * q ⊗ [omega_x, omega_y, omega_z, 0]

  Euler rigid-body equations:
    I * d(omega)/dt = tau - omega × (I * omega)

  where:
    q     = body-to-inertial quaternion (scalar-last convention).
    omega = angular velocity in body frame [rad/s].
    I     = inertia tensor in body frame [kg·m²].
    tau   = applied torque in body frame [N·m].

Assumptions:
  - Rigid body; flexible dynamics not modelled.
  - Torques include only commanded + disturbance; no actuator dynamics.

References:
  [1] Wertz, "Spacecraft Attitude Determination and Control", 1978.
  [2] Schaub & Junkins, "Analytical Mechanics of Space Systems", 3rd ed.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from app.domain.states import AbsoluteOrbitalState, AttitudeState


# ---------------------------------------------------------------------------
# Attitude propagator
# ---------------------------------------------------------------------------

class AttitudePropagator:
    """Integrates attitude quaternion and angular velocity forward in time.

    Uses SciPy RK45 for numerical integration.
    Quaternion normalisation is enforced at every step to prevent drift.
    """

    def propagate(
        self,
        state: AttitudeState,
        inertia_kgm2: NDArray[np.float64],
        torque_Nm: NDArray[np.float64],
        dt_s: float,
    ) -> AttitudeState:
        """Propagate attitude state forward by dt_s seconds.

        Args:
            state        : Current attitude state.
            inertia_kgm2 : Inertia tensor in body frame [kg·m²], shape (3, 3).
            torque_Nm    : Applied torque in body frame [N·m], shape (3,).
            dt_s         : Time step [s].

        Returns:
            New AttitudeState at epoch state.epoch_s + dt_s.
        """
        # TODO: implement quaternion + angular velocity propagation
        # Pseudo-code:
        #   y0 = concatenate(state.q_body_to_eci, state.omega_body_rads)  # shape (7,)
        #
        #   def ode(t, y):
        #       q     = y[:4]
        #       omega = y[4:]
        #       dq    = quaternion_kinematics(q, omega)  # from physics/quaternion.py
        #       domega = inv(I) @ (torque - cross(omega, I @ omega))
        #       return concatenate([dq, domega])
        #
        #   sol = solve_ivp(ode, [0, dt_s], y0, method='RK45')
        #   q_new = normalise(sol.y[:4, -1])
        #   omega_new = sol.y[4:, -1]
        #   return AttitudeState(q_new, omega_new, epoch_s=state.epoch_s + dt_s)
        raise NotImplementedError("AttitudePropagator.propagate is not yet implemented.")


# ---------------------------------------------------------------------------
# Pointing law interface
# ---------------------------------------------------------------------------

class AttitudeLaw(ABC):
    """Abstract interface for attitude pointing laws.

    Each pointing law computes a desired (reference) attitude quaternion
    given the current absolute state and optional parameters.
    Guidance and control are separate from the pointing law.
    """

    @abstractmethod
    def compute_reference_attitude(
        self,
        state: AbsoluteOrbitalState,
        epoch_s: float,
        **kwargs: object,
    ) -> NDArray[np.float64]:
        """Compute the reference quaternion for this pointing law.

        Args:
            state  : Current absolute orbital state.
            epoch_s: Current simulation time [s].
            kwargs : Law-specific parameters.

        Returns:
            Reference quaternion [q_x, q_y, q_z, q_w].
        """


# ---------------------------------------------------------------------------
# Concrete pointing laws
# ---------------------------------------------------------------------------

class TargetPointingLaw(AttitudeLaw):
    """Nadir / target-tracking pointing law.

    Aligns a specified body axis toward a target point (default: nadir).

    The pointing axis is rotated to align with the Q-direction in QSW frame
    (radial / nadir direction).
    """

    def __init__(
        self,
        pointing_axis_body: NDArray[np.float64] | None = None,
    ) -> None:
        """
        Args:
            pointing_axis_body: Body axis to point toward target.
                                Defaults to +z body axis.
        """
        if pointing_axis_body is None:
            self._axis = np.array([0.0, 0.0, 1.0])
        else:
            self._axis = np.asarray(pointing_axis_body, dtype=np.float64)

    def compute_reference_attitude(
        self,
        state: AbsoluteOrbitalState,
        epoch_s: float,
        **kwargs: object,
    ) -> NDArray[np.float64]:
        """Compute nadir-pointing quaternion.

        Returns the quaternion aligning pointing_axis_body with the nadir direction.
        """
        # TODO: compute nadir-pointing quaternion
        # Pseudo-code:
        #   nadir_eci = -state.r_eci_m / |state.r_eci_m|
        #   q = align_vector_to_direction(self._axis, nadir_eci)
        #   return q
        raise NotImplementedError(
            "TargetPointingLaw.compute_reference_attitude is not yet implemented."
        )


class SunPointingLaw(AttitudeLaw):
    """Sun-pointing law for maximum power generation.

    Aligns the solar panel normal toward the Sun direction.
    Requires Sun ephemeris (simplified Sun vector model acceptable for V1).
    """

    def compute_reference_attitude(
        self,
        state: AbsoluteOrbitalState,
        epoch_s: float,
        **kwargs: object,
    ) -> NDArray[np.float64]:
        """Compute sun-pointing quaternion.

        Returns the quaternion aligning the solar panel normal with the Sun direction.
        """
        # TODO: compute sun vector from epoch, then align panel axis
        raise NotImplementedError(
            "SunPointingLaw.compute_reference_attitude is not yet implemented."
        )


class DockingAxisAlignmentLaw(AttitudeLaw):
    """Aligns the docking axis toward the target docking port.

    Used during the final approach and docking phase.
    The docking axis is defined in Vehicle.docking_axis_body.
    """

    def compute_reference_attitude(
        self,
        state: AbsoluteOrbitalState,
        epoch_s: float,
        **kwargs: object,
    ) -> NDArray[np.float64]:
        """Compute docking-axis alignment quaternion.

        kwargs must include:
            target_abs_state: AbsoluteOrbitalState – target spacecraft state.
            target_att_state: AttitudeState – target attitude.
        """
        # TODO: compute docking alignment quaternion
        raise NotImplementedError(
            "DockingAxisAlignmentLaw.compute_reference_attitude is not yet implemented."
        )
