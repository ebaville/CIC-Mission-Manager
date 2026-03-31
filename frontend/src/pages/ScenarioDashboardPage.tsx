/**
 * pages/ScenarioDashboardPage.tsx – Scenario list and dashboard.
 *
 * Displays all available scenarios and their simulation status.
 * Provides navigation to create new scenarios or view results.
 */

import React from 'react';

const ScenarioDashboardPage: React.FC = () => {
  return (
    <div>
      <h1>Scenario Dashboard</h1>
      <p>
        Welcome to the CIC Mission Manager. Create a new scenario or select an
        existing one to view simulation results.
      </p>
      {/* TODO: fetch and list scenarios from GET /api/v1/scenarios */}
      <p>
        <em>No scenarios yet. Use &quot;New Scenario&quot; to create one.</em>
      </p>
    </div>
  );
};

export default ScenarioDashboardPage;
