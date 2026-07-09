"""Read-only Phoenix Core status payloads."""

from __future__ import annotations

from typing import Any

from phoenix_core.cli import build_plugin_inventory
from phoenix_core.plugins import PluginRegistry

CORE_STATUS_SCHEMA_VERSION = "phoenix.core_status.v1"
CORE_COMPONENT_NAME = "phoenix-core"
CORE_COMPONENT_VERSION = "0.1.0"


def build_core_status(registry: PluginRegistry) -> dict[str, Any]:
    """Build a deterministic read-only Core status payload."""

    return {
        "schema_version": CORE_STATUS_SCHEMA_VERSION,
        "core": {
            "component": CORE_COMPONENT_NAME,
            "version": CORE_COMPONENT_VERSION,
        },
        "plugin_inventory": build_plugin_inventory(registry),
    }
