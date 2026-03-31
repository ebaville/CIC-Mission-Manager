/**
 * models/scenario.ts – TypeScript models mirroring backend Pydantic schemas.
 *
 * Rules:
 *   - Keep aligned with backend schemas/scenario_schemas.py.
 *   - No physics logic here; these are data shapes only.
 *   - Explicit unit comments required on all numeric fields.
 */

import type { RelativeFrame, RelativeModelMode, MissionPhaseType, DragMode, GuidanceLawType } from './enums';

// ---------------------------------------------------------------------------
// Absolute orbital state
// ---------------------------------------------------------------------------

/** Cartesian ECI state. Units: metres and metres/second. Frame: ECI J2000. */
export interface AbsoluteOrbitalState {
  /** ECI position vector [m], 3 elements. */
  r_eci_m: [number, number, number];
  /** ECI velocity vector [m/s], 3 elements. */
  v_eci_mps: [number, number, number];
}

// ---------------------------------------------------------------------------
// Vehicle
// ---------------------------------------------------------------------------

export interface Vehicle {
  vehicle_id: string;
  name: string;
  /** Vehicle wet mass [kg]. */
  mass_kg: number;
  initial_abs_state: AbsoluteOrbitalState;
  /** Reference drag area [m²]. */
  drag_area_m2: number;
  drag_coeff: number;
}

// ---------------------------------------------------------------------------
// Perturbation configuration
// ---------------------------------------------------------------------------

export interface PerturbationConfig {
  use_j2: boolean;
  use_differential_drag: boolean;
  drag_mode: DragMode;
}

// ---------------------------------------------------------------------------
// Mission phase
// ---------------------------------------------------------------------------

export interface MissionPhase {
  phase_id: string;
  name: string;
  phase_type: MissionPhaseType;
  /** Phase duration [s]. */
  duration_s: number;
  relative_model: RelativeModelMode;
  guidance_law?: GuidanceLawType;
  output_frame: RelativeFrame;
  perturbation_config: PerturbationConfig;
  notes: string;
}

// ---------------------------------------------------------------------------
// Scenario
// ---------------------------------------------------------------------------

export interface ScenarioCreate {
  name: string;
  description: string;
  chief: Vehicle;
  deputy: Vehicle;
  phases: MissionPhase[];
  /** Simulation time step [s]. */
  time_step_s: number;
}

export interface ScenarioResponse {
  scenario_id: string;
  name: string;
  description: string;
  /** Sum of all phase durations [s]. */
  total_duration_s: number;
  phase_count: number;
  is_simulated: boolean;
}
