# Phoenix Core

Shared platform core for Phoenix AI.

## Purpose

`phoenix-core` owns platform-level coordination primitives.

The first responsibility is intentionally small:

- Register SDK-compatible plugins.
- Read plugin manifests.
- List plugin commands.
- Do not execute plugin commands yet.

## Design Rules

- Core depends on the SDK contract.
- Core must not contain plugin-specific business logic.
- Core must not execute commands until execution policy is explicitly designed.
- Deterministic plugin workflows remain inside their plugin repositories.
- Platform-level knowledge lives in `phoenix-pks`.

## Canonical Phoenix Knowledge

Platform-wide project state, architecture, decisions, roadmap, and agent guidance live in [`phoenix-pks`](https://github.com/Phoenix-AI-Platform/phoenix-pks).

Start with the [Project State](https://github.com/Phoenix-AI-Platform/phoenix-pks/blob/main/project/02_PROJECT_STATE.md), [Current Sprint](https://github.com/Phoenix-AI-Platform/phoenix-pks/blob/main/project/05_CURRENT_SPRINT.md), and [ADR Index](https://github.com/Phoenix-AI-Platform/phoenix-pks/blob/main/adr/README.md). Core-specific implementation documentation remains authoritative in this repository.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```
