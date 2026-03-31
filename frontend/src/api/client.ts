/**
 * api/client.ts – Typed HTTP API client.
 *
 * All physics and simulation data is fetched from the Python backend.
 * No physics is computed here.
 *
 * Rules:
 *   - Use explicit typed return types for all functions.
 *   - Declare units in comments on all numeric fields.
 *   - No `any` types.
 */

import axios from 'axios';
import type { ScenarioCreate, ScenarioResponse } from '../models/scenario';
import type { SimulationResults } from '../models/states';
import type { ExportFormat } from '../models/enums';

const BASE_URL = '/api/v1';

const http = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// ---------------------------------------------------------------------------
// Reference endpoints
// ---------------------------------------------------------------------------

export interface FramesResponse {
  inertial_frames: string[];
  relative_frames: string[];
}

export interface ModelsResponse {
  relative_models: string[];
  default_relative_model: string;
}

export async function getFrames(): Promise<FramesResponse> {
  const { data } = await http.get<FramesResponse>('/reference/frames');
  return data;
}

export async function getModels(): Promise<ModelsResponse> {
  const { data } = await http.get<ModelsResponse>('/reference/models');
  return data;
}

// ---------------------------------------------------------------------------
// Scenario endpoints
// ---------------------------------------------------------------------------

export async function validateScenario(
  scenario: ScenarioCreate
): Promise<{ is_valid: boolean; errors: string[]; warnings: string[] }> {
  const { data } = await http.post('/scenarios/validate', scenario);
  return data;
}

export async function simulateScenario(
  scenario: ScenarioCreate
): Promise<ScenarioResponse> {
  const { data } = await http.post<ScenarioResponse>('/scenarios/simulate', scenario);
  return data;
}

export async function getResults(
  scenarioId: string
): Promise<SimulationResults> {
  const { data } = await http.get<SimulationResults>(
    `/scenarios/${scenarioId}/results`
  );
  return data;
}

export async function exportResults(
  scenarioId: string,
  format: ExportFormat
): Promise<{ file_path: string }> {
  const { data } = await http.post(`/scenarios/${scenarioId}/export`, { format });
  return data;
}
