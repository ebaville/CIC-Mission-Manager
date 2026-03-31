"""
tests/unit/test_scenario_domain.py – Unit tests for Scenario and MissionPhase domain objects.
"""

import pytest

from app.core.enums import MissionPhaseType, RelativeModelMode
from app.domain.scenario import MissionPhase, PerturbationConfig, Scenario
from app.domain.states import AbsoluteOrbitalState
from app.domain.vehicle import Target, Vehicle
import numpy as np


def make_target() -> Target:
    return Target(
        vehicle_id="chief",
        name="Chief",
        mass_kg=500.0,
        initial_abs_state=AbsoluteOrbitalState(
            r_eci_m=np.array([6_778_000.0, 0.0, 0.0]),
            v_eci_mps=np.array([0.0, 7668.0, 0.0]),
        ),
    )


def make_deputy() -> Vehicle:
    return Vehicle(
        vehicle_id="deputy",
        name="Deputy",
        mass_kg=200.0,
        initial_abs_state=AbsoluteOrbitalState(
            r_eci_m=np.array([6_778_100.0, 0.0, 0.0]),
            v_eci_mps=np.array([0.0, 7668.0, 0.1]),
        ),
    )


def make_phase(duration_s: float = 3600.0) -> MissionPhase:
    return MissionPhase(
        phase_id="ph1",
        name="Homing",
        phase_type=MissionPhaseType.ROE_HOMING,
        duration_s=duration_s,
    )


class TestMissionPhase:
    def test_valid_phase(self) -> None:
        phase = make_phase()
        assert phase.duration_s == pytest.approx(3600.0)
        assert phase.relative_model == RelativeModelMode.KGD_QNS_J2

    def test_invalid_duration(self) -> None:
        with pytest.raises(ValueError):
            make_phase(duration_s=-1.0)


class TestScenario:
    def test_total_duration(self) -> None:
        scenario = Scenario(
            name="Test Scenario",
            chief=make_target(),
            deputy=make_deputy(),
            phases=[make_phase(1800.0), make_phase(3600.0)],
        )
        assert scenario.total_duration_s == pytest.approx(5400.0)

    def test_scenario_id_generated(self) -> None:
        scenario = Scenario(
            name="Test",
            chief=make_target(),
            deputy=make_deputy(),
        )
        assert scenario.scenario_id != ""
        assert len(scenario.scenario_id) == 36  # UUID format

    def test_invalid_time_step(self) -> None:
        with pytest.raises(ValueError):
            Scenario(
                name="Test",
                chief=make_target(),
                deputy=make_deputy(),
                time_step_s=0.0,
            )
