"""
physics/roe_definitions.py – ROE state definitions and conversion from absolute states.

Provides:
  RelativeStateDefinition  – Abstract interface.
  QnsRoeDefinition         – Quasi-nonsingular ROE from/to absolute states.

Governing equations (Koenig–Guffanti–D'Amico 2017, Table I):
  delta_a      = (a_d - a_c) / a_c
  delta_lambda = (M_d + omega_d) - (M_c + omega_c) + (Omega_d - Omega_c)*cos(i_c)
  delta_ex     = e_d*cos(omega_d) - e_c*cos(omega_c)
  delta_ey     = e_d*sin(omega_d) - e_c*sin(omega_c)
  delta_ix     = i_d - i_c
  delta_iy     = (Omega_d - Omega_c)*sin(i_c)

Assumptions:
  - Both spacecraft are in Keplerian (osculating or mean) orbits.
  - Differences are first-order small; not valid for large separations.
  - For the KGD STM to be valid, mean elements should be used.

Validity domain:
  - Arbitrary eccentricity (no near-circular restriction on the chief).
  - Small formation sizes (|delta_alpha| << 1).

References:
  [1] Koenig, Guffanti, D'Amico, JGCD 2017.
  [2] D'Amico, "Autonomous Formation Flying in Low Earth Orbit", PhD 2010.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from app.core.enums import RelativeFrame, RoeVariant
from app.domain.states import (
    AbsoluteOrbitalState,
    KeplerianElements,
    QnsRoeState,
    RelativeCartesianState,
)


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

class RelativeStateDefinition(ABC):
    """Abstract interface for relative state definitions."""

    @abstractmethod
    def from_absolute(
        self,
        chief: AbsoluteOrbitalState,
        deputy: AbsoluteOrbitalState,
        chief_elements: KeplerianElements,
        deputy_elements: KeplerianElements,
    ) -> QnsRoeState:
        """Compute ROE state from absolute Cartesian states and their elements."""

    @abstractmethod
    def to_cartesian(
        self,
        roe: QnsRoeState,
        chief_elements: KeplerianElements,
        frame: RelativeFrame,
    ) -> RelativeCartesianState:
        """Map ROE state to relative Cartesian state in the specified frame."""


# ---------------------------------------------------------------------------
# QNS ROE definition
# ---------------------------------------------------------------------------

class QnsRoeDefinition(RelativeStateDefinition):
    """Quasi-nonsingular relative orbital element definition.

    Implements the KGD 2017 quasi-nonsingular ROE formulation.
    This class handles the mapping between absolute Keplerian elements and
    the QNS ROE state vector.

    Notes:
      - Mean elements must be used for the KGD STM to be physically valid.
      - Osculating elements may be used for quick initialisation, but will
        introduce oscillatory differences relative to the STM prediction.
    """

    def from_absolute(
        self,
        chief: AbsoluteOrbitalState,
        deputy: AbsoluteOrbitalState,
        chief_elements: KeplerianElements,
        deputy_elements: KeplerianElements,
    ) -> QnsRoeState:
        """Compute QNS ROE state from Keplerian element pairs.

        Args:
            chief          : Chief absolute state (used for epoch).
            deputy         : Deputy absolute state (not directly used in QNS formula).
            chief_elements : Keplerian elements of the chief spacecraft.
            deputy_elements: Keplerian elements of the deputy spacecraft.

        Returns:
            QnsRoeState at the chief epoch.
        """
        # TODO: implement QNS ROE computation
        # Pseudo-code:
        #
        #   a_c, e_c, i_c = chief_elements.a_m, chief_elements.e, chief_elements.i_rad
        #   a_d, e_d, i_d = deputy_elements.a_m, deputy_elements.e, deputy_elements.i_rad
        #   omega_c, omega_d = chief_elements.omega_rad, deputy_elements.omega_rad
        #   RAAN_c, RAAN_d = chief_elements.raan_rad, deputy_elements.raan_rad
        #   M_c, M_d = chief_elements.m_rad, deputy_elements.m_rad
        #
        #   delta_a      = (a_d - a_c) / a_c
        #   delta_lambda = (M_d + omega_d) - (M_c + omega_c) \
        #                  + (RAAN_d - RAAN_c) * cos(i_c)
        #   delta_ex     = e_d*cos(omega_d) - e_c*cos(omega_c)
        #   delta_ey     = e_d*sin(omega_d) - e_c*sin(omega_c)
        #   delta_ix     = i_d - i_c
        #   delta_iy     = (RAAN_d - RAAN_c) * sin(i_c)
        #
        #   return QnsRoeState(delta_a, delta_lambda, delta_ex, delta_ey,
        #                      delta_ix, delta_iy,
        #                      chief_a_m=a_c, epoch_s=chief.epoch_s)
        raise NotImplementedError("QnsRoeDefinition.from_absolute is not yet implemented.")

    def to_cartesian(
        self,
        roe: QnsRoeState,
        chief_elements: KeplerianElements,
        frame: RelativeFrame,
    ) -> RelativeCartesianState:
        """Map QNS ROE state to relative Cartesian state.

        Delegates to RoeGeometryMapper (physics/roe_geometry.py).
        This method is a convenience wrapper.

        Args:
            roe            : QNS ROE state to convert.
            chief_elements : Keplerian elements of the chief.
            frame          : Target output frame (QSW, TNW, LOS, DOCK).

        Returns:
            RelativeCartesianState in the specified frame.
        """
        # TODO: delegate to RoeGeometryMapper.to_qsw() then frame-transform
        # Pseudo-code:
        #   from app.physics.roe_geometry import RoeGeometryMapper
        #   mapper = RoeGeometryMapper()
        #   rel_qsw = mapper.to_qsw(roe, chief_elements)
        #   if frame == RelativeFrame.QSW:
        #       return rel_qsw
        #   elif frame == RelativeFrame.LOS:
        #       return mapper.qsw_to_los(rel_qsw, ...)
        #   ...
        raise NotImplementedError("QnsRoeDefinition.to_cartesian is not yet implemented.")
