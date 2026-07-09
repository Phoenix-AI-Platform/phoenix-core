"""PKS-to-dashboard mapping seam for Phoenix Core.

This module maps explicit PKS-shaped records into dashboard project-state metadata.
It does not read files, call GitHub, or infer project state from external systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from phoenix_core.dashboard import DashboardProjectState


@dataclass(frozen=True, slots=True)
class PKSProjectStateRecord:
    """Explicit project-state record supplied by PKS integration code."""

    phase: str
    milestone: str
    summary: str

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> PKSProjectStateRecord:
        """Create a PKS project-state record from an explicit mapping."""

        phase = values.get("phase")
        milestone = values.get("milestone")
        summary = values.get("summary")
        if not isinstance(phase, str):
            raise ValueError("PKS project state requires a string 'phase'.")
        if not isinstance(milestone, str):
            raise ValueError("PKS project state requires a string 'milestone'.")
        if not isinstance(summary, str):
            raise ValueError("PKS project state requires a string 'summary'.")
        return cls(phase=phase, milestone=milestone, summary=summary)


def dashboard_project_state_from_pks_record(
    record: PKSProjectStateRecord,
) -> DashboardProjectState:
    """Convert an explicit PKS record into dashboard project-state metadata."""

    return DashboardProjectState(
        phase=record.phase,
        milestone=record.milestone,
        summary=record.summary,
    )
