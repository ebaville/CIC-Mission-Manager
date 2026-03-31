# Frames and Conventions

## Purpose

This document is the authoritative reference for all coordinate frames, unit conventions, quaternion ordering, and sign conventions used in this project.

**All conventions must be imported from `backend/app/core/conventions.py`.**  Never re-derive these in sub-modules.

---

## Physical constants

| Symbol | Value | Units | Description |
|--------|-------|-------|-------------|
| `mu` | 3.986004418 × 10¹⁴ | m³/s² | Earth gravitational parameter |
| `Re` | 6,378,137 | m | Earth mean equatorial radius |
| `J2` | 1.08262668 × 10⁻³ | – | J2 zonal harmonic |
| `omega_E` | 7.292115 × 10⁻⁵ | rad/s | Earth rotation rate |

---

## Inertial frame: ECI J2000

- **Origin**: Earth centre of mass.
- **X-axis**: vernal equinox direction at epoch J2000.0 (1 January 2000, 12:00 TT).
- **Z-axis**: Earth north celestial pole at J2000.0.
- **Y-axis**: completes right-handed triad.
- **Units**: metres [m] and metres/second [m/s].
- **Use**: truth inertial frame for all absolute states.

---

## QSW local orbital frame

Also called LVLH (Local Vertical Local Horizontal) or RSW.

- **Origin**: reference spacecraft centre of mass.
- **Q-axis** (radial): unit vector `r / |r|`, pointing away from Earth.
- **W-axis** (cross-track): `(r × v) / |r × v|`, perpendicular to orbital plane.
- **S-axis** (along-track): `W × Q`, approximately in the velocity direction for circular orbits.
- **Note**: Q-S-W form a right-handed triad.
- **Rotation**: the frame rotates with the orbital motion.

For a circular orbit: Q ≈ radial, S ≈ velocity, W = orbit normal.

---

## TNW local orbital frame

- **Origin**: reference spacecraft centre of mass.
- **T-axis** (tangential): unit vector `v / |v|`, along the velocity.
- **N-axis** (orbit-normal): `(r × v) / |r × v|`, same as W for QSW.
- **W-axis**: `T × N`.
- For circular orbits: T ≈ S (QSW).

---

## LOS (Line-of-Sight) frame

- **Origin**: chief spacecraft.
- **x_LOS**: unit vector from chief to deputy.
- **Azimuth**: angle in the local horizontal plane measured from the S-axis (along-track), positive toward the W-axis (cross-track).  Range: [0, 2π) rad.
- **Elevation**: angle above the local horizontal plane toward the orbit normal (W).  Range: [−π/2, π/2] rad.

---

## Docking frame

- **Origin**: deputy docking port.
- **z_DOCK**: docking approach axis (defined by vehicle geometry).
- **x_DOCK**, **y_DOCK**: lateral directions, right-handed triad.

The docking axis is defined per vehicle in `Vehicle.docking_axis_body`.

---

## Quaternion convention

**Repository-wide: SCALAR LAST**

```
q = [q_x, q_y, q_z, q_w]
```

- The scalar (real) component `q_w` is the **last** element.
- Unit quaternion: `|q| = 1`.
- Rotation semantics: **active rotation** of vectors.
- Body-to-inertial unless otherwise stated.
- Hamilton product for two quaternions:
  - `q1 ⊗ q2 = [w1*v2 + w2*v1 + v1×v2, w1*w2 - v1·v2]`
  - where `v = [q_x, q_y, q_z]`, `w = q_w`.

---

## Orbital element ordering

```
(a, e, i, RAAN, omega, M)
```

| Symbol | Name | Units | Range |
|--------|------|-------|-------|
| `a` | semi-major axis | m | > 0 |
| `e` | eccentricity | – | [0, 1) |
| `i` | inclination | rad | [0, π] |
| `RAAN` | right ascension of ascending node (Ω) | rad | [0, 2π) |
| `omega` | argument of perigee (ω) | rad | [0, 2π) |
| `M` | mean anomaly | rad | [0, 2π) |

---

## QNS ROE state ordering

```
delta_alpha_qns = [delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]
```

| Symbol | Definition | Units |
|--------|-----------|-------|
| `delta_a` | `(a_d - a_c) / a_c` | – |
| `delta_lambda` | `(M_d + ω_d) - (M_c + ω_c) + (Ω_d - Ω_c) cos(i_c)` | rad |
| `delta_ex` | `e_d cos(ω_d) - e_c cos(ω_c)` | – |
| `delta_ey` | `e_d sin(ω_d) - e_c sin(ω_c)` | – |
| `delta_ix` | `i_d - i_c` | rad |
| `delta_iy` | `(Ω_d - Ω_c) sin(i_c)` | rad |

Subscripts: `_c` = chief, `_d` = deputy.

---

## Angle wrapping rules

| Angle | Wrapping range |
|-------|----------------|
| Mean anomaly `M` | [0, 2π) |
| Argument of perigee `ω` | [0, 2π) |
| RAAN `Ω` | [0, 2π) |
| Inclination `i` | [0, π] – NOT wrapped |
| LOS azimuth | [0, 2π) |
| LOS elevation | [−π/2, π/2] – NOT wrapped |

---

## Unit system

All internal values are **SI**:
- Distances: metres [m]
- Velocities: metres/second [m/s]
- Angles: radians [rad]
- Time: seconds [s]
- Mass: kilograms [kg]
- Force: newtons [N]
- Torque: newton-metres [N·m]

**Silent unit conversion is forbidden.**  Units must be declared at every API boundary.

---

## References

1. Vallado, *Fundamentals of Astrodynamics and Applications*, 4th ed.
2. Montenbruck & Gill, *Satellite Orbits*, Springer, 2000.
3. Koenig, Guffanti, D'Amico, JGCD 2017.
4. Wertz (ed.), *Spacecraft Attitude Determination and Control*, 1978.
