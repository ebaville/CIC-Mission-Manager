# ADR-002: Scalar-Last Quaternion Convention

**Status**: Accepted  
**Date**: 2026-03

## Context

Quaternion representations differ in the position of the scalar (real) component:
- **Scalar-last**: `[q_x, q_y, q_z, q_w]` (common in robotics, ROS, many libraries)
- **Scalar-first**: `[q_w, q_x, q_y, q_z]` (Hamilton convention, MATLAB Aerospace)

A single convention must be fixed to avoid conversion bugs.

## Decision

Use **scalar-last** convention throughout: `q = [q_x, q_y, q_z, q_w]`.

Defined in `backend/app/core/conventions.py::QUATERNION_CONVENTION`.

## Rationale

- Scalar-last is the most common convention in modern robotics and GNC software.
- Consistent with numpy quaternion libraries and many aerospace Python tools.
- The choice is less important than consistency; scalar-last is documented and enforced centrally.

## Consequences

- Every quaternion in the backend uses `[q_x, q_y, q_z, q_w]`.
- The `Quaternion` class in `physics/quaternion.py` enforces this ordering.
- All API schemas declare quaternions as 4-element arrays in this order.
- Frontend models mirror this ordering.
