from __future__ import annotations

from dataclasses import FrozenInstanceError, fields

import pytest
from phoenix_sdk import CommandRequest, CommandResult, PluginCommand, PluginManifest

from phoenix_core import (
    CommandContractMismatchError,
    CommandNotFoundError,
    PluginNotFoundError,
    PluginRegistry,
    ResolvedCommand,
    resolve_command,
)


class DemoCommand:
    name = "demo.inspect"
    description = "Inspect demo command metadata."

    def execute(self, request: CommandRequest) -> CommandResult:
        raise AssertionError("Command resolution must never execute the command.")


class DemoPlugin:
    def __init__(
        self,
        *,
        command: PluginCommand | None = None,
        advertised_commands: tuple[str, ...] | None = None,
    ) -> None:
        self._command = command or DemoCommand()
        self._advertised_commands = (
            advertised_commands
            if advertised_commands is not None
            else ("demo.inspect",)
        )

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            plugin_id="demo.plugin",
            name="Demo Plugin",
            version="1.2.3",
            description="Command-resolution test plugin.",
            commands=self._advertised_commands,
        )

    def list_commands(self) -> tuple[PluginCommand, ...]:
        return (self._command,)

    def get_command(self, name: str) -> PluginCommand:
        if name != "demo.inspect":
            raise KeyError(name)
        return self._command


class MisnamedCommand(DemoCommand):
    name = "demo.other"


def _registry_with(plugin: DemoPlugin | None = None) -> PluginRegistry:
    registry = PluginRegistry()
    registry.register(plugin or DemoPlugin())
    return registry


def test_resolve_command_returns_immutable_metadata_without_execution_authority() -> None:
    resolved = resolve_command(_registry_with(), "demo.plugin", "demo.inspect")

    assert resolved == ResolvedCommand(
        plugin_id="demo.plugin",
        plugin_version="1.2.3",
        command_name="demo.inspect",
        description="Inspect demo command metadata.",
    )
    assert tuple(field.name for field in fields(resolved)) == (
        "plugin_id",
        "plugin_version",
        "command_name",
        "description",
    )
    assert not hasattr(resolved, "command")
    assert not hasattr(resolved, "execute")

    with pytest.raises(FrozenInstanceError):
        resolved.description = "changed"


def test_resolve_command_rejects_unknown_plugin() -> None:
    with pytest.raises(PluginNotFoundError) as exc_info:
        resolve_command(PluginRegistry(), "missing.plugin", "demo.inspect")

    assert exc_info.value.plugin_id == "missing.plugin"


def test_resolve_command_rejects_unknown_command() -> None:
    with pytest.raises(CommandNotFoundError) as exc_info:
        resolve_command(_registry_with(), "demo.plugin", "demo.missing")

    assert exc_info.value.plugin_id == "demo.plugin"
    assert exc_info.value.command_name == "demo.missing"


def test_resolve_command_rejects_returned_command_name_mismatch() -> None:
    registry = _registry_with(DemoPlugin(command=MisnamedCommand()))

    with pytest.raises(CommandContractMismatchError, match="returned command named"):
        resolve_command(registry, "demo.plugin", "demo.inspect")


def test_resolve_command_rejects_command_missing_from_manifest() -> None:
    registry = _registry_with(DemoPlugin(advertised_commands=()))

    with pytest.raises(CommandContractMismatchError, match="not advertised"):
        resolve_command(registry, "demo.plugin", "demo.inspect")


def test_command_resolution_is_exact_and_case_sensitive() -> None:
    with pytest.raises(CommandNotFoundError):
        resolve_command(_registry_with(), "demo.plugin", "Demo.Inspect")
