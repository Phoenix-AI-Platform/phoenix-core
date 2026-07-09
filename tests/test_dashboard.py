from __future__ import annotations

from phoenix_core import (
    DASHBOARD_DOCUMENT_SCHEMA_VERSION,
    DashboardDocument,
    PluginRegistry,
    build_core_status,
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
    }
