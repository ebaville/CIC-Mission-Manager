/**
 * pages/ScenarioEditorPage.tsx – Scenario creation and phase editor.
 *
 * Allows the user to:
 *   - Define chief and deputy vehicles (initial states, mass, drag).
 *   - Create and order mission phases.
 *   - Set perturbation model and guidance law per phase.
 *   - Validate and submit the scenario for simulation.
 *
 * Rules:
 *   - No physics here; submits JSON to the backend for simulation.
 *   - Always display: active frame, selected physics model, active phase.
 */

import React, { useState } from 'react';
import { simulateScenario, validateScenario } from '../api/client';
import type { ScenarioCreate } from '../models/scenario';
import { DragMode, MissionPhaseType, RelativeFrame, RelativeModelMode } from '../models/enums';

const ScenarioEditorPage: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [status, setStatus] = useState<string>('');

  const handleSubmit = async (): Promise<void> => {
    // TODO: build ScenarioCreate from form state and call simulateScenario
    setStatus('Scenario submission is not yet implemented.');
  };

  return (
    <div>
      <h1>New Scenario</h1>

      <section>
        <h2>Scenario Name</h2>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter scenario name"
          style={{ width: '300px' }}
        />
      </section>

      <section>
        <h2>Chief (Target) Vehicle</h2>
        {/* TODO: VehicleForm component */}
        <p><em>Vehicle definition form – TODO</em></p>
      </section>

      <section>
        <h2>Deputy (Chaser) Vehicle</h2>
        {/* TODO: VehicleForm component */}
        <p><em>Vehicle definition form – TODO</em></p>
      </section>

      <section>
        <h2>Mission Phases</h2>
        {/* TODO: PhaseEditor component */}
        <p><em>Phase editor – TODO</em></p>
      </section>

      <button onClick={handleSubmit}>Validate &amp; Simulate</button>

      {status && <p>{status}</p>}
    </div>
  );
};

export default ScenarioEditorPage;
