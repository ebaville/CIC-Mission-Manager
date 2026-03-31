"""
physics/orbital_elements.py – Orbital element conversion utilities.

Provides:
  OsculatingElements    – Alias and construction helpers for KeplerianElements.
  ElementConverter      – Cartesian ↔ Keplerian conversion interface and implementation.

Governing equations:
  Cartesian → Keplerian via angular momentum, node vector, eccentricity vector.
  Keplerian → Cartesian via perifocal frame transformation.

Assumptions:
  - Two-body problem; perturbations not accounted for in conversion.
  - Osculating elements at the instant of conversion.

Validity domain:
  - Elliptic orbits (0 ≤ e < 1).
  - For near-circular orbits (e < 1e-6), omega is numerically ill-conditioned;
    use quasi-nonsingular elements instead.

Units:
  - Input/output: SI (metres, radians).

References:
  [1] Bate, Mueller, White, "Fundamentals of Astrodynamics", 1971, Chap. 2.
  [2] Vallado, 4th ed., Chap. 2.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from app.core.conventions import MU_EARTH_M3S2
from app.domain.states import AbsoluteOrbitalState, KeplerianElements


# ---------------------------------------------------------------------------
# Conversion interface
# ---------------------------------------------------------------------------

class ElementConverter(ABC):
    """Abstract interface for orbital element conversion."""

    @abstractmethod
    def cartesian_to_keplerian(
        self, state: AbsoluteOrbitalState
    ) -> KeplerianElements:
        """Convert Cartesian ECI state to osculating Keplerian elements."""

    @abstractmethod
    def keplerian_to_cartesian(
        self, elements: KeplerianElements
    ) -> AbsoluteOrbitalState:
        """Convert Keplerian elements to Cartesian ECI state."""


# ---------------------------------------------------------------------------
# Standard implementation
# ---------------------------------------------------------------------------

class StandardElementConverter(ElementConverter):
    """Standard analytical Cartesian ↔ Keplerian conversion.

    Uses the classical angular-momentum / eccentricity-vector formulation.
    Valid for elliptic orbits with non-zero inclination and eccentricity.
    Numerically ill-conditioned near circular (e → 0) or equatorial (i → 0) orbits.
    """

    def __init__(self, mu_m3s2: float = MU_EARTH_M3S2) -> None:
        self._mu = mu_m3s2

    def cartesian_to_keplerian(
        self, state: AbsoluteOrbitalState
    ) -> KeplerianElements:
        """Convert Cartesian ECI state to osculating Keplerian elements.

        Algorithm:
          1. Compute specific angular momentum h = r × v.
          2. Compute node vector n = k × h (k = ECI z-axis unit vector).
          3. Compute eccentricity vector e_vec = (v × h)/mu - r_hat.
          4. Derive orbital elements from h, n, e_vec.
          5. Compute mean anomaly from eccentric anomaly via Kepler's equation.
        """
        # TODO: implement full Cartesian → Keplerian conversion
        # Pseudo-code:
        #
        #   r = state.r_eci_m
        #   v = state.v_eci_mps
        #   r_norm = |r|;  v_norm = |v|
        #
        #   h_vec = cross(r, v)       # specific angular momentum
        #   h_norm = |h_vec|
        #   n_vec = cross([0,0,1], h_vec)   # ascending node vector
        #   n_norm = |n_vec|
        #
        #   e_vec = (1/mu)*((v_norm^2 - mu/r_norm)*r - dot(r,v)*v)
        #   e = |e_vec|               # eccentricity
        #
        #   energy = v_norm^2/2 - mu/r_norm
        #   a = -mu / (2*energy)      # semi-major axis
        #
        #   i = arccos(h_vec[2] / h_norm)
        #   RAAN = arccos(n_vec[0] / n_norm)
        #   if n_vec[1] < 0: RAAN = 2*pi - RAAN
        #
        #   omega = arccos(dot(n_vec, e_vec) / (n_norm * e))
        #   if e_vec[2] < 0: omega = 2*pi - omega
        #
        #   nu = arccos(dot(e_vec, r) / (e * r_norm))  # true anomaly
        #   if dot(r, v) < 0: nu = 2*pi - nu
        #
        #   E = 2*arctan(sqrt((1-e)/(1+e)) * tan(nu/2))  # eccentric anomaly
        #   M = E - e*sin(E)   # mean anomaly
        #
        #   return KeplerianElements(a, e, i, RAAN, omega, M)
        raise NotImplementedError(
            "StandardElementConverter.cartesian_to_keplerian is not yet implemented."
        )

    def keplerian_to_cartesian(
        self, elements: KeplerianElements
    ) -> AbsoluteOrbitalState:
        """Convert Keplerian elements to Cartesian ECI state.

        Algorithm:
          1. Solve Kepler's equation M = E - e*sin(E) for eccentric anomaly E.
          2. Compute true anomaly nu from E.
          3. Compute position and velocity in perifocal frame.
          4. Rotate perifocal frame to ECI using Euler angles (omega, i, RAAN).
        """
        # TODO: implement full Keplerian → Cartesian conversion
        # Pseudo-code:
        #
        #   M = elements.m_rad
        #   e = elements.e
        #   E = solve_kepler_equation(M, e)   # Newton iteration
        #
        #   nu = 2 * arctan2(sqrt(1+e)*sin(E/2), sqrt(1-e)*cos(E/2))
        #
        #   r_peri  = a*(1-e^2) / (1 + e*cos(nu))
        #   r_perifocal = r_peri * [cos(nu), sin(nu), 0]
        #   v_peri = sqrt(mu / (a*(1-e^2)))
        #   v_perifocal = v_peri * [-sin(nu), e + cos(nu), 0]
        #
        #   R = rotation_matrix_peri_to_eci(elements.omega_rad,
        #                                   elements.i_rad,
        #                                   elements.raan_rad)
        #   r_eci = R @ r_perifocal
        #   v_eci = R @ v_perifocal
        #
        #   return AbsoluteOrbitalState(r_eci, v_eci, elements.epoch_s)
        raise NotImplementedError(
            "StandardElementConverter.keplerian_to_cartesian is not yet implemented."
        )


def solve_kepler_equation(mean_anomaly_rad: float, eccentricity: float) -> float:
    """Solve Kepler's equation M = E - e*sin(E) for eccentric anomaly E.

    Uses Newton–Raphson iteration.

    Args:
        mean_anomaly_rad: Mean anomaly M [rad].
        eccentricity    : Orbit eccentricity e, in [0, 1).

    Returns:
        Eccentric anomaly E [rad].

    Validity:
        Elliptic orbits only (0 ≤ e < 1).
        Converges in < 10 iterations for typical orbits.
    """
    # TODO: implement Newton-Raphson iteration
    # Pseudo-code:
    #   E = M  (initial guess)
    #   for _ in range(max_iter):
    #     dE = (M - E + e*sin(E)) / (1 - e*cos(E))
    #     E += dE
    #     if |dE| < tol: break
    #   return E
    raise NotImplementedError("solve_kepler_equation is not yet implemented.")
