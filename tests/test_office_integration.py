from __future__ import annotations

import pytest
from phoenix_office.sdk_adapter import create_plugin
from phoenix_sdk import CommandRequest, PhoenixPlugin

from phoenix_core import (
    ExecutionPlan,
    PluginRegistry,
    ResolvedCommand,
    create_execution_plan,
    resolve_command,
)


def test_core_registers_phoenix_office_plugin_metadata() -> None:
    registry = PluginRegistry()
    office_plugin = create_plugin()

    registered = registry.register(office_plugin)

    assert isinstance(office_plugin, PhoenixPlugin)
    assert registered.plugin_id == "phoenix.office"
    assert registered.manifest.name == "Phoenix Office"
    assert registered.manifest.metadata["execution"] == "metadata_only"


def test_core_lists_phoenix_office_commands_without_execution() -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    commands = registry.get("phoenix.office").list_commands()
    command_names = tuple(command.name for command in commands)

    assert command_names == (
        "proposal.prepare_fields",
        "proposal.generate_docx",
    )


@pytest.mark.parametrize(
    ("command_name", "description"),
    (
        (
            "proposal.prepare_fields",
            "Prepare deterministic proposal fields from validated proposal input.",
        ),
        (
            "proposal.generate_docx",
            "Render a DOCX proposal from validated input and an explicit template.",
        ),
    ),
)
def test_core_resolves_phoenix_office_command_metadata_without_execution(
    command_name: str,
    description: str,
) -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    resolved = resolve_command(registry, "phoenix.office", command_name)
    plan = create_execution_plan(
        resolved,
        request_id=f"office-test-{command_name}",
        approval_reason="Human approval is required before Phoenix Office execution.",
        approval_summary=f"Review Phoenix Office command {command_name}.",
    )

    assert resolved == ResolvedCommand(
        plugin_id="phoenix.office",
        plugin_version="0.1.0",
        command_name=command_name,
        description=description,
    )
    assert plan == ExecutionPlan(
        resolved_command=resolved,
        request_id=f"office-test-{command_name}",
        approval_reason="Human approval is required before Phoenix Office execution.",
        approval_summary=f"Review Phoenix Office command {command_name}.",
    )
    assert plan.resolved_command == resolved
    assert plan.resolved_command.plugin_id == "phoenix.office"
    assert plan.resolved_command.plugin_version == "0.1.0"
    assert plan.resolved_command.command_name == command_name
    assert plan.resolved_command.description == description
    assert plan.request_id == f"office-test-{command_name}"
    assert plan.approval_reason == (
        "Human approval is required before Phoenix Office execution."
    )
    assert plan.approval_summary == f"Review Phoenix Office command {command_name}."
    assert not hasattr(plan, "command")
    assert not hasattr(plan, "execute")
    assert not hasattr(plan, "payload")
    assert not hasattr(plan, "approval_decision")
    assert not hasattr(plan, "approved")
    assert not hasattr(resolved, "command")
    assert not hasattr(resolved, "execute")


def test_core_does_not_execute_phoenix_office_commands() -> None:
    registry = PluginRegistry()
    registry.register(create_plugin())

    command = registry.get("phoenix.office").list_commands()[0]

    with pytest.raises(NotImplementedError):
        command.execute(CommandRequest(command=command.name))
