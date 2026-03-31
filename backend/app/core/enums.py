"""
core/enums.py – Centralised enumeration definitions.

All enumerations used across the backend must be defined here.
Never re-declare an enum in a sub-module.
"""

from enum import Enum, auto


class InertialFrame(str, Enum):
    """Supported inertial frames.

    ECI (Earth-Centred Inertial, J2000) is the single truth inertial frame.
    """

    ECI = "ECI"


class RelativeFrame(str, Enum):
    """Supported relative / local orbital frames.

    QSW : radial (Q), along-track (S), cross-track (W).
    TNW : tangential (T), normal (N), cross-track (W).
    LOS : line-of-sight, elevation, cross-elevation.
    DOCK: docking-port aligned frame, origin at deputy docking port.
    """

    QSW = "QSW"
    TNW = "TNW"
    LOS = "LOS"
    DOCK = "DOCK"


class OrbitalElementSet(str, Enum):
    """Supported orbital element set families."""

    KEPLERIAN_OSCULATING = "KEPLERIAN_OSCULATING"
    KEPLERIAN_MEAN_J2 = "KEPLERIAN_MEAN_J2"
    CARTESIAN_ECI = "CARTESIAN_ECI"


class RoeVariant(str, Enum):
    """Relative orbital element (ROE) state variants.

    QNS : quasi-nonsingular (default, avoids circular-orbit singularity).
    SINGULAR : classical singular ROE, undefined for circular orbits.
    NONSINGULAR : fully nonsingular, valid for circular and equatorial orbits.
    """

    QNS = "QNS"
    SINGULAR = "SINGULAR"
    NONSINGULAR = "NONSINGULAR"


class RelativeModelMode(str, Enum):
    """Available analytical relative-motion models.

    KGD_QNS_J2       : Koenig–Guffanti–D'Amico STM, QNS state, J2 perturbation.
    KGD_QNS_J2_DRAG  : KGD STM with differential drag.
    HCW              : Hill–Clohessy–Wiltshire (circular, unperturbed – fallback only).
    TRUTH_DIFFERENCE : derive relative state by differencing absolute truth states.
    """

    KGD_QNS_J2 = "KGD_QNS_J2"
    KGD_QNS_J2_DRAG = "KGD_QNS_J2_DRAG"
    HCW = "HCW"
    TRUTH_DIFFERENCE = "TRUTH_DIFFERENCE"


class QuaternionConvention(str, Enum):
    """Quaternion scalar-component ordering.

    SCALAR_LAST  : [q_x, q_y, q_z, q_w]  (e.g. ROS, many robotics libs)
    SCALAR_FIRST : [q_w, q_x, q_y, q_z]  (e.g. Hamilton convention, MATLAB)

    The repository-wide convention is SCALAR_LAST; see core/conventions.py.
    """

    SCALAR_LAST = "SCALAR_LAST"
    SCALAR_FIRST = "SCALAR_FIRST"


class MissionPhaseType(str, Enum):
    """High-level mission-phase type labels."""

    FAR_RANGE_TRANSFER = "FAR_RANGE_TRANSFER"
    ROE_HOMING = "ROE_HOMING"
    CLOSING = "CLOSING"
    HOLD_POINT = "HOLD_POINT"
    INSPECTION = "INSPECTION"
    RETREAT = "RETREAT"
    ABORT = "ABORT"


class GuidanceLawType(str, Enum):
    """Guidance law type identifiers."""

    IMPULSIVE_TRANSFER = "IMPULSIVE_TRANSFER"
    ROE_HOMING = "ROE_HOMING"
    CLOSING = "CLOSING"
    HOLD_POINT = "HOLD_POINT"
    RETREAT = "RETREAT"


class SensorType(str, Enum):
    """Sensor type identifiers."""

    RANGE_AZ_EL = "RANGE_AZ_EL"
    LINE_OF_SIGHT = "LINE_OF_SIGHT"
    CAMERA_FEATURE = "CAMERA_FEATURE"


class ExportFormat(str, Enum):
    """Supported export file formats."""

    CSV = "CSV"
    JSON = "JSON"
    YAML = "YAML"
    CIC_OEM = "CIC_OEM"


class DragMode(str, Enum):
    """Differential-drag modelling mode for the KGD STM."""

    NONE = "NONE"
    DENSITY_MODEL_SPECIFIC = "DENSITY_MODEL_SPECIFIC"
    DENSITY_MODEL_FREE = "DENSITY_MODEL_FREE"
