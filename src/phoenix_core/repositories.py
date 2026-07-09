"""Repository status collection helpers for Phoenix Core.

This module accepts static repository declarations plus optional precomputed status
overrides. It does not call GitHub or any CI provider.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from phoenix_core.config import RepositoryConfig
from phoenix_core.dashboard import DashboardRepositoryStatus


@dataclass(frozen=True, slots=True)
class RepositoryStatusOverride:
    """Precomputed repository status supplied by an external collector."""

    ci_status: str
    latest_commit: str | None = None


def collect_repository_statuses(
    repositories: Iterable[RepositoryConfig],
    status_overrides: Mapping[str, RepositoryStatusOverride] | None = None,
) -> tuple[DashboardRepositoryStatus, ...]:
    """Build dashboard repository statuses from config and optional overrides."""

    overrides = status_overrides or {}
    statuses: list[DashboardRepositoryStatus] = []
    for repository in repositories:
        override = overrides.get(repository.name)
        statuses.append(
            DashboardRepositoryStatus(
                name=repository.name,
                url=repository.url,
                default_branch=repository.default_branch,
                ci_status=override.ci_status if override else "unknown",
                latest_commit=override.latest_commit if override else None,
            )
        )
    return tuple(statuses)
