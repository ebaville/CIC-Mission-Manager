"""
domain/ground_station.py – Ground station domain object.

Ground stations are used for visibility analysis and contact window computation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GroundStation:
    """Ground station descriptor.

    Attributes:
        station_id        : Unique identifier string.
        name              : Human-readable label.
        latitude_rad      : Geodetic latitude [rad], in [-pi/2, pi/2].
        longitude_rad     : East longitude [rad], in [0, 2*pi).
        altitude_m        : Altitude above WGS-84 ellipsoid [m].
        min_elevation_rad : Minimum elevation angle for line-of-sight [rad].
    """

    station_id: str
    name: str
    latitude_rad: float
    longitude_rad: float
    altitude_m: float
    min_elevation_rad: float = 0.0872664625  # default: 5 degrees
