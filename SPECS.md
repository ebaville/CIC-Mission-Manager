# SPECS.md

> **Note:** The full MVP specification lives in [`docs/MVP_Specs.md`](docs/MVP_Specs.md).  
> This file is the canonical entry-point reference for the project specification.

## Quick Summary

**Working name:** RPO Mission Scenario Tool — MVP

A lightweight mission-scenario tool for orbital proximity operations (RPO).  
Designed to prove end-to-end architecture from Python physics backend to React frontend,
with structured scenario exports compatible with SIMU-CIC data families.

### Scope
- One target + one chaser in Earth orbit
- Quasi-nonsingular ROE relative-motion propagation (Koenig–Guffanti–D'Amico STM)
- Phase-based mission model
- Browser-based scenario editor, simulation run, and results viewer
- Export to CSV and JSON

### Key Design Rules
- Python owns all physics and simulation logic
- Frontend edits scenario intent; no physics in TypeScript
- Internal units: SI only
- Default relative state: quasi-nonsingular ROE (6-element vector)

### See Also
- [`docs/MVP_Specs.md`](docs/MVP_Specs.md) – Full product specification
- [`docs/architecture/backend_architecture.md`](docs/architecture/backend_architecture.md)
- [`docs/architecture/frontend_architecture.md`](docs/architecture/frontend_architecture.md)
- [`docs/architecture/api_contracts.md`](docs/architecture/api_contracts.md)
- [`AGENTS.md`](AGENTS.md) – Coding agent instructions and design rules
- [`README.md`](README.md) – Setup and usage guide
