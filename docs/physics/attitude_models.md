# Attitude Models

## Purpose

This document describes the attitude dynamics and pointing law models implemented in `backend/app/physics/attitude_dynamics.py` and `backend/app/physics/quaternion.py`.

## Quaternion convention

**SCALAR LAST**: `q = [q_x, q_y, q_z, q_w]`

The scalar component `q_w` is the last element.  This is the repository-wide convention.  See `backend/app/core/conventions.py` and `docs/physics/frames_and_conventions.md`.

## Quaternion kinematics

The time evolution of the attitude quaternion is governed by:

```
dq/dt = 0.5 * q ⊗ [omega_x, omega_y, omega_z, 0]
```

where:
- `q` = body-to-inertial quaternion `[q_x, q_y, q_z, q_w]`
- `omega` = angular velocity in body frame [rad/s]
- `⊗` = Hamilton product

This is implemented in `physics/quaternion.py::quaternion_kinematics()`.

## Rigid-body attitude dynamics (Euler equations)

The rotational equations of motion are:

```
I * d(omega)/dt = tau - omega × (I * omega)
```

where:
- `I` = inertia tensor in body frame [kg·m²], shape (3, 3)
- `omega` = angular velocity in body frame [rad/s]
- `tau` = applied torque in body frame [N·m]
- `×` = cross product

These are the Euler rigid-body equations, implemented in `physics/attitude_dynamics.py::AttitudePropagator`.

## Attitude error quaternion

For a PD controller, the attitude error is computed as:

```
delta_q = q_desired^{-1} ⊗ q_current
```

The vector part `delta_q_xyz = [delta_q_x, delta_q_y, delta_q_z]` is the control error.

## Pointing laws

### TargetPointingLaw

Aligns a specified body axis toward the nadir direction.

Algorithm:
1. Compute nadir unit vector: `n = -r / |r|` in ECI.
2. Compute rotation aligning `pointing_axis_body` to `n`.
3. Return the corresponding unit quaternion.

### SunPointingLaw

Aligns the solar panel normal toward the Sun direction for maximum power generation.

Requires: Sun ephemeris (simplified analytic model acceptable for V1).

### DockingAxisAlignmentLaw

Aligns the docking axis toward the target docking port.

Used during final approach and docking.

## AttitudePropagator

Uses SciPy RK45 to integrate the 7-element state vector `[q_x, q_y, q_z, q_w, omega_x, omega_y, omega_z]` forward in time.

Quaternion normalisation is enforced at every step to prevent numerical drift.

## Quaternion class

`physics/quaternion.py::Quaternion` provides:
- `multiply(other)` – Hamilton product.
- `conjugate()` – Quaternion inverse (for unit quaternions).
- `normalize()` – Return normalised copy.
- `rotate_vector(v)` – Active rotation of a 3-vector.
- `to_dcm()` – Convert to 3×3 direction cosine matrix.
- `from_dcm(dcm)` – Convert DCM to quaternion (Shepperd's method).
- `attitude_error(q_ref)` – Compute error quaternion.

## Assumptions

- Rigid body; flexible dynamics are not modelled.
- Torques include commanded + disturbance torques; no actuator dynamics.
- No reaction wheel saturation modelling in V1.

## Status

`AttitudePropagator` and `Quaternion` algebra methods are **stubs** scheduled for Phase 4 implementation.

## References

1. Schaub, H. & Junkins, J. L. (2018). *Analytical Mechanics of Space Systems*, 3rd ed. AIAA.
2. Wertz, J. R. (ed.) (1978). *Spacecraft Attitude Determination and Control*. Kluwer.
3. Shepperd, S. W. (1978). Quaternion from rotation matrix. *JGCD*, 1(3), 223–224.
