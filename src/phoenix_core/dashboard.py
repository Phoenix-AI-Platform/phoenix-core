"""Read-only dashboard data models for Phoenix Core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DASHBOARD_DOCUMENT_SCHEMA_VERSION = "phoenix.dashboard_document.v1"


@dataclass(frozen=True, slots=True)
class DashboardPluginCommand:
    """Dashboard view of one plugin command."""

    name: str
    description: str


@dataclass(frozen=True, slots=True)
class DashboardPlugin:
    """Dashboard view of one registered plugin."""

    plugin_id: str
    name: str
    version: str
    description: str
    commands: tuple[DashboardPluginCommand, ...]


@dataclass(frozen=True, slots=True)
class DashboardCoreSummary:
    """Dashboard view of Phoenix Core metadata."""

    component: str
    version: str


@dataclass(frozen=True, slots=True)
class DashboardDocument:
    """Read-only dashboard document derived from Core status."""

    schema_version: str
    core: DashboardCoreSummary
    plugins: tuple[DashboardPlugin, ...]

    @classmethod
    def from_core_status(cls, status: dict[str, Any]) -> DashboardDocument:
        """Create a dashboard document from a Core status payload."""

        core = status["core"]
        plugin_inventory = status["plugin_inventory"]
        plugins = tuple(
            DashboardPlugin(
                plugin_id=plugin["plugin_id"],
                name=plugin["name"],
                version=plugin["version"],
                description=plugin["description"],
                commands=tuple(
                    DashboardPluginCommand(
                        name=command["name"],
                        description=command["description"],
                    )
                    for command in plugin["commands"]
                ),
            )
            for plugin in plugin_inventory["plugins"]
        )
        return cls(
            schema_version=DASHBOARD_DOCUMENT_SCHEMA_VERSION,
            core=DashboardCoreSummary(
                component=core["component"],
                version=core["version"],
            ),
            plugins=plugins,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-serializable dashboard document."""

        return {
            "schema_version": self.schema_version,
            "core": {
                "component": self.core.component,
                "version": self.core.version,
            },
            "plugins": [
                {
                    "plugin_id": plugin.plugin_id,
                    "name": plugin.name,
                    "version": plugin.version,
                    "description": plugin.description,
                    "commands": [
                        {
                            "name": command.name,
                            "description": command.description,
                        }
                        for command in plugin.commands
                    ],
                }
                for plugin in self.plugins
            ],
        }
