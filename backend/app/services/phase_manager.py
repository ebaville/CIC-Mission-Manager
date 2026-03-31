"""
services/phase_manager.py – Mission phase lifecycle management.

Responsibilities:
  - Track the currently active mission phase.
  - Evaluate phase-transition conditions (via event detectors).
  - Activate the next phase when conditions are met.
  - Enforce constraint checks at each step.
"""

from __future__ import annotations

from typing import Optional

from app.algorithms.event_detection import EventDetector, PhaseEndEvent
from app.domain.scenario import MissionPhase, Scenario
from app.domain.states import RelativeCartesianState


class PhaseManager:
    """Manages phase sequencing and transitions during simulation.

    Attributes:
        scenario         : The parent scenario.
        current_phase_idx: Index of the currently active phase.
        phase_start_epoch: Epoch at which the current phase started [s].
    """

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self.current_phase_idx: int = 0
        self.phase_start_epoch: float = 0.0
        self._phase_end_event: Optional[PhaseEndEvent] = None
        self._initialise_phase(0, 0.0)

    @property
    def current_phase(self) -> Optional[MissionPhase]:
        """Return the currently active MissionPhase, or None if simulation ended."""
        if self.current_phase_idx < len(self.scenario.phases):
            return self.scenario.phases[self.current_phase_idx]
        return None

    @property
    def is_finished(self) -> bool:
        """Return True when all phases have been completed."""
        return self.current_phase_idx >= len(self.scenario.phases)

    def _initialise_phase(self, idx: int, epoch_s: float) -> None:
        """Set up the phase-end event for the given phase index."""
        if idx < len(self.scenario.phases):
            phase = self.scenario.phases[idx]
            self._phase_end_event = PhaseEndEvent(
                phase_start_s=epoch_s,
                duration_s=phase.duration_s,
            )
            self.phase_start_epoch = epoch_s

    def check_and_advance(
        self,
        epoch_s: float,
        rel_state: RelativeCartesianState,
    ) -> bool:
        """Check phase-transition conditions and advance phase if needed.

        Args:
            epoch_s   : Current simulation epoch [s].
            rel_state : Current relative Cartesian state (for constraint checks).

        Returns:
            True if the phase advanced; False otherwise.
        """
        # TODO: implement phase transition logic
        # Pseudo-code:
        #   if self._phase_end_event is None or self.is_finished:
        #       return False
        #   result = self._phase_end_event.check(epoch_s)
        #   if result.triggered:
        #       self.current_phase_idx += 1
        #       self._initialise_phase(self.current_phase_idx, epoch_s)
        #       return True
        #   return False
        raise NotImplementedError("PhaseManager.check_and_advance is not yet implemented.")

    def check_constraints(
        self,
        epoch_s: float,
        rel_state: RelativeCartesianState,
    ) -> list[str]:
        """Check all constraints of the current phase.

        Returns:
            List of violated constraint descriptions (empty if all satisfied).
        """
        # TODO: implement constraint checking
        # Pseudo-code:
        #   violations = []
        #   phase = self.current_phase
        #   if phase is None:
        #       return violations
        #   for zone in phase.constraints.keep_out_zones:
        #       if rel_state.range_m < zone.radius_m:
        #           violations.append(f"Keep-out zone '{zone.label}' violated")
        #   if phase.constraints.max_range_m and rel_state.range_m > max_range:
        #       violations.append("Max range constraint violated")
        #   return violations
        raise NotImplementedError("PhaseManager.check_constraints is not yet implemented.")
