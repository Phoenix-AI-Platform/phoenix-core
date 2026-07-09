from __future__ import annotations

from phoenix_core.cli import inspect_plugins, main


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
