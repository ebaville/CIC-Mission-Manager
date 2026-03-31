# API Contracts

## General rules

- All routes are versioned under `/api/v1/`.
- No route contains physics logic (see `backend_architecture.md`).
- All request/response bodies are typed Pydantic schemas (see `backend/app/schemas/`).
- Enumerations are centralised in `backend/app/core/enums.py`.
- All payloads that contain physical quantities must declare units explicitly.
- Arrays without labeled schema fields are not allowed.

## Base URL

- Development: `http://localhost:8000/api/v1`
- Frontend proxied (Vite dev server): `/api/v1`

---

## Endpoints

### Health check

```
GET /health
```

Response:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

### Reference data

#### List available frames

```
GET /api/v1/reference/frames
```

Response:
```json
{
  "inertial_frames": ["ECI_J2000"],
  "relative_frames": ["QSW", "TNW", "LOS", "DOCK"]
}
```

#### List available physics models

```
GET /api/v1/reference/models
```

Response:
```json
{
  "relative_models": ["KGD_QNS_J2", "KGD_QNS_J2_DRAG", "HCW", "TRUTH_DIFFERENCE"],
  "default_relative_model": "KGD_QNS_J2"
}
```

---

### Scenarios

#### Validate a scenario

```
POST /api/v1/scenarios/validate
Content-Type: application/json
```

Request body: `ScenarioCreateSchema` (see below).

Response:
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": ["Chief initial orbit is below 200 km altitude."]
}
```

#### Simulate a scenario

```
POST /api/v1/scenarios/simulate
Content-Type: application/json
```

Request body: `ScenarioCreateSchema`.

Response (202 Accepted): `ScenarioResponseSchema`
```json
{
  "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "LEO Homing Demo",
  "description": "...",
  "total_duration_s": 7200.0,
  "phase_count": 2,
  "is_simulated": true
}
```

#### Retrieve results

```
GET /api/v1/scenarios/{scenario_id}/results
```

Response: `SimulationResultsSchema`
```json
{
  "scenario_id": "...",
  "step_count": 720,
  "start_epoch_s": 0.0,
  "end_epoch_s": 7200.0,
  "roe_time_series": [
    {
      "delta_a": 0.0,
      "delta_lambda": 0.001,
      "delta_ex": 0.0001,
      "delta_ey": 0.0,
      "delta_ix": 0.0002,
      "delta_iy": 0.0,
      "chief_a_m": 6778000.0,
      "epoch_s": 0.0
    }
  ],
  "qsw_time_series": [
    {
      "rho_m": [100.0, 500.0, 0.0],
      "rho_dot_mps": [0.0, 0.1, 0.0],
      "frame": "QSW",
      "epoch_s": 0.0
    }
  ]
}
```

#### Export results

```
POST /api/v1/scenarios/{scenario_id}/export
Content-Type: application/json
```

Request body:
```json
{
  "format": "CSV",
  "output_path": null
}
```

Response:
```json
{
  "file_path": "/path/to/output/results_<id>.csv"
}
```

---

## Schema reference

### AbsoluteOrbitalStateSchema

| Field | Type | Units | Notes |
|-------|------|-------|-------|
| `r_eci_m` | float[3] | m | ECI position, J2000 |
| `v_eci_mps` | float[3] | m/s | ECI velocity, J2000 |

### VehicleSchema

| Field | Type | Units | Notes |
|-------|------|-------|-------|
| `vehicle_id` | string | – | Unique ID |
| `name` | string | – | Label |
| `mass_kg` | float > 0 | kg | Wet mass |
| `initial_abs_state` | AbsoluteOrbitalStateSchema | – | ECI J2000 |
| `drag_area_m2` | float > 0 | m² | Reference drag area |
| `drag_coeff` | float > 0 | – | Cd |

### MissionPhaseSchema

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `phase_id` | string | – | Unique ID |
| `name` | string | – | Label |
| `phase_type` | MissionPhaseType enum | – | See core/enums.py |
| `duration_s` | float > 0 | – | Phase duration [s] |
| `relative_model` | RelativeModelMode enum | KGD_QNS_J2 | |
| `guidance_law` | GuidanceLawType \| null | null | Optional |
| `output_frame` | RelativeFrame enum | QSW | Primary output frame |
| `perturbation_config` | PerturbationConfigSchema | use_j2=true | |

### QnsRoeStateSchema

| Field | Type | Units | Notes |
|-------|------|-------|-------|
| `delta_a` | float | – | Relative SMA / chief SMA |
| `delta_lambda` | float | rad | Relative mean arg of latitude |
| `delta_ex` | float | – | Relative eccentricity x |
| `delta_ey` | float | – | Relative eccentricity y |
| `delta_ix` | float | rad | Relative inclination x |
| `delta_iy` | float | rad | Relative inclination y |
| `chief_a_m` | float | m | Chief SMA (for delta_a context) |
| `epoch_s` | float | s | Simulation epoch |

---

## Error responses

All error responses follow FastAPI's default format:

```json
{
  "detail": "Human-readable error message."
}
```

HTTP status codes:
- `200 OK` – Success.
- `202 Accepted` – Simulation submitted and completed (synchronous V1).
- `422 Unprocessable Entity` – Validation error (Pydantic).
- `501 Not Implemented` – Feature not yet implemented.
- `500 Internal Server Error` – Unexpected server error.
