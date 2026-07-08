from __future__ import annotations

import pytest
from phoenix_sdk import CommandRequest, CommandResult, PhoenixPlugin, PluginCommand, PluginManifest, ResultStatus

from phoenix_core import PluginRegistry


class DemoCommand:
    name = "demo.inspect"
    description = "Inspect demo plugin metadata."

    def execute(self, request: CommandRequest) -> CommandResult:
        raise AssertionError("Core bootstrap must not execute plugin commands.")


class DemoPlugin:
    def __init__(self) -> None:
        self._command = DemoCommand()

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            plugin_id="demo.plugin",
            name="Demo Plugin",
            version="0.1.0",
            description="Test plugin",
            commands=(self._command.name,),
        )

    def list_commands(self) -> tuple[PluginCommand, ...]:
        return (self._command,)

    def get_command(self, name: str) -> PluginCommand:
        if name != self._command.name:
            raise KeyError(name)
        return self._command


def test_registry_registers_sdk_plugin() -> None:
    registry = PluginRegistry()
    plugin = DemoPlugin()

    registered = registry.register(plugin)

    assert isinstance(plugin, PhoenixPlugin)
    assert registered.plugin_id == "demo.plugin"
    assert registry.get("demo.plugin") is registered


def test_registry_lists_manifests_and_commands_without_execution() -> None:
    registry = PluginRegistry()
    registry.register(DemoPlugin())

    manifests = registry.list_manifests()
    commands = registry.get("demo.plugin").list_commands()

    assert manifests[0].plugin_id == "demo.plugin"
    assert manifests[0].commands == ("demo.inspect",)
    assert commands[0].name == "demo.inspect"


def test_registry_rejects_duplicate_plugin_ids() -> None:
    registry = PluginRegistry()
    registry.register(DemoPlugin())

    with pytest.raises(ValueError, match="Plugin already registered"):
        registry.register(DemoPlugin())


def test_core_does_not_require_command_execution() -> None:
    registry = PluginRegistry()
    registry.register(DemoPlugin())

    # If Core accidentally executes command metadata during listing, DemoCommand raises.
    commands = registry.get("demo.plugin").list_commands()

    assert commands[0].description == "Inspect demo plugin metadata."
    assert ResultStatus.SUCCESS.value == "success"
