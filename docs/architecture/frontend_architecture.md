# Frontend Architecture

## Overview

The CIC Mission Manager frontend is a Node.js / React / TypeScript single-page application.  It is responsible for:

- scenario creation and editing,
- visualising simulation results,
- exporting results via the backend API.

**The frontend contains no physics logic.**  All physics, simulation, and export logic is in the Python backend.

## Technology stack

| Layer | Technology |
|-------|-----------|
| Bundler | Vite |
| UI framework | React 18 |
| Language | TypeScript (strict mode) |
| HTTP client | Axios |
| 2D plots | Plotly.js / react-plotly.js |
| 3D scene | Three.js / react-three-fiber (planned) |
| Routing | React Router v6 |
| Testing | Vitest + Testing Library |

## Directory structure

```
frontend/src/
  app/          – App-level constants (API base URL, defaults)
  api/          – Typed HTTP client functions
  models/       – TypeScript interfaces mirroring backend Pydantic schemas
  pages/        – Full-page React components
  components/   – Reusable UI components
  hooks/        – Custom React hooks
  plots/        – Plot components (ROE, QSW, LOS)
  scene/        – 3D scene components (planned)
  utils/        – Pure utility functions (formatting, etc.)
```

## Frontend rules

1. **TypeScript strict mode** is enabled in `tsconfig.json`.
2. **No physics in the frontend**.  Never compute orbital mechanics in TypeScript.
3. **No `any` types**.  All API responses are typed via `models/`.
4. The frontend always displays: active frame, selected physics model, active mission phase.
5. **Server-authoritative results**: simulation data is always fetched from the backend.
6. Local state is for editing only; it must round-trip through the backend before being treated as truth.

## Page structure

| Route | Page | Responsibility |
|-------|------|---------------|
| `/` | `ScenarioDashboardPage` | List all scenarios and their status |
| `/scenarios/new` | `ScenarioEditorPage` | Create and submit a new scenario |
| `/scenarios/:id` | `SimulationResultsPage` | View results, plots, exports |
| `/diagnostics` | `DiagnosticsPage` | Show available models and frames |

## Model alignment

TypeScript models in `src/models/` must stay aligned with backend Pydantic schemas.  Key files:
- `models/enums.ts` → mirrors `core/enums.py`
- `models/scenario.ts` → mirrors `schemas/scenario_schemas.py`
- `models/states.ts` → mirrors `schemas/simulation_schemas.py` + `domain/states.py`

When the backend schema changes, the corresponding TypeScript interface must be updated.

## API client

`src/api/client.ts` wraps all HTTP calls.  Rules:
- Explicit return types for every function.
- No `any` types.
- Unit comments on all numeric fields.
- Uses Vite's dev-server proxy (`/api` → `http://localhost:8000`) to avoid CORS issues in development.

## State management

- No global state manager in V1; React `useState` and `useEffect` per page.
- Custom hooks in `src/hooks/` encapsulate data-fetching logic.
- All mutations go through the API (no local-only state changes that bypass the backend).

## Testing

- `vitest` as the test runner.
- `@testing-library/react` for component tests.
- Tests must cover: API client contract, form validation, basic component rendering.
