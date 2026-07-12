# Phoenix Core Dashboard Data Flow

## Purpose

This document describes the current read-only data flow that builds the Phoenix Core dashboard document.

It documents existing behavior only. It does not add file loading, network access, command execution, or a dashboard user interface.

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
        -> PhoenixCoreConfig.project_state
        -> DashboardProjectState

build_core_status(...)
+ repository status records
+ optional DashboardProjectState
  -> build_dashboard_document(...)
  -> DashboardDocument
  -> deterministic JSON from `phoenix-core dashboard`
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

Without an override, CI status remains `unknown` and latest commit remains unset. Phoenix Core does not currently call GitHub or a CI provider to populate these values.

## Project-State Paths

Phoenix Core currently has two explicit project-state seams.

### CLI configuration path

The dashboard CLI reads an optional `[project_state]` section from the supplied Core TOML configuration and converts it into `DashboardProjectState`.

### PKS mapping seam

`read_dashboard_project_state_from_mapping(...)` accepts an already-loaded mapping with:

- `phase`
- `milestone`
- `summary`

It validates those values and returns `DashboardProjectState`.

This seam does not read Phoenix PKS Markdown, JSON, or any other file. A future integration layer must load and select the mapping explicitly before passing it to Core.

## Assembly Boundary

`build_dashboard_document(...)` is the single assembly point for:

- Core status
- Repository status records
- Optional project state

It returns a frozen `DashboardDocument`, which is then serialized deterministically through `to_dict()` and sorted JSON output.

## Explicitly Out of Scope

The current dashboard data flow does not:

- Read Phoenix PKS files
- Infer project state from prose
- Call GitHub or CI APIs
- Inspect live branches or commits
- Execute plugin commands
- Generate proposals or DOCX files
- Send customer-facing output
- Apply approvals or remediation
- Run a web server or dashboard UI
- Schedule or perform background work

## Safe Next Integration Boundary

A future PKS integration PR may add a read-only loader that produces the exact mapping accepted by `read_dashboard_project_state_from_mapping(...)`.

That work should remain separate from:

- Dashboard UI work
- Live repository or CI collection
- Plugin execution
- Workflow automation
- Phoenix Office behavior changes
