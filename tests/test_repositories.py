from __future__ import annotations

from phoenix_core import RepositoryConfig, RepositoryStatusOverride, collect_repository_statuses


def test_collect_repository_statuses_defaults_to_unknown() -> None:
    statuses = collect_repository_statuses(
        (
            RepositoryConfig(
                name="phoenix-core",
                url="https://github.com/Phoenix-AI-Platform/phoenix-core",
            ),
        )
    )

    assert statuses[0].name == "phoenix-core"
    assert statuses[0].default_branch == "main"
    assert statuses[0].ci_status == "unknown"
    assert statuses[0].latest_commit is None


def test_collect_repository_statuses_applies_precomputed_overrides() -> None:
    statuses = collect_repository_statuses(
        (
            RepositoryConfig(
                name="phoenix-core",
                url="https://github.com/Phoenix-AI-Platform/phoenix-core",
            ),
        ),
        {
            "phoenix-core": RepositoryStatusOverride(
                ci_status="success",
                latest_commit="abc123",
            )
        },
    )

    assert statuses[0].ci_status == "success"
    assert statuses[0].latest_commit == "abc123"
