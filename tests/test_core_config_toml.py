from __future__ import annotations

import pytest

from phoenix_core import PhoenixCoreConfig, PluginRegistry, register_plugins_from_core_config


def test_core_config_loads_from_toml_file(tmp_path) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    config = PhoenixCoreConfig.from_toml_file(config_path)

    assert config.plugin_factory_paths() == ("phoenix_office.sdk_adapter:create_plugin",)


def test_core_config_from_toml_registers_office_plugin(tmp_path) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )
    registry = PluginRegistry()

    registered_ids = register_plugins_from_core_config(
        registry,
        PhoenixCoreConfig.from_toml_file(config_path),
    )

    assert registered_ids == ("phoenix.office",)


def test_core_config_rejects_non_list_plugins() -> None:
    with pytest.raises(ValueError, match="plugins.*list"):
        PhoenixCoreConfig.from_mapping({"plugins": {}})


def test_core_config_rejects_plugin_without_factory_path() -> None:
    with pytest.raises(ValueError, match="factory_path"):
        PhoenixCoreConfig.from_mapping({"plugins": [{}]})


def test_core_config_rejects_non_table_plugin_entry() -> None:
    with pytest.raises(ValueError, match="table"):
        PhoenixCoreConfig.from_mapping({"plugins": ["bad"]})
