"""
physics/roe_geometry.py – ROE to Cartesian relative-state mapping.

Provides:
  RoeGeometryMapper  – Maps QNS ROE state to relative Cartesian states in
                       QSW, LOS, and docking frames.

Governing equations:
  The mapping from QNS ROE to QSW relative position/velocity is derived from
  the first-order linearised equations of relative motion in terms of ROE.
  For the quasi-nonsingular case (Koenig–Guffanti–D'Amico 2017, Sec. III-B):

  rho_R = a_c * (delta_a - delta_ex*cos(u_c) - delta_ey*sin(u_c))
  rho_S = a_c * (delta_lambda + 2*delta_ex*sin(u_c) - 2*delta_ey*cos(u_c)
                 + (e_c*sin(u_c-omega_c)) * delta_a / (1+eta_c))
  rho_W = a_c * (delta_ix*sin(u_c) - delta_iy*cos(u_c))

  where u_c = M_c + omega_c (mean argument of latitude of chief).

Assumptions:
  - First-order approximation; not valid for large separations.
  - Mean elements used for consistency with STM propagation.

References:
  [1] Koenig, Guffanti, D'Amico, JGCD 2017.
  [2] D'Amico, PhD thesis 2010.
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from app.core.enums import RelativeFrame
from app.domain.states import KeplerianElements, QnsRoeState, RelativeCartesianState


class RoeGeometryMapper:
    """Maps QNS ROE state to relative Cartesian states.

    All outputs are derived from the authoritative QNS ROE state; no new
    state is propagated here.

    Methods:
        to_qsw           : Map ROE → QSW relative Cartesian state.
        qsw_to_los       : Rotate QSW → LOS frame.
        qsw_to_tnw       : Rotate QSW → TNW frame.
        qsw_to_docking   : Rotate QSW → docking frame.
    """

    def to_qsw(
        self,
        roe: QnsRoeState,
        chief_mean_elements: KeplerianElements,
    ) -> RelativeCartesianState:
        """Map QNS ROE state to QSW relative Cartesian state.

        Args:
            roe                 : QNS ROE state.
            chief_mean_elements : Chief mean Keplerian elements at the same epoch.

        Returns:
            RelativeCartesianState in QSW frame [m, m/s].
        """
        # TODO: implement ROE → QSW mapping
        # Pseudo-code:
        #
        #   a_c   = chief_mean_elements.a_m
        #   e_c   = chief_mean_elements.e
        #   i_c   = chief_mean_elements.i_rad
        #   omega_c = chief_mean_elements.omega_rad
        #   M_c   = chief_mean_elements.m_rad
        #   eta_c = sqrt(1 - e_c^2)          # eccentricity parameter
        #   u_c   = M_c + omega_c            # mean argument of latitude
        #
        #   rho_R = a_c * (roe.delta_a
        #                  - roe.delta_ex * cos(u_c)
        #                  - roe.delta_ey * sin(u_c))
        #   rho_S = a_c * (roe.delta_lambda
        #                  + 2*roe.delta_ex*sin(u_c)
        #                  - 2*roe.delta_ey*cos(u_c)
        #                  + e_c*sin(u_c - omega_c)*roe.delta_a/(1+eta_c))
        #   rho_W = a_c * (roe.delta_ix*sin(u_c) - roe.delta_iy*cos(u_c))
        #
        #   # Velocity components (time-derivative of position):
        #   # drho_R/dt, drho_S/dt, drho_W/dt
        #   # ... (see KGD 2017 Appendix B for full expressions)
        #
        #   return RelativeCartesianState(
        #       rho_m=np.array([rho_R, rho_S, rho_W]),
        #       rho_dot_mps=np.array([drho_R, drho_S, drho_W]),
        #       frame=RelativeFrame.QSW,
        #       epoch_s=roe.epoch_s,
        #   )
        raise NotImplementedError("RoeGeometryMapper.to_qsw is not yet implemented.")

    def qsw_to_los(
        self,
        rel_qsw: RelativeCartesianState,
        target_geometry: Optional[object] = None,
    ) -> RelativeCartesianState:
        """Rotate QSW relative state to LOS frame.

        The LOS frame origin is at the chief spacecraft.
        The x-axis points from chief to deputy along the LOS.

        Args:
            rel_qsw        : Relative state in QSW frame.
            target_geometry: Optional target geometry for boresight definition.

        Returns:
            RelativeCartesianState in LOS frame.
        """
        # TODO: implement QSW → LOS rotation
        # Pseudo-code:
        #   rho = rel_qsw.rho_m
        #   range_m = |rho|
        #   los_unit = rho / range_m       # unit LOS vector in QSW
        #
        #   azimuth   = atan2(rho[2], rho[1])   # W/S components
        #   elevation = arcsin(rho[0] / range_m) # see conventions
        #
        #   R_qsw_to_los = build_rotation_matrix(azimuth, elevation)
        #   rho_los     = R_qsw_to_los @ rho
        #   rhodot_los  = R_qsw_to_los @ rel_qsw.rho_dot_mps
        #
        #   return RelativeCartesianState(rho_los, rhodot_los, RelativeFrame.LOS, ...)
        raise NotImplementedError("RoeGeometryMapper.qsw_to_los is not yet implemented.")

    def qsw_to_tnw(
        self,
        rel_qsw: RelativeCartesianState,
        chief_mean_elements: KeplerianElements,
    ) -> RelativeCartesianState:
        """Rotate QSW relative state to TNW frame.

        Returns:
            RelativeCartesianState in TNW frame.
        """
        # TODO: implement QSW → TNW rotation via frame transform service
        raise NotImplementedError("RoeGeometryMapper.qsw_to_tnw is not yet implemented.")

    def qsw_to_docking_frame(
        self,
        rel_qsw: RelativeCartesianState,
        target_attitude_q: NDArray[np.float64],
    ) -> RelativeCartesianState:
        """Rotate QSW relative state into the deputy docking frame.

        Args:
            rel_qsw           : Relative state in QSW frame.
            target_attitude_q : Target attitude quaternion [q_x, q_y, q_z, q_w].

        Returns:
            RelativeCartesianState in DOCK frame.
        """
        # TODO: implement QSW → docking frame transformation
        raise NotImplementedError(
            "RoeGeometryMapper.qsw_to_docking_frame is not yet implemented."
        )
