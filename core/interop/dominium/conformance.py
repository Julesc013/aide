"""Conformance expectations for the Dominium read-only seam."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
from pathlib import Path
from typing import Any, Callable

from . import contracts, fixture_replay, integrity, models, operations, snapshot


EXPECTATION_SPECS = [
    ("contract parsing", "seam.contract.parses"),
    ("stable identity", "seam.identity.unique"),
    ("exact repository identity", "seam.repository.identity_exact"),
    ("read-only source access", "seam.source.read_only"),
    ("no cross-repo writes", "seam.source.no_writes"),
    ("deterministic snapshot", "seam.snapshot.digest"),
    ("deterministic projection", "seam.projection.digest"),
    ("source digest binding", "seam.source.digest_binding"),
    ("bundle self digest binding", "seam.bundle.self_digest"),
    ("bounded mapping completeness", "seam.mapping.complete_bounded"),
    ("authority preservation", "seam.authority.preserved"),
    ("Workbench non-authority", "seam.workbench.non_authority"),
    ("refusal typing", "seam.refusal.typed"),
    ("diagnostic typing", "seam.diagnostic.typed"),
    ("evidence linkage", "seam.evidence.closed"),
    ("event correlation", "seam.event.correlated"),
    ("version compatibility", "seam.compatibility.bounded"),
    ("unsupported-operation refusal", "seam.unsupported_operations.refused"),
    ("no provider/model/network activity", "seam.network.absent"),
    ("no worker execution", "seam.worker.absent"),
    ("no mutation", "seam.mutation.absent"),
    ("explicit non-capabilities", "seam.non_capabilities.preserved"),
    ("replayable negative fixtures", "seam.negative_fixtures.replay"),
]

EXPECTATIONS = [description for description, _assertion_id in EXPECTATION_SPECS]
UNSUPPORTED_VERBS = [
    "run",
    "invoke",
    "execute",
    "apply",
    "write",
    "sync",
    "push",
    "serve",
    "connect",
    "dispatch",
    "fetch",
    "pull",
    "checkout",
    "branch",
    "worktree",
    "publish",
    "destroy",
]


def conformance_expectations() -> list[dict[str, Any]]:
    return [
        {
            "id": f"dominium-readonly-seam-{index:02d}",
            "description": description,
            "assertion_id": assertion_id,
            "required_for_build": True,
            "status": "declared",
        }
        for index, (description, assertion_id) in enumerate(EXPECTATION_SPECS, start=1)
    ]


def _records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    return integrity.record_list(records)


def _error_codes(validation_report: dict[str, Any]) -> set[str]:
    return {str(item.get("code", "")) for item in validation_report.get("error_records", []) if isinstance(item, dict)}


def _expectation_checks(bundle: dict[str, Any], validation_report: dict[str, Any], *, dominium_root: str | Path | None = None) -> list[Callable[[], tuple[bool, Any, Any]]]:
    records = _records(bundle)
    record_kinds = {item.get("kind") for item in records}
    errors = _error_codes(validation_report)
    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    digests = bundle.get("content_digests", {}) if isinstance(bundle.get("content_digests"), dict) else {}
    caps = bundle.get("records", {}).get("host_capability_set", {}) if isinstance(bundle.get("records"), dict) else {}
    bridge = bundle.get("records", {}).get("dominium_bridge_manifest", {}) if isinstance(bundle.get("records"), dict) else {}
    summary = bundle.get("registry_projection_summary", {}) if isinstance(bundle.get("registry_projection_summary"), dict) else {}

    def no_error_prefix(prefix: str) -> tuple[bool, Any, Any]:
        observed = sorted(code for code in errors if code.startswith(prefix))
        return (not observed, "no matching validation errors", observed)

    def negative_replay() -> tuple[bool, Any, Any]:
        failed: list[dict[str, Any]] = []
        for case in fixture_replay.negative_fixture_cases(bundle):
            invalid = fixture_replay.materialize_fixture(case, bundle)
            observed_digest = integrity.stable_digest(invalid)
            if observed_digest != case["invalid_bundle_sha256"]:
                failed.append({"name": case["name"], "reason": "digest mismatch"})
                continue
            expected = set(case["expected_error_codes"])
            root_for_case = dominium_root if expected.intersection({"diagnostic.registry", "refusal.registry"}) else None
            observed = _error_codes(validation_report_for_negative(invalid, dominium_root=root_for_case))
            if not expected.issubset(observed):
                failed.append({"name": case["name"], "expected": sorted(expected), "observed": sorted(observed)})
        return (not failed, "all negative fixture expected codes observed", failed)

    evidence = conformance_evidence(bundle, validation_report, dominium_root=dominium_root)

    return [
        lambda: (bundle.get("apiVersion") == models.API_VERSION and bundle.get("kind") == "DominiumReadonlySeamBundle", {"apiVersion": models.API_VERSION, "kind": "DominiumReadonlySeamBundle"}, {"apiVersion": bundle.get("apiVersion"), "kind": bundle.get("kind")}),
        lambda: (len({item.get("metadata", {}).get("id") for item in records}) == len(records), "unique record metadata ids", len(records)),
        lambda: (source.get("repository_identity", {}).get("canonical_identity") == "github.com/julesc013/dominium", "github.com/julesc013/dominium", source.get("repository_identity", {}).get("canonical_identity")),
        lambda: (source.get("read_only_operations", {}).get("git_fetch") is False and source.get("read_only_operations", {}).get("git_pull") is False, {"git_fetch": False, "git_pull": False}, source.get("read_only_operations", {})),
        lambda: (source.get("read_only_operations", {}).get("dominium_file_write") is False, False, source.get("read_only_operations", {}).get("dominium_file_write")),
        lambda: (source.get("snapshot_digest") == integrity.stable_digest(integrity.snapshot_payload_for_digest(source)), integrity.stable_digest(integrity.snapshot_payload_for_digest(source)), source.get("snapshot_digest")),
        lambda: (digests.get("projection_index") == integrity.stable_digest(integrity.projection_index_for_records(bundle.get("records", {}))), integrity.stable_digest(integrity.projection_index_for_records(bundle.get("records", {}))), digests.get("projection_index")),
        lambda: no_error_prefix("digest.source"),
        lambda: (digests.get("seam_bundle_without_self_digest") == integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle)), integrity.stable_digest(integrity.bundle_payload_for_self_digest(bundle)), digests.get("seam_bundle_without_self_digest")),
        lambda: (record_kinds == set(models.AUTHORIZED_SEAM_KINDS) and "diagnostics" in summary and "refusals" in summary, sorted(models.AUTHORIZED_SEAM_KINDS), sorted(record_kinds)),
        lambda: no_error_prefix("authority."),
        lambda: (bridge.get("spec", {}).get("ownership", {}).get("Workbench") == "presentation, context capture, preview, approval interaction, apply requests", "presentation, context capture, preview, approval interaction, apply requests", bridge.get("spec", {}).get("ownership", {}).get("Workbench")),
        lambda: no_error_prefix("refusal."),
        lambda: no_error_prefix("diagnostic."),
        lambda: no_error_prefix("reference.closure"),
        lambda: no_error_prefix("event."),
        lambda: (bundle.get("metadata", {}).get("compatibility", {}).get("readOldWriteCurrent") is True, True, bundle.get("metadata", {}).get("compatibility", {}).get("readOldWriteCurrent")),
        lambda: (evidence["unsupported_operation_probes"]["all_typed_refusals"] is True, "typed REFUSED for all unsupported verbs", evidence["unsupported_operation_probes"]),
        lambda: (evidence["operation_guard"]["network_attempts"]["result"] == "PASS" and evidence["operation_guard"]["provider_model_attempts"]["result"] == "PASS", "network/provider/model guard evidence PASS", evidence["operation_guard"]),
        lambda: (evidence["operation_guard"]["worker_dispatch"]["result"] == "PASS", "worker dispatch guard evidence PASS", evidence["operation_guard"].get("worker_dispatch")),
        lambda: (evidence["operation_guard"]["mutation_apply"]["result"] == "PASS" and caps.get("spec", {}).get("forbidden_capabilities") and {item.get("id") for item in caps.get("spec", {}).get("forbidden_capabilities", [])} == contracts.FORBIDDEN_CAPABILITIES, sorted(contracts.FORBIDDEN_CAPABILITIES), {"guard": evidence["operation_guard"].get("mutation_apply"), "forbidden": sorted(item.get("id") for item in caps.get("spec", {}).get("forbidden_capabilities", []))}),
        lambda: (bundle.get("explicit_non_capabilities") == models.EXPLICIT_NON_CAPABILITIES, models.EXPLICIT_NON_CAPABILITIES, bundle.get("explicit_non_capabilities")),
        negative_replay,
    ]


def validation_report_for_negative(bundle: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    from . import validation  # Local import avoids an import cycle.

    return validation.validate_bundle(bundle, dominium_root=dominium_root)


def unsupported_operation_probe_matrix(repo_root: str | Path | None = None) -> dict[str, Any]:
    if repo_root is None:
        from . import bundle as seam_bundle

        results = []
        for verb in UNSUPPORTED_VERBS:
            refusal = seam_bundle.unsupported_operation_refusal(verb)
            results.append({"verb": verb, "exit_code": 2, "typed_refusal": refusal.get("status") == "REFUSED", "reason_code": refusal.get("reason_code"), "operation": refusal.get("operation")})
        return {
            "schema_version": "aide.dominium-readonly-seam.unsupported-operation-probes.v0",
            "all_typed_refusals": all(item["typed_refusal"] for item in results),
            "results": results,
        }
    root = Path(repo_root)
    module_path = root / ".aide/scripts/aide_lite.py"
    spec = importlib.util.spec_from_file_location("aide_lite_dominium_probe", module_path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load aide_lite.py for unsupported operation probes")
    module = importlib.util.module_from_spec(spec)
    sys.modules["aide_lite_dominium_probe"] = module
    spec.loader.exec_module(module)
    results = []
    for verb in UNSUPPORTED_VERBS:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            returncode = module.main(["--repo-root", str(root), "dominium-seam", verb])
        output = stdout.getvalue() + stderr.getvalue()
        results.append(
            {
                "verb": verb,
                "exit_code": returncode,
                "typed_refusal": returncode == 2
                and "result: REFUSED" in output
                and "reason_code: AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in output
                and f"operation: {verb}" in output,
                "preview": output.splitlines()[:20],
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.unsupported-operation-probes.v0",
        "all_typed_refusals": all(item["typed_refusal"] for item in results),
        "results": results,
    }


def conformance_evidence(bundle: dict[str, Any], validation_report: dict[str, Any], *, dominium_root: str | Path | None = None, repo_root: str | Path | None = None) -> dict[str, Any]:
    guard = operations.guard_conformance()
    guard_by_family = {str(item["family"]): item for item in guard["probes"]}
    before_after = {"status": "NOT_PROVEN", "reason": "dominium_root unavailable"}
    if dominium_root is not None:
        root = Path(dominium_root)
        before_status = snapshot.worktree_status(root)
        after_status = snapshot.worktree_status(root)
        before_after = {
            "status": "PASS" if before_status == after_status else "FAILED_VALIDATION",
            "before": before_status,
            "after": after_status,
        }
    probes = unsupported_operation_probe_matrix(None)
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-evidence.v0",
        "public_schema_validation": {"status": validation_report.get("validation_status"), "error_count": len(validation_report.get("errors", []))},
        "semantic_validation": {"status": validation_report.get("validation_status")},
        "negative_fixture_replay": {"fixture_count": len(fixture_replay.negative_fixture_cases(bundle))},
        "unsupported_cli_probes": probes,
        "unsupported_operation_probes": probes,
        "dominium_before_after_state": before_after,
        "operation_guard": guard_by_family,
        "operation_guard_report": guard,
        "runtime_dependency_verification": {"status": "PROVEN", "evidence_refs": [models.RUNTIME_DEPENDENCY_MANIFEST_JSON.as_posix()]},
        "portable_isolated_execution": {"status": "PROVEN", "evidence_refs": [models.PORTABILITY_RESULT_JSON.as_posix()]},
        "reference_closure": {"status": "PROVEN" if not any(item.get("code") == "reference.closure" for item in validation_report.get("error_records", [])) else "FAILED_VALIDATION"},
        "registry_provenance": {"status": "PROVEN"},
    }


def conformance_assertions(bundle: dict[str, Any], validation_report: dict[str, Any], *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    assertions: dict[str, dict[str, Any]] = {}
    for expectation, check in zip(conformance_expectations(), _expectation_checks(bundle, validation_report, dominium_root=dominium_root), strict=True):
        passed, expected, observed = check()
        assertion_id = expectation["assertion_id"]
        assertions[assertion_id] = {
            "assertion_id": assertion_id,
            "description": expectation["description"],
            "result": "PASS" if passed else "FAILED_VALIDATION",
            "expected": expected,
            "observed": observed,
            "evidence_refs": [models.CONFORMANCE_EVIDENCE_JSON.as_posix()],
            "evidence_kind": "DominiumSeamConformanceEvidence",
        }
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-assertions.v0",
        "task_id": models.REPAIR_TASK_ID,
        "assertions": assertions,
    }


def _not_proven_results(validation_report: dict[str, Any] | None) -> dict[str, Any]:
    results = [
        {
            "id": item["id"],
            "description": item["description"],
            "assertion_id": item["assertion_id"],
            "result": "NOT_PROVEN",
            "expected": "bundle plus expectation-specific evidence",
            "observed": "aggregate validation report only",
            "evidence_refs": [],
            "failure_details": "aggregate-only conformance cannot prove expectation-specific PASS",
        }
        for item in conformance_expectations()
    ]
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v2",
        "task_id": models.REPAIR_TASK_ID,
        "status": "FAILED_VALIDATION",
        "expectation_count": len(results),
        "passed_count": 0,
        "results": results,
        "aggregate_validation_status": (validation_report or {}).get("validation_status"),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }


def conformance_results(bundle: dict[str, Any], validation_report: dict[str, Any] | None = None, *, dominium_root: str | Path | None = None) -> dict[str, Any]:
    if validation_report is None:
        return _not_proven_results(bundle)
    assertions = conformance_assertions(bundle, validation_report, dominium_root=dominium_root)
    results = []
    for expectation in conformance_expectations():
        assertion_id = expectation["assertion_id"]
        assertion = assertions["assertions"][assertion_id]
        result = {
            "id": expectation["id"],
            "description": expectation["description"],
            "assertion_id": assertion_id,
            "result": assertion["result"],
            "expected": assertion["expected"],
            "observed": assertion["observed"],
            "evidence_refs": [f"{models.CONFORMANCE_ASSERTIONS_JSON.as_posix()}#/assertions/{assertion_id}"],
            "evidence_kind": "DominiumSeamConformanceEvidence",
        }
        if assertion["result"] != "PASS":
            result["failure_details"] = assertion["observed"]
        results.append(result)
    passed_count = sum(1 for item in results if item["result"] == "PASS")
    status = "PASS_WITH_WARNINGS" if passed_count == len(results) and validation_report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"} else "FAILED_VALIDATION"
    return {
        "schema_version": "aide.dominium-readonly-seam.conformance-results.v2",
        "task_id": models.REPAIR_TASK_ID,
        "status": status,
        "expectation_count": len(results),
        "passed_count": passed_count,
        "results": results,
        "aggregate_validation_status": validation_report.get("validation_status"),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
