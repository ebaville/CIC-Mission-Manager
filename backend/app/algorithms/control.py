"""
algorithms/control.py – Control law strategy objects.

Provides:
  TranslationalController  – Converts delta-v commands to acceleration requests.
  AttitudePdController     – Quaternion proportional-derivative attitude controller.

Design rules:
  - Controllers convert guidance COMMANDS into force/torque/acceleration requests.
  - Controllers do not plan manoeuvres (that is guidance's role).
  - Actuator allocation is separate from control.

Governing equations:

  PD attitude control law:
    tau = -Kp * q_error_xyz - Kd * omega_error

  where:
    q_error_xyz = vector part of the attitude error quaternion.
    omega_error = omega_body - omega_desired.
    Kp, Kd      = proportional and derivative gain matrices.

References:
  [1] Wertz, "Spacecraft Attitude Determination and Control", 1978.
  [2] Schaub & Junkins, "Analytical Mechanics of Space Systems", 3rd ed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


# ---------------------------------------------------------------------------
# Control output
# ---------------------------------------------------------------------------

@dataclass
class TranslationalControlOutput:
    """Translational control output.

    Attributes:
        delta_v_body_mps : Delta-v request in body frame [m/s], shape (3,).
        epoch_s          : Command epoch [s].
    """

    delta_v_body_mps: NDArray[np.float64]
    epoch_s: float = 0.0


@dataclass
class AttitudeControlOutput:
    """Attitude control output.

    Attributes:
        torque_Nm : Requested torque in body frame [N·m], shape (3,).
        epoch_s   : Command epoch [s].
    """

    torque_Nm: NDArray[np.float64]
    epoch_s: float = 0.0


# ---------------------------------------------------------------------------
# Translational controller
# ---------------------------------------------------------------------------

class TranslationalController:
    """Simple translational controller.

    Converts a guidance delta-v command (in QSW frame) into an equivalent
    delta-v request in the body frame, after applying actuator limits.

    Attributes:
        max_delta_v_mps: Maximum delta-v per manoeuvre [m/s].
    """

    def __init__(self, max_delta_v_mps: float = 10.0) -> None:
        self._max_dv = max_delta_v_mps

    def compute(
        self,
        delta_v_qsw_mps: NDArray[np.float64],
        q_body_to_eci: NDArray[np.float64],
        qsw_to_eci_matrix: NDArray[np.float64],
        epoch_s: float = 0.0,
    ) -> TranslationalControlOutput:
        """Convert QSW delta-v command to body-frame delta-v, with magnitude limit.

        Args:
            delta_v_qsw_mps  : Requested delta-v in QSW frame [m/s].
            q_body_to_eci    : Current body quaternion [q_x, q_y, q_z, q_w].
            qsw_to_eci_matrix: 3×3 rotation matrix from QSW to ECI.
            epoch_s          : Command epoch [s].

        Returns:
            TranslationalControlOutput with delta-v in body frame.
        """
        # TODO: implement translational control
        # Pseudo-code:
        #   delta_v_eci = qsw_to_eci_matrix @ delta_v_qsw_mps
        #   R_body_from_eci = quaternion_to_dcm(q_body_to_eci)
        #   delta_v_body = R_body_from_eci @ delta_v_eci
        #
        #   # Apply magnitude limit
        #   dv_norm = |delta_v_body|
        #   if dv_norm > max_delta_v_mps:
        #       delta_v_body = delta_v_body / dv_norm * max_delta_v_mps
        #
        #   return TranslationalControlOutput(delta_v_body, epoch_s)
        raise NotImplementedError(
            "TranslationalController.compute is not yet implemented."
        )


# ---------------------------------------------------------------------------
# PD attitude controller
# ---------------------------------------------------------------------------

class AttitudePdController:
    """Quaternion proportional-derivative attitude controller.

    Computes a torque command based on attitude error quaternion and angular
    velocity error.

    PD control law:
        tau = -Kp * q_error_xyz - Kd * omega_error_body

    Attributes:
        Kp : Proportional gain matrix [N·m], shape (3, 3) or scalar.
        Kd : Derivative gain matrix [N·m·s/rad], shape (3, 3) or scalar.
    """

    def __init__(
        self,
        Kp: float | NDArray[np.float64] = 1.0,  # noqa: N803
        Kd: float | NDArray[np.float64] = 0.1,  # noqa: N803
    ) -> None:
        self._Kp = np.atleast_2d(Kp) if isinstance(Kp, np.ndarray) else Kp * np.eye(3)
        self._Kd = np.atleast_2d(Kd) if isinstance(Kd, np.ndarray) else Kd * np.eye(3)

    def compute(
        self,
        q_current: NDArray[np.float64],
        q_desired: NDArray[np.float64],
        omega_body_rads: NDArray[np.float64],
        omega_desired_rads: NDArray[np.float64] | None = None,
        epoch_s: float = 0.0,
    ) -> AttitudeControlOutput:
        """Compute PD torque command.

        Args:
            q_current          : Current quaternion [q_x, q_y, q_z, q_w].
            q_desired          : Desired quaternion [q_x, q_y, q_z, q_w].
            omega_body_rads    : Current angular velocity [rad/s].
            omega_desired_rads : Desired angular velocity [rad/s] (default: zero).
            epoch_s            : Command epoch [s].

        Returns:
            AttitudeControlOutput with torque [N·m].
        """
        # TODO: implement quaternion PD control
        # Pseudo-code:
        #   q_err = Quaternion(q_desired).conjugate().multiply(Quaternion(q_current))
        #   q_err_xyz = q_err.q_xyz   # vector part of error quaternion
        #
        #   omega_des = omega_desired_rads if provided else zeros(3)
        #   omega_err = omega_body_rads - omega_des
        #
        #   tau = -Kp @ q_err_xyz - Kd @ omega_err
        #   return AttitudeControlOutput(tau, epoch_s)
        raise NotImplementedError(
            "AttitudePdController.compute is not yet implemented."
        )
