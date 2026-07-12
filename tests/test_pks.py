from __future__ import annotations

import json

import pytest

from phoenix_core import (
    PKSProjectStateRecord,
    dashboard_project_state_from_pks_record,
    load_dashboard_project_state_from_json_file,
    read_dashboard_project_state_from_mapping,
)


def test_pks_project_state_record_builds_from_mapping() -> None:
    record = PKSProjectStateRecord.from_mapping(
        {
            "phase": "Dashboard Foundation",
            "milestone": "PKS seam",
            "summary": "Map explicit PKS records into dashboard project state.",
        }
    )

    assert record.phase == "Dashboard Foundation"
    assert record.milestone == "PKS seam"
    assert record.summary == "Map explicit PKS records into dashboard project state."


def test_pks_project_state_record_rejects_missing_phase() -> None:
    with pytest.raises(ValueError, match="phase"):
        PKSProjectStateRecord.from_mapping(
            {
                "milestone": "PKS seam",
                "summary": "Map explicit PKS records into dashboard project state.",
            }
        )


def test_dashboard_project_state_from_pks_record_maps_fields() -> None:
    dashboard_state = dashboard_project_state_from_pks_record(
        PKSProjectStateRecord(
            phase="Dashboard Foundation",
            milestone="PKS seam",
            summary="Map explicit PKS records into dashboard project state.",
        )
    )

    assert dashboard_state.phase == "Dashboard Foundation"
    assert dashboard_state.milestone == "PKS seam"
    assert dashboard_state.summary == "Map explicit PKS records into dashboard project state."


def test_read_dashboard_project_state_from_mapping_maps_loaded_record() -> None:
    dashboard_state = read_dashboard_project_state_from_mapping(
        {
            "phase": "Dashboard Foundation",
            "milestone": "PKS reader seam",
            "summary": "Read already-loaded PKS mappings without file I/O.",
        }
    )

    assert dashboard_state.phase == "Dashboard Foundation"
    assert dashboard_state.milestone == "PKS reader seam"
    assert dashboard_state.summary == "Read already-loaded PKS mappings without file I/O."


def test_load_dashboard_project_state_from_json_file(tmp_path) -> None:
    state_path = tmp_path / "project-state.json"
    state_path.write_text(
        json.dumps(
            {
                "phase": "Dashboard Foundation",
                "milestone": "PKS JSON loader",
                "summary": "Load explicit project state without prose inference.",
            }
        ),
        encoding="utf-8",
    )

    dashboard_state = load_dashboard_project_state_from_json_file(state_path)

    assert dashboard_state.phase == "Dashboard Foundation"
    assert dashboard_state.milestone == "PKS JSON loader"
    assert dashboard_state.summary == "Load explicit project state without prose inference."


def test_load_dashboard_project_state_rejects_invalid_json(tmp_path) -> None:
    state_path = tmp_path / "project-state.json"
    state_path.write_text("{not-json}", encoding="utf-8")

    with pytest.raises(ValueError, match="valid JSON"):
        load_dashboard_project_state_from_json_file(state_path)


def test_load_dashboard_project_state_rejects_non_object_json(tmp_path) -> None:
    state_path = tmp_path / "project-state.json"
    state_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        load_dashboard_project_state_from_json_file(state_path)
