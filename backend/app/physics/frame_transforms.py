"""
physics/frame_transforms.py – Frame transformation service.

Provides:
  FrameTransformService  – Centralized service for all frame rotations.

Supported transforms:
  ECI → QSW  (radial, along-track, cross-track)
  ECI → TNW  (tangential, orbit-normal, cross-track)
  QSW → ECI
  QSW → TNW

Convention:
  QSW frame definition (see core/conventions.py):
    Q = r / |r|                  (radial)
    W = (r × v) / |r × v|       (cross-track / orbit-normal)
    S = W × Q                    (along-track)

  TNW frame definition:
    T = v / |v|                  (tangential = velocity direction)
    N = (r × v) / |r × v|       (orbit-normal, same as W for QSW)
    W = T × N                    (cross-track)

Units: SI (metres, metres/second).  Rotation matrices are dimensionless.

References:
  [1] Vallado, 4th ed., Appendix D.
  [2] Montenbruck & Gill, Chap. 2.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from app.domain.states import AbsoluteOrbitalState


class FrameTransformService:
    """Centralized, stateless service for orbital frame rotations.

    All methods return rotation matrices (3×3) or transformed vectors.
    No state is stored; all methods are effectively pure functions.

    Usage:
        svc = FrameTransformService()
        R_eci_to_qsw = svc.eci_to_qsw_matrix(chief_abs_state)
        r_qsw = R_eci_to_qsw @ r_eci
    """

    @staticmethod
    def eci_to_qsw_matrix(state: AbsoluteOrbitalState) -> NDArray[np.float64]:
        """Compute the 3×3 rotation matrix from ECI to QSW frame.

        Args:
            state: Reference spacecraft absolute state in ECI.

        Returns:
            R_eci_to_qsw : 3×3 rotation matrix such that v_qsw = R @ v_eci.
        """
        # TODO: implement ECI → QSW rotation matrix
        # Pseudo-code:
        #   r = state.r_eci_m
        #   v = state.v_eci_mps
        #
        #   Q_hat = r / |r|                    # radial unit vector
        #   W_hat = cross(r, v) / |cross(r,v)| # cross-track unit vector
        #   S_hat = cross(W_hat, Q_hat)         # along-track unit vector
        #
        #   # Rows of rotation matrix = local unit vectors expressed in ECI:
        #   R = np.vstack([Q_hat, S_hat, W_hat])   # shape (3, 3)
        #   return R
        raise NotImplementedError(
            "FrameTransformService.eci_to_qsw_matrix is not yet implemented."
        )

    @staticmethod
    def qsw_to_eci_matrix(state: AbsoluteOrbitalState) -> NDArray[np.float64]:
        """Compute the 3×3 rotation matrix from QSW to ECI.

        Returns the transpose of eci_to_qsw_matrix (rotation matrices are orthogonal).
        """
        # TODO: return FrameTransformService.eci_to_qsw_matrix(state).T
        raise NotImplementedError(
            "FrameTransformService.qsw_to_eci_matrix is not yet implemented."
        )

    @staticmethod
    def eci_to_tnw_matrix(state: AbsoluteOrbitalState) -> NDArray[np.float64]:
        """Compute the 3×3 rotation matrix from ECI to TNW frame.

        Args:
            state: Reference spacecraft absolute state in ECI.

        Returns:
            R_eci_to_tnw : 3×3 rotation matrix such that v_tnw = R @ v_eci.
        """
        # TODO: implement ECI → TNW rotation matrix
        # Pseudo-code:
        #   r = state.r_eci_m
        #   v = state.v_eci_mps
        #
        #   T_hat = v / |v|                    # tangential unit vector
        #   N_hat = cross(r, v) / |cross(r,v)| # orbit-normal unit vector
        #   W_hat = cross(T_hat, N_hat)         # cross-track unit vector
        #
        #   R = np.vstack([T_hat, N_hat, W_hat])
        #   return R
        raise NotImplementedError(
            "FrameTransformService.eci_to_tnw_matrix is not yet implemented."
        )

    @staticmethod
    def qsw_to_tnw_matrix(state: AbsoluteOrbitalState) -> NDArray[np.float64]:
        """Compute the 3×3 rotation matrix from QSW to TNW.

        Returns:
            R_qsw_to_tnw = R_eci_to_tnw @ R_qsw_to_eci
        """
        # TODO: compose eci_to_tnw and qsw_to_eci matrices
        raise NotImplementedError(
            "FrameTransformService.qsw_to_tnw_matrix is not yet implemented."
        )
