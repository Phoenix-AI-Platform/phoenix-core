"""Phoenix Core public API."""

from phoenix_core.command_resolution import (
    CommandContractMismatchError,
    CommandNotFoundError,
    CommandResolutionError,
    PluginNotFoundError,
    ResolvedCommand,
    resolve_command,
)
from phoenix_core.config import (
    PhoenixCoreConfig,
    PluginFactoryConfig,
    ProjectStateConfig,
    RepositoryConfig,
)
from phoenix_core.dashboard import (
    DASHBOARD_DOCUMENT_SCHEMA_VERSION,
    UNKNOWN_REPOSITORY_STATUS,
    DashboardCoreSummary,
    DashboardDocument,
    DashboardPlugin,
    DashboardPluginCommand,
    DashboardProjectState,
    DashboardRepositoryStatus,
    build_dashboard_document,
)
from phoenix_core.loader import (
    PluginLoadError,
    load_plugin_factory,
    register_plugins_from_config,
    register_plugins_from_core_config,
)
from phoenix_core.pks import (
    PKSProjectStateRecord,
    dashboard_project_state_from_pks_record,
    load_dashboard_project_state_from_json_file,
    read_dashboard_project_state_from_mapping,
)
from phoenix_core.plugins import PluginRegistry, RegisteredPlugin
from phoenix_core.repositories import RepositoryStatusOverride, collect_repository_statuses
from phoenix_core.status import (
    CORE_COMPONENT_NAME,
    CORE_COMPONENT_VERSION,
    CORE_STATUS_SCHEMA_VERSION,
    build_core_status,
)

__all__ = [
    "CORE_COMPONENT_NAME",
    "CORE_COMPONENT_VERSION",
    "CORE_STATUS_SCHEMA_VERSION",
    "DASHBOARD_DOCUMENT_SCHEMA_VERSION",
    "UNKNOWN_REPOSITORY_STATUS",
    "CommandContractMismatchError",
    "CommandNotFoundError",
    "CommandResolutionError",
    "DashboardCoreSummary",
    "DashboardDocument",
    "DashboardPlugin",
    "DashboardPluginCommand",
    "DashboardProjectState",
    "DashboardRepositoryStatus",
    "PKSProjectStateRecord",
    "PhoenixCoreConfig",
    "PluginFactoryConfig",
    "PluginLoadError",
    "PluginNotFoundError",
    "PluginRegistry",
    "ProjectStateConfig",
    "RegisteredPlugin",
    "RepositoryConfig",
    "RepositoryStatusOverride",
    "ResolvedCommand",
    "build_core_status",
    "build_dashboard_document",
    "collect_repository_statuses",
    "dashboard_project_state_from_pks_record",
    "load_dashboard_project_state_from_json_file",
    "load_plugin_factory",
    "read_dashboard_project_state_from_mapping",
    "register_plugins_from_config",
    "register_plugins_from_core_config",
    "resolve_command",
]
