from __future__ import annotations

import pytest

from phoenix_core import (
    PluginLoadError,
    PluginRegistry,
    load_plugin_factory,
    register_plugins_from_config,
)


def test_load_plugin_factory_loads_phoenix_office_adapter() -> None:
    plugin = load_plugin_factory("phoenix_office.sdk_adapter:create_plugin")

    assert plugin.manifest.plugin_id == "phoenix.office"
    assert plugin.manifest.commands == (
        "proposal.prepare_fields",
        "proposal.generate_docx",
    )


def test_register_plugins_from_config_registers_office_plugin() -> None:
    registry = PluginRegistry()

    registered_ids = register_plugins_from_config(
        registry,
        ["phoenix_office.sdk_adapter:create_plugin"],
    )

    assert registered_ids == ("phoenix.office",)
    assert registry.get("phoenix.office").manifest.name == "Phoenix Office"


def test_loader_rejects_invalid_factory_path() -> None:
    with pytest.raises(PluginLoadError, match="Invalid plugin factory path"):
        load_plugin_factory("phoenix_office.sdk_adapter.create_plugin")


def test_loader_rejects_missing_factory() -> None:
    with pytest.raises(PluginLoadError, match="Unable to load plugin factory"):
        load_plugin_factory("phoenix_office.sdk_adapter:missing_factory")


def test_loader_does_not_execute_plugin_commands() -> None:
    registry = PluginRegistry()
    register_plugins_from_config(registry, ["phoenix_office.sdk_adapter:create_plugin"])

    commands = registry.get("phoenix.office").list_commands()

    assert commands[0].name == "proposal.prepare_fields"
