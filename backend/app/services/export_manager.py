"""
services/export_manager.py – Export orchestration service.

Delegates to specific exporters in the exporters/ package.
Manages export format selection and output file naming.
"""

from __future__ import annotations

from app.core.enums import ExportFormat
from app.services.results_store import SimulationResults


class ExportManager:
    """Orchestrates export of simulation results to various formats.

    Supported formats (see core/enums.py ExportFormat):
      CSV     : Tabular time-series data.
      JSON    : Structured scenario + results JSON.
      YAML    : Human-readable scenario specification.
      CIC_OEM : CIC Orbit Ephemeris Message format (future).
    """

    def export(
        self,
        results: SimulationResults,
        fmt: ExportFormat,
        output_path: str,
    ) -> str:
        """Export simulation results to the specified format.

        Args:
            results    : Completed simulation results.
            fmt        : Output format.
            output_path: Directory or file path for the output.

        Returns:
            Absolute path to the created export file.
        """
        # TODO: implement export dispatch
        # Pseudo-code:
        #   if fmt == ExportFormat.CSV:
        #       return CsvExporter().export(results, output_path)
        #   elif fmt == ExportFormat.JSON:
        #       return JsonExporter().export(results, output_path)
        #   elif fmt == ExportFormat.YAML:
        #       return YamlExporter().export(results, output_path)
        #   elif fmt == ExportFormat.CIC_OEM:
        #       return CicOemExporter().export(results, output_path)
        #   else:
        #       raise ValueError(f"Unsupported export format: {fmt}")
        raise NotImplementedError("ExportManager.export is not yet implemented.")
