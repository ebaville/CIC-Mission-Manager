# CIC Mission Manager

A mission-scenario tool for orbital proximity operations, rendezvous, inspection, and docking-like studies.

## Architecture

This is a monorepo containing:

- **`backend/`** – Python (FastAPI) backend owning all physics, simulation, and export logic.
- **`frontend/`** – Node.js / React / TypeScript web application for configuration, visualization, and export.
- **`docs/`** – Architecture, physics, API, and decision documentation.

## Design highlights

- **ROE-first relative dynamics** using the Koenig–Guffanti–D'Amico analytical STM as the default relative propagator.
- **Phase-based mission model**: the main abstraction is a `MissionPhase`, not a raw condition tree.
- **Absolute truth backbone**: chaser and target absolute states remain explicit and authoritative.
- **SI units everywhere** internally; explicit unit declarations at all API boundaries.
- **No physics in the frontend**; the frontend consumes typed API contracts only.

## Quick start

### Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Documentation

See the `docs/` folder for:

- [Architecture overview](docs/architecture/backend_architecture.md)
- [Physics models](docs/physics/absolute_orbit_models.md)
- [Frame conventions](docs/physics/frames_and_conventions.md)
- [API contracts](docs/architecture/api_contracts.md)

## Implementation roadmap

See [AGENTS.md](AGENTS.md) for the full design specification and phase-by-phase implementation order.