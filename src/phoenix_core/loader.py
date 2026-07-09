"""Explicit plugin loading helpers for Phoenix Core.

The loader accepts explicit Python import paths and registers returned SDK-compatible
plugins. It does not discover packages automatically and does not execute plugin
commands.
"""

from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module

from phoenix_sdk import PhoenixPlugin

from phoenix_core.config import PhoenixCoreConfig
from phoenix_core.plugins import PluginRegistry


class PluginLoadError(RuntimeError):
    """Raised when a configured plugin cannot be loaded."""


def load_plugin_factory(factory_path: str) -> PhoenixPlugin:
    """Load a plugin factory from ``module:function`` and return its plugin."""

    if ":" not in factory_path:
        raise PluginLoadError(f"Invalid plugin factory path: {factory_path!r}")

    module_name, factory_name = factory_path.split(":", 1)
    if not module_name or not factory_name:
        raise PluginLoadError(f"Invalid plugin factory path: {factory_path!r}")

    try:
        module = import_module(module_name)
        factory = getattr(module, factory_name)
    except (ImportError, AttributeError) as exc:
        raise PluginLoadError(f"Unable to load plugin factory: {factory_path!r}") from exc

    plugin = factory()
    if not isinstance(plugin, PhoenixPlugin):
        raise PluginLoadError(f"Factory did not return a PhoenixPlugin: {factory_path!r}")
    return plugin


def register_plugins_from_config(
    registry: PluginRegistry,
    factory_paths: Iterable[str],
) -> tuple[str, ...]:
    """Register plugins from explicit factory paths and return registered ids."""

    registered_ids: list[str] = []
    for factory_path in factory_paths:
        plugin = load_plugin_factory(factory_path)
        registered = registry.register(plugin)
        registered_ids.append(registered.plugin_id)
    return tuple(registered_ids)


def register_plugins_from_core_config(
    registry: PluginRegistry,
    config: PhoenixCoreConfig,
) -> tuple[str, ...]:
    """Register plugins declared in typed Phoenix Core config."""

    return register_plugins_from_config(registry, config.plugin_factory_paths())
