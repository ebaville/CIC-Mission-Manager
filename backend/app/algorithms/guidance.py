"""
algorithms/guidance.py – Guidance law strategy objects.

Provides:
  GuidanceLaw          – Abstract interface for all guidance laws.
  HoldPointGuidance    – Maintain a fixed ROE hold-point.
  RoeHomingGuidance    – ROE-based homing to a target ROE state.
  ClosingGuidance      – Terminal closing toward target from short range.
  RetreatGuidance      – Safe retreat / abort manoeuvre.

Design rules:
  - Guidance laws are phase-aware; they do not know about the sim engine.
  - Guidance produces control COMMANDS (delta-v requests or ROE targets).
  - Controllers convert commands into force/torque; this is a separate step.
  - Guidance must not merge with control (anti-pattern, per AGENTS.md).

References:
  [1] D'Amico, PhD thesis 2010.
  [2] Sullivan, Grimberg, D'Amico, "Comprehensive Survey and Assessment of
      Spacecraft Relative Motion Dynamics Models", JGCD 2017.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from app.domain.states import QnsRoeState, RelativeCartesianState


# ---------------------------------------------------------------------------
# Guidance command
# ---------------------------------------------------------------------------

@dataclass
class GuidanceCommand:
    """Output of a guidance law.

    Attributes:
        delta_v_qsw_mps : Requested delta-v in QSW frame [m/s], shape (3,).
                          Zero vector means no manoeuvre requested.
        target_roe      : Target ROE state for the next phase (optional).
        epoch_s         : Command epoch [s].
    """

    delta_v_qsw_mps: NDArray[np.float64]
    target_roe: QnsRoeState | None = None
    epoch_s: float = 0.0


# ---------------------------------------------------------------------------
# Guidance interface
# ---------------------------------------------------------------------------

class GuidanceLaw(ABC):
    """Abstract interface for guidance laws.

    Each guidance law must implement compute_command().
    """

    @abstractmethod
    def compute_command(
        self,
        current_roe: QnsRoeState,
        current_rel_qsw: RelativeCartesianState,
        epoch_s: float,
        **kwargs: object,
    ) -> GuidanceCommand:
        """Compute guidance command for the current state.

        Args:
            current_roe     : Current QNS ROE state.
            current_rel_qsw : Current relative QSW Cartesian state.
            epoch_s         : Current simulation time [s].
            kwargs          : Law-specific parameters.

        Returns:
            GuidanceCommand with delta-v request.
        """


# ---------------------------------------------------------------------------
# Concrete guidance laws
# ---------------------------------------------------------------------------

class HoldPointGuidance(GuidanceLaw):
    """Hold a fixed ROE target state.

    Generates small corrective delta-v manoeuvres to maintain a desired
    relative ROE configuration in the presence of perturbations.

    Guidance strategy:
      Compare current ROE to target ROE; if deviation exceeds a dead-band,
      compute a corrective manoeuvre using the inverse of the Gauss variational
      equations or an ROE control mapping.
    """

    def __init__(
        self,
        target_roe: QnsRoeState,
        dead_band_roe: float = 1e-5,
    ) -> None:
        self._target_roe = target_roe
        self._dead_band = dead_band_roe

    def compute_command(
        self,
        current_roe: QnsRoeState,
        current_rel_qsw: RelativeCartesianState,
        epoch_s: float,
        **kwargs: object,
    ) -> GuidanceCommand:
        """Compute hold-point maintenance manoeuvre.

        Returns zero delta-v if within dead-band; corrective delta-v otherwise.
        """
        # TODO: implement hold-point guidance
        # Pseudo-code:
        #   error_vec = target_roe.as_vector() - current_roe.as_vector()
        #   if norm(error_vec) < dead_band:
        #       return GuidanceCommand(delta_v=zeros(3), epoch_s=epoch_s)
        #   delta_v = compute_roe_control_delta_v(error_vec, chief_elements)
        #   return GuidanceCommand(delta_v, target_roe=target_roe, epoch_s=epoch_s)
        raise NotImplementedError("HoldPointGuidance.compute_command is not yet implemented.")


class RoeHomingGuidance(GuidanceLaw):
    """ROE-based homing guidance for far-range rendezvous.

    Plans a sequence of impulsive manoeuvres to drive the ROE state from the
    initial configuration to a target ROE configuration using the ROE control
    mapping (Gauss variational equations in ROE form).
    """

    def __init__(
        self,
        target_roe: QnsRoeState,
    ) -> None:
        self._target_roe = target_roe

    def compute_command(
        self,
        current_roe: QnsRoeState,
        current_rel_qsw: RelativeCartesianState,
        epoch_s: float,
        **kwargs: object,
    ) -> GuidanceCommand:
        """Compute ROE-based homing manoeuvre.

        Plans transfer using the ROE control input matrix Gamma.
        """
        # TODO: implement ROE homing manoeuvre planning
        # Pseudo-code:
        #   chief_elements = kwargs['chief_elements']
        #   Gamma = compute_roe_control_matrix(chief_elements, n_manoeuvres)
        #   delta_v = lstsq(Gamma, target_roe - current_roe)
        #   return GuidanceCommand(delta_v, target_roe=target_roe, epoch_s=epoch_s)
        raise NotImplementedError(
            "RoeHomingGuidance.compute_command is not yet implemented."
        )


class ClosingGuidance(GuidanceLaw):
    """Terminal closing guidance for short-range proximity operations.

    Uses Cartesian relative state (QSW) for the final approach.
    Generates velocity-to-be-gained commands toward the approach corridor axis.
    """

    def __init__(self, approach_speed_mps: float = 0.1) -> None:
        self._approach_speed = approach_speed_mps

    def compute_command(
        self,
        current_roe: QnsRoeState,
        current_rel_qsw: RelativeCartesianState,
        epoch_s: float,
        **kwargs: object,
    ) -> GuidanceCommand:
        """Compute closing guidance delta-v command."""
        # TODO: implement closing guidance
        # Pseudo-code:
        #   range_m = current_rel_qsw.range_m
        #   los_unit = current_rel_qsw.rho_m / range_m
        #   v_desired = -approach_speed * los_unit
        #   delta_v = v_desired - current_rel_qsw.rho_dot_mps
        #   return GuidanceCommand(delta_v, epoch_s=epoch_s)
        raise NotImplementedError(
            "ClosingGuidance.compute_command is not yet implemented."
        )


class RetreatGuidance(GuidanceLaw):
    """Safe retreat / abort guidance.

    Generates a manoeuvre to drive the relative state away from the target
    along a defined retreat corridor.
    """

    def __init__(self, retreat_speed_mps: float = 0.5) -> None:
        self._retreat_speed = retreat_speed_mps

    def compute_command(
        self,
        current_roe: QnsRoeState,
        current_rel_qsw: RelativeCartesianState,
        epoch_s: float,
        **kwargs: object,
    ) -> GuidanceCommand:
        """Compute retreat manoeuvre delta-v command."""
        # TODO: implement retreat guidance
        # Pseudo-code:
        #   los_unit = current_rel_qsw.rho_m / current_rel_qsw.range_m
        #   delta_v = retreat_speed * los_unit   # fly away from target
        #   return GuidanceCommand(delta_v, epoch_s=epoch_s)
        raise NotImplementedError(
            "RetreatGuidance.compute_command is not yet implemented."
        )
