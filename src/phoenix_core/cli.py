"""Command-line interface for Phoenix Core."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from phoenix_core.config import PhoenixCoreConfig
from phoenix_core.loader import register_plugins_from_core_config
from phoenix_core.plugins import PluginRegistry
from phoenix_core.repositories import collect_repository_statuses

PLUGIN_INVENTORY_SCHEMA_VERSION = "phoenix.plugin_inventory.v1"


def build_parser() -> argparse.ArgumentParser:
    """Build the Phoenix Core CLI parser."""

    parser = argparse.ArgumentParser(prog="phoenix-core")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect-plugins",
        help="Load approved plugins from config and print manifest metadata.",
    )
    inspect_parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to Phoenix Core TOML config.",
    )
    inspect_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for plugin inventory.",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Load approved plugins from config and print Core status JSON.",
    )
    status_parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to Phoenix Core TOML config.",
    )

    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Load approved plugins from config and print dashboard document JSON.",
    )
    dashboard_parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to Phoenix Core TOML config.",
    )

    return parser


def build_plugin_inventory(registry: PluginRegistry) -> dict[str, Any]:
    """Build a deterministic plugin inventory payload."""

    plugins: list[dict[str, Any]] = []
    for registered in registry.list_plugins():
        manifest = registered.manifest
        plugins.append(
            {
                "plugin_id": manifest.plugin_id,
                "name": manifest.name,
                "version": manifest.version,
                "description": manifest.description,
                "commands": [
                    {
                        "name": command.name,
                        "description": command.description,
                    }
                    for command in registered.list_commands()
                ],
            }
        )
    return {
        "schema_version": PLUGIN_INVENTORY_SCHEMA_VERSION,
        "plugins": plugins,
    }


def load_core_config(config_path: Path) -> PhoenixCoreConfig:
    """Load Phoenix Core config from TOML."""

    return PhoenixCoreConfig.from_toml_file(config_path)


def load_registry(config_path: Path) -> PluginRegistry:
    """Load configured plugins into a registry."""

    config = load_core_config(config_path)
    registry = PluginRegistry()
    register_plugins_from_core_config(registry, config)
    return registry


def print_text_inventory(registry: PluginRegistry) -> None:
    """Print plugin inventory in human-readable text."""

    for registered in registry.list_plugins():
        manifest = registered.manifest
        print(f"{manifest.plugin_id} | {manifest.name} | {manifest.version}")
        for command in registered.list_commands():
            print(f"  - {command.name}: {command.description}")


def inspect_plugins(config_path: Path, output_format: str = "text") -> int:
    """Load configured plugins and print manifest/command metadata."""

    registry = load_registry(config_path)

    if output_format == "json":
        print(json.dumps(build_plugin_inventory(registry), sort_keys=True))
        return 0

    print_text_inventory(registry)
    return 0


def print_status(config_path: Path) -> int:
    """Load configured plugins and print read-only Core status JSON."""

    from phoenix_core.status import build_core_status

    registry = load_registry(config_path)
    print(json.dumps(build_core_status(registry), sort_keys=True))
    return 0


def print_dashboard(config_path: Path) -> int:
    """Load configured plugins and print read-only dashboard document JSON."""

    from phoenix_core.dashboard import DashboardDocument
    from phoenix_core.status import build_core_status

    config = load_core_config(config_path)
    registry = PluginRegistry()
    register_plugins_from_core_config(registry, config)
    document = DashboardDocument.from_core_status(build_core_status(registry))
    document = DashboardDocument(
        schema_version=document.schema_version,
        core=document.core,
        plugins=document.plugins,
        repositories=collect_repository_statuses(config.repositories),
    )
    print(json.dumps(document.to_dict(), sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Phoenix Core CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "inspect-plugins":
        return inspect_plugins(args.config, args.format)
    if args.command == "status":
        return print_status(args.config)
    if args.command == "dashboard":
        return print_dashboard(args.config)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
