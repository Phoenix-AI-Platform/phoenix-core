"""Typed configuration models for Phoenix Core."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any


@dataclass(frozen=True, slots=True)
class PluginFactoryConfig:
    """Configuration for one explicitly approved plugin factory."""

    factory_path: str

    def __post_init__(self) -> None:
        if ":" not in self.factory_path:
            raise ValueError("Plugin factory path must use 'module:function' format.")


@dataclass(frozen=True, slots=True)
class PhoenixCoreConfig:
    """Top-level Phoenix Core configuration."""

    plugins: tuple[PluginFactoryConfig, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "plugins", tuple(self.plugins))

    @classmethod
    def from_plugin_paths(cls, plugin_paths: tuple[str, ...]) -> PhoenixCoreConfig:
        """Create config from explicit plugin factory paths."""

        return cls(plugins=tuple(PluginFactoryConfig(path) for path in plugin_paths))

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> PhoenixCoreConfig:
        """Create config from a parsed mapping."""

        plugins = values.get("plugins", [])
        if not isinstance(plugins, list):
            raise ValueError("Core config 'plugins' must be a list.")

        plugin_configs: list[PluginFactoryConfig] = []
        for plugin in plugins:
            if not isinstance(plugin, dict):
                raise ValueError("Each plugin config must be a table.")
            factory_path = plugin.get("factory_path")
            if not isinstance(factory_path, str):
                raise ValueError("Each plugin config requires a string 'factory_path'.")
            plugin_configs.append(PluginFactoryConfig(factory_path))

        return cls(plugins=tuple(plugin_configs))

    @classmethod
    def from_toml_file(cls, path: str | Path) -> PhoenixCoreConfig:
        """Load Core config from a TOML file."""

        with Path(path).open("rb") as config_file:
            values = tomllib.load(config_file)
        return cls.from_mapping(values)

    def plugin_factory_paths(self) -> tuple[str, ...]:
        """Return configured plugin factory paths."""

        return tuple(plugin.factory_path for plugin in self.plugins)
