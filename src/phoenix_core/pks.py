"""PKS-to-dashboard mapping seam for Phoenix Core.

This module maps explicit PKS-shaped records into dashboard project-state metadata.
It can read one explicit local JSON record, but it does not infer project state from
prose, call GitHub, or access other external systems.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
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


def read_dashboard_project_state_from_mapping(
    values: dict[str, Any],
) -> DashboardProjectState:
    """Read dashboard project-state metadata from an already-loaded PKS mapping."""

    return dashboard_project_state_from_pks_record(PKSProjectStateRecord.from_mapping(values))


def load_dashboard_project_state_from_json_file(path: Path) -> DashboardProjectState:
    """Load explicit dashboard project-state metadata from a UTF-8 JSON file."""

    try:
        values = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        raise ValueError("Unable to read PKS project state JSON file.") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("PKS project state file must contain valid JSON.") from exc

    if not isinstance(values, dict):
        raise ValueError("PKS project state file must contain a JSON object.")

    return read_dashboard_project_state_from_mapping(values)
