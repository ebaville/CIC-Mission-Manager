# AGENTS.md

## Purpose

This repository contains the implementation of a mission-scenario tool for orbital proximity operations, rendezvous, inspection, and docking-like studies.

The tool must:
- be implemented with a **Python backend** for all physics, simulation, and export logic,
- expose a **web application frontend** implemented with **Node.js tooling**,
- remain architecturally compatible with future export toward **SIMU-CIC-like data families**,
- use a **phase-based mission model**,
- use **ROE-based relative dynamics** as the default analytical relative-motion representation,
- keep **absolute chaser and target propagation** as the truth backbone.

This file instructs coding agents how to work in this repository.

---

## Non-negotiable design rules

1. **Python owns the physics**
   - All orbital dynamics, attitude dynamics, relative dynamics, geometry, navigation, guidance, control, and exports must live in Python.
   - The frontend must never implement authoritative physics.
   - The frontend may display, edit, validate, and visualize scenario data only.

2. **Relative motion is ROE-first**
   - Do not build the tool around HCW Cartesian LVLH states.
   - The default relative state is **quasi-nonsingular ROE**.
   - Cartesian relative states are derived views for visualization, geometry, sensors, and terminal operations.

3. **Absolute truth remains authoritative**
   - Chaser and target absolute states must remain explicit runtime objects.
   - Relative truth must be reconstructible from absolute states.
   - Analytical relative models are operational/planning models unless clearly marked as truth models.

4. **Phase-based architecture**
   - The main user abstraction is a **mission phase**, not a raw condition tree.
   - Different phases may use different guidance laws, relative frames, active sensors, and constraints.

5. **Strict unit discipline**
   - Internal units: **SI only**.
   - Frames and units must be explicit at every API boundary.
   - Silent unit conversion is forbidden.

6. **No hidden conventions**
   - Quaternion ordering, handedness, frame definitions, orbital-element definitions, and angle conventions must be fixed centrally and documented.
   - Never duplicate frame logic ad hoc in multiple modules.

7. **Explainability over cleverness**
   - Prefer explicit domain objects and clear algebra over compact but opaque code.
   - Every important model must have a short technical docstring with equations, assumptions, and validity domain.

---

## Target stack

### Backend
- Python 3.12+
- FastAPI for HTTP API
- Pydantic for schema validation
- NumPy for linear algebra
- SciPy for numerical utilities
- Optional:
  - poliastro or custom utilities for orbital conversion helpers
  - pyarrow / pandas for tabular export
  - pytest for tests

### Frontend
- Node.js LTS
- TypeScript
- React
- Vite
- Recommended visualization:
  - Plotly for plots
  - Three.js or react-three-fiber for 3D scene rendering

### Repository philosophy
- Backend and frontend are separate apps in one monorepo.
- Physics logic must not leak into TypeScript.
- Frontend consumes typed API contracts only.

---

## Repository structure

```text
repo/
  AGENTS.md
  README.md

  backend/
    pyproject.toml
    app/
      api/
      core/
      domain/
      physics/
      algorithms/
      services/
      exporters/
      schemas/
      tests/
    scripts/

  frontend/
    package.json
    vite.config.ts
    src/
      app/
      components/
      pages/
      hooks/
      api/
      models/
      scene/
      plots/
      utils/
    public/

  docs/
    architecture/
    physics/
    api/
    decisions/
```

---

## Core architecture to preserve

### Domain layer

Contains pure business objects, no framework logic:

* `Scenario`
* `MissionPhase`
* `Vehicle`
* `Target`
* `Sensor`
* `GroundStation`
* `ConstraintSet`
* `AbsoluteOrbitalState`
* `AttitudeState`
* `QnsRoeState`
* `RelativeCartesianState`
* `MeasurementPacket`

### Physics layer

Contains equations and transformations:

* absolute orbit propagation
* orbital element conversion
* ROE definitions and mappings
* ROE-to-Cartesian reconstruction
* frame transformations
* quaternion kinematics
* rigid-body attitude dynamics
* environment models
* sensor measurement models

### Algorithms layer

Contains strategy objects:

* guidance laws
* navigation filters
* controllers
* event detection
* actuator allocation

### Services layer

Contains orchestration:

* simulation engine
* phase manager
* scenario compiler
* results store
* export manager

### API layer

Contains HTTP routes and schema adapters only.

### Frontend

Contains:

* scenario editor
* phase editor
* visualization
* export controls
* diagnostics pages

---

## Physics model priorities

### 1. Absolute orbit truth

Implement first:

* Two-body propagation
* Optional J2-enabled mode
* Ephemeris-import mode

Equation baseline:

```
dr_I/dt = v_I
dv_I/dt = -mu * r_I / |r_I|^3 + a_pert + a_ctrl
```

Requirements:

* ECI is the truth inertial frame.
* Output transforms to QSW/TNW/LOS must be centralized.
* Integrators must be replaceable behind an interface.

Recommended interfaces:

* `OrbitPropagator`
* `ElementConverter`
* `FrameTransformService`

---

### 2. Relative motion

#### Default model

Use the **Koenig–Guffanti–D'Amico analytical STM formulation** as the default operational relative-dynamics model.

Default state (quasi-nonsingular ROE):
```
delta_alpha_qns = [delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]
```

where:
```
delta_a      = (a_d - a_c) / a_c
delta_lambda = (M_d + omega_d) - (M_c + omega_c) + (Omega_d - Omega_c)*cos(i_c)
delta_ex     = e_d*cos(omega_d) - e_c*cos(omega_c)
delta_ey     = e_d*sin(omega_d) - e_c*sin(omega_c)
delta_ix     = i_d - i_c
delta_iy     = (Omega_d - Omega_c)*sin(i_c)
```

Implementation rules:

* The propagated state is ROE.
* Cartesian relative position/velocity are derived products.
* The relative STM provider must be swappable.

Required components:

* `QnsRoeDefinition`
* `RoeGeometryMapper`
* `StateTransitionMatrixProvider`
* `RoeRelativePropagator`

Also support:

* HCW as a simplified optional local model
* direct truth differencing from absolute states

Never make HCW the core state representation.

---

### 3. Attitude

Use quaternions as the default representation.

Required:

* quaternion normalization at every propagation step where needed
* explicit quaternion ordering convention in one place only
* rigid-body dynamics class
* pointing-law strategy classes

Required classes:

* `Quaternion`
* `AttitudePropagator`
* `AttitudeLaw`
* `TargetPointingLaw`
* `SunPointingLaw`
* `DockingAxisAlignmentLaw`

---

### 4. Sensors and navigation

Separate truth, measurements, and estimates.

Minimum sensors for first implementation:

* range / azimuth / elevation sensor
* line-of-sight sensor
* simple camera-feature measurement model

Minimum filters:

* linear KF where justified
* EKF for nonlinear measurement models

Required components:

* `MeasurementModel`
* `NoiseModel`
* `NavigationFilter`
* `RelativePoseEkf`

---

### 5. Guidance and control

Minimum guidance families:

* far-range orbital transfer
* ROE-based homing
* closing guidance
* hold-point logic
* retreat / abort guidance

Minimum control families:

* translational tracking control
* quaternion PD attitude control

Do not merge guidance and control into one class.

---

## API rules

### General

* FastAPI routes must be thin.
* No route may contain physics logic.
* Every request/response schema must be typed with Pydantic.
* Version APIs from the start: `/api/v1/...`

### Suggested endpoints

* `POST /api/v1/scenarios/validate`
* `POST /api/v1/scenarios/simulate`
* `GET /api/v1/scenarios/{id}/results`
* `POST /api/v1/scenarios/{id}/export`
* `GET /api/v1/reference/frames`
* `GET /api/v1/reference/models`

### API payload rules

* Payloads must explicitly declare units and frame identifiers where relevant.
* Avoid ambiguous arrays without labeled schema fields.
* All enums must be centralized.

---

## Frontend rules

1. TypeScript strict mode must be enabled.
2. No physics in the frontend.
3. The frontend must edit scenario intent, not low-level solver internals by default.
4. The frontend must always show: active frame, active unit system, selected physics model, active mission phase.

### Main frontend pages

* Scenario dashboard
* Vehicle and target definition
* Mission phase editor
* Constraint editor
* Simulation results
* Exports
* Diagnostics / model assumptions

---

## Coding standards

### Python

* Use type hints everywhere.
* Use dataclasses or Pydantic models where appropriate.
* Prefer composition over inheritance.
* Keep classes small and focused.
* Use pure functions for algebra-heavy operations where possible.

### TypeScript

* Use strict typing.
* Avoid `any`.
* Keep API client models aligned with backend schemas.
* Use reusable UI components, not page-local duplicated widgets.

### Naming

* Use explicit names: `chief_abs_state`, `deputy_abs_state`, `roe_state_qns`, `relative_state_qsw`.
* Do not use vague names like `data`, `obj`, `value`, `misc`.

---

## Testing policy

### Backend tests

Required categories:

* unit tests for math utilities
* unit tests for frame transforms
* unit tests for orbital-element conversion
* unit tests for ROE mapping
* unit tests for STM propagation
* unit tests for quaternion math
* integration tests for full scenario execution
* regression tests with stored golden cases

### Frontend tests

Required minimum:

* schema/form validation tests
* API client contract tests
* basic component rendering tests

### Numerical validation

Every major physics module must include at least one validation test against an analytic expectation or trusted reference.

---

## Documentation policy

Every major module must have: purpose, governing equations, assumptions, validity domain, units, frame conventions, references if applicable.

Required docs in `docs/physics/`:

* `absolute_orbit_models.md`
* `roe_relative_motion.md`
* `frames_and_conventions.md`
* `attitude_models.md`
* `sensor_models.md`
* `navigation_filters.md`
* `guidance_and_control.md`

Required docs in `docs/architecture/`:

* `backend_architecture.md`
* `frontend_architecture.md`
* `api_contracts.md`

---

## Implementation order

### Phase 1: foundations

* repository setup
* backend app skeleton
* frontend app skeleton
* shared docs
* central conventions module

### Phase 2: absolute dynamics

* Cartesian absolute state
* orbit propagator interface
* two-body propagator
* state logging
* basic results API

### Phase 3: relative dynamics

* ROE state definitions
* ROE converter from absolute states
* KGD STM provider
* ROE propagation service
* ROE-to-QSW mapping
* relative plots

### Phase 4: attitude and pointing

* quaternion utilities
* attitude propagation
* phase-based pointing laws
* target-pointing visualization

### Phase 5: sensors and navigation

* measurement models
* EKF
* estimated-vs-truth diagnostics

### Phase 6: guidance and control

* hold-point guidance
* homing guidance
* closing guidance
* basic translational and attitude controllers

### Phase 7: export layer

* CSV export
* JSON/YAML scenario export
* CIC-like export families
* VTS-oriented package generation hooks

### Phase 8: hardening

* regression suite
* API refinement
* UX cleanup
* docs completion

---

## Anti-patterns to avoid

Do not:

* put simulation logic in FastAPI routes
* put physics logic in React components
* use HCW as the repository-wide default relative state
* duplicate frame transform formulas across files
* mix osculating and mean elements silently
* hide model assumptions in frontend labels only
* build one giant `Simulator` class that knows everything
* serialize raw NumPy arrays without schema metadata
* use notebook code as production source

---

## Expected deliverables from coding agents

When implementing a new feature, produce:

1. code,
2. tests,
3. docstrings,
4. one short architecture note if the design changed,
5. at least one usage example or fixture.

When adding a new physics model, also provide:

* governing equations summary,
* assumptions,
* validity range,
* comparison against existing model where relevant.

---

## Preferred first milestone

A usable first milestone is:

* one Python backend service,
* one React frontend,
* one scenario with:
  * chief target in Earth orbit,
  * deputy chaser,
  * quasi-nonsingular ROE propagation,
  * QSW relative-state reconstruction,
  * simple range/azimuth/elevation sensor,
  * basic results plots,
  * export to CSV and JSON.

---

## Final rule

When uncertain, prefer:

* clearer abstractions,
* stronger typing,
* explicit conventions,
* smaller modules,
* testable math,
* backend authority over frontend convenience.
