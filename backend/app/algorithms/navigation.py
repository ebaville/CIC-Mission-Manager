"""
algorithms/navigation.py – Navigation filter strategy objects.

Provides:
  NavigationFilter   – Abstract interface for navigation filters.
  RelativePoseEkf    – Extended Kalman filter for relative pose estimation.

State vector for relative navigation:
  x = [rho_R, rho_S, rho_W, rho_dot_R, rho_dot_S, rho_dot_W]  (QSW Cartesian)

The EKF uses:
  - Process model: ROE STM (converted to Cartesian for filter update).
  - Measurement model: range/azimuth/elevation or LOS (from physics/sensors.py).

Design rules:
  - Navigation filters consume explicit MeasurementPackets, not raw payloads.
  - Estimated states are distinct objects from truth states.
  - Do not merge physics and filter logic.

References:
  [1] Bar-Shalom, "Estimation with Applications to Tracking and Navigation".
  [2] D'Amico, PhD thesis 2010, Chap. 5.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from app.domain.states import MeasurementPacket, RelativeCartesianState


# ---------------------------------------------------------------------------
# Filter state estimate
# ---------------------------------------------------------------------------

@dataclass
class FilterStateEstimate:
    """Navigation filter state estimate.

    Attributes:
        x_hat   : State estimate vector, shape (n,).
        P       : State estimate covariance matrix, shape (n, n).
        epoch_s : Estimate epoch [s].
    """

    x_hat: NDArray[np.float64]
    P: NDArray[np.float64]
    epoch_s: float = 0.0

    def __post_init__(self) -> None:
        self.x_hat = np.asarray(self.x_hat, dtype=np.float64)
        self.P = np.asarray(self.P, dtype=np.float64)
        n = self.x_hat.shape[0]
        if self.P.shape != (n, n):
            raise ValueError(f"P shape {self.P.shape} inconsistent with x_hat length {n}.")


# ---------------------------------------------------------------------------
# Navigation filter interface
# ---------------------------------------------------------------------------

class NavigationFilter(ABC):
    """Abstract interface for navigation filters."""

    @abstractmethod
    def predict(
        self,
        dt_s: float,
        process_noise_Q: NDArray[np.float64] | None = None,
    ) -> None:
        """Propagate the filter state estimate forward by dt_s seconds."""

    @abstractmethod
    def update(
        self,
        measurement: MeasurementPacket,
    ) -> None:
        """Update the filter estimate with a new measurement."""

    @property
    @abstractmethod
    def estimate(self) -> FilterStateEstimate:
        """Return the current state estimate."""


# ---------------------------------------------------------------------------
# Relative pose EKF
# ---------------------------------------------------------------------------

class RelativePoseEkf(NavigationFilter):
    """Extended Kalman filter for relative pose estimation.

    State vector: [rho_R, rho_S, rho_W, rho_dot_R, rho_dot_S, rho_dot_W] (QSW, 6 states).

    Process model:
      Uses the ROE STM mapped to Cartesian space for the predict step.

    Measurement model:
      Supports range/azimuth/elevation (nonlinear → linearised Jacobian).

    Attributes:
        _x_hat : Current state estimate (6,).
        _P     : Current covariance estimate (6, 6).
        _epoch_s: Current filter epoch [s].
    """

    def __init__(
        self,
        initial_estimate: FilterStateEstimate,
    ) -> None:
        self._x_hat = initial_estimate.x_hat.copy()
        self._P = initial_estimate.P.copy()
        self._epoch_s = initial_estimate.epoch_s

    @property
    def estimate(self) -> FilterStateEstimate:
        return FilterStateEstimate(
            x_hat=self._x_hat.copy(),
            P=self._P.copy(),
            epoch_s=self._epoch_s,
        )

    def predict(
        self,
        dt_s: float,
        process_noise_Q: NDArray[np.float64] | None = None,
    ) -> None:
        """EKF predict step.

        Propagates state and covariance forward using the process model STM.
        """
        # TODO: implement EKF predict step
        # Pseudo-code:
        #   F = compute_process_jacobian(self._x_hat, dt_s)  # or use linear STM
        #   Q = process_noise_Q if provided else default_Q
        #   self._x_hat = process_model(self._x_hat, dt_s)
        #   self._P     = F @ self._P @ F.T + Q
        #   self._epoch_s += dt_s
        raise NotImplementedError("RelativePoseEkf.predict is not yet implemented.")

    def update(
        self,
        measurement: MeasurementPacket,
    ) -> None:
        """EKF update step.

        Updates state estimate using a new measurement packet.
        """
        # TODO: implement EKF update step
        # Pseudo-code:
        #   H   = compute_measurement_jacobian(self._x_hat, measurement.sensor_id)
        #   S   = H @ self._P @ H.T + measurement.covariance
        #   K   = self._P @ H.T @ inv(S)     # Kalman gain
        #   y   = measurement.values - h(self._x_hat)  # innovation
        #   self._x_hat += K @ y
        #   self._P = (I - K @ H) @ self._P  # or Joseph form for stability
        raise NotImplementedError("RelativePoseEkf.update is not yet implemented.")
