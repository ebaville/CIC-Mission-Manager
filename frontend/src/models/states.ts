/**
 * models/states.ts – TypeScript models for simulation state objects.
 *
 * These mirror backend domain/states.py and schemas/simulation_schemas.py.
 * No physics logic here.
 */

import type { RelativeFrame } from './enums';

/** QNS ROE state. All quantities in SI (metres, radians). */
export interface QnsRoeState {
  delta_a: number;
  delta_lambda: number;
  delta_ex: number;
  delta_ey: number;
  delta_ix: number;
  delta_iy: number;
  /** Chief semi-major axis [m] used to normalise delta_a. */
  chief_a_m: number;
  /** Simulation epoch [s]. */
  epoch_s: number;
}

/** Relative Cartesian state in a named frame. Units: metres, metres/second. */
export interface RelativeCartesianState {
  /** Relative position [m], 3 elements. */
  rho_m: [number, number, number];
  /** Relative velocity [m/s], 3 elements. */
  rho_dot_mps: [number, number, number];
  frame: RelativeFrame;
  epoch_s: number;
}

/** Full simulation results response from the API. */
export interface SimulationResults {
  scenario_id: string;
  step_count: number;
  start_epoch_s: number;
  end_epoch_s: number;
  roe_time_series: QnsRoeState[];
  qsw_time_series: RelativeCartesianState[];
}
