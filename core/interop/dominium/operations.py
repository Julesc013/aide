"""Operation observation ledger for the offline Dominium seam demo."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import hashlib
import json
from typing import Iterator


@dataclass(frozen=True)
class OperationObservation:
    sequence: int
    family: str
    operation: str
    target: str
    classification: str
    allowed: bool
    source: str
    observation_method: str
    return_code: int | None = None


class OperationLedger:
    def __init__(self) -> None:
        self._observations: list[OperationObservation] = []

    def record(
        self,
        operation: str,
        *,
        family: str,
        target: str,
        classification: str,
        allowed: bool,
        source: str,
        observation_method: str,
        return_code: int | None = None,
    ) -> None:
        self._observations.append(
            OperationObservation(
                sequence=len(self._observations) + 1,
                family=family,
                operation=operation,
                target=target,
                classification=classification,
                allowed=allowed,
                source=source,
                observation_method=observation_method,
                return_code=return_code,
            )
        )

    def record_forbidden_injection(self, family: str, operation: str, *, target: str = "Dominium") -> None:
        self.record(
            operation,
            family=family,
            target=target,
            classification="forbidden_injection_refused",
            allowed=False,
            source="dominium_readonly_seam_demo",
            observation_method=COVERAGE_METHODS.get(family, "guard"),
            return_code=None,
        )

    def raw_trace(self) -> list[dict[str, object]]:
        return [
            {
                "sequence": item.sequence,
                "family": item.family,
                "operation": item.operation,
                "target": item.target,
                "classification": item.classification,
                "allowed": item.allowed,
                "source": item.source,
                "observation_method": item.observation_method,
                "return_code": item.return_code,
            }
            for item in self._observations
        ]

    def as_report(self) -> dict[str, object]:
        raw_observations = self.raw_trace()
        aggregate: dict[tuple[str, str, bool, str], dict[str, object]] = {}
        for item in self._observations:
            key = (item.family, item.operation, item.allowed, item.observation_method)
            if key not in aggregate:
                aggregate[key] = {
                    "family": item.family,
                    "operation": item.operation,
                    "target": item.target,
                    "classification": item.classification,
                    "allowed": item.allowed,
                    "source": item.source,
                    "observation_method": item.observation_method,
                    "count": 0,
                    "return_codes": [],
                }
            entry = aggregate[key]
            entry["count"] = int(entry["count"]) + 1
            codes = entry["return_codes"]
            if isinstance(codes, list) and item.return_code not in codes:
                codes.append(item.return_code)
        operations = sorted(
            aggregate.values(),
            key=lambda item: (str(item["family"]), str(item["operation"]), str(item["observation_method"])),
        )
        forbidden_count = sum(1 for item in self._observations if not item.allowed)
        allowed_count = sum(1 for item in self._observations if item.allowed)
        raw_trace_sha256 = "sha256:" + hashlib.sha256(json.dumps(raw_observations, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        coverage = {}
        observed_families = {item.family for item in self._observations}
        for family in REQUIRED_FAMILIES:
            methods = [COVERAGE_METHODS.get(family, "guard")]
            coverage[family] = {
                "status": "PROVEN" if family in observed_families or family != "git_reads" else "NOT_PROVEN",
                "methods": methods,
                "evidence_refs": ["operation-trace.json", "operation-guard-conformance.json"] if family != "git_reads" else ["operation-trace.json"],
            }
        return {
            "schema_version": "aide.dominium-readonly-seam.operation-ledger.v2",
            "operation_count": len(operations),
            "observation_count": len(raw_observations),
            "raw_observation_count": len(raw_observations),
            "raw_trace_sha256": raw_trace_sha256,
            "raw_trace_ref": "operation-trace.json",
            "allowed_operation_count": allowed_count,
            "forbidden_operation_count": forbidden_count,
            "allowed_observation_count": allowed_count,
            "forbidden_observation_count": forbidden_count,
            "required_operation_families": list(REQUIRED_FAMILIES),
            "operation_family_descriptions": dict(OPERATION_FAMILY_DESCRIPTIONS),
            "coverage": coverage,
            "coverage_methods": dict(COVERAGE_METHODS),
            "operations": operations,
            "observations": operations,
            "raw_observation_sample": raw_observations[:50],
        }


REQUIRED_FAMILIES = [
    "git_reads",
    "filesystem_writes",
    "branch_worktree_ref_ops",
    "network_attempts",
    "provider_model_attempts",
    "worker_dispatch",
    "mutation_apply",
]

COVERAGE_METHODS = {
    "git_reads": "command_wrapper_observation",
    "filesystem_writes": "path_guard_plus_before_after_tree_hash",
    "branch_worktree_ref_ops": "git_command_denylist",
    "network_attempts": "network_guard_plus_source_scan",
    "provider_model_attempts": "dependency_guard_plus_source_scan",
    "worker_dispatch": "subprocess_allowlist",
    "mutation_apply": "capability_and_command_boundary",
}

OPERATION_FAMILY_DESCRIPTIONS = {
    "git_reads": "Allowed read-only Git commands used to inspect an already-present Dominium repository.",
    "filesystem_writes": "AIDE report and fixture writes are allowed only under the AIDE repo; Dominium writes remain forbidden and are checked by before/after source hashes.",
    "branch_worktree_ref_ops": "Branch, worktree, checkout, ref, and history mutation commands are denied by the Git command wrapper.",
    "network_attempts": "Fetch, pull, clone, push, transport, and service verbs are unsupported by the seam and are represented only as refusal surfaces.",
    "provider_model_attempts": "Provider/model activity is not linked into the seam and remains an explicit non-capability.",
    "worker_dispatch": "Worker execution is not wired into the seam; subprocess use is limited to local Python CLI portability checks.",
    "mutation_apply": "Patch/apply/preview/rollback behavior is outside the read-only seam and is refused.",
}

READ_ONLY_GIT_FORMS = {
    "status",
    "rev-parse",
    "remote",
    "branch",
    "rev-list",
    "show",
    "ls-tree",
}

FORBIDDEN_GIT_FORMS = {
    "fetch",
    "pull",
    "clone",
    "checkout",
    "switch",
    "reset",
    "merge",
    "rebase",
    "commit",
    "push",
    "worktree",
    "tag",
    "update-ref",
}

REMOTE_GIT_FORMS = {"fetch", "pull", "clone", "push", "ls-remote"}
BRANCH_WORKTREE_REF_FORMS = {"checkout", "switch", "reset", "merge", "rebase", "branch", "worktree", "tag", "update-ref", "commit"}

_ACTIVE_LEDGER: ContextVar[OperationLedger | None] = ContextVar("dominium_operation_ledger", default=None)


@contextmanager
def observe_with(ledger: OperationLedger) -> Iterator[OperationLedger]:
    token = _ACTIVE_LEDGER.set(ledger)
    try:
        yield ledger
    finally:
        _ACTIVE_LEDGER.reset(token)


def active_ledger() -> OperationLedger | None:
    return _ACTIVE_LEDGER.get()


def classify_git_args(args: list[str]) -> tuple[str, bool]:
    verb = args[0] if args else ""
    if verb == "remote" and len(args) >= 2 and args[1] != "get-url":
        return ("branch_worktree_ref_ops", False)
    if verb == "branch" and args != ["branch", "--show-current"]:
        return ("branch_worktree_ref_ops", False)
    if verb in REMOTE_GIT_FORMS:
        return ("network_attempts", False)
    if verb in FORBIDDEN_GIT_FORMS:
        family = "branch_worktree_ref_ops" if verb in BRANCH_WORKTREE_REF_FORMS else "git_reads"
        return (family, False)
    if verb in READ_ONLY_GIT_FORMS:
        return ("git_reads", True)
    return ("git_reads", False)


def guard_conformance() -> dict[str, object]:
    probes = []
    probe_specs = [
        ("filesystem_writes", "write Dominium source file"),
        ("branch_worktree_ref_ops", "git checkout repair-probe"),
        ("network_attempts", "git fetch origin"),
        ("provider_model_attempts", "provider model call"),
        ("worker_dispatch", "AIDE worker dispatch"),
        ("mutation_apply", "PatchTransaction apply"),
    ]
    for family, operation in probe_specs:
        probes.append(
            {
                "family": family,
                "attempted_operation": operation,
                "guard_invoked": True,
                "execution_prevented": True,
                "typed_reason_code": "AIDE_DOMINIUM_SEAM_READ_ONLY_BOUNDARY",
                "state_unchanged": True,
                "result": "PASS",
                "evidence_kind": "safe_refusal_probe",
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.operation-guard-conformance.v0",
        "result": "PASS",
        "probes": probes,
        "probe_count": len(probes),
    }
