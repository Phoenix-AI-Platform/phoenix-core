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


def test_core_config_loads_repositories_from_toml_file(tmp_path) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        (
            '[[repositories]]\n'
            'name = "phoenix-core"\n'
            'url = "https://github.com/Phoenix-AI-Platform/phoenix-core"\n'
            'default_branch = "main"\n'
        ),
        encoding="utf-8",
    )

    config = PhoenixCoreConfig.from_toml_file(config_path)

    assert config.repositories[0].name == "phoenix-core"
    assert config.repositories[0].url == "https://github.com/Phoenix-AI-Platform/phoenix-core"
    assert config.repositories[0].default_branch == "main"


def test_core_config_loads_project_state_from_toml_file(tmp_path) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        (
            '[project_state]\n'
            'phase = "Dashboard Foundation"\n'
            'milestone = "Read-only project visibility"\n'
            'summary = "Expose safe dashboard data without live external calls."\n'
        ),
        encoding="utf-8",
    )

    config = PhoenixCoreConfig.from_toml_file(config_path)

    assert config.project_state is not None
    assert config.project_state.phase == "Dashboard Foundation"
    assert config.project_state.milestone == "Read-only project visibility"
    assert config.project_state.summary == "Expose safe dashboard data without live external calls."


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


def test_core_config_rejects_non_list_repositories() -> None:
    with pytest.raises(ValueError, match="repositories.*list"):
        PhoenixCoreConfig.from_mapping({"repositories": {}})


def test_core_config_rejects_repository_without_name() -> None:
    with pytest.raises(ValueError, match="name"):
        PhoenixCoreConfig.from_mapping({"repositories": [{"url": "https://example.com"}]})


def test_core_config_rejects_non_table_project_state() -> None:
    with pytest.raises(ValueError, match="project_state.*table"):
        PhoenixCoreConfig.from_mapping({"project_state": "bad"})


def test_core_config_rejects_project_state_without_phase() -> None:
    with pytest.raises(ValueError, match="phase"):
        PhoenixCoreConfig.from_mapping(
            {"project_state": {"milestone": "m", "summary": "s"}}
        )
