# Absolute Orbit Models

## Purpose

This document describes the absolute orbit propagation models implemented in `backend/app/physics/absolute_propagation.py`.

## Governing equations

The equations of motion for a spacecraft in the gravitational field of Earth are:

```
dr/dt = v
dv/dt = -mu/|r|^3 * r + a_pert + a_ctrl
```

where:
- `r` = ECI position vector [m]
- `v` = ECI velocity vector [m/s]
- `mu` = Earth gravitational parameter = 3.986004418 × 10¹⁴ m³/s²
- `a_pert` = sum of perturbation accelerations [m/s²]
- `a_ctrl` = control (thrust) acceleration [m/s²]

## Two-body model (`TwoBodyPropagator`)

### Assumptions

- Point-mass Earth; no oblateness, no atmospheric drag, no solar radiation pressure.
- Only gravitational acceleration acts on the spacecraft (no perturbations unless `a_ctrl` is provided).

### Validity domain

- Circular to highly elliptic Earth orbits.
- Suitable for short time arcs (minutes to hours) where perturbations are negligible.
- Not suitable for long-duration LEO propagation (secular J2 drift not captured).

### Implementation

Uses SciPy RK45 adaptive-step numerical integrator.

Tolerances:
- `rtol = 1e-10`
- `atol = 1e-12`

These are conservative defaults to ensure energy conservation < 1 ppm per step.

### Conservation laws

For unperturbed two-body motion:
- Specific orbital energy `E = v²/2 - mu/r` is conserved.
- Specific angular momentum `h = r × v` is conserved (magnitude and direction).

Both are validated in `app/tests/unit/test_two_body_propagator.py`.

## J2 model (`J2Propagator`)

### Perturbation equation

The J2 zonal harmonic acceleration in ECI is:

```
a_J2 = (3/2) * J2 * mu * Re² / r^5 *
       [ x*(5*(z/r)² - 1),
         y*(5*(z/r)² - 1),
         z*(5*(z/r)² - 3) ]
```

where:
- `J2 = 1.08262668 × 10⁻³`
- `Re = 6,378,137 m` (Earth equatorial radius)
- `r = |r|`

### Assumptions

- Only J2 is included; higher-order zonals (J3, J4, ...) are not modelled.
- Drag, solar radiation pressure, and lunar/solar gravity are not included.

### Validity domain

- LEO to GEO.
- Accurate for secular drift rates over days to weeks.
- Not suitable for precise long-term orbit determination.

### Status

`J2Propagator` is a **stub** (raises `NotImplementedError`); it is scheduled for Phase 2 implementation.

## Frame convention

The inertial frame used for all absolute states is **ECI J2000**:
- Origin: Earth centre of mass.
- X-axis: vernal equinox at J2000.0.
- Z-axis: Earth north celestial pole at J2000.0.
- Right-handed triad.

See `core/conventions.py` for the authoritative definition.

## Integrator interface

All propagators implement the `OrbitPropagator` abstract interface:

```python
class OrbitPropagator(ABC):
    def propagate(
        self,
        state: AbsoluteOrbitalState,
        dt_s: float,
        control_accel_mps2: Optional[NDArray] = None,
    ) -> AbsoluteOrbitalState: ...
```

This allows the integrator to be swapped without changing the simulation engine.

## References

1. Montenbruck & Gill, *Satellite Orbits*, Springer, 2000. Chapter 3.
2. Vallado, *Fundamentals of Astrodynamics and Applications*, 4th ed. Chapter 9.
