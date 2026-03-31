# Navigation Filters

## Purpose

This document describes the navigation filter implemented in `backend/app/algorithms/navigation.py`.

## Architecture

Navigation is separated from truth and guidance:
- **Truth**: absolute and relative states from the simulation propagator.
- **Measurements**: noisy sensor outputs from `physics/sensors.py`.
- **Estimates**: navigation filter outputs (`FilterStateEstimate`).

Filters consume explicit `MeasurementPacket` objects, not raw arrays.

## State vector

The relative navigation filter state is:

```
x = [rho_R, rho_S, rho_W, rho_dot_R, rho_dot_S, rho_dot_W]   [QSW Cartesian, 6 states]
```

## Relative Pose EKF (`RelativePoseEkf`)

### Process model

The process model uses the ROE STM (converted to Cartesian space) for the predict step.

Predict step:
```
x_k+1|k   = F_k * x_k
P_k+1|k   = F_k * P_k * F_k^T + Q_k
```

where:
- `F_k` = process Jacobian (linearised relative motion).
- `Q_k` = process noise covariance matrix.

### Measurement model

The measurement model `h(x)` maps the Cartesian relative state to sensor outputs.

For the RangeAzEl sensor:
```
h(x) = [|rho|, atan2(rho_W, rho_S), arcsin(rho_R / |rho|)]
```

The Jacobian `H = dh/dx` is computed analytically.

Update step (standard EKF):
```
S   = H * P * H^T + R
K   = P * H^T * S^{-1}             (Kalman gain)
x   = x + K * (z - h(x))
P   = (I - K * H) * P
```

The Joseph form is preferred for numerical stability:
```
P   = (I - K * H) * P * (I - K * H)^T + K * R * K^T
```

### Initial conditions

The initial state estimate can be seeded from:
1. The absolute state difference (truth difference).
2. A first measurement (if sufficiently informative).

The initial covariance `P_0` must reflect the actual initial uncertainty.

### Assumptions

- Zero-mean Gaussian measurement noise.
- No systematic biases.
- Gaussian process noise.
- Measurement Jacobian is accurate (valid for small measurement residuals).

### Validity domain

- Valid for near-linear measurement models (range > ~10 m to avoid singularity in elevation).
- Not valid when the deputy is directly overhead or below (elevation ≈ ±π/2).

## `FilterStateEstimate` object

```python
@dataclass
class FilterStateEstimate:
    x_hat: NDArray[float64]   # state estimate (n,)
    P: NDArray[float64]       # covariance (n, n)
    epoch_s: float
```

## Status

`RelativePoseEkf` is a **stub** scheduled for Phase 5 implementation.

## References

1. Bar-Shalom, Y., Li, X. R., & Kirubarajan, T. (2001). *Estimation with Applications to Tracking and Navigation*. Wiley.
2. D'Amico, S. (2010). *Autonomous Formation Flying in Low Earth Orbit*. PhD thesis. Chapter 5.
