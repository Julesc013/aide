"""Diagnostic model for AIDE Harness v0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


SEVERITIES = ("info", "warning", "error")


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    message: str
    path: str | None = None
    hint: str | None = None

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"unknown diagnostic severity: {self.severity}")


def count_by_severity(diagnostics: Iterable[Diagnostic]) -> dict[str, int]:
    counts = {severity: 0 for severity in SEVERITIES}
    for diagnostic in diagnostics:
        counts[diagnostic.severity] += 1
    return counts


def has_errors(diagnostics: Iterable[Diagnostic]) -> bool:
    return any(diagnostic.severity == "error" for diagnostic in diagnostics)


def status_label(diagnostics: list[Diagnostic]) -> str:
    counts = count_by_severity(diagnostics)
    if counts["error"]:
        return "FAIL"
    if counts["warning"]:
        return "PASS_WITH_WARNINGS"
    return "PASS"


def render_diagnostic(diagnostic: Diagnostic) -> str:
    location = f" path={diagnostic.path}" if diagnostic.path else ""
    line = f"[{diagnostic.severity}] {diagnostic.code}: {diagnostic.message}{location}"
    if diagnostic.hint:
        line += f"\n  hint: {diagnostic.hint}"
    return line


def render_report(title: str, diagnostics: list[Diagnostic]) -> str:
    counts = count_by_severity(diagnostics)
    lines = [
        title,
        f"status: {status_label(diagnostics)}",
        f"summary: {counts['info']} info, {counts['warning']} warning, {counts['error']} error",
    ]
    if diagnostics:
        lines.append("")
        lines.extend(render_diagnostic(diagnostic) for diagnostic in diagnostics)
    return "\n".join(lines)
