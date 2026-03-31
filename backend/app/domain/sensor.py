"""
domain/sensor.py – Sensor domain objects.

Sensors are modelled as pure descriptors.  The actual measurement model
(noise, FOV, measurement equations) lives in physics/sensors.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.core.enums import SensorType


@dataclass
class Sensor:
    """Abstract sensor descriptor.

    Attributes:
        sensor_id     : Unique identifier string.
        sensor_type   : Type enumeration (see SensorType in core/enums.py).
        noise_1sigma  : 1-sigma measurement noise values [SI units, sensor-specific].
        fov_half_angle_rad: Half-angle of the field-of-view cone [rad]. None = omnidirectional.
        is_active     : Whether this sensor is active in the current phase.
        mount_axis_body: Boresight unit vector in body frame (required for FOV checks).
    """

    sensor_id: str
    sensor_type: SensorType
    noise_1sigma: list[float]
    fov_half_angle_rad: Optional[float] = None
    is_active: bool = True
    mount_axis_body: Optional[list[float]] = None


@dataclass
class RangeAzElSensor(Sensor):
    """Range / azimuth / elevation sensor.

    Measurement vector: [range [m], azimuth [rad], elevation [rad]].
    Noise units:        [m, rad, rad] (1-sigma).
    """

    sensor_type: SensorType = field(default=SensorType.RANGE_AZ_EL, init=False)


@dataclass
class LineOfSightSensor(Sensor):
    """Line-of-sight direction sensor.

    Measurement vector: [azimuth [rad], elevation [rad]].
    Noise units:        [rad, rad] (1-sigma).
    """

    sensor_type: SensorType = field(default=SensorType.LINE_OF_SIGHT, init=False)
