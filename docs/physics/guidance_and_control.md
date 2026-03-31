# Guidance and Control

## Purpose

This document describes the guidance and control strategy objects implemented in `backend/app/algorithms/guidance.py` and `backend/app/algorithms/control.py`.

## Architecture

**Guidance and control are strictly separated** (AGENTS.md anti-pattern rule):

- **Guidance**: computes a desired state or delta-v request (intent, not actuation).
- **Control**: converts guidance commands into force/torque/acceleration (actuation).
- **Allocation**: converts control outputs into actuator commands (separate from control).

## Guidance laws

### `HoldPointGuidance`

Maintains a fixed ROE hold-point.

Strategy:
1. Compute ROE error: `delta = target_roe - current_roe`.
2. If `|delta| < dead_band`, return zero delta-v.
3. Otherwise, compute corrective manoeuvre using ROE control input matrix `Gamma`.

ROE control input matrix:
```
delta_alpha_new = delta_alpha_old + Gamma * delta_v
```

where `Gamma` maps a QSW delta-v impulse to a change in ROE (from Gauss variational equations).

### `RoeHomingGuidance`

Plans a sequence of impulsive manoeuvres to drive ROE from initial to target configuration.

Strategy:
1. Define target ROE state.
2. Compute `Gamma` matrix for `n_manoeuvres` epochs.
3. Solve least-squares problem: `min |delta_v|` subject to `Gamma * delta_v = target_roe - current_roe`.

### `ClosingGuidance`

Terminal closing toward the target from short range.

Strategy:
1. Compute LOS unit vector to target.
2. Compute velocity-to-be-gained: `delta_v = v_desired - v_current`.
3. `v_desired = -approach_speed * los_unit`.

### `RetreatGuidance`

Safe retreat from the target.

Strategy:
- Generate delta-v impulse along the outgoing LOS direction.

### Guidance command

All guidance laws produce a `GuidanceCommand`:

```python
@dataclass
class GuidanceCommand:
    delta_v_qsw_mps: NDArray[float64]  # requested delta-v [m/s] in QSW frame
    target_roe: QnsRoeState | None
    epoch_s: float
```

## Control laws

### `TranslationalController`

Converts a guidance delta-v request to a body-frame delta-v request.

Steps:
1. Rotate delta-v from QSW to ECI: `dv_eci = R_qsw_to_eci @ dv_qsw`.
2. Rotate from ECI to body: `dv_body = R_body_from_eci @ dv_eci`.
3. Apply magnitude limit: if `|dv_body| > max_dv`, clip proportionally.

### `AttitudePdController`

Quaternion proportional-derivative controller.

PD control law:
```
tau = -Kp * delta_q_xyz - Kd * omega_error
```

where:
- `delta_q_xyz` = vector part of attitude error quaternion.
- `omega_error = omega_body - omega_desired`.
- `Kp`, `Kd` = gain matrices (3×3 or scalar × identity).

## Phase awareness

Each guidance law is used within a specific mission phase type.  The `PhaseManager` activates the appropriate guidance law based on `MissionPhase.guidance_law`.

## Guidance → Control → Allocation chain

```
GuidanceLaw.compute_command()
    → GuidanceCommand (delta_v request)
    → TranslationalController.compute()
    → TranslationalControlOutput (delta_v in body frame)
    → ActuatorAllocator (future: thruster selection)
    → Thruster commands
```

## Status

All guidance and control classes are **stubs** scheduled for Phase 6 implementation.

## References

1. D'Amico, S. (2010). *Autonomous Formation Flying in Low Earth Orbit*. PhD thesis, TU Delft / DLR.
2. Schaub, H. & Junkins, J. L. (2018). *Analytical Mechanics of Space Systems*, 3rd ed.
3. Sullivan, J., Grimberg, S., & D'Amico, S. (2017). Comprehensive survey and assessment of spacecraft relative motion dynamics models. *JGCD*.
