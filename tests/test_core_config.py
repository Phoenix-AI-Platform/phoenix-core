from __future__ import annotations

import pytest

from phoenix_core import (
    PhoenixCoreConfig,
    PluginFactoryConfig,
    PluginRegistry,
    register_plugins_from_core_config,
)


def test_core_config_builds_from_plugin_paths() -> None:
    config = PhoenixCoreConfig.from_plugin_paths(("phoenix_office.sdk_adapter:create_plugin",))

    assert config.plugin_factory_paths() == ("phoenix_office.sdk_adapter:create_plugin",)


def test_plugin_factory_config_rejects_invalid_path() -> None:
    with pytest.raises(ValueError, match="module:function"):
        PluginFactoryConfig("phoenix_office.sdk_adapter.create_plugin")


def test_core_config_registers_phoenix_office_plugin() -> None:
    registry = PluginRegistry()
    config = PhoenixCoreConfig.from_plugin_paths(("phoenix_office.sdk_adapter:create_plugin",))

    registered_ids = register_plugins_from_core_config(registry, config)

    assert registered_ids == ("phoenix.office",)
    assert registry.get("phoenix.office").manifest.commands == (
        "proposal.prepare_fields",
        "proposal.generate_docx",
    )


def test_core_config_is_immutable() -> None:
    config = PhoenixCoreConfig.from_plugin_paths(("phoenix_office.sdk_adapter:create_plugin",))

    with pytest.raises(AttributeError):
        config.plugins = ()  # type: ignore[misc]
