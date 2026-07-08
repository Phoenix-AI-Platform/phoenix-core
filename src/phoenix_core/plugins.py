"""Plugin registration primitives for Phoenix Core.

This module can register SDK-compatible plugins and inspect their manifests and
command metadata. It intentionally does not execute plugin commands.
"""

from __future__ import annotations

from dataclasses import dataclass

from phoenix_sdk import PhoenixPlugin, PluginCommand, PluginManifest


@dataclass(frozen=True, slots=True)
class RegisteredPlugin:
    """Read-only view of a registered Phoenix plugin."""

    plugin: PhoenixPlugin

    @property
    def manifest(self) -> PluginManifest:
        """Return the plugin manifest."""

        return self.plugin.manifest

    @property
    def plugin_id(self) -> str:
        """Return the stable plugin id."""

        return self.manifest.plugin_id

    def list_commands(self) -> tuple[PluginCommand, ...]:
        """Return command metadata without executing commands."""

        return tuple(self.plugin.list_commands())


class PluginRegistry:
    """Read-only plugin registry for Phoenix Core bootstrap."""

    def __init__(self) -> None:
        self._plugins: dict[str, RegisteredPlugin] = {}

    def register(self, plugin: PhoenixPlugin) -> RegisteredPlugin:
        """Register a plugin by manifest id."""

        registered = RegisteredPlugin(plugin=plugin)
        plugin_id = registered.plugin_id
        if plugin_id in self._plugins:
            raise ValueError(f"Plugin already registered: {plugin_id}")
        self._plugins[plugin_id] = registered
        return registered

    def get(self, plugin_id: str) -> RegisteredPlugin:
        """Return a registered plugin by id."""

        return self._plugins[plugin_id]

    def list_plugins(self) -> tuple[RegisteredPlugin, ...]:
        """Return registered plugins in insertion order."""

        return tuple(self._plugins.values())

    def list_manifests(self) -> tuple[PluginManifest, ...]:
        """Return manifests for all registered plugins."""

        return tuple(plugin.manifest for plugin in self.list_plugins())
