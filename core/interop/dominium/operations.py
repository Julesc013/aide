"""Operation observation ledger for the offline Dominium seam demo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationObservation:
    operation: str
    target: str
    classification: str
    allowed: bool
    source: str


class OperationLedger:
    def __init__(self) -> None:
        self._observations: list[OperationObservation] = []

    def record(self, operation: str, *, target: str, classification: str, allowed: bool, source: str) -> None:
        self._observations.append(
            OperationObservation(
                operation=operation,
                target=target,
                classification=classification,
                allowed=allowed,
                source=source,
            )
        )

    def record_demo_readonly_flow(self) -> None:
        for operation in [
            "git status --short --branch",
            "git rev-parse",
            "git remote get-url",
            "git branch --show-current",
            "git rev-list --left-right --count",
            "git show <revision>:<path>",
        ]:
            self.record(
                operation,
                target="Dominium",
                classification="read_only_observation",
                allowed=True,
                source="dominium_readonly_seam_demo",
            )

    def as_report(self) -> dict[str, object]:
        observations = [
            {
                "operation": item.operation,
                "target": item.target,
                "classification": item.classification,
                "allowed": item.allowed,
                "source": item.source,
            }
            for item in self._observations
        ]
        return {
            "schema_version": "aide.dominium-readonly-seam.operation-ledger.v0",
            "observation_count": len(observations),
            "forbidden_operation_count": sum(1 for item in self._observations if not item.allowed),
            "observations": observations,
        }
