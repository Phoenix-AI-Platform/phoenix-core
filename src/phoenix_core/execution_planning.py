"""Immutable descriptive planning metadata.

Plans do not grant approval, authorization, permission, or execution authority.
Planning never invokes plugin execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from phoenix_core.command_resolution import ResolvedCommand


class ExecutionPlanValidationError(ValueError):
    """Raised when execution-plan metadata is incomplete or invalid."""


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    """Immutable metadata describing a possible future operation."""

    resolved_command: ResolvedCommand
    request_id: str
    approval_reason: str
    approval_summary: str

    def __post_init__(self) -> None:
        if not isinstance(self.resolved_command, ResolvedCommand):
            raise ExecutionPlanValidationError("resolved_command must be a ResolvedCommand")

        for field_name in ("request_id", "approval_reason", "approval_summary"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ExecutionPlanValidationError(
                    f"{field_name} must be a non-empty string"
                )


def create_execution_plan(
    resolved_command: ResolvedCommand,
    *,
    request_id: str,
    approval_reason: str,
    approval_summary: str,
) -> ExecutionPlan:
    """Create immutable descriptive planning metadata without side effects."""

    return ExecutionPlan(
        resolved_command=resolved_command,
        request_id=request_id,
        approval_reason=approval_reason,
        approval_summary=approval_summary,
    )
