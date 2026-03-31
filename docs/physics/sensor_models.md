# Sensor Models

## Purpose

This document describes the sensor measurement models implemented in `backend/app/physics/sensors.py`.

## Design principle

Sensors are separated into three layers:
1. **Truth**: true relative state (from simulation propagation).
2. **Measurement**: noisy measurement generated from truth.
3. **Estimate**: navigation filter estimate (from navigation filters).

This separation enables clean diagnostics by comparing truth vs. measured vs. estimated states.

## Range / Azimuth / Elevation sensor (`RangeAzElModel`)

### Measurement vector

```
z = [range [m], azimuth [rad], elevation [rad]]
```

### Governing equations

```
range     = |rho_QSW|                           [m]
azimuth   = atan2(rho_W, rho_S)                 [rad]
elevation = arcsin(rho_R / range)               [rad]
```

where `rho_QSW = [rho_R, rho_S, rho_W]` is the relative position in QSW frame.

### Sign convention (see `docs/physics/frames_and_conventions.md`)

- Azimuth: measured from the S-axis (along-track), positive toward the W-axis (cross-track).  Range: [0, 2π).
- Elevation: measured from the local horizontal plane toward the orbit normal, positive upward.  Range: [−π/2, π/2].

### Noise model

Additive Gaussian white noise:

```
z_meas = z_true + noise
noise ~ N(0, R)  where R = diag(sigma_range², sigma_az², sigma_el²)
```

Typical values (TBD):
- `sigma_range ≈ 1–10 m`
- `sigma_az ≈ 0.001–0.01 rad`
- `sigma_el ≈ 0.001–0.01 rad`

### Assumptions

- Unobstructed line of sight; no occlusion modelling.
- No bias; no correlated noise.
- Not valid when `range < 1 mm` (numerical singularity).

## Line-of-Sight sensor (`LineOfSightModel`)

### Measurement vector

```
z = [azimuth [rad], elevation [rad]]
```

No range measurement.

### Governing equations

Same as RangeAzEl but without range output.

## Noise model (`NoiseModel`)

```python
class NoiseModel:
    sigma_1sigma: list[float]  # 1-sigma noise standard deviations [SI units]
```

Provides:
- `covariance` property: returns diagonal `R = diag(sigma²)`.
- `sample()`: draws one Gaussian noise vector from `N(0, R)`.

## Sensor descriptor (domain layer)

`domain/sensor.py` defines the sensor descriptor objects:
- `Sensor` – base class with `sensor_id`, `sensor_type`, `noise_1sigma`, `fov_half_angle_rad`.
- `RangeAzElSensor` – concrete descriptor for the RangeAzEl model.
- `LineOfSightSensor` – concrete descriptor for the LOS model.

The descriptor lives in the domain layer (no physics).  The measurement model (with equations) lives in the physics layer.

## FOV check

If `Sensor.fov_half_angle_rad` is set, the sensor measures only when the deputy is within the cone:

```
angle = arccos(dot(los_unit_body, mount_axis_body))
is_valid = angle <= fov_half_angle_rad
```

## Status

`RangeAzElModel` and `LineOfSightModel` are **stubs** scheduled for Phase 5 implementation.

## References

1. Bar-Shalom, Y., Li, X. R., & Kirubarajan, T. (2001). *Estimation with Applications to Tracking and Navigation*. Wiley.
