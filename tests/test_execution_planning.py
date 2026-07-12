from __future__ import annotations

from dataclasses import FrozenInstanceError, fields

import pytest
from phoenix_sdk import CommandRequest, CommandResult, PluginCommand, PluginManifest

from phoenix_core import (
    ExecutionPlan,
    ExecutionPlanValidationError,
    PluginRegistry,
    ResolvedCommand,
    create_execution_plan,
    resolve_command,
)

REQUEST_ID = "request-001"
APPROVAL_REASON = "Human review is required before execution."
APPROVAL_SUMMARY = "Review the proposed demo command operation."


def _resolved_command() -> ResolvedCommand:
    return ResolvedCommand(
        plugin_id="demo.plugin",
        plugin_version="1.2.3",
        command_name="demo.inspect",
        description="Inspect demo command metadata.",
    )


def test_create_execution_plan_returns_required_immutable_shape() -> None:
    resolved = _resolved_command()

    plan = create_execution_plan(
        resolved,
        request_id=REQUEST_ID,
        approval_reason=APPROVAL_REASON,
        approval_summary=APPROVAL_SUMMARY,
    )

    assert plan == ExecutionPlan(
        resolved_command=resolved,
        request_id="request-001",
        approval_reason="Human review is required before execution.",
        approval_summary="Review the proposed demo command operation.",
    )
    assert tuple(field.name for field in fields(plan)) == (
        "resolved_command",
        "request_id",
        "approval_reason",
        "approval_summary",
    )

    with pytest.raises(FrozenInstanceError):
        plan.request_id = "changed"


def test_create_execution_plan_preserves_exact_caller_values() -> None:
    plan = create_execution_plan(
        _resolved_command(),
        request_id="  request-001 ",
        approval_reason=" Human review is required.\t",
        approval_summary="\nReview the operation. ",
    )

    assert plan.request_id == "  request-001 "
    assert plan.approval_reason == " Human review is required.\t"
    assert plan.approval_summary == "\nReview the operation. "


@pytest.mark.parametrize("request_id", ["", " ", "\t\r\n"])
def test_create_execution_plan_rejects_empty_request_id(request_id: str) -> None:
    with pytest.raises(ExecutionPlanValidationError, match="request_id"):
        create_execution_plan(
            _resolved_command(),
            request_id=request_id,
            approval_reason=APPROVAL_REASON,
            approval_summary=APPROVAL_SUMMARY,
        )


def test_create_execution_plan_rejects_non_string_request_id() -> None:
    with pytest.raises(ExecutionPlanValidationError, match="request_id"):
        create_execution_plan(
            _resolved_command(),
            request_id=123,  # type: ignore[arg-type]
            approval_reason=APPROVAL_REASON,
            approval_summary=APPROVAL_SUMMARY,
        )


@pytest.mark.parametrize("approval_reason", ["", " ", "\t\r\n"])
def test_create_execution_plan_rejects_empty_approval_reason(
    approval_reason: str,
) -> None:
    with pytest.raises(ExecutionPlanValidationError, match="approval_reason"):
        create_execution_plan(
            _resolved_command(),
            request_id=REQUEST_ID,
            approval_reason=approval_reason,
            approval_summary=APPROVAL_SUMMARY,
        )


def test_create_execution_plan_rejects_non_string_approval_reason() -> None:
    with pytest.raises(ExecutionPlanValidationError, match="approval_reason"):
        create_execution_plan(
            _resolved_command(),
            request_id=REQUEST_ID,
            approval_reason=123,  # type: ignore[arg-type]
            approval_summary=APPROVAL_SUMMARY,
        )


@pytest.mark.parametrize("approval_summary", ["", " ", "\t\r\n"])
def test_create_execution_plan_rejects_empty_approval_summary(
    approval_summary: str,
) -> None:
    with pytest.raises(ExecutionPlanValidationError, match="approval_summary"):
        create_execution_plan(
            _resolved_command(),
            request_id=REQUEST_ID,
            approval_reason=APPROVAL_REASON,
            approval_summary=approval_summary,
        )


def test_create_execution_plan_rejects_non_string_approval_summary() -> None:
    with pytest.raises(ExecutionPlanValidationError, match="approval_summary"):
        create_execution_plan(
            _resolved_command(),
            request_id=REQUEST_ID,
            approval_reason=APPROVAL_REASON,
            approval_summary=123,  # type: ignore[arg-type]
        )


def test_create_execution_plan_rejects_invalid_resolved_command() -> None:
    with pytest.raises(ExecutionPlanValidationError, match="resolved_command"):
        create_execution_plan(
            "not resolved",  # type: ignore[arg-type]
            request_id=REQUEST_ID,
            approval_reason=APPROVAL_REASON,
            approval_summary=APPROVAL_SUMMARY,
        )


def test_execution_plan_exposes_no_executable_capability() -> None:
    plan = create_execution_plan(
        _resolved_command(),
        request_id=REQUEST_ID,
        approval_reason=APPROVAL_REASON,
        approval_summary=APPROVAL_SUMMARY,
    )

    forbidden_attributes = (
        "command",
        "execute",
        "callback",
        "payload",
        "request",
        "approval_decision",
        "approved",
        "authorization",
        "token",
        "artifact_path",
    )
    assert all(not hasattr(plan, attribute) for attribute in forbidden_attributes)


class ExplodingCommand:
    name = "demo.inspect"
    description = "Inspect demo command metadata."

    def execute(self, request: CommandRequest) -> CommandResult:
        raise AssertionError("Planning must never execute the command.")


class DemoPlugin:
    def __init__(self) -> None:
        self._command = ExplodingCommand()

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            plugin_id="demo.plugin",
            name="Demo Plugin",
            version="1.2.3",
            description="Execution-planning test plugin.",
            commands=("demo.inspect",),
        )

    def list_commands(self) -> tuple[PluginCommand, ...]:
        return (self._command,)

    def get_command(self, name: str) -> PluginCommand:
        if name != self._command.name:
            raise KeyError(name)
        return self._command


def test_planning_existing_resolved_command_never_executes_plugin_command() -> None:
    registry = PluginRegistry()
    registry.register(DemoPlugin())
    resolved = resolve_command(registry, "demo.plugin", "demo.inspect")

    plan = create_execution_plan(
        resolved,
        request_id=REQUEST_ID,
        approval_reason=APPROVAL_REASON,
        approval_summary=APPROVAL_SUMMARY,
    )

    assert plan.resolved_command == resolved
