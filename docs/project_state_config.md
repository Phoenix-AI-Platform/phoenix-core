# Project State Config

Phoenix Core can include a static project-state summary in dashboard output.

This is intentionally local and explicit. Phoenix Core does not infer project state from GitHub, CI, PKS, or external systems in this slice.

## TOML example

```toml
[project_state]
phase = "Dashboard Foundation"
milestone = "Read-only project visibility"
summary = "Expose safe dashboard data without live external calls."
```

## Dashboard output

When present, `phoenix-core dashboard --config <path>` includes:

```json
{
  "project_state": {
    "phase": "Dashboard Foundation",
    "milestone": "Read-only project visibility",
    "summary": "Expose safe dashboard data without live external calls."
  }
}
```

## Boundaries

Project state config is read-only metadata.

It does not:

- execute plugin commands,
- call GitHub,
- call CI providers,
- read PKS state,
- infer project progress automatically.

Future PKS integration should treat this field as the dashboard-facing destination shape, not as an execution trigger.
