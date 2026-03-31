"""
api/v1/scenarios.py – Scenario and simulation API routes.

Routes:
  POST   /api/v1/scenarios/validate    – Validate a scenario specification.
  POST   /api/v1/scenarios/simulate    – Create and simulate a scenario.
  GET    /api/v1/scenarios/{id}/results – Retrieve simulation results.
  POST   /api/v1/scenarios/{id}/export  – Export simulation results.

Rules:
  - Routes must be thin; no physics or simulation logic here.
  - All physics calls are delegated to the services layer.
  - All request/response bodies are typed Pydantic schemas.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.scenario_schemas import (
    ScenarioCreateSchema,
    ScenarioResponseSchema,
)
from app.schemas.simulation_schemas import (
    ExportRequest,
    SimulateRequest,
    SimulationResultsSchema,
)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post(
    "/validate",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Validate a scenario specification.",
)
def validate_scenario(body: ScenarioCreateSchema) -> dict:
    """Validate the scenario without running a simulation.

    Returns a dict with fields:
      is_valid : bool
      errors   : list[str]
      warnings : list[str]
    """
    # TODO: delegate to ScenarioCompiler.compile()
    # Pseudo-code:
    #   scenario = schema_to_domain(body)
    #   result = ScenarioCompiler().compile(scenario)
    #   return result.model_dump()
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Scenario validation is not yet implemented.",
    )


@router.post(
    "/simulate",
    response_model=ScenarioResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create and simulate a scenario.",
)
def simulate_scenario(body: ScenarioCreateSchema) -> ScenarioResponseSchema:
    """Accept a scenario, validate it, run the simulation, and return a summary.

    For long simulations this should be made async; V1 runs synchronously.
    """
    # TODO: delegate to ScenarioCompiler + SimulationEngine
    # Pseudo-code:
    #   scenario = schema_to_domain(body)
    #   compile_result = ScenarioCompiler().compile(scenario)
    #   if not compile_result.is_valid:
    #       raise HTTPException(422, detail=compile_result.errors)
    #
    #   engine = SimulationEngine(scenario)
    #   results = engine.run()
    #   _results_store[scenario.scenario_id] = results
    #
    #   return ScenarioResponseSchema(
    #       scenario_id=scenario.scenario_id,
    #       name=scenario.name,
    #       ...
    #   )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Scenario simulation is not yet implemented.",
    )


@router.get(
    "/{scenario_id}/results",
    response_model=SimulationResultsSchema,
    summary="Retrieve simulation results.",
)
def get_results(scenario_id: str) -> SimulationResultsSchema:
    """Return the simulation results for a completed scenario."""
    # TODO: look up results in results store
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Result retrieval is not yet implemented.",
    )


@router.post(
    "/{scenario_id}/export",
    response_model=dict,
    summary="Export simulation results.",
)
def export_results(scenario_id: str, body: ExportRequest) -> dict:
    """Export simulation results in the requested format."""
    # TODO: delegate to ExportManager
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Export is not yet implemented.",
    )
