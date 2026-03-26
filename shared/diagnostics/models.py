"""Structured diagnostics used by the shared-core bootstrap runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class DiagnosticSource:
    layer: str
    component: str | None


@dataclass(frozen=True)
class DiagnosticLocation:
    start_line: int | None = None
    start_column: int | None = None
    end_line: int | None = None
    end_column: int | None = None


@dataclass(frozen=True)
class DiagnosticContext:
    document_uri: str | None = None
    workspace_id: str | None = None
    location: DiagnosticLocation = field(default_factory=DiagnosticLocation)


@dataclass(frozen=True)
class DiagnosticDetails:
    evidence: Mapping[str, Any] | list[Any] | str | None = None
    machine_reason: str | None = None


@dataclass(frozen=True)
class SuggestedAction:
    action_id: str | None = None
    summary: str | None = None


@dataclass(frozen=True)
class Diagnostic:
    id: str
    severity: str
    source: DiagnosticSource
    message: str
    context: DiagnosticContext = field(default_factory=DiagnosticContext)
    details: DiagnosticDetails = field(default_factory=DiagnosticDetails)
    suggested_action: SuggestedAction = field(default_factory=SuggestedAction)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_diagnostic(
    *,
    diagnostic_id: str,
    severity: str,
    component: str,
    message: str,
    machine_reason: str | None = None,
    evidence: Mapping[str, Any] | list[Any] | str | None = None,
    action_summary: str | None = None,
    document_uri: str | None = None,
    workspace_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a JSON-friendly diagnostic payload."""

    diagnostic = Diagnostic(
        id=diagnostic_id,
        severity=severity,
        source=DiagnosticSource(layer="shared-core", component=component),
        message=message,
        context=DiagnosticContext(document_uri=document_uri, workspace_id=workspace_id),
        details=DiagnosticDetails(evidence=evidence, machine_reason=machine_reason),
        suggested_action=SuggestedAction(summary=action_summary),
        metadata=metadata or {},
    )
    return diagnostic.to_dict()
