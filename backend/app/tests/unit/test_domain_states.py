"""
tests/unit/test_domain_states.py – Unit tests for domain state objects.

Tests that domain state objects are correctly constructed, validated,
and provide correct derived properties.

These tests cover the structural layer only; no physics equations are exercised.
"""

import math

import numpy as np
import pytest

from app.domain.states import (
    AbsoluteOrbitalState,
    AttitudeState,
    KeplerianElements,
    MeasurementPacket,
    QnsRoeState,
    RelativeCartesianState,
    RelativeMotionSnapshot,
)
from app.core.enums import RelativeFrame, RoeVariant


# ---------------------------------------------------------------------------
# AbsoluteOrbitalState tests
# ---------------------------------------------------------------------------

class TestAbsoluteOrbitalState:
    def test_creation_valid(self) -> None:
        r = np.array([6_778_000.0, 0.0, 0.0])
        v = np.array([0.0, 7668.0, 0.0])
        state = AbsoluteOrbitalState(r_eci_m=r, v_eci_mps=v, epoch_s=0.0)
        assert state.radius_m == pytest.approx(6_778_000.0)
        assert state.speed_mps == pytest.approx(7668.0)

    def test_radius_property(self) -> None:
        r = np.array([3000.0, 4000.0, 0.0])
        v = np.zeros(3)
        state = AbsoluteOrbitalState(r_eci_m=r, v_eci_mps=v)
        assert state.radius_m == pytest.approx(5000.0)

    def test_invalid_r_shape(self) -> None:
        with pytest.raises(ValueError):
            AbsoluteOrbitalState(
                r_eci_m=np.array([1.0, 2.0]),   # wrong shape
                v_eci_mps=np.zeros(3),
            )

    def test_invalid_v_shape(self) -> None:
        with pytest.raises(ValueError):
            AbsoluteOrbitalState(
                r_eci_m=np.zeros(3),
                v_eci_mps=np.array([1.0, 2.0, 3.0, 4.0]),  # wrong shape
            )


# ---------------------------------------------------------------------------
# KeplerianElements tests
# ---------------------------------------------------------------------------

class TestKeplerianElements:
    def test_creation_valid(self) -> None:
        oe = KeplerianElements(
            a_m=6_778_000.0,
            e=0.001,
            i_rad=0.9,
            raan_rad=1.2,
            omega_rad=0.5,
            m_rad=1.0,
        )
        vec = oe.as_vector()
        assert vec.shape == (6,)
        assert vec[0] == pytest.approx(6_778_000.0)

    def test_invalid_sma(self) -> None:
        with pytest.raises(ValueError):
            KeplerianElements(a_m=-1.0, e=0.0, i_rad=0.0,
                              raan_rad=0.0, omega_rad=0.0, m_rad=0.0)

    def test_invalid_eccentricity(self) -> None:
        with pytest.raises(ValueError):
            KeplerianElements(a_m=7e6, e=1.5, i_rad=0.0,
                              raan_rad=0.0, omega_rad=0.0, m_rad=0.0)

    def test_invalid_inclination(self) -> None:
        with pytest.raises(ValueError):
            KeplerianElements(a_m=7e6, e=0.0, i_rad=4.0,  # > pi
                              raan_rad=0.0, omega_rad=0.0, m_rad=0.0)


# ---------------------------------------------------------------------------
# AttitudeState tests
# ---------------------------------------------------------------------------

class TestAttitudeState:
    def test_identity_quaternion(self) -> None:
        q = np.array([0.0, 0.0, 0.0, 1.0])  # scalar-last identity
        omega = np.zeros(3)
        state = AttitudeState(q_body_to_eci=q, omega_body_rads=omega)
        assert state.is_normalised

    def test_non_unit_quaternion(self) -> None:
        q = np.array([0.1, 0.0, 0.0, 1.0])  # not normalised
        omega = np.zeros(3)
        state = AttitudeState(q_body_to_eci=q, omega_body_rads=omega)
        assert not state.is_normalised

    def test_invalid_quaternion_shape(self) -> None:
        with pytest.raises(ValueError):
            AttitudeState(
                q_body_to_eci=np.array([0.0, 0.0, 1.0]),  # 3-vector, not 4
                omega_body_rads=np.zeros(3),
            )


# ---------------------------------------------------------------------------
# QnsRoeState tests
# ---------------------------------------------------------------------------

class TestQnsRoeState:
    def _make_roe(self) -> QnsRoeState:
        return QnsRoeState(
            delta_a=0.0,
            delta_lambda=0.001,
            delta_ex=0.0001,
            delta_ey=0.0,
            delta_ix=0.0002,
            delta_iy=0.0,
            chief_a_m=6_778_000.0,
        )

    def test_as_vector(self) -> None:
        roe = self._make_roe()
        vec = roe.as_vector()
        assert vec.shape == (6,)
        assert vec[1] == pytest.approx(0.001)

    def test_from_vector_roundtrip(self) -> None:
        roe = self._make_roe()
        vec = roe.as_vector()
        roe2 = QnsRoeState.from_vector(vec, chief_a_m=roe.chief_a_m)
        assert roe2.delta_a == pytest.approx(roe.delta_a)
        assert roe2.delta_lambda == pytest.approx(roe.delta_lambda)

    def test_relative_eccentricity_magnitude(self) -> None:
        roe = QnsRoeState(
            delta_a=0.0, delta_lambda=0.0,
            delta_ex=3.0, delta_ey=4.0,
            delta_ix=0.0, delta_iy=0.0,
            chief_a_m=7e6,
        )
        assert roe.relative_eccentricity_magnitude == pytest.approx(5.0)

    def test_from_vector_wrong_length(self) -> None:
        with pytest.raises(ValueError):
            QnsRoeState.from_vector(np.zeros(5), chief_a_m=7e6)


# ---------------------------------------------------------------------------
# RelativeCartesianState tests
# ---------------------------------------------------------------------------

class TestRelativeCartesianState:
    def test_range(self) -> None:
        state = RelativeCartesianState(
            rho_m=np.array([300.0, 400.0, 0.0]),
            rho_dot_mps=np.zeros(3),
            frame=RelativeFrame.QSW,
        )
        assert state.range_m == pytest.approx(500.0)

    def test_invalid_rho_shape(self) -> None:
        with pytest.raises(ValueError):
            RelativeCartesianState(
                rho_m=np.array([1.0, 2.0]),
                rho_dot_mps=np.zeros(3),
                frame=RelativeFrame.QSW,
            )


# ---------------------------------------------------------------------------
# MeasurementPacket tests
# ---------------------------------------------------------------------------

class TestMeasurementPacket:
    def test_valid_packet(self) -> None:
        pkt = MeasurementPacket(
            sensor_id="rae_sensor",
            epoch_s=100.0,
            values=np.array([500.0, 0.1, 0.05]),
            covariance=np.diag([1.0, 0.001, 0.001]),
        )
        assert pkt.is_valid
        assert pkt.values.shape == (3,)
        assert pkt.covariance.shape == (3, 3)

    def test_covariance_shape_mismatch(self) -> None:
        with pytest.raises(ValueError):
            MeasurementPacket(
                sensor_id="s",
                epoch_s=0.0,
                values=np.array([1.0, 2.0]),
                covariance=np.eye(3),   # shape mismatch: (3,3) vs len(values)=2
            )
