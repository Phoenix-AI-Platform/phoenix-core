"""Typed configuration models for Phoenix Core."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class PluginFactoryConfig:
    """Configuration for one explicitly approved plugin factory."""

    factory_path: str

    def __post_init__(self) -> None:
        if ":" not in self.factory_path:
            raise ValueError("Plugin factory path must use 'module:function' format.")


@dataclass(frozen=True, slots=True)
class RepositoryConfig:
    """Static repository declaration for dashboard display."""

    name: str
    url: str
    default_branch: str = "main"


@dataclass(frozen=True, slots=True)
class ProjectStateConfig:
    """Static project-state declaration for dashboard display."""

    phase: str
    milestone: str
    summary: str


@dataclass(frozen=True, slots=True)
class PhoenixCoreConfig:
    """Top-level Phoenix Core configuration."""

    plugins: tuple[PluginFactoryConfig, ...] = ()
    repositories: tuple[RepositoryConfig, ...] = ()
    project_state: ProjectStateConfig | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "plugins", tuple(self.plugins))
        object.__setattr__(self, "repositories", tuple(self.repositories))

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

        repositories = values.get("repositories", [])
        if not isinstance(repositories, list):
            raise ValueError("Core config 'repositories' must be a list.")

        repository_configs: list[RepositoryConfig] = []
        for repository in repositories:
            if not isinstance(repository, dict):
                raise ValueError("Each repository config must be a table.")
            name = repository.get("name")
            url = repository.get("url")
            default_branch = repository.get("default_branch", "main")
            if not isinstance(name, str):
                raise ValueError("Each repository config requires a string 'name'.")
            if not isinstance(url, str):
                raise ValueError("Each repository config requires a string 'url'.")
            if not isinstance(default_branch, str):
                raise ValueError("Each repository config requires a string 'default_branch'.")
            repository_configs.append(
                RepositoryConfig(
                    name=name,
                    url=url,
                    default_branch=default_branch,
                )
            )

        project_state = values.get("project_state")
        project_state_config = None
        if project_state is not None:
            if not isinstance(project_state, dict):
                raise ValueError("Core config 'project_state' must be a table.")
            phase = project_state.get("phase")
            milestone = project_state.get("milestone")
            summary = project_state.get("summary")
            if not isinstance(phase, str):
                raise ValueError("Project state requires a string 'phase'.")
            if not isinstance(milestone, str):
                raise ValueError("Project state requires a string 'milestone'.")
            if not isinstance(summary, str):
                raise ValueError("Project state requires a string 'summary'.")
            project_state_config = ProjectStateConfig(
                phase=phase,
                milestone=milestone,
                summary=summary,
            )

        return cls(
            plugins=tuple(plugin_configs),
            repositories=tuple(repository_configs),
            project_state=project_state_config,
        )

    @classmethod
    def from_toml_file(cls, path: str | Path) -> PhoenixCoreConfig:
        """Load Core config from a TOML file."""

        with Path(path).open("rb") as config_file:
            values = tomllib.load(config_file)
        return cls.from_mapping(values)

    def plugin_factory_paths(self) -> tuple[str, ...]:
        """Return configured plugin factory paths."""

        return tuple(plugin.factory_path for plugin in self.plugins)
