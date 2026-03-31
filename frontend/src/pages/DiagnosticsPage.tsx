/**
 * pages/DiagnosticsPage.tsx – Physics model diagnostics page.
 *
 * Displays:
 *   - Available physics models (from GET /api/v1/reference/models).
 *   - Available frames (from GET /api/v1/reference/frames).
 *   - API health status.
 *
 * Always shows the active model assumptions to support explainability.
 */

import React, { useEffect, useState } from 'react';
import { getFrames, getModels } from '../api/client';
import type { FramesResponse, ModelsResponse } from '../api/client';

const DiagnosticsPage: React.FC = () => {
  const [frames, setFrames] = useState<FramesResponse | null>(null);
  const [models, setModels] = useState<ModelsResponse | null>(null);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    Promise.all([getFrames(), getModels()])
      .then(([f, m]) => {
        setFrames(f);
        setModels(m);
      })
      .catch(() => setError('Backend unavailable. Is the Python backend running?'));
  }, []);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h1>Diagnostics &amp; Model Assumptions</h1>

      <section>
        <h2>API Backend</h2>
        {frames && models ? (
          <p style={{ color: 'green' }}>✓ Backend connected</p>
        ) : (
          <p>Connecting…</p>
        )}
      </section>

      {frames && (
        <section>
          <h2>Available Reference Frames</h2>
          <h3>Inertial</h3>
          <ul>
            {frames.inertial_frames.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
          <h3>Relative / Local Orbital</h3>
          <ul>
            {frames.relative_frames.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
        </section>
      )}

      {models && (
        <section>
          <h2>Available Relative Dynamics Models</h2>
          <p>
            <strong>Default:</strong> {models.default_relative_model}
          </p>
          <ul>
            {models.relative_models.map((m) => (
              <li key={m}>{m}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
};

export default DiagnosticsPage;
