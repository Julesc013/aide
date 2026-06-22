"""Independent bounded check for Repair 05 of the Dominium read-only seam.

This script lives under the check task evidence directory on purpose. It does
not import production audit helpers for expected results. Production validation
and guard dispatch are invoked only as the system under test.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


SCRIPT = Path(__file__).resolve()
EVIDENCE_DIR = SCRIPT.parent
TASK_DIR = EVIDENCE_DIR.parent
ROOT = TASK_DIR.parent.parent.parent
REPORT_DIR = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-05-check"
DOMINIUM_ROOT = Path("C:/Projects/Dominium/dominium")
SCHEMA_PATH = ROOT / ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json"
BUNDLE_PATH = ROOT / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json"

PRODUCTION_SURFACES = [
    ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json",
    "core/interop/dominium",
    "core/protocol",
    ".aide/scripts/aide_lite.py",
    ".aide/scripts/tests",
    ".aide/fixtures/dominium-readonly-seam",
    ".aide/interop/dominium",
    ".aide/reports/dominium-readonly-seam-v0",
    ".aide/reports/dominium-readonly-seam-v0-repair-05",
]

SOURCE_FINDINGS = [
    "schema.open_object_surfaces_bounded",
    "extension.authority_names_semantically_refused",
    "conformance.guard_evidence_exercised",
    "operation.guard_report_not_static",
]

REQUIRED_GUARD_FAMILIES = [
    "filesystem_writes",
    "branch_worktree_ref_ops",
    "network_attempts",
    "provider_model_attempts",
    "worker_dispatch",
    "mutation_apply",
]

REQUIRED_PORTABLE_OUTPUTS = {
    ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json",
    ".aide/reports/dominium-readonly-seam-v0/source-snapshot.json",
    ".aide/reports/dominium-readonly-seam-v0/projection-index.json",
    ".aide/reports/dominium-readonly-seam-v0/validation.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-results.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json",
    ".aide/reports/dominium-readonly-seam-v0/compatibility.json",
    ".aide/reports/dominium-readonly-seam-v0/demo-result.json",
    ".aide/reports/dominium-readonly-seam-v0/fixture-manifest.json",
    ".aide/reports/dominium-readonly-seam-v0/operation-trace.json",
    ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json",
    ".aide/interop/dominium/conformance-evidence.json",
    ".aide/interop/dominium/runtime-dependency-manifest.json",
    ".aide/interop/dominium/seam-bundle.json",
    ".aide/interop/dominium/dominium-bridge-manifest.json",
    ".aide/interop/dominium/conformance-expectations.json",
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def stable_digest(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def production_tree_snapshot() -> dict[str, Any]:
    files: dict[str, str] = {}
    for rel in PRODUCTION_SURFACES:
        path = ROOT / rel
        if path.is_file():
            files[path.relative_to(ROOT).as_posix()] = file_sha256(path)
            continue
        if not path.exists():
            continue
        for child in sorted(item for item in path.rglob("*") if item.is_file()):
            if "__pycache__" in child.parts or child.suffix in {".pyc", ".pyo"}:
                continue
            if child.name.startswith("."):
                continue
            files[child.relative_to(ROOT).as_posix()] = file_sha256(child)
    return {
        "schema_version": "aide.dominium-readonly-seam.production-tree-snapshot.v0",
        "file_count": len(files),
        "files": files,
        "tree_digest": stable_digest(files),
    }


def run(cmd: list[str], *, timeout: int = 120) -> dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def assertion(
    assertions: list[dict[str, Any]],
    *,
    id: str,
    category: str,
    description: str,
    passed: bool,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    source_finding_id: str | None = None,
    severity: str = "material",
) -> None:
    assertions.append(
        {
            "id": id,
            "category": category,
            "description": description,
            "outcome": "PASS" if passed else "FAIL",
            "severity": "none" if passed else severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def json_pointer(parts: list[str]) -> str:
    if not parts:
        return "#"
    escaped = [part.replace("~", "~0").replace("/", "~1") for part in parts]
    return "#/" + "/".join(escaped)


def schema_surface_audit(schema: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    extension_ref_paths: list[str] = []

    def is_object_schema(node: dict[str, Any]) -> bool:
        return (
            node.get("type") == "object"
            or "properties" in node
            or "additionalProperties" in node
            or "patternProperties" in node
            or "propertyNames" in node
        )

    def typed_schema(value: Any) -> bool:
        return isinstance(value, dict) and bool(value) and value != {}

    def walk(node: Any, parts: list[str]) -> None:
        if isinstance(node, dict):
            properties = node.get("properties") if isinstance(node.get("properties"), dict) else {}
            for name, value in properties.items():
                if name == "extensions" and value == {"$ref": "#/$defs/ExtensionMap"}:
                    extension_ref_paths.append(json_pointer(parts + ["properties", name]))
            if is_object_schema(node):
                addl_marker = node.get("additionalProperties", "__OMITTED__")
                pattern_props = node.get("patternProperties") if isinstance(node.get("patternProperties"), dict) else {}
                if addl_marker is False:
                    classification = "closed canonical object"
                    reason = "additionalProperties is false"
                elif parts == ["$defs", "ExtensionMap"]:
                    classification = "explicit ExtensionMap"
                    reason = "documented ExtensionMap definition"
                elif typed_schema(addl_marker) or pattern_props:
                    pattern_values_typed = all(typed_schema(value) for value in pattern_props.values())
                    if typed_schema(addl_marker) or pattern_values_typed:
                        classification = "typed dynamic map"
                        reason = "dynamic keys have typed value schema"
                    else:
                        classification = "unclassified"
                        reason = "dynamic map has untyped pattern value"
                else:
                    classification = "unclassified"
                    reason = "object is neither closed nor explicitly typed"
                if addl_marker == "__OMITTED__":
                    addl_state = "omitted"
                elif addl_marker is True:
                    addl_state = "true"
                elif addl_marker is False:
                    addl_state = "false"
                elif addl_marker == {}:
                    addl_state = "empty_schema"
                else:
                    addl_state = "typed_schema"
                records.append(
                    {
                        "json_pointer": json_pointer(parts),
                        "classification": classification,
                        "additionalProperties": addl_state,
                        "property_count": len(properties),
                        "patternProperties": sorted(pattern_props),
                        "has_propertyNames": "propertyNames" in node,
                        "reason": reason,
                    }
                )
            for key, value in node.items():
                walk(value, parts + [str(key)])
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, parts + [str(index)])

    walk(schema, [])
    unclassified = [item for item in records if item["classification"] == "unclassified"]
    open_unintended = [
        item
        for item in records
        if item["additionalProperties"] in {"omitted", "true", "empty_schema"}
        and item["classification"] != "explicit ExtensionMap"
    ]
    return {
        "schema_version": "aide.dominium-readonly-seam.independent-schema-surface-audit.v0",
        "object_count": len(records),
        "objects": records,
        "unclassified_object_count": len(unclassified),
        "unintentionally_open_object_count": len(open_unintended),
        "extension_ref_paths": extension_ref_paths,
        "extension_ref_count": len(extension_ref_paths),
    }


def iter_records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    containers = bundle.get("records", {})
    if isinstance(containers, dict):
        for value in containers.values():
            if isinstance(value, list):
                records.extend(item for item in value if isinstance(item, dict))
            elif isinstance(value, dict):
                records.append(value)
    elif isinstance(containers, list):
        records.extend(item for item in containers if isinstance(item, dict))
    return records


def first_record(bundle: dict[str, Any], kind: str) -> dict[str, Any]:
    for record in iter_records(bundle):
        if record.get("kind") == kind:
            return record
    raise AssertionError(f"missing record kind: {kind}")


def validate_bundle_subprocess(bundle: dict[str, Any]) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(bundle, handle)
        temp_path = Path(handle.name)
    try:
        code = (
            "import json,sys;"
            "from core.interop.dominium.validation import validate_bundle;"
            "bundle=json.load(open(sys.argv[1],encoding='utf-8'));"
            "print(json.dumps(validate_bundle(bundle),sort_keys=True))"
        )
        result = run(["py", "-3", "-c", code, str(temp_path)], timeout=180)
        if result["returncode"] != 0:
            return {"subprocess_failed": True, "result": result}
        return json.loads(result["stdout"])
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def insert_extension(bundle: dict[str, Any], location: str, key: str, value: Any) -> None:
    if location == "bundle_metadata":
        bundle.setdefault("metadata", {}).setdefault("extensions", {})[key] = value
        return
    if location == "bundle_root":
        bundle.setdefault("extensions", {})[key] = value
        return
    if location == "record_metadata":
        first_record(bundle, "HostManifest").setdefault("metadata", {}).setdefault("extensions", {})[key] = value
        return
    if location == "record_spec":
        first_record(bundle, "HostManifest").setdefault("spec", {}).setdefault("extensions", {})[key] = value
        return
    if location == "nested_extension":
        bundle.setdefault("metadata", {}).setdefault("extensions", {}).setdefault("vendor.note", {}).setdefault("extensions", {})[key] = value
        return
    raise AssertionError(f"unknown extension location: {location}")


def extension_matrix(base_bundle: dict[str, Any]) -> dict[str, Any]:
    denied_keys = [
        "authoritative",
        "canonicalAuthority",
        "workbench.is-authority",
        "runtime.enabled",
        "hostRuntimeStarted",
        "bridge/runtime/started",
        "network_allowed",
        "provider.enabled",
        "modelEnabled",
        "worker-enabled",
        "mutation.apply.allowed",
        "patchApplyEnabled",
        "releaseAllowed",
        "promotion_allowed",
        "private_tool_bypass",
        "\uff54\uff52\uff55\uff53\uff54\uff45\uff44",
    ]
    benign_keys = ["vendor.color", "documentation.note", "ui.group", "source.annotation"]
    locations = ["bundle_metadata", "bundle_root", "record_metadata", "record_spec", "nested_extension"]
    denied_results: list[dict[str, Any]] = []
    benign_results: list[dict[str, Any]] = []
    for location in locations:
        for key in denied_keys:
            candidate = deepcopy(base_bundle)
            insert_extension(candidate, location, key, True)
            result = validate_bundle_subprocess(candidate)
            records = result.get("error_records", []) if isinstance(result, dict) else []
            authority_records = [item for item in records if item.get("code") == "extension.authority_change"]
            denied_results.append(
                {
                    "location": location,
                    "key": key,
                    "status": result.get("status"),
                    "authority_error_count": len(authority_records),
                    "first_error": authority_records[0] if authority_records else None,
                    "passed": len(authority_records) > 0,
                }
            )
        for key in benign_keys:
            candidate = deepcopy(base_bundle)
            insert_extension(candidate, location, key, {"note": "benign"})
            result = validate_bundle_subprocess(candidate)
            records = result.get("error_records", []) if isinstance(result, dict) else []
            authority_records = [item for item in records if item.get("code") == "extension.authority_change"]
            benign_results.append(
                {
                    "location": location,
                    "key": key,
                    "status": result.get("status"),
                    "authority_error_count": len(authority_records),
                    "passed": len(authority_records) == 0,
                }
            )
    return {
        "schema_version": "aide.dominium-readonly-seam.independent-extension-matrix.v0",
        "denied_results": denied_results,
        "benign_results": benign_results,
        "denied_passed": all(item["passed"] for item in denied_results),
        "benign_passed": all(item["passed"] for item in benign_results),
        "denied_count": len(denied_results),
        "benign_count": len(benign_results),
    }


def direct_guard_matrix() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    from core.interop.dominium.operations import GuardRequest, dispatch_guarded_request  # noqa: PLC0415

    probes: list[dict[str, Any]] = []
    nonce = "phaseb-direct-nonce"
    for family in REQUIRED_GUARD_FAMILIES:
        called = {"value": False}

        def sentinel() -> object:
            called["value"] = True
            raise AssertionError(f"forbidden executor invoked for {family}")

        target = f".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05/evidence/{family}-{nonce}.target"
        if family != "filesystem_writes":
            target = f"Dominium/{family}/{nonce}"
        request = GuardRequest(
            request_id=f"phaseb-{family}-{nonce}",
            family=family,
            operation=f"phaseb guarded {family} {nonce}",
            target=target,
            source="phase_b_independent_check",
            requested_effect="forbidden side effect",
            metadata={"nonce": nonce},
        )
        decision = dispatch_guarded_request(request, sentinel)
        probes.append(
            {
                "family": family,
                "request_id": decision.get("request_id"),
                "nonce_present": nonce in json.dumps(decision, sort_keys=True),
                "guard_reached": decision.get("guard_reached"),
                "executor_called_by_sentinel": called["value"],
                "executor_invoked": decision.get("executor_invoked"),
                "execution_prevented": decision.get("execution_prevented"),
                "state_unchanged": decision.get("state_unchanged"),
                "reason_code": decision.get("reason_code"),
                "result": decision.get("result"),
                "evidence_refs": decision.get("evidence_refs"),
                "passed": (
                    decision.get("guard_reached") is True
                    and called["value"] is False
                    and decision.get("executor_invoked") is False
                    and decision.get("execution_prevented") is True
                    and decision.get("state_unchanged") is True
                    and decision.get("result") == "PASS"
                    and nonce in json.dumps(decision, sort_keys=True)
                ),
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.independent-guard-matrix.v0",
        "nonce": nonce,
        "probes": probes,
        "probe_count": len(probes),
        "passed_count": sum(1 for item in probes if item["passed"]),
        "failed_count": sum(1 for item in probes if not item["passed"]),
        "passed": all(item["passed"] for item in probes),
    }


def guard_report_matrix() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    from core.interop.dominium.operations import guard_conformance  # noqa: PLC0415

    report_a = guard_conformance(nonce="phaseb-report-a")
    report_b = guard_conformance(nonce="phaseb-report-b")

    def recompute_digest(report: dict[str, Any]) -> str:
        clone = dict(report)
        clone.pop("report_digest", None)
        return stable_digest(clone)

    checks = {
        "report_a_digest_recomputes": recompute_digest(report_a) == report_a.get("report_digest"),
        "report_b_digest_recomputes": recompute_digest(report_b) == report_b.get("report_digest"),
        "report_digest_changes_with_nonce": report_a.get("report_digest") != report_b.get("report_digest"),
        "report_a_contains_nonce": "phaseb-report-a" in json.dumps(report_a, sort_keys=True),
        "report_b_contains_nonce": "phaseb-report-b" in json.dumps(report_b, sort_keys=True),
        "static_report_a_cannot_satisfy_nonce_b": "phaseb-report-b" not in json.dumps(report_a, sort_keys=True),
        "counts_reconcile": (
            report_a.get("probe_count") == len(report_a.get("probes", []))
            and report_a.get("passed_count") + report_a.get("failed_count") == report_a.get("probe_count")
            and report_a.get("unique_request_count") == len({item.get("request_id") for item in report_a.get("probes", [])})
        ),
        "all_probe_fields_pass": all(
            item.get("guard_reached") is True
            and item.get("executor_injected") is True
            and item.get("executor_invoked") is False
            and item.get("execution_prevented") is True
            and item.get("state_unchanged") is True
            and item.get("result") == "PASS"
            for item in report_a.get("probes", [])
        ),
    }
    return {
        "schema_version": "aide.dominium-readonly-seam.independent-guard-report-matrix.v0",
        "checks": checks,
        "report_a_summary": {
            "probe_count": report_a.get("probe_count"),
            "passed_count": report_a.get("passed_count"),
            "failed_count": report_a.get("failed_count"),
            "report_digest": report_a.get("report_digest"),
        },
        "report_b_summary": {
            "probe_count": report_b.get("probe_count"),
            "passed_count": report_b.get("passed_count"),
            "failed_count": report_b.get("failed_count"),
            "report_digest": report_b.get("report_digest"),
        },
        "passed": all(checks.values()),
    }


def schema_discrimination_sample(base_bundle: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    seam_record = schema["$defs"]["SeamRecord"]
    one_of_count = len(seam_record.get("oneOf", []))
    expected_kinds = {
        "HostManifest",
        "HostCapabilitySet",
        "WorkspaceDescriptor",
        "ContextDescriptor",
        "ArtifactReference",
        "DiagnosticProjection",
        "RefusalProjection",
        "EvidenceReferenceSet",
        "EventEnvelope",
        "DominiumBridgeManifest",
    }
    bundle_kinds = {str(record.get("kind")) for record in iter_records(base_bundle)}
    pairs = [
        ("HostManifest", "ContextDescriptor"),
        ("ContextDescriptor", "HostManifest"),
        ("ArtifactReference", "DiagnosticProjection"),
        ("DiagnosticProjection", "RefusalProjection"),
        ("EventEnvelope", "ArtifactReference"),
        ("DominiumBridgeManifest", "HostCapabilitySet"),
    ]
    substitutions: list[dict[str, Any]] = []
    for target_kind, donor_kind in pairs:
        candidate = deepcopy(base_bundle)
        target = first_record(candidate, target_kind)
        donor = first_record(base_bundle, donor_kind)
        target["spec"] = deepcopy(donor.get("spec"))
        result = validate_bundle_subprocess(candidate)
        substitutions.append(
            {
                "target_kind": target_kind,
                "donor_kind": donor_kind,
                "status": result.get("status"),
                "error_codes": sorted({item.get("code") for item in result.get("error_records", []) if isinstance(item, dict)}),
                "passed": result.get("validated") is not True,
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.schema-discrimination-sample.v0",
        "seam_record_oneOf_count": one_of_count,
        "expected_kind_count": len(expected_kinds),
        "bundle_kinds": sorted(bundle_kinds),
        "all_expected_kinds_present": expected_kinds <= bundle_kinds,
        "substitutions": substitutions,
        "passed": one_of_count == 10 and expected_kinds <= bundle_kinds and all(item["passed"] for item in substitutions),
    }


def fixture_strictness_sample() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    from core.interop.dominium.fixture_replay import FixtureReplayError, apply_operations  # noqa: PLC0415

    base = {"items": ["a", "b"], "obj": {"a": 1}, "arr": [1]}
    negative_ops = {
        "missing_add_value": [{"op": "add", "path": "/obj/b"}],
        "unicode_index": [{"op": "replace", "path": "/items/\u0661", "value": "x"}],
        "ambiguous_index": [{"op": "replace", "path": "/items/01", "value": "x"}],
        "forbidden_key": [{"op": "replace", "path": "/obj/a", "value": 2, "command": "x"}],
        "root_mutation": [{"op": "replace", "path": "", "value": {}}],
        "append_non_array": [{"op": "append", "path": "/obj/a", "value": 2}],
    }
    results: list[dict[str, Any]] = []
    for name, ops in negative_ops.items():
        try:
            apply_operations(base, ops)
        except FixtureReplayError as exc:
            results.append({"name": name, "passed": True, "error": str(exc)})
        else:
            results.append({"name": name, "passed": False, "error": None})
    explicit_null = apply_operations(base, [{"op": "replace", "path": "/obj/a", "value": None}])
    return {
        "schema_version": "aide.dominium-readonly-seam.fixture-strictness-sample.v0",
        "negative_results": results,
        "explicit_null_value_preserved": explicit_null["obj"]["a"] is None,
        "passed": all(item["passed"] for item in results) and explicit_null["obj"]["a"] is None,
    }


def unsupported_cli_sample() -> dict[str, Any]:
    verbs = ["phaseb-unknown-operation", "future-operation", "xyzzy"]
    results: list[dict[str, Any]] = []
    for verb in verbs:
        proc = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", verb], timeout=120)
        text = proc["stdout"] + proc["stderr"]
        results.append(
            {
                "verb": verb,
                "returncode": proc["returncode"],
                "has_refused": "result: REFUSED" in text,
                "has_reason": "reason_code: AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in text,
                "has_operation": f"operation: {verb}" in text,
                "passed": (
                    proc["returncode"] == 2
                    and "result: REFUSED" in text
                    and "reason_code: AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in text
                    and f"operation: {verb}" in text
                ),
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.unsupported-cli-sample.v0",
        "results": results,
        "passed": all(item["passed"] for item in results),
    }


def no_write_sample() -> dict[str, Any]:
    evidence = json.loads((ROOT / ".aide/interop/dominium/conformance-evidence.json").read_text(encoding="utf-8"))
    state = evidence.get("dominium_before_after_state", {})
    actual_operations = state.get("actual_operations", [])
    dominium_status = run(["git", "-C", str(DOMINIUM_ROOT), "status", "--short", "--branch"], timeout=120)
    return {
        "schema_version": "aide.dominium-readonly-seam.no-write-sample.v0",
        "before": state.get("before"),
        "after": state.get("after"),
        "status": state.get("status"),
        "actual_operation_count": len(actual_operations) if isinstance(actual_operations, list) else 0,
        "dominium_status": dominium_status["stdout"].strip(),
        "passed": (
            state.get("status") == "PASS"
            and state.get("before") == state.get("after")
            and isinstance(actual_operations, list)
            and len(actual_operations) >= 3
            and dominium_status["returncode"] == 0
            and not any(line and not line.startswith("##") for line in dominium_status["stdout"].splitlines())
        ),
    }


def operation_trace_sample() -> dict[str, Any]:
    trace = json.loads((ROOT / ".aide/reports/dominium-readonly-seam-v0/operation-trace.json").read_text(encoding="utf-8"))
    demo = json.loads((ROOT / ".aide/reports/dominium-readonly-seam-v0/demo-result.json").read_text(encoding="utf-8"))
    observations = trace.get("observations", [])
    sequence = [item.get("sequence") for item in observations]
    raw_digest = stable_digest(observations)
    aggregate: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in observations:
        key = (
            item.get("family"),
            item.get("operation"),
            item.get("target"),
            item.get("classification"),
            item.get("allowed"),
            item.get("source"),
            item.get("observation_method"),
        )
        aggregate.setdefault(key, {"count": 0, "return_codes": set()})
        aggregate[key]["count"] += 1
        aggregate[key]["return_codes"].add(item.get("return_code"))
    operation_count = len(aggregate)
    allowed_count = sum(1 for item in observations if item.get("allowed") is True)
    forbidden_count = sum(1 for item in observations if item.get("allowed") is not True)
    operation_report = demo.get("operation_report") or demo.get("operation_ledger") or demo
    return {
        "schema_version": "aide.dominium-readonly-seam.operation-trace-sample.v0",
        "raw_observation_count": len(observations),
        "sequence_contiguous": sequence == list(range(1, len(observations) + 1)),
        "raw_digest": raw_digest,
        "recorded_raw_digest": trace.get("raw_trace_sha256"),
        "operation_count": operation_count,
        "recorded_operation_count": operation_report.get("operation_count"),
        "allowed_count": allowed_count,
        "recorded_allowed_count": operation_report.get("allowed_operation_count"),
        "forbidden_count": forbidden_count,
        "recorded_forbidden_count": operation_report.get("forbidden_operation_count"),
        "passed": (
            sequence == list(range(1, len(observations) + 1))
            and raw_digest == trace.get("raw_trace_sha256") == operation_report.get("raw_trace_sha256")
            and operation_count == operation_report.get("operation_count")
            and allowed_count == operation_report.get("allowed_operation_count")
            and forbidden_count == operation_report.get("forbidden_operation_count")
        ),
    }


def portability_sample() -> dict[str, Any]:
    portability = json.loads((ROOT / ".aide/reports/dominium-readonly-seam-v0/portability-result.json").read_text(encoding="utf-8"))
    output_sets = portability.get("required_output_sets", [])
    set_results = []
    for index, item in enumerate(output_sets):
        outputs = set(item if isinstance(item, list) else item.get("relative_paths", []))
        set_results.append(
            {
                "root": index,
                "output_count": len(outputs),
                "missing": sorted(REQUIRED_PORTABLE_OUTPUTS - outputs),
                "extra_required_check": sorted(outputs - REQUIRED_PORTABLE_OUTPUTS)[:25],
                "passed": REQUIRED_PORTABLE_OUTPUTS <= outputs,
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.portability-sample.v0",
        "status": portability.get("status"),
        "required_output_set_equal": portability.get("required_output_set_equal"),
        "output_hashes_equal": portability.get("output_hashes_equal"),
        "absolute_path_leak_count": portability.get("absolute_path_leak_count"),
        "undeclared_dependency_count": portability.get("undeclared_dependency_count"),
        "set_results": set_results,
        "passed": (
            portability.get("status") in {"PASS", "PASS_WITH_WARNINGS"}
            and portability.get("required_output_set_equal") is True
            and portability.get("output_hashes_equal") is True
            and portability.get("absolute_path_leak_count") == 0
            and portability.get("undeclared_dependency_count") == 0
            and bool(set_results)
            and all(item["passed"] for item in set_results)
        ),
    }


def run_check() -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    assertions: list[dict[str, Any]] = []
    before = production_tree_snapshot()
    write_json(EVIDENCE_DIR / "production-tree-before.json", before)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    base_bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))

    schema_audit = schema_surface_audit(schema)
    write_json(EVIDENCE_DIR / "schema-surface-independent-audit.json", schema_audit)
    assertion(
        assertions,
        id="phaseb.schema.open_object_surfaces_bounded",
        category="schema",
        description="Every public schema object is closed, typed dynamic, or an explicit ExtensionMap.",
        passed=schema_audit["unclassified_object_count"] == 0 and schema_audit["unintentionally_open_object_count"] == 0,
        expected={"unclassified_object_count": 0, "unintentionally_open_object_count": 0},
        observed={
            "unclassified_object_count": schema_audit["unclassified_object_count"],
            "unintentionally_open_object_count": schema_audit["unintentionally_open_object_count"],
            "extension_ref_count": schema_audit["extension_ref_count"],
        },
        evidence_refs=["evidence/schema-surface-independent-audit.json"],
        source_finding_id="schema.open_object_surfaces_bounded",
    )

    extension_results = extension_matrix(base_bundle)
    write_json(EVIDENCE_DIR / "extension-authority-independent-matrix.json", extension_results)
    assertion(
        assertions,
        id="phaseb.extension.authority_names_semantically_refused",
        category="extension",
        description="Denied authority-changing extension key variants fail with extension.authority_change while benign keys pass.",
        passed=extension_results["denied_passed"] and extension_results["benign_passed"],
        expected={"denied_passed": True, "benign_passed": True},
        observed={
            "denied_passed": extension_results["denied_passed"],
            "benign_passed": extension_results["benign_passed"],
            "denied_count": extension_results["denied_count"],
            "benign_count": extension_results["benign_count"],
        },
        evidence_refs=["evidence/extension-authority-independent-matrix.json"],
        source_finding_id="extension.authority_names_semantically_refused",
    )

    guard_results = direct_guard_matrix()
    write_json(EVIDENCE_DIR / "guard-dispatch-independent-matrix.json", guard_results)
    assertion(
        assertions,
        id="phaseb.conformance.guard_evidence_exercised",
        category="guard",
        description="Actual guard dispatcher reaches every forbidden guard family without invoking sentinel executors.",
        passed=guard_results["passed"],
        expected={"failed_count": 0, "probe_count": len(REQUIRED_GUARD_FAMILIES)},
        observed={"failed_count": guard_results["failed_count"], "probe_count": guard_results["probe_count"]},
        evidence_refs=["evidence/guard-dispatch-independent-matrix.json"],
        source_finding_id="conformance.guard_evidence_exercised",
    )

    guard_report_results = guard_report_matrix()
    write_json(EVIDENCE_DIR / "guard-report-independent-matrix.json", guard_report_results)
    assertion(
        assertions,
        id="phaseb.operation.guard_report_not_static",
        category="guard_report",
        description="Guard conformance report counts and digest recompute and change with nonce-bearing probes.",
        passed=guard_report_results["passed"],
        expected="digest recomputes and changes with nonce",
        observed=guard_report_results["checks"],
        evidence_refs=["evidence/guard-report-independent-matrix.json"],
        source_finding_id="operation.guard_report_not_static",
    )

    regression = {
        "schema_discrimination": schema_discrimination_sample(base_bundle),
        "fixture_strictness": fixture_strictness_sample(),
        "unsupported_cli": unsupported_cli_sample(),
        "no_write": no_write_sample(),
        "operation_trace": operation_trace_sample(),
        "portability": portability_sample(),
    }
    write_json(EVIDENCE_DIR / "regression-sampling.json", regression)
    for name, result in regression.items():
        assertion(
            assertions,
            id=f"phaseb.regression.{name}",
            category="regression",
            description=f"Critical prior invariant sample: {name}.",
            passed=result.get("passed") is True,
            expected=True,
            observed=result,
            evidence_refs=["evidence/regression-sampling.json"],
            source_finding_id=None,
        )

    after = production_tree_snapshot()
    write_json(EVIDENCE_DIR / "production-tree-after.json", after)
    production_unchanged = before["tree_digest"] == after["tree_digest"] and before["files"] == after["files"]
    assertion(
        assertions,
        id="phaseb.production_tree_unchanged",
        category="immutability",
        description="Production seam surfaces are byte-identical before and after the check.",
        passed=production_unchanged,
        expected=before["tree_digest"],
        observed=after["tree_digest"],
        evidence_refs=["evidence/production-tree-before.json", "evidence/production-tree-after.json"],
        source_finding_id=None,
    )

    material_failures = [
        item
        for item in assertions
        if item["outcome"] != "PASS" and item.get("severity") == "material"
    ]
    four_dispositions = []
    for finding_id in SOURCE_FINDINGS:
        matching = [item for item in assertions if item.get("source_finding_id") == finding_id]
        closed = matching and all(item["outcome"] == "PASS" for item in matching)
        four_dispositions.append(
            {
                "finding_id": finding_id,
                "original_observed_defect": {
                    "schema.open_object_surfaces_bounded": "Repair 04 check found unbounded/open public schema object surfaces.",
                    "extension.authority_names_semantically_refused": "Repair 04 check found authority-changing extension name variants not semantically refused.",
                    "conformance.guard_evidence_exercised": "Repair 04 check found guard evidence was not proven by exercised guard paths.",
                    "operation.guard_report_not_static": "Repair 04 check found guard report could be static rather than derived from runtime probes.",
                }[finding_id],
                "repair_05_change": {
                    "schema.open_object_surfaces_bounded": "Repair 05 tightened schema object surfaces and added schema surface audit evidence.",
                    "extension.authority_names_semantically_refused": "Repair 05 added deterministic extension key normalization and recursive semantic refusal.",
                    "conformance.guard_evidence_exercised": "Repair 05 added a guard dispatcher with sentinel executors and state digests.",
                    "operation.guard_report_not_static": "Repair 05 generated guard conformance reports from nonce-bearing dispatcher probes with recomputed digest.",
                }[finding_id],
                "independent_test": [item["id"] for item in matching],
                "expected": "all matching assertions PASS",
                "observed": [item["outcome"] for item in matching],
                "evidence_refs": sorted({ref for item in matching for ref in item.get("evidence_refs", [])}),
                "disposition": "CLOSED" if closed else "OPEN",
            }
        )

    warnings = [
        "offline/read-only seam",
        "local Dominium behind remote",
        "non-Windows platforms not separately executed",
        "minimum Python 3.11 not separately executed",
        "external Draft 2020-12 validator unavailable",
    ]
    result = "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES"
    recommended = (
        "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"
        if not material_failures
        else "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-06"
    )
    output = {
        "schema_version": "aide.dominium-readonly-seam.repair-05-check.v0",
        "task_id": "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05",
        "source_task": "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05",
        "source_commit": "05cb2b82980d1dbb9fb18524f0ba191a460b7962",
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended,
        "assertions": assertions,
        "four_finding_dispositions": four_dispositions,
        "warnings": warnings,
        "production_tree_unchanged": production_unchanged,
        "production_before_digest": before["tree_digest"],
        "production_after_digest": after["tree_digest"],
    }
    write_json(EVIDENCE_DIR / "independent-check-results.json", output)
    write_json(REPORT_DIR / "check-report.json", output)
    write_json(REPORT_DIR / "four-finding-closure.json", four_dispositions)
    return output


if __name__ == "__main__":
    result = run_check()
    print(json.dumps({
        "result": result["result"],
        "material_finding_count": result["material_finding_count"],
        "recommended_next_task": result["recommended_next_task"],
    }, sort_keys=True))
    raise SystemExit(0 if result["result"] == "PASS_WITH_WARNINGS" else 1)
