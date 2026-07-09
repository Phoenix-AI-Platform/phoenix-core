"""Typed configuration models for Phoenix Core."""

from __future__ import annotations

from dataclasses import dataclass


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

    def plugin_factory_paths(self) -> tuple[str, ...]:
        """Return configured plugin factory paths."""

        return tuple(plugin.factory_path for plugin in self.plugins)
