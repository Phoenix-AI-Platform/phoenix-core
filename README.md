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

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```
