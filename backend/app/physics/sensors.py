"""
physics/sensors.py – Sensor measurement models.

Provides:
  MeasurementModel    – Abstract interface for sensor models.
  NoiseModel          – Gaussian noise model for sensor outputs.
  RangeAzElModel      – Range / azimuth / elevation sensor model.
  LineOfSightModel    – Line-of-sight direction sensor model.

Governing equations (RangeAzEl sensor):
  range     = |rho_QSW|                  [m]
  azimuth   = atan2(rho_W, rho_S)        [rad]  (per core/conventions.py)
  elevation = arcsin(rho_R / range)      [rad]  (per core/conventions.py)

Noise model:
  z_meas = z_true + noise
  noise ~ N(0, R)  where R = diag(sigma_1^2, ..., sigma_n^2)

Assumptions:
  - Gaussian white noise; no bias, no correlated noise.
  - Line-of-sight is unobstructed (no occlusion modelling in V1).
  - Field-of-view check uses half-angle cone; see domain/sensor.py.

Units: SI throughout (metres, radians).

References:
  [1] Bar-Shalom, "Estimation with Applications to Tracking and Navigation".
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from app.domain.states import MeasurementPacket, RelativeCartesianState


# ---------------------------------------------------------------------------
# Noise model
# ---------------------------------------------------------------------------

class NoiseModel:
    """Simple diagonal Gaussian noise model.

    Attributes:
        sigma_1sigma: 1-sigma noise standard deviations [SI units].
    """

    def __init__(self, sigma_1sigma: list[float]) -> None:
        self._sigma = np.asarray(sigma_1sigma, dtype=np.float64)

    @property
    def covariance(self) -> NDArray[np.float64]:
        """Return diagonal covariance matrix R = diag(sigma^2)."""
        return np.diag(self._sigma**2)

    def sample(self) -> NDArray[np.float64]:
        """Draw one noise sample from N(0, R)."""
        return np.random.normal(0.0, self._sigma)


# ---------------------------------------------------------------------------
# Measurement model interface
# ---------------------------------------------------------------------------

class MeasurementModel(ABC):
    """Abstract interface for sensor measurement models.

    Separates truth measurements from noise injection, allowing clean
    comparison of truth vs. estimated vs. measured states.
    """

    @abstractmethod
    def compute_true_measurement(
        self,
        rel_state: RelativeCartesianState,
    ) -> NDArray[np.float64]:
        """Compute the noiseless (truth) measurement from relative state."""

    @abstractmethod
    def add_noise(
        self,
        true_measurement: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Add sensor noise to a truth measurement."""

    def measure(
        self,
        rel_state: RelativeCartesianState,
        sensor_id: str,
        epoch_s: float,
        is_valid: bool = True,
    ) -> MeasurementPacket:
        """Generate a full measurement packet with noise.

        Args:
            rel_state : Current relative Cartesian state.
            sensor_id : Sensor identifier string.
            epoch_s   : Current simulation time [s].
            is_valid  : Whether the measurement is within FOV / usable.

        Returns:
            MeasurementPacket with noisy values and covariance.
        """
        z_true = self.compute_true_measurement(rel_state)
        z_noisy = self.add_noise(z_true)
        return MeasurementPacket(
            sensor_id=sensor_id,
            epoch_s=epoch_s,
            values=z_noisy,
            covariance=self.noise_model.covariance,
            is_valid=is_valid,
        )

    @property
    @abstractmethod
    def noise_model(self) -> NoiseModel:
        """Return the associated noise model."""


# ---------------------------------------------------------------------------
# Range / azimuth / elevation sensor
# ---------------------------------------------------------------------------

class RangeAzElModel(MeasurementModel):
    """Range / azimuth / elevation measurement model.

    Measurement vector: [range [m], azimuth [rad], elevation [rad]].

    Convention (see core/conventions.py):
      azimuth   = atan2(rho_W, rho_S)   positive from S toward W
      elevation = arcsin(rho_R / range) positive upward (toward W)
    """

    def __init__(
        self,
        range_sigma_m: float,
        az_sigma_rad: float,
        el_sigma_rad: float,
    ) -> None:
        self._noise_model = NoiseModel([range_sigma_m, az_sigma_rad, el_sigma_rad])

    @property
    def noise_model(self) -> NoiseModel:
        return self._noise_model

    def compute_true_measurement(
        self,
        rel_state: RelativeCartesianState,
    ) -> NDArray[np.float64]:
        """Compute noiseless [range, azimuth, elevation] from QSW relative state.

        Args:
            rel_state: Relative state in QSW frame (rho = [rho_R, rho_S, rho_W]).
        """
        # TODO: implement range/azimuth/elevation computation
        # Pseudo-code:
        #   rho_R, rho_S, rho_W = rel_state.rho_m
        #   range_m = |rel_state.rho_m|
        #   if range_m < 1e-3:
        #       return np.zeros(3)
        #   azimuth_rad   = atan2(rho_W, rho_S)        # S is 0-azimuth reference
        #   elevation_rad = arcsin(rho_R / range_m)    # radial = elevation direction
        #   return np.array([range_m, azimuth_rad, elevation_rad])
        raise NotImplementedError(
            "RangeAzElModel.compute_true_measurement is not yet implemented."
        )

    def add_noise(
        self,
        true_measurement: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Add Gaussian noise to [range, azimuth, elevation]."""
        return true_measurement + self._noise_model.sample()


# ---------------------------------------------------------------------------
# Line-of-sight sensor
# ---------------------------------------------------------------------------

class LineOfSightModel(MeasurementModel):
    """Line-of-sight direction sensor.

    Measurement vector: [azimuth [rad], elevation [rad]].
    """

    def __init__(
        self,
        az_sigma_rad: float,
        el_sigma_rad: float,
    ) -> None:
        self._noise_model = NoiseModel([az_sigma_rad, el_sigma_rad])

    @property
    def noise_model(self) -> NoiseModel:
        return self._noise_model

    def compute_true_measurement(
        self,
        rel_state: RelativeCartesianState,
    ) -> NDArray[np.float64]:
        """Compute noiseless [azimuth, elevation] from QSW relative state."""
        # TODO: implement LOS direction computation
        # Pseudo-code:
        #   rho_R, rho_S, rho_W = rel_state.rho_m
        #   range_m = |rel_state.rho_m|
        #   azimuth_rad   = atan2(rho_W, rho_S)
        #   elevation_rad = arcsin(rho_R / range_m)
        #   return np.array([azimuth_rad, elevation_rad])
        raise NotImplementedError(
            "LineOfSightModel.compute_true_measurement is not yet implemented."
        )

    def add_noise(
        self,
        true_measurement: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Add Gaussian noise to [azimuth, elevation]."""
        return true_measurement + self._noise_model.sample()
