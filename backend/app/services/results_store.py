"""
services/results_store.py – Simulation results storage.

Accumulates snapshots, measurements, and outputs during a simulation run.
Provides access methods for export and API responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.domain.states import RelativeMotionSnapshot


@dataclass
class SimulationResults:
    """Container for all simulation outputs.

    Attributes:
        scenario_id : Identifier of the parent scenario.
        snapshots   : Ordered list of RelativeMotionSnapshots (one per step).
        is_complete : True after finalise() is called.
        metadata    : Key-value metadata (e.g. total duration, step count).
    """

    scenario_id: str
    snapshots: list[RelativeMotionSnapshot] = field(default_factory=list)
    is_complete: bool = False
    metadata: dict[str, object] = field(default_factory=dict)

    def append_snapshot(self, snapshot: RelativeMotionSnapshot) -> None:
        """Append a new snapshot to the results."""
        self.snapshots.append(snapshot)

    def finalise(self) -> None:
        """Mark the results as complete and compute summary metadata."""
        self.is_complete = True
        self.metadata["step_count"] = len(self.snapshots)
        if self.snapshots:
            self.metadata["start_epoch_s"] = self.snapshots[0].epoch_s
            self.metadata["end_epoch_s"] = self.snapshots[-1].epoch_s

    @property
    def step_count(self) -> int:
        """Number of stored snapshots."""
        return len(self.snapshots)

    @property
    def epochs_s(self) -> list[float]:
        """List of epoch values for all stored snapshots."""
        return [s.epoch_s for s in self.snapshots]
