# SPECS.md

## 1. Product name

**Working name:** RPO Mission Scenario Tool — MVP

---

## 2. Purpose

This MVP is a lightweight mission-scenario tool for orbital proximity operations.

It must allow a user to:
- define one target and one chaser,
- run a simple orbital and relative-motion simulation,
- visualize results in a browser,
- inspect simple pointing and measurement outputs,
- run a minimal closed-loop hold-point case,
- export scenario and result files.

The MVP is not intended to be a full GNC laboratory. It is intended to prove the end-to-end architecture:
- Python backend for physics and simulation,
- Node.js/React frontend for editing, running, and viewing scenarios,
- simple but structured outputs,
- future extensibility toward a richer rendezvous and inspection tool.

This direction remains aligned with the SIMU-CIC philosophy of scenario simulation plus exportable engineering datasets, while simplifying the user workflow for chaser-target missions. SIMU-CIC already provides orbit, attitude, sensor, export, and visualization-oriented outputs, which motivates the architecture of this tool. :contentReference[oaicite:1]{index=1}

---

## 3. MVP goals

### 3.1 Primary goals
- Deliver one complete browser-based simulation workflow.
- Keep all physics and simulation in Python.
- Provide a minimal but clear web UI.
- Support one nominal Earth-orbit proximity scenario.
- Prove the core domain model:
  - scenario,
  - target,
  - chaser,
  - simulation results,
  - export.

### 3.2 Secondary goals
- Keep the codebase easy to extend.
- Make the tool understandable to system engineers.
- Preserve explicit frames, units, and conventions.
- Prepare for future export families inspired by SIMU-CIC. :contentReference[oaicite:2]{index=2}

---

## 4. Non-goals for the MVP

The MVP explicitly does **not** include:
- docking contact dynamics,
- manipulator dynamics,
- plume impingement,
- flexible appendages,
- full navigation filter stack as a mandatory feature,
- optimal rendezvous guidance,
- actuator allocation optimization,
- multi-chaser or multi-target scenarios,
- full CIC/VTS compatibility,
- high-fidelity perturbation models beyond the minimum selected set.

---

## 5. Users

### 5.1 Primary users
- system engineers,
- mission analysts,
- GNC engineers doing early studies,
- internal software engineers building the platform.

### 5.2 Expected usage
The MVP is for:
- early design demonstration,
- architecture validation,
- simple scenario walkthroughs,
- internal testing,
- future development foundation.

---

## 6. MVP scope

## 6.1 Mission scope
The MVP shall support:
- Earth orbit only,
- 1 target,
- 1 chaser,
- one nominal mission flow,
- one simple closed-loop hold-point mode.

## 6.2 Physics scope
The MVP shall support:
- absolute Cartesian state propagation,
- two-body orbital propagation,
- relative state computation from absolute states,
- simple relative outputs in QSW,
- simple target-pointing attitude mode,
- one synthetic measurement family,
- one simple hold-point guidance mode,
- one simple translational controller.

## 6.3 Frontend scope
The MVP shall support:
- one scenario editor page,
- one results page,
- one pointing/diagnostics panel,
- one export panel.

---

## 7. Governing design principles

### 7.1 Python owns the physics
All authoritative physics and simulation logic shall be implemented in Python.

### 7.2 Frontend does not own the simulation
The frontend may:
- edit scenarios,
- submit runs,
- retrieve results,
- display plots and diagnostics,
- trigger exports.

The frontend shall not implement authoritative orbital or attitude dynamics.

### 7.3 Keep the MVP simple
The MVP must prefer:
- fewer models,
- fewer switches,
- clear behavior,
- explicit schemas,
- deterministic results.

### 7.4 Explicit conventions
Frames, units, and quaternion conventions shall be explicit and centralized.

### 7.5 End-to-end first
The MVP must prioritize a complete working scenario flow over feature breadth.

---

## 8. Technology stack

## 8.1 Backend
- Python 3.12+
- FastAPI
- Pydantic
- NumPy
- SciPy
- pytest

## 8.2 Frontend
- Node.js LTS
- TypeScript
- React
- Vite
- Plotly for charts

---

## 9. Repository structure

```text
repo/
  AGENTS.md
  SPECS.md
  README.md

  backend/
    app/
      api/
      domain/
      physics/
      services/
      schemas/
      tests/

  frontend/
    src/
      pages/
      components/
      api/
      models/
      plots/

  docs/
