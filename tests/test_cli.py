from __future__ import annotations

import json

from phoenix_core.cli import (
    PLUGIN_INVENTORY_SCHEMA_VERSION,
    inspect_plugins,
    main,
    print_dashboard,
    print_status,
)


def test_inspect_plugins_prints_configured_plugin_metadata(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = inspect_plugins(config_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "phoenix.office | Phoenix Office | 0.1.0" in captured.out
    assert "proposal.prepare_fields" in captured.out
    assert "proposal.generate_docx" in captured.out


def test_inspect_plugins_prints_json_inventory(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = inspect_plugins(config_path, output_format="json")

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == PLUGIN_INVENTORY_SCHEMA_VERSION
    assert payload["plugins"][0]["plugin_id"] == "phoenix.office"
    assert payload["plugins"][0]["commands"][0]["name"] == "proposal.prepare_fields"


def test_print_status_outputs_core_status_json(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = print_status(config_path)

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == "phoenix.core_status.v1"
    assert payload["core"]["component"] == "phoenix-core"
    assert payload["plugin_inventory"]["plugins"][0]["plugin_id"] == "phoenix.office"


def test_print_dashboard_outputs_dashboard_document_json(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = print_dashboard(config_path)

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == "phoenix.dashboard_document.v1"
    assert payload["core"]["component"] == "phoenix-core"
    assert payload["plugins"][0]["plugin_id"] == "phoenix.office"
    assert payload["repositories"] == []


def test_print_dashboard_outputs_static_repositories(tmp_path, capsys) -> None:
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

    exit_code = print_dashboard(config_path)

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["repositories"] == [
        {
            "name": "phoenix-core",
            "url": "https://github.com/Phoenix-AI-Platform/phoenix-core",
            "default_branch": "main",
            "ci_status": "unknown",
            "latest_commit": None,
        }
    ]


def test_main_inspect_plugins_command(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = main(["inspect-plugins", "--config", str(config_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "phoenix.office" in captured.out


def test_main_inspect_plugins_json_format(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = main(["inspect-plugins", "--config", str(config_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == "phoenix.plugin_inventory.v1"
    assert payload["plugins"][0]["name"] == "Phoenix Office"


def test_main_status_command_outputs_json(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = main(["status", "--config", str(config_path)])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == "phoenix.core_status.v1"
    assert payload["plugin_inventory"]["schema_version"] == "phoenix.plugin_inventory.v1"


def test_main_dashboard_command_outputs_json(tmp_path, capsys) -> None:
    config_path = tmp_path / "phoenix_core.toml"
    config_path.write_text(
        '[[plugins]]\nfactory_path = "phoenix_office.sdk_adapter:create_plugin"\n',
        encoding="utf-8",
    )

    exit_code = main(["dashboard", "--config", str(config_path)])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["schema_version"] == "phoenix.dashboard_document.v1"
    assert payload["plugins"][0]["commands"][0]["name"] == "proposal.prepare_fields"
