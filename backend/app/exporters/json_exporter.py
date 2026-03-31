"""
exporters/json_exporter.py – JSON scenario and results export.

Exports the scenario specification and simulation results to structured JSON.
All arrays are serialised with explicit unit and frame metadata to avoid
ambiguity.  NumPy arrays are never serialised raw.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.services.results_store import SimulationResults


class JsonExporter:
    """Exports scenario and simulation results to JSON format."""

    def export(self, results: SimulationResults, output_path: str) -> str:
        """Write results to a JSON file.

        Args:
            results    : Completed simulation results.
            output_path: Path to output directory or .json file.

        Returns:
            Absolute path to the created JSON file.
        """
        # TODO: implement JSON export with schema metadata
        # Pseudo-code:
        #   path = Path(output_path)
        #   if path.is_dir():
        #       path = path / f"results_{results.scenario_id}.json"
        #
        #   data = {
        #       "schema_version": "1.0",
        #       "scenario_id": results.scenario_id,
        #       "step_count": results.step_count,
        #       "snapshots": [snapshot_to_dict(s) for s in results.snapshots],
        #   }
        #   with open(path, 'w') as f:
        #       json.dump(data, f, indent=2, default=numpy_to_list)
        #
        #   return str(path.resolve())
        raise NotImplementedError("JsonExporter.export is not yet implemented.")
