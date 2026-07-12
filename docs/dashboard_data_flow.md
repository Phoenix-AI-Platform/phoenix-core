# Phoenix Core Dashboard Data Flow

## Purpose

This document describes the current read-only data flow that builds the Phoenix Core dashboard document.

The dashboard can load approved plugin metadata, static repository declarations, and one explicit project-state source. It does not call network services, execute plugin commands, infer project state from prose, or run a dashboard server.

## Current Output Contract

Phoenix Core serializes dashboard data with schema version:

```text
phoenix.dashboard_document.v1
```

The dashboard document contains:

- Core component metadata
- Registered plugin and command metadata
- Repository status records
- Optional project-state metadata

## Current Data Flow

```text
Phoenix Core TOML config
  |
  +-- plugin declarations
  |     -> PhoenixCoreConfig
  |     -> register_plugins_from_core_config(...)
  |     -> PluginRegistry
  |     -> build_core_status(...)
  |     -> dashboard plugin metadata
  |
  +-- repository declarations
  |     -> PhoenixCoreConfig.repositories
  |     -> collect_repository_statuses(...)
  |     -> DashboardRepositoryStatus records
  |
  +-- optional [project_state]
        -> DashboardProjectState

optional caller-selected --project-state-json
  -> load_dashboard_project_state_from_json_file(...)
  -> DashboardProjectState

exactly one project-state source
+ Core status
+ repository status records
  -> build_dashboard_document(...)
  -> DashboardDocument
  -> deterministic sorted JSON from `phoenix-core dashboard`
```

## Plugin Metadata Path

Configured plugins are loaded through the existing Core loader and registry.

The dashboard reads only:

- Plugin ID
- Name
- Version
- Description
- Command names
- Command descriptions

The dashboard path does not call `PluginCommand.execute()` and does not route work into Phoenix Office.

## Repository Status Path

Repository declarations come from explicit Core configuration.

`collect_repository_statuses(...)` converts those declarations, plus any caller-supplied status overrides, into dashboard repository records.

Without an override, CI status remains `unknown` and latest commit remains unset. Phoenix Core does not call GitHub or a CI provider to populate these values.

## Project-State Sources

Phoenix Core supports exactly one project-state source for each dashboard invocation.

### Static Core configuration

An optional `[project_state]` section in the supplied Core TOML configuration may contain:

- `phase`
- `milestone`
- `summary`

Existing static configuration behavior remains supported.

### Explicit JSON file

The caller may supply one UTF-8 JSON object:

```bash
phoenix-core dashboard \
  --config examples/phoenix_core.toml \
  --project-state-json ../phoenix-pks/project/dashboard-project-state.json
```

The JSON object must contain string values for:

- `phase`
- `milestone`
- `summary`

The path is caller-controlled. Core does not search for PKS files or infer a default location.

`load_dashboard_project_state_from_json_file(...)` parses the explicit file and delegates field validation to the existing PKS mapping seam.

### Conflict behavior

Supplying both `[project_state]` in Core TOML and `--project-state-json` is rejected. Core does not silently choose or merge competing project-state sources.

Invalid JSON, a non-object top-level value, unreadable input, or invalid field types also fail before dashboard output is produced.

## Assembly Boundary

`build_dashboard_document(...)` is the single assembly point for:

- Core status
- Repository status records
- Optional project state

It returns a frozen `DashboardDocument`, which is serialized deterministically through `to_dict()` and sorted JSON output.

## Explicitly Out of Scope

The current dashboard data flow does not:

- Parse PKS Markdown or YAML front matter
- Infer project state from prose
- Automatically discover or synchronize PKS state
- Call GitHub or CI APIs
- Inspect live branches or commits
- Execute plugin commands
- Generate proposals or DOCX files
- Send customer-facing output
- Apply approvals or remediation
- Run a web server or dashboard UI
- Schedule or perform background work

## Safe Next Integration Boundary

The end-to-end local read-only path can now be verified by explicitly passing the reviewed Phoenix PKS projection to the Core dashboard command.

Future work should remain separate from:

- Dashboard UI work
- Live repository or CI collection
- Plugin execution
- Workflow automation
- Phoenix Office behavior changes
