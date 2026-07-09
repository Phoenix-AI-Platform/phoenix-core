"""Command-line interface for Phoenix Core."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from phoenix_core.config import PhoenixCoreConfig
from phoenix_core.loader import register_plugins_from_core_config
from phoenix_core.plugins import PluginRegistry


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

    return parser


def inspect_plugins(config_path: Path) -> int:
    """Load configured plugins and print manifest/command metadata."""

    config = PhoenixCoreConfig.from_toml_file(config_path)
    registry = PluginRegistry()
    register_plugins_from_core_config(registry, config)

    for registered in registry.list_plugins():
        manifest = registered.manifest
        print(f"{manifest.plugin_id} | {manifest.name} | {manifest.version}")
        for command in registered.list_commands():
            print(f"  - {command.name}: {command.description}")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Phoenix Core CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "inspect-plugins":
        return inspect_plugins(args.config)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
