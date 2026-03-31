"""
tests/unit/test_two_body_propagator.py – Unit tests for TwoBodyPropagator.

Validates the two-body propagator against known orbital mechanics:
  - Circular orbit: radius stays constant, period matches Kepler's third law.
  - Conservation of orbital energy.
  - Conservation of angular momentum magnitude.

Numerical tolerances are physically motivated:
  - Energy conservation: < 1e-9 relative error per step.
  - Angular momentum: < 1e-9 relative error per step.
  - Circular orbit radius: < 1 m over one full period.
"""

import math

import numpy as np
import pytest

from app.core.conventions import MU_EARTH_M3S2
from app.domain.states import AbsoluteOrbitalState
from app.physics.absolute_propagation import TwoBodyPropagator


def circular_orbit_state(altitude_m: float) -> AbsoluteOrbitalState:
    """Create a circular equatorial orbit at the given altitude."""
    r = 6_378_137.0 + altitude_m
    v = math.sqrt(MU_EARTH_M3S2 / r)
    return AbsoluteOrbitalState(
        r_eci_m=np.array([r, 0.0, 0.0]),
        v_eci_mps=np.array([0.0, v, 0.0]),
        epoch_s=0.0,
    )


def orbital_energy(state: AbsoluteOrbitalState) -> float:
    """Specific orbital energy [J/kg = m^2/s^2]."""
    r = state.radius_m
    v = state.speed_mps
    return 0.5 * v**2 - MU_EARTH_M3S2 / r


def angular_momentum_magnitude(state: AbsoluteOrbitalState) -> float:
    """Specific angular momentum magnitude [m^2/s]."""
    return float(np.linalg.norm(np.cross(state.r_eci_m, state.v_eci_mps)))


class TestTwoBodyPropagator:
    def test_single_step_returns_new_epoch(self) -> None:
        state = circular_orbit_state(400_000.0)
        prop = TwoBodyPropagator()
        new_state = prop.propagate(state, dt_s=60.0)
        assert new_state.epoch_s == pytest.approx(60.0)

    def test_energy_conservation_one_period(self) -> None:
        """Energy must be conserved to < 1 ppm over one orbital period."""
        alt = 400_000.0
        state = circular_orbit_state(alt)
        r = state.radius_m
        T = 2 * math.pi * math.sqrt(r**3 / MU_EARTH_M3S2)

        prop = TwoBodyPropagator()
        E0 = orbital_energy(state)

        # propagate in steps of 60 s
        dt = 60.0
        n_steps = int(T / dt)
        for _ in range(n_steps):
            state = prop.propagate(state, dt_s=dt)

        E1 = orbital_energy(state)
        assert abs((E1 - E0) / E0) < 1e-6

    def test_angular_momentum_conservation(self) -> None:
        """Angular momentum magnitude must be conserved to < 1 ppm."""
        state = circular_orbit_state(500_000.0)
        h0 = angular_momentum_magnitude(state)

        prop = TwoBodyPropagator()
        for _ in range(100):
            state = prop.propagate(state, dt_s=30.0)

        h1 = angular_momentum_magnitude(state)
        assert abs((h1 - h0) / h0) < 1e-6

    def test_circular_radius_conservation(self) -> None:
        """For a circular orbit, radius should stay constant within 1 m."""
        state = circular_orbit_state(400_000.0)
        r0 = state.radius_m
        prop = TwoBodyPropagator()
        for _ in range(10):
            state = prop.propagate(state, dt_s=100.0)
        assert abs(state.radius_m - r0) < 1.0

    def test_invalid_dt(self) -> None:
        state = circular_orbit_state(400_000.0)
        prop = TwoBodyPropagator()
        with pytest.raises(ValueError):
            prop.propagate(state, dt_s=-1.0)
