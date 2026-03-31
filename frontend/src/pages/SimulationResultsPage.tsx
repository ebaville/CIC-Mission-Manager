/**
 * pages/SimulationResultsPage.tsx – Simulation results viewer.
 *
 * Displays:
 *   - ROE state time series.
 *   - QSW relative position plots.
 *   - Active mission phase timeline.
 *   - Export controls.
 *
 * Rules:
 *   - All data fetched from the backend; no physics computed here.
 *   - Always display active frame and selected model.
 */

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getResults } from '../api/client';
import type { SimulationResults } from '../models/states';

const SimulationResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [results, setResults] = useState<SimulationResults | null>(null);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (!id) return;
    getResults(id)
      .then(setResults)
      .catch((err: unknown) => {
        setError('Failed to load results. Has this scenario been simulated?');
      });
  }, [id]);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!results) return <p>Loading results for scenario {id}…</p>;

  return (
    <div>
      <h1>Simulation Results – {results.scenario_id}</h1>
      <p>
        Steps: {results.step_count} | Duration:{' '}
        {(results.end_epoch_s - results.start_epoch_s).toFixed(0)} s
      </p>

      <section>
        <h2>ROE Time Series</h2>
        {/* TODO: RoePlot component */}
        <p><em>ROE plot – TODO</em></p>
      </section>

      <section>
        <h2>QSW Relative Position</h2>
        {/* TODO: QswPlot component */}
        <p><em>QSW plot – TODO</em></p>
      </section>

      <section>
        <h2>Export</h2>
        {/* TODO: ExportControls component */}
        <p><em>Export controls – TODO</em></p>
      </section>
    </div>
  );
};

export default SimulationResultsPage;
