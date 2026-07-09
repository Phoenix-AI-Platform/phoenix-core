from __future__ import annotations

from phoenix_core import (
    CORE_COMPONENT_NAME,
    CORE_COMPONENT_VERSION,
    CORE_STATUS_SCHEMA_VERSION,
    PluginRegistry,
    build_core_status,
    register_plugins_from_config,
)


def test_build_core_status_wraps_plugin_inventory() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    status = build_core_status(registry)

    assert status["schema_version"] == CORE_STATUS_SCHEMA_VERSION
    assert status["core"] == {
        "component": CORE_COMPONENT_NAME,
        "version": CORE_COMPONENT_VERSION,
    }
    assert status["plugin_inventory"]["schema_version"] == "phoenix.plugin_inventory.v1"
    assert status["plugin_inventory"]["plugins"][0]["plugin_id"] == "phoenix.office"


def test_core_status_includes_office_command_metadata_without_execution() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    status = build_core_status(registry)
    commands = status["plugin_inventory"]["plugins"][0]["commands"]

    assert commands == [
        {
            "name": "proposal.prepare_fields",
            "description": "Prepare deterministic proposal fields from validated proposal input.",
        },
        {
            "name": "proposal.generate_docx",
            "description": "Render a DOCX proposal from validated input and an explicit template.",
        },
    ]
