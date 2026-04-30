"""Replay metadata for Q06 Compatibility baseline checks.

Replay here means deterministic Harness summary expectations, not Runtime
execution replay.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReplayExpectation:
    id: str
    command: str
    mutation: str
    expected_hard_errors: int
    expected_warning_posture: str
    notes: str


def replay_expectations() -> list[ReplayExpectation]:
    return [
        ReplayExpectation(
            id="validate-current-repo",
            command="py -3 scripts/aide validate",
            mutation="none",
            expected_hard_errors=0,
            expected_warning_posture="review-gate warnings are acceptable while Q00-Q03/Q05/Q06 remain review-gated",
            notes="Structural validation should include compatibility version checks after Q06.",
        ),
        ReplayExpectation(
            id="doctor-current-repo",
            command="py -3 scripts/aide doctor",
            mutation="none",
            expected_hard_errors=0,
            expected_warning_posture="same as validate",
            notes="Doctor should report Q06 compatibility baseline and the next review step.",
        ),
        ReplayExpectation(
            id="compile-dry-run-current-repo",
            command="py -3 scripts/aide compile --dry-run",
            mutation="none",
            expected_hard_errors=0,
            expected_warning_posture="generated manifest should be current after allowed refresh",
            notes="Compile remains generated-artifact v0 behavior; Q06 does not change generation policy.",
        ),
        ReplayExpectation(
            id="migrate-current-noop",
            command="py -3 scripts/aide migrate",
            mutation="none",
            expected_hard_errors=0,
            expected_warning_posture="unknown future versions would be errors",
            notes="Migrate reports the no-op baseline and available registry entries.",
        ),
    ]

