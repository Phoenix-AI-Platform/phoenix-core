"""Deterministic, non-executing command resolution for Phoenix Core.

Resolution returns immutable command metadata only. It never returns an executable
command object and never invokes ``PluginCommand.execute()``.
"""

from __future__ import annotations

from dataclasses import dataclass

from phoenix_core.plugins import PluginRegistry


class CommandResolutionError(LookupError):
    """Base error for deterministic command-resolution failures."""


class PluginNotFoundError(CommandResolutionError):
    """Raised when an explicitly requested plugin is not registered."""

    def __init__(self, plugin_id: str) -> None:
        self.plugin_id = plugin_id
        super().__init__(f"Plugin is not registered: {plugin_id}")


class CommandNotFoundError(CommandResolutionError):
    """Raised when a plugin does not provide the explicitly requested command."""

    def __init__(self, plugin_id: str, command_name: str) -> None:
        self.plugin_id = plugin_id
        self.command_name = command_name
        super().__init__(f"Command is not available from plugin {plugin_id}: {command_name}")


class CommandContractMismatchError(CommandResolutionError):
    """Raised when plugin manifest and command metadata disagree."""

    def __init__(self, plugin_id: str, command_name: str, reason: str) -> None:
        self.plugin_id = plugin_id
        self.command_name = command_name
        self.reason = reason
        super().__init__(
            f"Command contract mismatch for {plugin_id}:{command_name}: {reason}"
        )


@dataclass(frozen=True, slots=True)
class ResolvedCommand:
    """Immutable metadata identifying one resolved command without execution authority."""

    plugin_id: str
    plugin_version: str
    command_name: str
    description: str


def resolve_command(
    registry: PluginRegistry,
    plugin_id: str,
    command_name: str,
) -> ResolvedCommand:
    """Resolve exact plugin and command identifiers into immutable metadata."""

    try:
        registered = registry.get(plugin_id)
    except KeyError as exc:
        raise PluginNotFoundError(plugin_id) from exc

    try:
        command = registered.plugin.get_command(command_name)
    except LookupError as exc:
        raise CommandNotFoundError(plugin_id, command_name) from exc

    if command.name != command_name:
        raise CommandContractMismatchError(
            plugin_id,
            command_name,
            f"plugin returned command named {command.name!r}",
        )

    if command_name not in registered.manifest.commands:
        raise CommandContractMismatchError(
            plugin_id,
            command_name,
            "resolved command is not advertised by the plugin manifest",
        )

    return ResolvedCommand(
        plugin_id=registered.plugin_id,
        plugin_version=registered.manifest.version,
        command_name=command.name,
        description=command.description,
    )
