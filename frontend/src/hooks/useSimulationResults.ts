/**
 * hooks/useSimulationResults.ts – Hook for fetching simulation results.
 */

import { useEffect, useState } from 'react';
import { getResults } from '../api/client';
import type { SimulationResults } from '../models/states';

interface UseSimulationResultsReturn {
  results: SimulationResults | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * Fetch simulation results for the given scenario ID.
 *
 * @param scenarioId – The scenario UUID to fetch results for.
 */
export function useSimulationResults(
  scenarioId: string | undefined
): UseSimulationResultsReturn {
  const [results, setResults] = useState<SimulationResults | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!scenarioId) return;

    setIsLoading(true);
    setError(null);

    getResults(scenarioId)
      .then((data) => {
        setResults(data);
      })
      .catch(() => {
        setError('Failed to load simulation results.');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [scenarioId]);

  return { results, isLoading, error };
}
