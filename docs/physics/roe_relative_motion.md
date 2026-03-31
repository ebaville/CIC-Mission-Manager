# ROE Relative Motion

## Purpose

This document describes the Relative Orbital Element (ROE) based relative motion model used as the default analytical relative propagator.

## Model selection rationale

The default model is the **Koenig–Guffanti–D'Amico (KGD) analytical State Transition Matrix (STM)** for quasi-nonsingular ROE.

This model is preferred over Hill–Clohessy–Wiltshire (HCW) because:
- It is valid for **arbitrarily eccentric** chief orbits.
- It includes **J2** secular perturbation effects analytically.
- It supports **differential drag** modelling.
- It uses **ROE** as the internal state, which is more physically meaningful for formation-flying and rendezvous design.

HCW is retained as an optional fallback model for quick local previews only.

## Default state: Quasi-Nonsingular ROE

```
delta_alpha_qns = [delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]
```

Definitions (see `docs/physics/frames_and_conventions.md` for full table):

```
delta_a      = (a_d - a_c) / a_c
delta_lambda = (M_d + omega_d) - (M_c + omega_c) + (RAAN_d - RAAN_c) * cos(i_c)
delta_ex     = e_d*cos(omega_d) - e_c*cos(omega_c)
delta_ey     = e_d*sin(omega_d) - e_c*sin(omega_c)
delta_ix     = i_d - i_c
delta_iy     = (RAAN_d - RAAN_c) * sin(i_c)
```

The QNS state avoids the singular behaviour of the classical ROE at `e → 0` (near-circular orbit), while keeping a compact 6-parameter structure.

## Propagation model

The relative state is propagated by the closed-form STM:

```
delta_alpha(t) = Phi(t, t0) * delta_alpha(t0)
```

With control input:

```
delta_alpha(t) = Phi(t, t0) * delta_alpha(t0) + Gamma(t, t0) * u
```

where:
- `Phi` is the 6×6 KGD analytical STM.
- `Gamma` is the control input matrix (from Gauss variational equations in ROE form).
- `u` is the delta-v manoeuvre input [m/s] in QSW frame.

**This is NOT a numerical ODE integrator.**  The STM is evaluated analytically at each step.

## KGD STM structure

The KGD STM (Koenig, Guffanti, D'Amico 2017) is derived by:
1. First-order Taylor expansion of relative-motion equations in ROE.
2. Exact closed-form solution of the resulting linear differential system.

The STM includes:
- **Keplerian drift**: secular drift of `delta_lambda` due to semi-major axis difference.
- **J2 secular rates**: precession of `RAAN` and `omega` due to Earth oblateness.
- **Differential drag**: differential deceleration of deputy vs. chief (optional).

### Keplerian drift (dominant for SMA difference)

The dominant term is:

```
d(delta_lambda)/dt ≈ -3/2 * n * delta_a
```

where `n = sqrt(mu / a_c^3)` is the mean motion.

### J2 secular rates

For the chief orbit:

```
d(RAAN)/dt   = -3/2 * J2 * (Re/p)^2 * n * cos(i)
d(omega)/dt  =  3/4 * J2 * (Re/p)^2 * n * (5*cos^2(i) - 1)
```

where `p = a*(1-e^2)` is the semi-latus rectum.

These secular rates appear in the off-diagonal elements of the STM for `delta_iy` and `delta_ex`, `delta_ey`.

## Cartesian reconstruction

The ROE state is mapped to QSW Cartesian position/velocity using the first-order linearisation (KGD 2017, Appendix B):

```
rho_R = a_c * (delta_a - delta_ex*cos(u_c) - delta_ey*sin(u_c))
rho_S = a_c * (delta_lambda + 2*delta_ex*sin(u_c) - 2*delta_ey*cos(u_c) + ...)
rho_W = a_c * (delta_ix*sin(u_c) - delta_iy*cos(u_c))
```

where `u_c = M_c + omega_c` is the mean argument of latitude of the chief.

This mapping is implemented in `backend/app/physics/roe_geometry.py`.

## Perturbation configuration

```python
class RelativePerturbationConfig:
    use_j2: bool = True              # default: include J2
    use_differential_drag: bool = False   # default: no drag
    drag_mode: DragMode = DragMode.NONE
```

Default configuration:
- `use_j2 = True` for all scenarios.
- `use_differential_drag = False` for V1 (near-circular LEO with similar BCs).

## Architecture

See `docs/architecture/backend_architecture.md` for the class structure.

Key classes:
- `QnsRoeDefinition` – Computes ROE from absolute element pairs.
- `KoenigGuffantiDamicoSTM` – Provides the 6×6 STM.
- `RoeSTMPropagator` – Applies the STM to propagate the state.
- `RoeGeometryMapper` – Maps ROE → QSW/LOS/DOCK Cartesian.

## Validity domain

- Arbitrary chief eccentricity (no near-circular restriction for the KGD model).
- Small relative separations: `|delta_alpha| << 1` (first-order theory).
- J2 is the dominant perturbation; higher harmonics not included.
- Differential drag model assumes slowly varying ballistic coefficient difference.

## References

1. Koenig, J.-S., Guffanti, T., & D'Amico, S. (2017). *New State Transition Matrices for Spacecraft Relative Motion in Perturbed Orbits.* AIAA Journal of Guidance, Control, and Dynamics. DOI: 10.2514/1.G001514
2. D'Amico, S. (2010). *Autonomous Formation Flying in Low Earth Orbit.* PhD thesis, TU Delft / DLR.
3. Sullivan, J., Grimberg, S., & D'Amico, S. (2017). *Comprehensive Survey and Assessment of Spacecraft Relative Motion Dynamics Models.* JGCD.
