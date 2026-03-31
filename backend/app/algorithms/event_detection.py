"""
algorithms/event_detection.py – Orbital event detection utilities.

Provides:
  EventDetector   – Abstract interface for event detectors.
  PhaseEndEvent   – Triggers end-of-phase based on duration or condition.
  KeepOutViolation– Detects keep-out zone constraint violations.
  GroundContactEvent – Detects ground station contact windows.

Design rule:
  Event detectors are stateless predicates evaluated by the phase manager.
  They do not modify the simulation state.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.constraints import ConstraintSet
from app.domain.states import RelativeCartesianState


# ---------------------------------------------------------------------------
# Event result
# ---------------------------------------------------------------------------

@dataclass
class EventResult:
    """Result of an event detection check.

    Attributes:
        triggered : True if the event condition is satisfied.
        event_id  : Identifier of the triggered event.
        epoch_s   : Epoch at which the event was detected [s].
        message   : Human-readable description.
    """

    triggered: bool
    event_id: str
    epoch_s: float
    message: str = ""


# ---------------------------------------------------------------------------
# Event detector interface
# ---------------------------------------------------------------------------

class EventDetector(ABC):
    """Abstract interface for event detectors."""

    @abstractmethod
    def check(
        self,
        epoch_s: float,
        **kwargs: object,
    ) -> EventResult:
        """Evaluate the event condition at the current epoch.

        Args:
            epoch_s: Current simulation time [s].
            kwargs : Context-specific arguments (state, constraints, etc.).

        Returns:
            EventResult indicating whether the event triggered.
        """


# ---------------------------------------------------------------------------
# Concrete event detectors
# ---------------------------------------------------------------------------

class PhaseEndEvent(EventDetector):
    """Triggers when the phase duration has elapsed.

    Attributes:
        phase_start_s : Epoch at which this phase began [s].
        duration_s    : Planned phase duration [s].
    """

    def __init__(self, phase_start_s: float, duration_s: float) -> None:
        self._start = phase_start_s
        self._duration = duration_s

    def check(self, epoch_s: float, **kwargs: object) -> EventResult:
        """Check if phase duration has elapsed."""
        triggered = (epoch_s - self._start) >= self._duration
        return EventResult(
            triggered=triggered,
            event_id="PHASE_END",
            epoch_s=epoch_s,
            message=f"Phase end at epoch {epoch_s:.1f}s" if triggered else "",
        )


class KeepOutViolation(EventDetector):
    """Detects violations of keep-out zone constraints.

    Checks if the deputy has entered any keep-out sphere defined in the
    ConstraintSet.
    """

    def check(
        self,
        epoch_s: float,
        **kwargs: object,
    ) -> EventResult:
        """Check for keep-out zone violations.

        kwargs must include:
            rel_state   : RelativeCartesianState (QSW).
            constraints : ConstraintSet.
        """
        # TODO: implement keep-out zone violation check
        # Pseudo-code:
        #   rel_state   = kwargs['rel_state']
        #   constraints = kwargs['constraints']
        #   range_m = rel_state.range_m
        #   for zone in constraints.keep_out_zones:
        #       if range_m < zone.radius_m:
        #           return EventResult(True, 'KEEP_OUT_VIOLATION', epoch_s,
        #                              f"Range {range_m:.1f} m < {zone.radius_m:.1f} m")
        #   return EventResult(False, 'KEEP_OUT_VIOLATION', epoch_s)
        raise NotImplementedError("KeepOutViolation.check is not yet implemented.")
