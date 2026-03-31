# Backend Architecture

## Overview

The CIC Mission Manager backend is a Python FastAPI application that owns all physics, simulation, and export logic for orbital proximity-operations mission scenarios.

## Package structure

```
backend/app/
  core/           – Central conventions, enums, unit definitions (no logic)
  domain/         – Pure data objects (no framework, no physics)
  physics/        – Equations and transformations only
  algorithms/     – Strategy objects (guidance, navigation, control)
  services/       – Orchestration (simulation engine, phase manager, export)
  exporters/      – Output formatters (CSV, JSON, CIC OEM)
  schemas/        – Pydantic API request/response schemas
  api/v1/         – FastAPI route handlers (thin, no physics)
  tests/          – Unit and integration tests
  main.py         – FastAPI application entry point
```

## Layering rules

1. **Dependency direction**: `api → services → algorithms + physics → domain + core`.
2. **No upward dependencies**: domain objects do not import from services or API.
3. **Physics isolation**: equations live only in `physics/`; `services/` calls physics, never re-implements it.
4. **Thin routes**: no simulation logic in `api/`; routes validate input, delegate, return output.

## Core module

`core/conventions.py` is the **single authoritative source** for:
- Physical constants (mu, J2, Re)
- Frame definitions (ECI, QSW, TNW, LOS, DOCK)
- Quaternion ordering convention (scalar-last)
- Orbital element ordering
- Angle wrapping rules
- SI unit declarations

`core/enums.py` defines all enumerations used across the backend.  Never re-declare an enum outside this file.

## Domain layer

Pure Python dataclasses.  No framework imports.  All values in SI units.

Key objects:
- `AbsoluteOrbitalState` – Cartesian ECI position and velocity.
- `KeplerianElements` – Classical Keplerian elements (osculating or mean).
- `AttitudeState` – Quaternion + angular velocity.
- `QnsRoeState` – Quasi-nonsingular ROE state (the default propagated relative state).
- `RelativeCartesianState` – Derived Cartesian relative state in a named frame.
- `MeasurementPacket` – Sensor measurement with covariance.
- `Scenario`, `MissionPhase`, `Vehicle`, `Target` – Mission-level abstractions.

## Physics layer

Contains only equations and transformations.  No orchestration, no I/O.

Key modules:
| Module | Responsibility |
|--------|---------------|
| `absolute_propagation.py` | `OrbitPropagator` interface, `TwoBodyPropagator`, `J2Propagator` |
| `orbital_elements.py` | Cartesian ↔ Keplerian conversion |
| `roe_definitions.py` | QNS ROE definition, ROE ↔ Keplerian mapping |
| `roe_propagation.py` | KGD STM provider, `RoeSTMPropagator` |
| `roe_geometry.py` | ROE → QSW/LOS/DOCK Cartesian mapping |
| `frame_transforms.py` | ECI ↔ QSW ↔ TNW rotation matrices |
| `quaternion.py` | Quaternion algebra (scalar-last convention) |
| `attitude_dynamics.py` | Attitude propagator, pointing laws |
| `sensors.py` | Range/AzEl model, LOS model, noise models |

## Algorithms layer

Strategy objects for GNC (Guidance, Navigation, Control).

| Module | Responsibility |
|--------|---------------|
| `guidance.py` | `HoldPointGuidance`, `RoeHomingGuidance`, `ClosingGuidance`, `RetreatGuidance` |
| `navigation.py` | `RelativePoseEkf` (Extended Kalman Filter) |
| `control.py` | `TranslationalController`, `AttitudePdController` |
| `event_detection.py` | `PhaseEndEvent`, `KeepOutViolation` |

## Services layer

Orchestration services that compose physics and algorithms.

| Service | Responsibility |
|---------|---------------|
| `SimulationEngine` | Runs the full scenario; step loop; delegates to physics and algorithms |
| `PhaseManager` | Phase sequencing and transition logic |
| `ScenarioCompiler` | Validates scenario before simulation |
| `ResultsStore` | Accumulates simulation snapshots |
| `ExportManager` | Dispatches to the correct exporter |

## Simulation step sequence

For each time step the `SimulationEngine._step()` method:
1. Propagates absolute truth states (chief + deputy) via `OrbitPropagator`.
2. Computes chief mean elements for STM input.
3. Propagates QNS ROE state via `RoeSTMPropagator` (KGD STM).
4. Derives QSW and LOS Cartesian views via `RoeGeometryMapper`.
5. Generates sensor measurements via `MeasurementModel`.
6. Runs navigation filter predict + update cycle.
7. Computes guidance command via `GuidanceLaw`.
8. Computes control command via controller.
9. Logs `RelativeMotionSnapshot` to `ResultsStore`.

## API design

- All routes are under `/api/v1/`.
- Routes are thin: validate input → delegate to services → return schema.
- All enums are centralised in `core/enums.py`.
- Payloads declare units and frames explicitly.

## Testing strategy

See `app/tests/`:
- `unit/` – Fast, isolated tests for domain objects, physics functions, API endpoints.
- `integration/` – End-to-end scenario execution tests.

Numerical tests use physically motivated tolerances (not arbitrary loose tolerances).
