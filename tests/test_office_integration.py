from __future__ import annotations

import pytest
from phoenix_office.sdk_adapter import create_plugin
from phoenix_sdk import CommandRequest, PhoenixPlugin

from phoenix_core import PluginRegistry, ResolvedCommand, resolve_command


def test_core_registers_phoenix_office_plugin_metadata() -> None:
    registry = PluginRegistry()
    office_plugin = create_plugin()

    registered = registry.register(office_plugin)

    assert isinstance(office_plugin, PhoenixPlugin)
    assert registered.plugin_id == "phoenix.office"
    assert registered.manifest.name == "Phoenix Office"
    assert registered.manifest.metadata["execution"] == "metadata_only"


def test_core_lists_phoenix_office_commands_without_execution() -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    commands = registry.get("phoenix.office").list_commands()
    command_names = tuple(command.name for command in commands)

    assert command_names == (
        "proposal.prepare_fields",
        "proposal.generate_docx",
    )


@pytest.mark.parametrize(
    ("command_name", "description"),
    (
        (
            "proposal.prepare_fields",
            "Prepare deterministic proposal fields from validated proposal input.",
        ),
        (
            "proposal.generate_docx",
            "Render a DOCX proposal from validated input and an explicit template.",
        ),
    ),
)
def test_core_resolves_phoenix_office_command_metadata_without_execution(
    command_name: str,
    description: str,
) -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    resolved = resolve_command(registry, "phoenix.office", command_name)

    assert resolved == ResolvedCommand(
        plugin_id="phoenix.office",
        plugin_version="0.1.0",
        command_name=command_name,
        description=description,
    )
    assert not hasattr(resolved, "command")
    assert not hasattr(resolved, "execute")


def test_core_does_not_execute_phoenix_office_commands() -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    command = registry.get("phoenix.office").list_commands()[0]

    with pytest.raises(NotImplementedError):
        command.execute(CommandRequest(command=command.name))
