"""
physics/absolute_propagation.py – Absolute orbit propagation.

Provides:
  OrbitPropagator  – Abstract interface for orbit propagators.
  TwoBodyPropagator – Two-body (Keplerian) propagator using SciPy RK45.
  J2Propagator     – Two-body + J2 zonal harmonic propagator (stub).

Governing equations:
  dr/dt = v
  dv/dt = -mu/|r|^3 * r + a_pert + a_ctrl

where:
  r     = ECI position [m]
  v     = ECI velocity [m/s]
  mu    = Earth gravitational parameter [m^3/s^2]
  a_pert= perturbation acceleration [m/s^2]
  a_ctrl= control acceleration [m/s^2]

Validity domain:
  Two-body: circular or elliptic Earth orbits, no perturbations.
  J2: LEO to GEO, dominant secular perturbation included.

References:
  [1] Montenbruck & Gill, "Satellite Orbits", 2000, Chap. 3.
  [2] Vallado, "Fundamentals of Astrodynamics and Applications", 4th ed., Chap. 9.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp  # type: ignore[import]

from app.core.conventions import J2_EARTH, MU_EARTH_M3S2, R_EARTH_M
from app.domain.states import AbsoluteOrbitalState


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

class OrbitPropagator(ABC):
    """Abstract interface for orbit propagators.

    All propagators must implement propagate(); the choice of integrator,
    perturbation model, and step size is an implementation detail.
    """

    @abstractmethod
    def propagate(
        self,
        state: AbsoluteOrbitalState,
        dt_s: float,
        control_accel_mps2: Optional[NDArray[np.float64]] = None,
    ) -> AbsoluteOrbitalState:
        """Propagate state forward by dt_s seconds.

        Args:
            state              : Current absolute orbital state.
            dt_s               : Propagation time step [s].  Must be > 0.
            control_accel_mps2 : Optional control acceleration in ECI [m/s^2].

        Returns:
            New AbsoluteOrbitalState at epoch state.epoch_s + dt_s.
        """


# ---------------------------------------------------------------------------
# Two-body propagator
# ---------------------------------------------------------------------------

class TwoBodyPropagator(OrbitPropagator):
    """Two-body (Keplerian) orbit propagator.

    Uses SciPy RK45 numerical integration with adaptive step size.
    No perturbations are modelled.

    Validity domain:
      - Circular to highly elliptic Earth orbits.
      - Accurate for short arcs; secular drift neglected.
    """

    def __init__(
        self,
        mu_m3s2: float = MU_EARTH_M3S2,
        rtol: float = 1e-10,
        atol: float = 1e-12,
    ) -> None:
        self._mu = mu_m3s2
        self._rtol = rtol
        self._atol = atol

    def _ode(
        self,
        t: float,  # noqa: ARG002 – time unused in autonomous two-body
        y: NDArray[np.float64],
        control_accel: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Two-body equations of motion.

        State vector: y = [r_x, r_y, r_z, v_x, v_y, v_z]

        dy/dt = [v_x, v_y, v_z, a_x, a_y, a_z]
        where a = -mu/r^3 * r + control_accel
        """
        r = y[:3]
        v = y[3:]
        r_norm = np.linalg.norm(r)
        a_grav = -self._mu / r_norm**3 * r
        a_total = a_grav + control_accel
        return np.concatenate([v, a_total])

    def propagate(
        self,
        state: AbsoluteOrbitalState,
        dt_s: float,
        control_accel_mps2: Optional[NDArray[np.float64]] = None,
    ) -> AbsoluteOrbitalState:
        """Propagate forward by dt_s seconds using RK45."""
        if dt_s <= 0.0:
            raise ValueError("dt_s must be positive.")

        if control_accel_mps2 is None:
            control_accel_mps2 = np.zeros(3, dtype=np.float64)

        y0 = np.concatenate([state.r_eci_m, state.v_eci_mps])

        sol = solve_ivp(
            fun=self._ode,
            t_span=(0.0, dt_s),
            y0=y0,
            method="RK45",
            args=(control_accel_mps2,),
            rtol=self._rtol,
            atol=self._atol,
            dense_output=False,
        )

        if not sol.success:
            raise RuntimeError(f"TwoBodyPropagator integration failed: {sol.message}")

        y_final = sol.y[:, -1]
        return AbsoluteOrbitalState(
            r_eci_m=y_final[:3],
            v_eci_mps=y_final[3:],
            epoch_s=state.epoch_s + dt_s,
        )


# ---------------------------------------------------------------------------
# J2 propagator (stub)
# ---------------------------------------------------------------------------

class J2Propagator(OrbitPropagator):
    """Two-body + J2 zonal harmonic propagator.

    Adds the oblate-Earth J2 acceleration to the two-body model.

    J2 acceleration in ECI:
      a_J2 = (3/2) * J2 * mu * Re^2 / r^5 *
             [ x*(5*z^2/r^2 - 1),
               y*(5*z^2/r^2 - 1),
               z*(5*z^2/r^2 - 3) ]

    Validity domain:
      LEO to GEO.  Higher-order zonals not included.

    Status: stub – pseudo-code only, not yet numerically validated.
    """

    def __init__(
        self,
        mu_m3s2: float = MU_EARTH_M3S2,
        j2: float = J2_EARTH,
        r_earth_m: float = R_EARTH_M,
        rtol: float = 1e-10,
        atol: float = 1e-12,
    ) -> None:
        self._mu = mu_m3s2
        self._j2 = j2
        self._re = r_earth_m
        self._rtol = rtol
        self._atol = atol

    def _j2_accel(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute J2 acceleration vector [m/s^2]."""
        # TODO: implement J2 acceleration
        # Pseudo-code:
        #   r_norm = |r|
        #   factor = 1.5 * J2 * mu * Re^2 / r_norm^5
        #   z2_r2  = (r[2] / r_norm)^2
        #   return factor * [r[0]*(5*z2_r2 - 1),
        #                    r[1]*(5*z2_r2 - 1),
        #                    r[2]*(5*z2_r2 - 3)]
        raise NotImplementedError("J2Propagator is not yet implemented.")

    def _ode(
        self,
        t: float,  # noqa: ARG002
        y: NDArray[np.float64],
        control_accel: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Two-body + J2 equations of motion."""
        r = y[:3]
        v = y[3:]
        r_norm = np.linalg.norm(r)
        a_grav = -self._mu / r_norm**3 * r
        a_j2 = self._j2_accel(r)
        a_total = a_grav + a_j2 + control_accel
        return np.concatenate([v, a_total])

    def propagate(
        self,
        state: AbsoluteOrbitalState,
        dt_s: float,
        control_accel_mps2: Optional[NDArray[np.float64]] = None,
    ) -> AbsoluteOrbitalState:
        """Propagate forward by dt_s seconds using RK45 with J2."""
        raise NotImplementedError("J2Propagator is not yet implemented.")
