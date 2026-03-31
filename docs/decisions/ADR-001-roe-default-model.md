# ADR-001: ROE-Based Relative Dynamics as Default Model

**Status**: Accepted  
**Date**: 2026-03  
**Authors**: Design team

## Context

The tool requires a relative-motion model for proximity operations scenario analysis.  Two candidate approaches were evaluated:

1. **Hill–Clohessy–Wiltshire (HCW)**: Cartesian LVLH state, circular chief orbit, unperturbed.
2. **Koenig–Guffanti–D'Amico (KGD) ROE STM**: Quasi-nonsingular ROE state, arbitrary eccentricity, J2 + differential drag.

## Decision

Use the **KGD ROE STM** as the default internal relative-motion model.

The propagated internal state is `QnsRoeState` (quasi-nonsingular ROE).  Cartesian states (`RelativeCartesianState`) are derived views computed on demand for sensors, visualisation, and terminal operations.

## Consequences

**Positive:**
- Valid for eccentric orbits (no near-circular restriction on the chief).
- J2 secular effects included analytically.
- More physically meaningful state for formation-flying GNC.
- STM evaluation is computationally efficient (no ODE integration for relative state).

**Negative:**
- More complex to implement than HCW.
- Requires mean element conversion before applying the STM.
- First-order theory; not valid for very large formation sizes.

**Retained:**
- HCW is available as an optional fallback (`RelativeModelMode.HCW`).
- Yamanaka–Ankersen is a planned optional eccentric Cartesian model.

## References

- Koenig, Guffanti, D'Amico, JGCD 2017.
- AGENTS.md: "Relative motion is ROE-first" rule.
