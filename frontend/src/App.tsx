/**
 * App.tsx – Root application component with routing.
 *
 * Page list:
 *   /              → Scenario dashboard
 *   /scenarios/new → Create new scenario
 *   /scenarios/:id → Scenario detail / simulation results
 *   /diagnostics   → Model diagnostics
 */

import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import ScenarioDashboardPage from './pages/ScenarioDashboardPage';
import ScenarioEditorPage from './pages/ScenarioEditorPage';
import SimulationResultsPage from './pages/SimulationResultsPage';
import DiagnosticsPage from './pages/DiagnosticsPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <nav style={{ padding: '0.5rem 1rem', borderBottom: '1px solid #ccc' }}>
        <strong>CIC Mission Manager</strong>
        {' | '}
        <NavLink to="/">Dashboard</NavLink>
        {' | '}
        <NavLink to="/scenarios/new">New Scenario</NavLink>
        {' | '}
        <NavLink to="/diagnostics">Diagnostics</NavLink>
      </nav>

      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<ScenarioDashboardPage />} />
          <Route path="/scenarios/new" element={<ScenarioEditorPage />} />
          <Route path="/scenarios/:id" element={<SimulationResultsPage />} />
          <Route path="/diagnostics" element={<DiagnosticsPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
};

export default App;
