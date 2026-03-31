"""
services/scenario_compiler.py – Scenario validation and compilation.

Validates a scenario specification before simulation, resolves cross-references,
and builds the runtime objects needed by the SimulationEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.scenario import Scenario


@dataclass
class CompilationResult:
    """Result of scenario compilation.

    Attributes:
        is_valid     : True if scenario is valid and ready for simulation.
        errors       : List of fatal error messages.
        warnings     : List of non-fatal warning messages.
    """

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ScenarioCompiler:
    """Validates and compiles a scenario before simulation.

    Checks:
      - At least one phase exists.
      - All phase durations are positive.
      - Initial states are physically valid (orbit above surface, etc.).
      - Vehicle masses are positive.
      - Constraint sets are internally consistent.
    """

    def compile(self, scenario: Scenario) -> CompilationResult:
        """Validate and compile a scenario.

        Args:
            scenario: The scenario to validate.

        Returns:
            CompilationResult with validation outcome.
        """
        # TODO: implement scenario validation
        # Pseudo-code:
        #   errors, warnings = [], []
        #
        #   if not scenario.phases:
        #       errors.append("Scenario must have at least one phase.")
        #
        #   for phase in scenario.phases:
        #       if phase.duration_s <= 0:
        #           errors.append(f"Phase '{phase.name}' has non-positive duration.")
        #
        #   chief_r = scenario.chief.initial_abs_state.radius_m
        #   if chief_r < R_EARTH_M + 100_000:
        #       warnings.append("Chief initial orbit is below 100 km altitude.")
        #
        #   return CompilationResult(is_valid=not errors, errors=errors, warnings=warnings)
        raise NotImplementedError("ScenarioCompiler.compile is not yet implemented.")
