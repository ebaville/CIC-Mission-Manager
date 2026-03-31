"""
domain/states.py – Core state representations.

All state objects are pure data containers.  Units are SI throughout.
See core/conventions.py for ordering and frame conventions.

State classes:
  AbsoluteOrbitalState    – Cartesian ECI position and velocity.
  KeplerianElements       – Classical Keplerian elements (osculating or mean).
  AttitudeState           – Quaternion attitude + body angular velocity.
  QnsRoeState             – Quasi-nonsingular relative orbital elements.
  RelativeCartesianState  – Cartesian relative position/velocity in a named frame.
  MeasurementPacket       – Single sensor measurement with metadata.
  RelativeMotionSnapshot  – Combined ROE + derived Cartesian views at one epoch.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from app.core.enums import RelativeFrame, RoeVariant


# ---------------------------------------------------------------------------
# Absolute orbital state
# ---------------------------------------------------------------------------

@dataclass
class AbsoluteOrbitalState:
    """Cartesian absolute orbital state in the ECI J2000 inertial frame.

    Attributes:
        r_eci_m   : Position vector in ECI [m], shape (3,).
        v_eci_mps : Velocity vector in ECI [m/s], shape (3,).
        epoch_s   : Simulation time since scenario epoch [s].

    Convention: ECI J2000 as defined in core/conventions.py.
    """

    r_eci_m: NDArray[np.float64]
    v_eci_mps: NDArray[np.float64]
    epoch_s: float = 0.0

    def __post_init__(self) -> None:
        self.r_eci_m = np.asarray(self.r_eci_m, dtype=np.float64)
        self.v_eci_mps = np.asarray(self.v_eci_mps, dtype=np.float64)
        if self.r_eci_m.shape != (3,):
            raise ValueError("r_eci_m must be a 3-vector.")
        if self.v_eci_mps.shape != (3,):
            raise ValueError("v_eci_mps must be a 3-vector.")

    @property
    def radius_m(self) -> float:
        """Magnitude of position vector [m]."""
        return float(np.linalg.norm(self.r_eci_m))

    @property
    def speed_mps(self) -> float:
        """Magnitude of velocity vector [m/s]."""
        return float(np.linalg.norm(self.v_eci_mps))


# ---------------------------------------------------------------------------
# Keplerian elements
# ---------------------------------------------------------------------------

@dataclass
class KeplerianElements:
    """Classical Keplerian orbital elements.

    Ordering (see core/conventions.py): (a, e, i, RAAN, omega, M)
    Units: metres for a; radians for angular elements.

    Attributes:
        a_m     : Semi-major axis [m].
        e       : Eccentricity [-], in [0, 1).
        i_rad   : Inclination [rad], in [0, pi].
        raan_rad: Right ascension of ascending node [rad], wrapped to [0, 2*pi).
        omega_rad: Argument of perigee [rad], wrapped to [0, 2*pi).
        m_rad   : Mean anomaly [rad], wrapped to [0, 2*pi).
        is_mean : True if elements are mean (J2-averaged); False if osculating.
    """

    a_m: float
    e: float
    i_rad: float
    raan_rad: float
    omega_rad: float
    m_rad: float
    is_mean: bool = False

    def __post_init__(self) -> None:
        if self.a_m <= 0.0:
            raise ValueError("Semi-major axis must be positive.")
        if not (0.0 <= self.e < 1.0):
            raise ValueError("Eccentricity must be in [0, 1).")
        if not (0.0 <= self.i_rad <= math.pi):
            raise ValueError("Inclination must be in [0, pi] rad.")

    def as_vector(self) -> NDArray[np.float64]:
        """Return (a, e, i, RAAN, omega, M) as a NumPy array."""
        return np.array(
            [self.a_m, self.e, self.i_rad, self.raan_rad, self.omega_rad, self.m_rad],
            dtype=np.float64,
        )


# ---------------------------------------------------------------------------
# Attitude state
# ---------------------------------------------------------------------------

@dataclass
class AttitudeState:
    """Spacecraft attitude state.

    Uses the repository-wide SCALAR_LAST quaternion convention:
        q = [q_x, q_y, q_z, q_w]
    Represents the rotation from body frame to ECI inertial frame.

    Attributes:
        q_body_to_eci : Unit quaternion [q_x, q_y, q_z, q_w], shape (4,).
        omega_body_rads: Angular velocity in body frame [rad/s], shape (3,).
        epoch_s       : Simulation time since scenario epoch [s].
    """

    q_body_to_eci: NDArray[np.float64]
    omega_body_rads: NDArray[np.float64]
    epoch_s: float = 0.0

    def __post_init__(self) -> None:
        self.q_body_to_eci = np.asarray(self.q_body_to_eci, dtype=np.float64)
        self.omega_body_rads = np.asarray(self.omega_body_rads, dtype=np.float64)
        if self.q_body_to_eci.shape != (4,):
            raise ValueError("Quaternion must be a 4-vector [q_x, q_y, q_z, q_w].")
        if self.omega_body_rads.shape != (3,):
            raise ValueError("Angular velocity must be a 3-vector.")

    @property
    def is_normalised(self) -> bool:
        """Return True if quaternion norm is within 1e-9 of 1."""
        return abs(float(np.linalg.norm(self.q_body_to_eci)) - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# Quasi-nonsingular ROE state
# ---------------------------------------------------------------------------

@dataclass
class QnsRoeState:
    """Quasi-nonsingular relative orbital element (ROE) state.

    Ordering (see core/conventions.py):
        delta_alpha_qns = [delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]

    Definitions (Koenig–Guffanti–D'Amico 2017):
        delta_a      = (a_d - a_c) / a_c                              [-]
        delta_lambda = (M_d + omega_d) - (M_c + omega_c)
                       + (Omega_d - Omega_c) * cos(i_c)               [rad]
        delta_ex     = e_d*cos(omega_d) - e_c*cos(omega_c)            [-]
        delta_ey     = e_d*sin(omega_d) - e_c*sin(omega_c)            [-]
        delta_ix     = i_d - i_c                                       [rad]
        delta_iy     = (Omega_d - Omega_c) * sin(i_c)                 [rad]

    The state is NOT purely dimensionless: delta_a is normalised by a_c,
    delta_lambda/ix/iy are angular; this mixed convention matches the KGD paper.

    Attributes:
        delta_a       : Relative semi-major axis [-].
        delta_lambda  : Relative mean argument of latitude [rad].
        delta_ex      : x-component of relative eccentricity vector [-].
        delta_ey      : y-component of relative eccentricity vector [-].
        delta_ix      : x-component of relative inclination vector [rad].
        delta_iy      : y-component of relative inclination vector [rad].
        chief_a_m     : Chief semi-major axis used to normalise delta_a [m].
        epoch_s       : Simulation time since scenario epoch [s].
        variant       : ROE variant (must be QNS for this class).
    """

    delta_a: float
    delta_lambda: float
    delta_ex: float
    delta_ey: float
    delta_ix: float
    delta_iy: float
    chief_a_m: float
    epoch_s: float = 0.0
    variant: RoeVariant = RoeVariant.QNS

    def as_vector(self) -> NDArray[np.float64]:
        """Return the 6-element ROE state vector."""
        return np.array(
            [
                self.delta_a,
                self.delta_lambda,
                self.delta_ex,
                self.delta_ey,
                self.delta_ix,
                self.delta_iy,
            ],
            dtype=np.float64,
        )

    @classmethod
    def from_vector(
        cls,
        vec: NDArray[np.float64],
        chief_a_m: float,
        epoch_s: float = 0.0,
    ) -> "QnsRoeState":
        """Construct a QnsRoeState from a 6-element array."""
        if vec.shape != (6,):
            raise ValueError("ROE vector must have 6 elements.")
        return cls(
            delta_a=float(vec[0]),
            delta_lambda=float(vec[1]),
            delta_ex=float(vec[2]),
            delta_ey=float(vec[3]),
            delta_ix=float(vec[4]),
            delta_iy=float(vec[5]),
            chief_a_m=chief_a_m,
            epoch_s=epoch_s,
        )

    @property
    def relative_eccentricity_magnitude(self) -> float:
        """Magnitude of the relative eccentricity vector: sqrt(dex^2 + dey^2)."""
        return math.hypot(self.delta_ex, self.delta_ey)

    @property
    def relative_inclination_magnitude(self) -> float:
        """Magnitude of the relative inclination vector: sqrt(dix^2 + diy^2)."""
        return math.hypot(self.delta_ix, self.delta_iy)


# ---------------------------------------------------------------------------
# Relative Cartesian state
# ---------------------------------------------------------------------------

@dataclass
class RelativeCartesianState:
    """Cartesian relative position and velocity in a named local orbital frame.

    This is a **derived** state produced by mapping from QnsRoeState; it is
    NOT propagated directly as the primary state.

    Attributes:
        rho_m      : Relative position [m] in the specified frame, shape (3,).
        rho_dot_mps: Relative velocity [m/s] in the specified frame, shape (3,).
        frame      : Identifier of the reference frame (QSW, TNW, LOS, DOCK).
        epoch_s    : Simulation time since scenario epoch [s].
    """

    rho_m: NDArray[np.float64]
    rho_dot_mps: NDArray[np.float64]
    frame: RelativeFrame
    epoch_s: float = 0.0

    def __post_init__(self) -> None:
        self.rho_m = np.asarray(self.rho_m, dtype=np.float64)
        self.rho_dot_mps = np.asarray(self.rho_dot_mps, dtype=np.float64)
        if self.rho_m.shape != (3,):
            raise ValueError("rho_m must be a 3-vector.")
        if self.rho_dot_mps.shape != (3,):
            raise ValueError("rho_dot_mps must be a 3-vector.")

    @property
    def range_m(self) -> float:
        """Scalar range (magnitude of relative position) [m]."""
        return float(np.linalg.norm(self.rho_m))


# ---------------------------------------------------------------------------
# Measurement packet
# ---------------------------------------------------------------------------

@dataclass
class MeasurementPacket:
    """Single sensor measurement with metadata.

    Attributes:
        sensor_id    : Identifier of the originating sensor.
        epoch_s      : Simulation time at measurement epoch [s].
        values       : Raw measurement values, shape (n,).  Unit and semantics
                       are sensor-specific (see physics/sensors.py).
        covariance   : Measurement noise covariance matrix, shape (n, n).
        is_valid     : False if the measurement is outside sensor FOV or faulty.
    """

    sensor_id: str
    epoch_s: float
    values: NDArray[np.float64]
    covariance: NDArray[np.float64]
    is_valid: bool = True

    def __post_init__(self) -> None:
        self.values = np.asarray(self.values, dtype=np.float64)
        self.covariance = np.asarray(self.covariance, dtype=np.float64)
        n = self.values.shape[0]
        if self.covariance.shape != (n, n):
            raise ValueError(
                f"Covariance shape {self.covariance.shape} does not match "
                f"values length {n}."
            )


# ---------------------------------------------------------------------------
# Combined snapshot
# ---------------------------------------------------------------------------

@dataclass
class RelativeMotionSnapshot:
    """Combined relative-state snapshot at one epoch.

    Contains the ROE state (authoritative) plus derived Cartesian views.

    Attributes:
        epoch_s           : Simulation time since scenario epoch [s].
        roe               : Propagated QNS ROE state (authoritative).
        cartesian_qsw     : Derived relative state in QSW frame.
        cartesian_los     : Derived relative state in LOS frame (optional).
        chief_abs_state   : Chief absolute state at this epoch.
        deputy_abs_state  : Deputy absolute state at this epoch (truth, optional).
    """

    epoch_s: float
    roe: QnsRoeState
    cartesian_qsw: RelativeCartesianState
    cartesian_los: Optional[RelativeCartesianState] = None
    chief_abs_state: Optional[AbsoluteOrbitalState] = None
    deputy_abs_state: Optional[AbsoluteOrbitalState] = None
