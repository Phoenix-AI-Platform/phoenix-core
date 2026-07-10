from __future__ import annotations

from phoenix_core import (
    DASHBOARD_DOCUMENT_SCHEMA_VERSION,
    UNKNOWN_REPOSITORY_STATUS,
    DashboardDocument,
    DashboardProjectState,
    DashboardRepositoryStatus,
    PluginRegistry,
    build_core_status,
    build_dashboard_document,
    register_plugins_from_config,
)


def test_dashboard_document_builds_from_core_status() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    document = DashboardDocument.from_core_status(build_core_status(registry))

    assert document.schema_version == DASHBOARD_DOCUMENT_SCHEMA_VERSION
    assert document.core.component == "phoenix-core"
    assert document.core.version == "0.1.0"
    assert document.plugins[0].plugin_id == "phoenix.office"
    assert document.plugins[0].commands[0].name == "proposal.prepare_fields"
    assert document.repositories == ()
    assert document.project_state is None


def test_build_dashboard_document_composes_read_only_inputs() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    document = build_dashboard_document(
        core_status=build_core_status(registry),
        repositories=(
            DashboardRepositoryStatus(
                name="phoenix-core",
                url="https://github.com/Phoenix-AI-Platform/phoenix-core",
                default_branch="main",
                ci_status="success",
                latest_commit="abc123",
            ),
        ),
        project_state=DashboardProjectState(
            phase="Dashboard Foundation",
            milestone="Builder seam",
            summary="Compose dashboard document from explicit read-only inputs.",
        ),
    )

    assert document.plugins[0].plugin_id == "phoenix.office"
    assert document.repositories[0].ci_status == "success"
    assert document.repositories[0].latest_commit == "abc123"
    assert document.project_state is not None
    assert document.project_state.milestone == "Builder seam"


def test_dashboard_repository_status_defaults_to_unknown_ci() -> None:
    repository = DashboardRepositoryStatus(
        name="phoenix-core",
        url="https://github.com/Phoenix-AI-Platform/phoenix-core",
        default_branch="main",
    )

    assert repository.ci_status == UNKNOWN_REPOSITORY_STATUS
    assert repository.latest_commit is None


def test_dashboard_document_serializes_to_deterministic_dict() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    payload = DashboardDocument.from_core_status(build_core_status(registry)).to_dict()

    assert payload == {
        "schema_version": "phoenix.dashboard_document.v1",
        "core": {
            "component": "phoenix-core",
            "version": "0.1.0",
        },
        "plugins": [
            {
                "plugin_id": "phoenix.office",
                "name": "Phoenix Office",
                "version": "0.1.0",
                "description": "Contractor office automation plugin for Phoenix.",
                "commands": [
                    {
                        "name": "proposal.prepare_fields",
                        "description": (
                            "Prepare deterministic proposal fields from validated proposal input."
                        ),
                    },
                    {
                        "name": "proposal.generate_docx",
                        "description": (
                            "Render a DOCX proposal from validated input and an explicit template."
                        ),
                    },
                ],
            }
        ],
        "repositories": [],
        "project_state": None,
    }


def test_dashboard_document_serializes_repository_placeholders() -> None:
    document = DashboardDocument(
        schema_version=DASHBOARD_DOCUMENT_SCHEMA_VERSION,
        core=DashboardDocument.from_core_status(
            {
                "core": {"component": "phoenix-core", "version": "0.1.0"},
                "plugin_inventory": {"plugins": []},
            }
        ).core,
        plugins=(),
        repositories=(
            DashboardRepositoryStatus(
                name="phoenix-core",
                url="https://github.com/Phoenix-AI-Platform/phoenix-core",
                default_branch="main",
            ),
        ),
    )

    assert document.to_dict()["repositories"] == [
        {
            "name": "phoenix-core",
            "url": "https://github.com/Phoenix-AI-Platform/phoenix-core",
            "default_branch": "main",
            "ci_status": "unknown",
            "latest_commit": None,
        }
    ]


def test_dashboard_document_serializes_project_state() -> None:
    document = DashboardDocument(
        schema_version=DASHBOARD_DOCUMENT_SCHEMA_VERSION,
        core=DashboardDocument.from_core_status(
            {
                "core": {"component": "phoenix-core", "version": "0.1.0"},
                "plugin_inventory": {"plugins": []},
            }
        ).core,
        plugins=(),
        project_state=DashboardProjectState(
            phase="Dashboard Foundation",
            milestone="Read-only project visibility",
            summary="Expose safe dashboard data without live external calls.",
        ),
    )

    assert document.to_dict()["project_state"] == {
        "phase": "Dashboard Foundation",
        "milestone": "Read-only project visibility",
        "summary": "Expose safe dashboard data without live external calls.",
    }
