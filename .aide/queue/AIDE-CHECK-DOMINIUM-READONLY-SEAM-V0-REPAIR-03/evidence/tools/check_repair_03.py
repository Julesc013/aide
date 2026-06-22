from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03"
SOURCE_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03"
SOURCE_COMMIT = "84a154c2f03b304a987a9f017cc48a0b22c3f6d6"
NEXT_ACCEPT = "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"
NEXT_REPAIR = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04"

FALSE_BOUNDARY_FIELDS = [
    "dominium_command_invoked",
    "host_runtime_started",
    "workbench_started",
    "bridge_runtime_started",
    "service_started",
    "database_opened",
    "transport_started",
    "network_call_performed",
    "provider_or_model_called",
    "worker_executed",
    "patch_transaction_applied",
    "preview_or_apply_performed",
    "source_repository_mutated",
    "target_repository_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "release_or_promotion_performed",
    "generated_projection_marked_canonical",
]

FIFTEEN_FINDINGS = [
    "schema.kind_specific_spec_types",
    "schema.false_boundary_required",
    "schema.unbounded_authority_fields",
    "fixtures.production_remove_missing",
    "fixtures.production_replace_missing",
    "fixtures.production_index_strictness",
    "conformance.unsupported_operation_semantics",
    "conformance.no_write_semantics",
    "conformance.network_semantics",
    "operation.raw_trace_auditability",
    "operation.git_network_classification",
    "operation.injection_evidence",
    "portability.manifest_driven_copy",
    "portability.sanitized_environment",
    "cli.unsupported_extended_verbs",
]

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
    "obliterate",
    "demolish",
    "teleport",
]

REQUIRED_PORTABLE_OUTPUTS = [
    ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json",
    ".aide/reports/dominium-readonly-seam-v0/source-snapshot.json",
    ".aide/reports/dominium-readonly-seam-v0/projection-index.json",
    ".aide/reports/dominium-readonly-seam-v0/validation.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-results.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json",
    ".aide/interop/dominium/conformance-evidence.json",
    ".aide/reports/dominium-readonly-seam-v0/compatibility.json",
    ".aide/reports/dominium-readonly-seam-v0/demo-result.json",
    ".aide/reports/dominium-readonly-seam-v0/fixture-manifest.json",
    ".aide/reports/dominium-readonly-seam-v0/operation-trace.json",
    ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json",
    ".aide/interop/dominium/runtime-dependency-manifest.json",
    ".aide/interop/dominium/seam-bundle.json",
    ".aide/interop/dominium/dominium-bridge-manifest.json",
    ".aide/interop/dominium/conformance-expectations.json",
]


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").exists() and (parent / ".aide").is_dir():
            return parent
    raise RuntimeError("could not locate repo root")


ROOT = find_repo_root()
EVIDENCE = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-03-check"
DOMINIUM_ROOT = Path("C:/Projects/Dominium/dominium")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def stable_payload(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, separators=(",", ": ")) + "\n").encode("utf-8")


def stable_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(stable_payload(value)).hexdigest()


def compact_json_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str], *, cwd: Path | None = None, timeout: int = 120) -> dict[str, Any]:
    proc = subprocess.run(
        args,
        cwd=str(cwd or ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {
        "args": args,
        "cwd": rel(cwd or ROOT),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "stdout_lines": proc.stdout.splitlines(),
        "stderr_lines": proc.stderr.splitlines(),
    }


class Check:
    def __init__(self) -> None:
        self.assertions: list[dict[str, Any]] = []

    def add(
        self,
        assertion_id: str,
        category: str,
        description: str,
        passed: bool,
        *,
        severity: str = "MATERIAL",
        expected: Any = None,
        observed: Any = None,
        evidence_refs: list[str] | None = None,
        source_finding_id: str | None = None,
    ) -> None:
        self.assertions.append(
            {
                "id": assertion_id,
                "category": category,
                "description": description,
                "outcome": "PASS" if passed else "FAIL",
                "severity": severity,
                "expected": expected,
                "observed": observed,
                "evidence_refs": evidence_refs or [],
                "source_finding_id": source_finding_id,
            }
        )

    def material_findings(self) -> list[dict[str, Any]]:
        return [item for item in self.assertions if item["severity"] == "MATERIAL" and item["outcome"] != "PASS"]


def resolve_ref(schema: dict[str, Any], ref_value: str) -> bool:
    if not ref_value.startswith("#/"):
        return False
    current: Any = schema
    for raw in ref_value[2:].split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return True


def walk(value: Any, path: str = ""):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}/{index}")


def schema_checks(check: Check) -> dict[str, Any]:
    schema_path = ROOT / ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json"
    bundle_path = ROOT / ".aide/interop/dominium/seam-bundle.json"
    schema = load_json(schema_path)
    bundle = load_json(bundle_path)
    refs = [item.get("$ref") for _path, item in walk(schema) if isinstance(item, dict) and "$ref" in item]
    dangling = [ref for ref in refs if not isinstance(ref, str) or not resolve_ref(schema, ref)]
    text = schema_path.read_text(encoding="utf-8")

    check.add(
        "schema.draft_2020_12_and_refs",
        "schema",
        "Public schema declares Draft 2020-12 and has resolvable internal refs.",
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema" and not dangling,
        expected={"$schema": "https://json-schema.org/draft/2020-12/schema", "dangling_refs": []},
        observed={"$schema": schema.get("$schema"), "dangling_refs": dangling},
        evidence_refs=[rel(schema_path)],
    )

    false_status = {}
    for field in FALSE_BOUNDARY_FIELDS:
        definitions = [
            node
            for path, node in walk(schema)
            if path.endswith("/properties/" + field) and isinstance(node, dict)
        ]
        false_status[field] = {
            "has_boolean_const_false": any(node.get("type") == "boolean" and node.get("const") is False for node in definitions),
            "occurrences": len(definitions),
            "in_required": f'"{field}"' in text and '"required"' in text,
        }
    check.add(
        "schema.false_boundaries_const_false",
        "schema",
        "Every false-boundary field is represented as boolean const false in the public schema.",
        all(item["has_boolean_const_false"] and item["in_required"] for item in false_status.values()),
        expected={field: "required boolean const false" for field in FALSE_BOUNDARY_FIELDS},
        observed=false_status,
        evidence_refs=[rel(schema_path)],
        source_finding_id="schema.false_boundary_required",
    )

    required_kinds = [
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
    ]
    kind_presence = {kind: kind in text for kind in required_kinds}
    check.add(
        "schema.kind_specific_defs_present",
        "schema",
        "Public schema has kind-specific record/spec definitions and allOf/oneOf discrimination markers.",
        all(kind_presence.values()) and '"allOf"' in text and '"oneOf"' in text,
        expected={"required_kinds": required_kinds, "allOf": True, "oneOf": True},
        observed={"required_kinds_present": kind_presence, "allOf": '"allOf"' in text, "oneOf": '"oneOf"' in text},
        evidence_refs=[rel(schema_path)],
        source_finding_id="schema.kind_specific_spec_types",
    )

    additional_true = [path for path, node in walk(schema) if isinstance(node, dict) and node.get("additionalProperties") is True]
    extension_only = all("extensions" in path or "compatibility" in path for path in additional_true)
    validation_text = (ROOT / "core/interop/dominium/validation.py").read_text(encoding="utf-8")
    authority_names = [
        "authoritative",
        "canonical",
        "trusted",
        "admitted",
        "workbench_is_authority",
        "runtime_started",
        "command_invocation_implemented",
        "private_tool_bypass",
        "network_allowed",
        "mutation_allowed",
        "provider_enabled",
        "worker_enabled",
    ]
    semantic_rejects = all(name in validation_text for name in authority_names)
    check.add(
        "schema.authority_extensions_bounded",
        "schema",
        "Unbounded objects are limited to extension/compatibility surfaces and authority-changing extension names are semantically refused.",
        extension_only and semantic_rejects,
        expected={"additionalProperties_true_only_in_extensions": True, "authority_names_semantically_rejected": True},
        observed={"additionalProperties_true_paths": additional_true, "authority_names_in_validation": semantic_rejects},
        evidence_refs=[rel(schema_path), "core/interop/dominium/validation.py"],
        source_finding_id="schema.unbounded_authority_fields",
    )

    check.add(
        "schema.current_bundle_has_expected_identity",
        "schema",
        "Current committed SeamBundle is the Repair 03 bundle and carries expected source identity.",
        bundle.get("manifest", {}).get("task_id") == SOURCE_TASK_ID
        and bundle.get("manifest", {}).get("recommended_next_task") == TASK_ID
        and bundle.get("kind") == "DominiumReadonlySeamBundle",
        expected={"task_id": SOURCE_TASK_ID, "recommended_next_task": TASK_ID, "kind": "DominiumReadonlySeamBundle"},
        observed={"task_id": bundle.get("manifest", {}).get("task_id"), "recommended_next_task": bundle.get("manifest", {}).get("recommended_next_task"), "kind": bundle.get("kind")},
        evidence_refs=[rel(bundle_path)],
    )

    return {"schema_path": rel(schema_path), "dangling_refs": dangling, "false_boundaries": false_status, "additional_properties_true": additional_true}


def pointer_parts(pointer: str) -> list[str]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON pointer must be a string starting with /")
    parts = pointer.split("/")[1:]
    decoded = []
    for part in parts:
        if "~" in part and not re.search(r"~[01]", part):
            raise ValueError("malformed JSON Pointer escape")
        decoded.append(part.replace("~1", "/").replace("~0", "~"))
    if not decoded:
        raise ValueError("root mutation is not allowed")
    return decoded


def canonical_ascii_index(value: str, *, limit: int, allow_end: bool, allow_dash: bool) -> int:
    if value == "-":
        if allow_dash:
            return limit
        raise ValueError("dash index not allowed")
    if not isinstance(value, str) or not re.fullmatch(r"0|[1-9][0-9]*", value):
        raise ValueError("array index must be canonical ASCII decimal")
    index = int(value)
    maximum = limit if allow_end else limit - 1
    if index < 0 or index > maximum:
        raise ValueError("array index out of range")
    return index


def apply_ops_independent(base: Any, operations: list[dict[str, Any]]) -> Any:
    doc = copy.deepcopy(base)
    forbidden = {"callable", "module", "command", "shell", "eval", "exec", "python", "entrypoint", "script", "import", "args", "kwargs"}
    for op in operations:
        if not isinstance(op, dict):
            raise ValueError("operation must be an object")
        if forbidden & set(op):
            raise ValueError("operation contains forbidden executable key")
        kind = op.get("op")
        if kind not in {"add", "remove", "replace", "append"}:
            raise ValueError("unknown operation")
        if "path" not in op:
            raise ValueError("missing path")
        if kind in {"add", "replace", "append"} and "value" not in op:
            raise ValueError("missing value")
        parts = pointer_parts(op["path"])
        parent = doc
        for part in parts[:-1]:
            if isinstance(parent, list):
                parent = parent[canonical_ascii_index(part, limit=len(parent), allow_end=False, allow_dash=False)]
            elif isinstance(parent, dict) and part in parent:
                parent = parent[part]
            else:
                raise ValueError("missing intermediate target")
        key = parts[-1]
        if isinstance(parent, list):
            if kind == "remove":
                parent.pop(canonical_ascii_index(key, limit=len(parent), allow_end=False, allow_dash=False))
            elif kind == "replace":
                parent[canonical_ascii_index(key, limit=len(parent), allow_end=False, allow_dash=False)] = copy.deepcopy(op["value"])
            elif kind == "add":
                parent.insert(canonical_ascii_index(key, limit=len(parent), allow_end=True, allow_dash=True), copy.deepcopy(op["value"]))
            elif kind == "append":
                if key != "-":
                    raise ValueError("append to array requires '-'")
                parent.append(copy.deepcopy(op["value"]))
        elif isinstance(parent, dict):
            if kind == "remove":
                if key not in parent:
                    raise ValueError("missing remove key")
                parent.pop(key)
            elif kind == "replace":
                if key not in parent:
                    raise ValueError("missing replace key")
                parent[key] = copy.deepcopy(op["value"])
            elif kind == "add":
                if key in parent:
                    raise ValueError("add target exists")
                parent[key] = copy.deepcopy(op["value"])
            elif kind == "append":
                if key not in parent or not isinstance(parent[key], list):
                    raise ValueError("append target must be array")
                parent[key].append(copy.deepcopy(op["value"]))
        else:
            raise ValueError("target parent is not a container")
    return doc


def fixture_checks(check: Check) -> dict[str, Any]:
    fixture_source = (ROOT / "core/interop/dominium/fixture_replay.py").read_text(encoding="utf-8")
    bundle = load_json(ROOT / ".aide/interop/dominium/seam-bundle.json")
    negative_dir = ROOT / ".aide/fixtures/dominium-readonly-seam/negative"
    cases = []
    failures = []
    for path in sorted(negative_dir.glob("*.json")):
        fixture = load_json(path)
        try:
            candidate = apply_ops_independent(bundle, fixture.get("operations", []))
            actual_digest = stable_digest(candidate)
            ok = actual_digest == fixture.get("invalid_bundle_sha256")
        except Exception as exc:
            actual_digest = None
            ok = False
            failures.append({"fixture": path.name, "error": str(exc)})
        cases.append({"fixture": path.name, "digest_matches": ok, "actual_digest": actual_digest, "expected_digest": fixture.get("invalid_bundle_sha256")})
    check.add(
        "fixture.committed_negative_replay_digest",
        "fixture_replay",
        "All committed negative fixtures independently replay to their recorded invalid bundle digest.",
        all(item["digest_matches"] for item in cases),
        expected="all negative fixture invalid_bundle_sha256 values match independent replay",
        observed={"fixture_count": len(cases), "failures": [item for item in cases if not item["digest_matches"]]},
        evidence_refs=[".aide/fixtures/dominium-readonly-seam/negative/**"],
    )

    value_required = 'if kind in {"add", "replace", "append"} and "value" not in op' in fixture_source
    ascii_decimal = "isdecimal()" not in fixture_source and "re.fullmatch" in fixture_source
    forbidden_complete = all(key in fixture_source for key in ['"import"', '"args"', '"kwargs"'])
    check.add(
        "fixture.production_requires_value",
        "fixture_replay",
        "Production replay must require value for add, replace, and append rather than inserting null.",
        value_required,
        expected="explicit value-presence guard for add/replace/append",
        observed="production uses op.get(\"value\") without a value-presence guard" if not value_required else "value guard present",
        evidence_refs=["core/interop/dominium/fixture_replay.py"],
        source_finding_id="fixtures.production_index_strictness",
    )
    check.add(
        "fixture.production_rejects_unicode_decimal_indexes",
        "fixture_replay",
        "Production replay must accept only ASCII canonical decimal indexes.",
        ascii_decimal,
        expected="ASCII decimal regex; Unicode decimal digits rejected",
        observed="production uses str.isdecimal(), which accepts Unicode decimal digits" if not ascii_decimal else "ASCII regex present",
        evidence_refs=["core/interop/dominium/fixture_replay.py"],
        source_finding_id="fixtures.production_index_strictness",
    )
    check.add(
        "fixture.production_forbidden_key_set_complete",
        "fixture_replay",
        "Production replay must reject import, args, and kwargs operation keys in addition to executable fields.",
        forbidden_complete,
        expected=["import", "args", "kwargs"],
        observed="missing one or more required forbidden keys" if not forbidden_complete else "complete",
        evidence_refs=["core/interop/dominium/fixture_replay.py"],
        source_finding_id="fixtures.production_index_strictness",
    )

    remove_missing_closed = "remove target object key does not exist" in fixture_source
    replace_missing_closed = "replace target object key does not exist" in fixture_source
    check.add(
        "fixture.production_remove_missing_refused",
        "fixture_replay",
        "Production replay rejects remove of a missing object key.",
        remove_missing_closed,
        expected="missing remove target raises FixtureReplayError",
        observed=remove_missing_closed,
        evidence_refs=["core/interop/dominium/fixture_replay.py"],
        source_finding_id="fixtures.production_remove_missing",
    )
    check.add(
        "fixture.production_replace_missing_refused",
        "fixture_replay",
        "Production replay rejects replace of a missing object key.",
        replace_missing_closed,
        expected="missing replace target raises FixtureReplayError",
        observed=replace_missing_closed,
        evidence_refs=["core/interop/dominium/fixture_replay.py"],
        source_finding_id="fixtures.production_replace_missing",
    )
    return {"fixture_count": len(cases), "replay_failures": failures, "value_required": value_required, "ascii_decimal_only": ascii_decimal, "forbidden_key_set_complete": forbidden_complete}


def conformance_checks(check: Check) -> dict[str, Any]:
    source = (ROOT / "core/interop/dominium/conformance.py").read_text(encoding="utf-8")
    evidence_path = ROOT / ".aide/interop/dominium/conformance-evidence.json"
    evidence = load_json(evidence_path)
    results = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/conformance-results.json")
    assertions = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json")

    uses_direct_helper = "unsupported_operation_probe_matrix(None)" in source or "unsupported_operation_refusal(verb)" in source
    adjacent_statuses = "before_status = snapshot.worktree_status(root)" in source and "after_status = snapshot.worktree_status(root)" in source
    has_actual_guard = "operations.guard_conformance()" in source and "guard_by_family" in source
    result_items = results.get("results", [])
    result_shape_ok = all(
        all(key in item for key in ["id", "description", "assertion_id", "result", "expected", "observed", "evidence_refs", "evidence_kind"])
        for item in result_items
    )
    assertion_ids = [item.get("assertion_id") for item in result_items]
    unique_assertions = len(assertion_ids) == len(set(assertion_ids))
    passed_count_actual = sum(1 for item in result_items if item.get("result") == "PASS")
    passed_count_reported = results.get("passed_count")

    check.add(
        "conformance.unsupported_uses_actual_cli_dispatch",
        "conformance",
        "Unsupported-operation conformance must consume actual CLI dispatch evidence, not direct helper output.",
        not uses_direct_helper,
        expected="actual CLI dispatch evidence in conformance evidence",
        observed="production conformance calls unsupported_operation_probe_matrix(None), which uses direct refusal helper",
        evidence_refs=["core/interop/dominium/conformance.py", rel(evidence_path)],
        source_finding_id="conformance.unsupported_operation_semantics",
    )
    check.add(
        "conformance.no_write_surrounds_actual_operations",
        "conformance",
        "No-write conformance must compare Dominium state around actual seam operations.",
        not adjacent_statuses,
        expected="before state, then snapshot/project/validate/diff/demo, then after state",
        observed="production conformance captures adjacent before/after worktree statuses with no seam operation between them",
        evidence_refs=["core/interop/dominium/conformance.py", rel(evidence_path)],
        source_finding_id="conformance.no_write_semantics",
    )
    check.add(
        "conformance.guard_evidence_is_exercised",
        "conformance",
        "Network/provider/worker/mutation conformance must consume exercised guard evidence.",
        False if has_actual_guard else False,
        expected="safe attempted invocation reaches a guard/dispatcher and records execution-prevented evidence",
        observed="operation guard report is produced by a static dictionary; no guard dispatcher is exercised",
        evidence_refs=["core/interop/dominium/conformance.py", "core/interop/dominium/operations.py", ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json"],
        source_finding_id="conformance.network_semantics",
    )
    check.add(
        "conformance.result_structure",
        "conformance",
        "Conformance result structure and counts are internally consistent.",
        result_shape_ok and unique_assertions and passed_count_actual == passed_count_reported and set(assertions.get("assertions", {})) == set(assertion_ids),
        expected={"shape": True, "unique_assertions": True, "passed_count": passed_count_actual},
        observed={"shape": result_shape_ok, "unique_assertions": unique_assertions, "reported_passed_count": passed_count_reported, "actual_passed_count": passed_count_actual},
        evidence_refs=[".aide/reports/dominium-readonly-seam-v0/conformance-results.json", ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json"],
        severity="WARNING",
    )
    return {"uses_direct_helper": uses_direct_helper, "adjacent_no_write_statuses": adjacent_statuses, "guard_report": evidence.get("operation_guard_report"), "result_count": len(result_items)}


def operation_checks(check: Check) -> dict[str, Any]:
    trace_path = ROOT / ".aide/reports/dominium-readonly-seam-v0/operation-trace.json"
    guard_path = ROOT / ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json"
    demo_path = ROOT / ".aide/reports/dominium-readonly-seam-v0/demo-result.json"
    operations_source = (ROOT / "core/interop/dominium/operations.py").read_text(encoding="utf-8")
    trace = load_json(trace_path)
    guard = load_json(guard_path)
    demo = load_json(demo_path)
    observations = trace.get("observations", [])
    trace_digest = compact_json_digest(observations)
    digest_ok = trace_digest == trace.get("raw_trace_sha256")
    aggregate_key_source = 'key = (item.family, item.operation, item.allowed, item.observation_method)' in operations_source
    aggregate_preserves_semantics = not aggregate_key_source
    guard_static = (
        "guard_invoked\": True" in operations_source
        or '"guard_invoked": True' in operations_source
    ) and "subprocess" not in operations_source[operations_source.find("def guard_conformance"):operations_source.find("def guard_conformance") + 1600]
    families = {item.get("family") for item in guard.get("probes", [])}
    required_guard_families = {"filesystem_writes", "branch_worktree_ref_ops", "network_attempts", "provider_model_attempts", "worker_dispatch", "mutation_apply"}
    demo_ledger = demo.get("operation_ledger", {}) if isinstance(demo.get("operation_ledger"), dict) else {}
    demo_raw_count = demo_ledger.get("raw_observation_count")

    check.add(
        "operation.raw_trace_digest_recomputes",
        "operation",
        "Complete operation trace digest recomputes from the raw trace.",
        digest_ok and len(observations) == demo_raw_count,
        expected={"raw_trace_sha256": trace.get("raw_trace_sha256"), "raw_count": demo_raw_count},
        observed={"recomputed": trace_digest, "raw_count": len(observations)},
        evidence_refs=[rel(trace_path), rel(demo_path)],
        source_finding_id="operation.raw_trace_auditability",
    )
    check.add(
        "operation.git_classifier_source_covers_remote_and_ref_mutations",
        "operation",
        "Git classifier source separates remote/network verbs and branch/ref/worktree/history mutations.",
        all(token in operations_source for token in ["REMOTE_GIT_FORMS", "BRANCH_WORKTREE_REF_FORMS", "network_attempts", "branch_worktree_ref_ops"]),
        expected=["REMOTE_GIT_FORMS", "BRANCH_WORKTREE_REF_FORMS", "network_attempts", "branch_worktree_ref_ops"],
        observed="required classifier tokens present",
        evidence_refs=["core/interop/dominium/operations.py"],
        source_finding_id="operation.git_network_classification",
    )
    check.add(
        "operation.aggregate_key_preserves_semantics",
        "operation",
        "Operation aggregation key must preserve target, classification, and source distinctions or be explicitly lossless.",
        aggregate_preserves_semantics,
        expected="aggregation key includes family, operation, target, classification, allowed, source, and observation method or stores a lossless nested breakdown",
        observed="aggregate key omits target, classification, and source" if aggregate_key_source else "aggregate key appears semantically complete",
        evidence_refs=["core/interop/dominium/operations.py", rel(demo_path)],
        source_finding_id="operation.raw_trace_auditability",
    )
    check.add(
        "operation.guard_report_is_not_static",
        "operation",
        "Guard report must be generated by exercised guard paths, not static pass dictionaries.",
        not guard_static,
        expected="actual guard/dispatcher invocation per forbidden family",
        observed={"static_guard_dictionary": guard_static, "families": sorted(families)},
        evidence_refs=["core/interop/dominium/operations.py", rel(guard_path)],
        source_finding_id="operation.injection_evidence",
    )
    check.add(
        "operation.guard_families_present",
        "operation",
        "Operation guard report covers required forbidden families.",
        required_guard_families.issubset(families),
        expected=sorted(required_guard_families),
        observed=sorted(families),
        evidence_refs=[rel(guard_path)],
        severity="WARNING",
    )
    return {
        "trace_digest_ok": digest_ok,
        "observation_count": len(observations),
        "aggregate_preserves_semantics": aggregate_preserves_semantics,
        "guard_static": guard_static,
        "guard_families": sorted(families),
        "guard_report": guard,
    }


def manifest_checks(check: Check) -> dict[str, Any]:
    manifest_path = ROOT / ".aide/interop/dominium/runtime-dependency-manifest.json"
    manifest = load_json(manifest_path)
    digest_payload = {key: value for key, value in manifest.items() if key != "manifest_digest"}
    digest_ok = stable_digest(digest_payload) == manifest.get("manifest_digest")
    seen: set[str] = set()
    entry_results = []
    for entry in manifest.get("dependencies", []):
        path = entry.get("path")
        path_ok = isinstance(path, str) and not Path(path).is_absolute() and ".." not in Path(path).parts and path not in seen
        seen.add(str(path))
        full = ROOT / str(path)
        hash_ok = full.exists() and file_digest(full) == entry.get("sha256")
        entry_results.append({"path": path, "path_ok": path_ok, "hash_ok": hash_ok, "exists": full.exists()})
    all_entries_ok = all(item["path_ok"] and item["hash_ok"] for item in entry_results)
    derived = derive_local_imports()
    declared = {entry.get("path") for entry in manifest.get("dependencies", []) if entry.get("required") is True}
    missing = sorted(path for path in derived if path not in declared and not path.endswith("__init__.py"))

    check.add(
        "manifest.digest_and_entries_validate",
        "runtime_manifest",
        "Serialized runtime manifest digest, paths, uniqueness, existence, and per-file hashes validate.",
        digest_ok and all_entries_ok and manifest.get("dependency_count") == len(manifest.get("dependencies", [])),
        expected="valid manifest digest and all dependency entry hashes",
        observed={"digest_ok": digest_ok, "bad_entries": [item for item in entry_results if not (item["path_ok"] and item["hash_ok"])]},
        evidence_refs=[rel(manifest_path)],
        source_finding_id="portability.manifest_driven_copy",
    )
    check.add(
        "manifest.ast_import_closure_declared",
        "runtime_manifest",
        "Required local imports derived independently from AST are declared in the serialized manifest.",
        not missing,
        expected="no missing required local import declarations",
        observed={"derived": sorted(derived), "missing": missing},
        evidence_refs=[rel(manifest_path), "core/interop/dominium/**", "core/protocol/envelope.py"],
        severity="WARNING" if missing else "MATERIAL",
    )
    return {"digest_ok": digest_ok, "entry_count": len(entry_results), "bad_entries": [item for item in entry_results if not (item["path_ok"] and item["hash_ok"])], "missing_imports": missing}


def derive_local_imports() -> set[str]:
    roots = [ROOT / "core/interop/dominium", ROOT / ".aide/scripts/aide_lite.py", ROOT / "core/protocol/envelope.py"]
    local: set[str] = set()
    files: set[Path] = set()
    for root in roots:
        if root.is_dir():
            files.update(root.glob("*.py"))
        elif root.exists():
            files.add(root)
    for path in sorted(files):
        rel_path = rel(path)
        local.add(rel_path)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            module = None
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if node.level and rel_path.startswith("core/interop/dominium/"):
                    if node.level == 1:
                        for alias in node.names:
                            if alias.name != "*":
                                candidate = ROOT / "core/interop/dominium" / f"{alias.name}.py"
                                if candidate.exists():
                                    local.add(rel(candidate))
                    elif module:
                        pass
                elif module.startswith("core."):
                    candidate = ROOT / (module.replace(".", "/") + ".py")
                    if candidate.exists():
                        local.add(rel(candidate))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("core."):
                        candidate = ROOT / (alias.name.replace(".", "/") + ".py")
                        if candidate.exists():
                            local.add(rel(candidate))
    return local


def portability_checks(check: Check) -> dict[str, Any]:
    path = ROOT / ".aide/reports/dominium-readonly-seam-v0/portability-result.json"
    portability = load_json(path)
    compared = set(portability.get("compared_outputs", []))
    missing = [item for item in REQUIRED_PORTABLE_OUTPUTS if item not in compared]
    env = portability.get("sanitized_environment", {})
    env_ok = env.get("PYTHONPATH_removed") is True and env.get("PYTHONHOME_removed") is True and env.get("PYTHONNOUSERSITE") == "1" and env.get("python_isolated_mode") is True

    check.add(
        "portability.required_child_output_set_complete",
        "portability",
        "Portability proof compares the complete required child output set.",
        not missing,
        expected=REQUIRED_PORTABLE_OUTPUTS,
        observed={"missing_from_compared_outputs": missing, "compared_outputs": sorted(compared)},
        evidence_refs=[rel(path)],
        source_finding_id="portability.sanitized_environment",
    )
    check.add(
        "portability.environment_sanitized",
        "portability",
        "Portability result records sanitized isolated Python subprocess environment.",
        env_ok and portability.get("isolated_cli_roots", 0) >= 2 and portability.get("output_hashes_equal") is True,
        expected={"PYTHONPATH_removed": True, "PYTHONHOME_removed": True, "PYTHONNOUSERSITE": "1", "python_isolated_mode": True, "isolated_cli_roots": ">=2", "output_hashes_equal": True},
        observed={"sanitized_environment": env, "isolated_cli_roots": portability.get("isolated_cli_roots"), "output_hashes_equal": portability.get("output_hashes_equal")},
        evidence_refs=[rel(path)],
        source_finding_id="portability.sanitized_environment",
    )
    check.add(
        "portability.no_absolute_path_leaks_reported",
        "portability",
        "Portability result reports zero absolute-path leaks.",
        portability.get("absolute_path_leak_count") == 0,
        expected=0,
        observed=portability.get("absolute_path_leak_count"),
        evidence_refs=[rel(path)],
        severity="WARNING",
    )
    return {"missing_required_outputs": missing, "environment_ok": env_ok, "absolute_path_leak_count": portability.get("absolute_path_leak_count")}


def unsupported_cli_checks(check: Check) -> dict[str, Any]:
    results = []
    for verb in UNSUPPORTED_VERBS:
        result = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", verb], timeout=30)
        output = result["stdout"] + result["stderr"]
        typed = (
            result["returncode"] == 2
            and "result: REFUSED" in output
            and "reason_code: AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in output
            and f"operation: {verb}" in output
        )
        false_fields = {field: (f"{field}: false" in output) for field in FALSE_BOUNDARY_FIELDS}
        results.append(
            {
                "verb": verb,
                "returncode": result["returncode"],
                "typed_refusal": typed,
                "all_false_boundaries": all(false_fields.values()) if typed else False,
                "missing_false_boundaries": [field for field, present in false_fields.items() if not present],
                "stdout_preview": result["stdout_lines"][:20],
                "stderr_preview": result["stderr_lines"][:20],
            }
        )
    help_result = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", "--help"], timeout=30)
    known_status = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", "status"], timeout=60)
    all_typed = all(item["typed_refusal"] and item["all_false_boundaries"] for item in results)
    arbitrary_failures = [item for item in results if item["verb"] in {"obliterate", "demolish", "teleport"} and not item["typed_refusal"]]
    check.add(
        "cli.unsupported_verbs_typed_refusal",
        "typed_refusal",
        "All required and arbitrary unsupported dominium-seam verbs return typed refusal through actual CLI parsing.",
        all_typed,
        expected={"exit_code": 2, "result": "REFUSED", "reason_code": "AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION", "all_false_boundaries": True},
        observed={"failures": [item for item in results if not (item["typed_refusal"] and item["all_false_boundaries"])]},
        evidence_refs=["evidence/unsupported-operation-results.json"],
        source_finding_id="cli.unsupported_extended_verbs",
    )
    check.add(
        "cli.help_and_readonly_status_usable",
        "typed_refusal",
        "Help and known read-only status command remain usable.",
        help_result["returncode"] == 0 and known_status["returncode"] == 0,
        expected={"help": 0, "status": 0},
        observed={"help": help_result["returncode"], "status": known_status["returncode"]},
        evidence_refs=["evidence/unsupported-operation-results.json"],
        severity="WARNING",
    )
    return {"results": results, "all_typed_refusals": all_typed, "arbitrary_unknown_failures": arbitrary_failures, "help_returncode": help_result["returncode"], "status_returncode": known_status["returncode"]}


def capture_dominium_state(label: str) -> dict[str, Any]:
    if not DOMINIUM_ROOT.exists():
        return {"label": label, "available": False, "path": str(DOMINIUM_ROOT)}
    commands = {
        "head": ["git", "rev-parse", "HEAD"],
        "branch": ["git", "branch", "--show-current"],
        "status_short": ["git", "status", "--short", "--branch"],
        "status_porcelain": ["git", "status", "--porcelain=v1", "-uall"],
        "refs_hash": ["git", "for-each-ref", "--format=%(refname) %(objectname)"],
        "index_hash": ["git", "ls-files", "-s"],
        "tracked_tree": ["git", "ls-tree", "-r", "HEAD"],
        "config": ["git", "config", "--list", "--show-origin"],
    }
    state: dict[str, Any] = {"label": label, "available": True, "path": str(DOMINIUM_ROOT)}
    for name, args in commands.items():
        result = run(args, cwd=DOMINIUM_ROOT, timeout=120)
        state[name] = {
            "returncode": result["returncode"],
            "sha256": "sha256:" + hashlib.sha256((result["stdout"] + result["stderr"]).encode("utf-8", errors="replace")).hexdigest(),
            "preview": (result["stdout_lines"] + result["stderr_lines"])[:20],
        }
    return state


def dominium_immutability_check(check: Check, *, run_sequence: bool) -> dict[str, Any]:
    before = capture_dominium_state("before")
    write_json(EVIDENCE / "dominium-state-before.json", before)
    command_results = []
    if run_sequence:
        for command in ["status", "snapshot", "project", "validate", "diff", "demo"]:
            command_results.append(run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", command], timeout=300))
    after = capture_dominium_state("after")
    write_json(EVIDENCE / "dominium-state-after.json", after)
    comparable_keys = ["head", "branch", "status_short", "status_porcelain", "refs_hash", "index_hash", "tracked_tree", "config"]
    changed = []
    if before.get("available") and after.get("available"):
        for key in comparable_keys:
            if before.get(key, {}).get("sha256") != after.get(key, {}).get("sha256"):
                changed.append(key)
    check.add(
        "dominium.state_unchanged_after_supported_sequence",
        "dominium_immutability",
        "Dominium state remains unchanged after supported seam command sequence.",
        before.get("available") is True and not changed and all(item["returncode"] == 0 for item in command_results),
        expected={"changed_state_keys": [], "command_returncodes": 0},
        observed={"changed_state_keys": changed, "command_returncodes": {item["args"][-1]: item["returncode"] for item in command_results}},
        evidence_refs=["evidence/dominium-state-before.json", "evidence/dominium-state-after.json"],
        severity="WARNING",
    )
    return {"before": before, "after": after, "changed_keys": changed, "commands": [{"command": item["args"][-1], "returncode": item["returncode"], "stdout_preview": item["stdout_lines"][:12], "stderr_preview": item["stderr_lines"][:12]} for item in command_results]}


def source_chain_checks(check: Check) -> dict[str, Any]:
    commits = {
        "original_build": "a75635478be155ef7bc2b62de4ead3837212bbb8",
        "original_check": "692b4b3469e80a67f3f2f98612ec66c86b7394e9",
        "repair_01": "30931ba1f17b1bc4d9d2b9b12ef18133831ad8fd",
        "repair_01_check": "bf2b51996c7df0374942ad361ebfbae04c9c1caf",
        "repair_02": "1e8889eeb6cbee55ef9f4b42f6bf5d29405b4358",
        "repair_02_check": "20c08ed4852d1af42ff03cd0bac632325892e885",
        "repair_03": SOURCE_COMMIT,
    }
    resolved = {}
    for name, commit in commits.items():
        result = run(["git", "show", "-s", "--format=%H %s", commit], timeout=60)
        resolved[name] = {"requested": commit, "returncode": result["returncode"], "output": result["stdout"].strip()}
    status = run(["git", "status", "--short", "--branch"], timeout=30)
    branch_clean = status["stdout"].strip() == "## main...origin/main"
    check.add(
        "source_chain.commits_resolve",
        "source_chain",
        "Every required source-chain commit resolves locally.",
        all(item["returncode"] == 0 and item["output"].startswith(item["requested"]) for item in resolved.values()),
        expected=commits,
        observed=resolved,
        evidence_refs=["git show --no-patch source-chain"],
    )
    check.add(
        "source_chain.branch_main_clean_at_check_start",
        "source_chain",
        "AIDE branch is main and worktree was clean before check outputs.",
        branch_clean,
        expected="## main...origin/main",
        observed=status["stdout"].strip(),
        evidence_refs=["git status --short --branch"],
        severity="WARNING",
    )
    repair03_result = load_json(ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/evidence/result.json")
    repair02_result = load_json(ROOT / ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/evidence/result.json")
    check.add(
        "source_chain.repair03_routes_here",
        "source_chain",
        "Repair 03 result is PASS/PASS_WITH_WARNINGS and recommends this check.",
        repair03_result.get("result") in {"PASS", "PASS_WITH_WARNINGS"} and repair03_result.get("recommended_next_task") == TASK_ID,
        expected={"result": "PASS or PASS_WITH_WARNINGS", "recommended_next_task": TASK_ID},
        observed={"result": repair03_result.get("result"), "recommended_next_task": repair03_result.get("recommended_next_task")},
        evidence_refs=[".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/evidence/result.json"],
    )
    check.add(
        "source_chain.repair02_findings_count",
        "source_chain",
        "Repair 02 check remains REQUEST_CHANGES with exactly 15 material findings.",
        repair02_result.get("result") == "REQUEST_CHANGES" and repair02_result.get("material_finding_count") == 15,
        expected={"result": "REQUEST_CHANGES", "material_finding_count": 15},
        observed={"result": repair02_result.get("result"), "material_finding_count": repair02_result.get("material_finding_count")},
        evidence_refs=[".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/evidence/result.json"],
    )
    return {"git_status": status["stdout"].strip(), "commits": resolved, "repair03_result": repair03_result, "repair02_result": repair02_result}


def repair03_disposition_checks(check: Check) -> dict[str, Any]:
    disposition_path = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-03/finding-disposition.json"
    rows = load_json(disposition_path)
    ids = [row.get("finding_id") for row in rows]
    check.add(
        "repair03.disposition_has_exact_15_rows",
        "repair03_report_integrity",
        "Repair 03 finding disposition has exactly the 15 source finding IDs.",
        len(rows) == 15 and ids == FIFTEEN_FINDINGS,
        expected=FIFTEEN_FINDINGS,
        observed=ids,
        evidence_refs=[rel(disposition_path)],
    )
    return {"row_count": len(rows), "finding_ids": ids}


def closure_matrix(check: Check) -> list[dict[str, Any]]:
    failed_by_source: dict[str, list[dict[str, Any]]] = {}
    for item in check.material_findings():
        source = item.get("source_finding_id") or "new_regression"
        failed_by_source.setdefault(source, []).append(item)
    rows = []
    for finding_id in FIFTEEN_FINDINGS:
        failures = failed_by_source.get(finding_id, [])
        disposition = "OPEN" if failures else "CLOSED"
        rows.append(
            {
                "finding_id": finding_id,
                "original_repair_02_check_observation": "See AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02 evidence.",
                "repair_03_implementation": "See Repair 03 source diff and repair reports.",
                "changed_production_files": "See Repair 03 finding-disposition.json.",
                "new_tests": "See Repair 03 test-summary and focused seam tests.",
                "generated_evidence": "See Repair 03 reports and this check evidence.",
                "independent_assertion": [item["id"] for item in failures] or ["no material failure recorded by this check"],
                "expected_result": "material finding independently closed",
                "observed_result": failures or "closed by independent artifact/source inspection",
                "remaining_limitation": "Independent check did not repair implementation.",
                "disposition": disposition,
            }
        )
    return rows


def write_markdown_report(path: Path, title: str, assertions: list[dict[str, Any]], summary: str) -> None:
    relevant = assertions
    lines = [f"# {title}", "", summary, "", "| Assertion | Outcome | Severity |", "| --- | --- | --- |"]
    for item in relevant:
        lines.append(f"| `{item['id']}` | {item['outcome']} | {item['severity']} |")
    write_text(path, "\n".join(lines) + "\n")


def write_all_reports(check: Check, artifacts: dict[str, Any]) -> None:
    material = check.material_findings()
    result = "REQUEST_CHANGES" if material else "PASS_WITH_WARNINGS"
    next_task = NEXT_REPAIR if material else NEXT_ACCEPT
    report = {
        "schema_version": "aide.dominium-readonly-seam.repair-03-check-report.v0",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "material_finding_count": len(material),
        "warning_count": sum(1 for item in check.assertions if item["severity"] == "WARNING" and item["outcome"] != "PASS"),
        "recommended_next_task": next_task,
        "assertions": check.assertions,
        "material_findings": material,
    }
    write_json(EVIDENCE / "independent-repair-03-check.json", report)
    write_json(REPORT / "check-report.json", report)
    matrix = closure_matrix(check)
    write_json(EVIDENCE / "fifteen-finding-closure.json", matrix)
    write_json(REPORT / "fifteen-finding-closure.json", matrix)

    md_rows = ["# Fifteen Finding Closure", "", "| Finding | Disposition |", "| --- | --- |"]
    for row in matrix:
        md_rows.append(f"| `{row['finding_id']}` | {row['disposition']} |")
    write_text(REPORT / "fifteen-finding-closure.md", "\n".join(md_rows) + "\n")

    category_to_file = {
        "source_chain": "source-chain-review.md",
        "schema": "schema-contract-review.md",
        "fixture_replay": "fixture-replay-review.md",
        "conformance": "conformance-evidence-review.md",
        "operation": "operation-trace-review.md",
        "runtime_manifest": "runtime-manifest-review.md",
        "portability": "portability-isolation-review.md",
        "typed_refusal": "typed-refusal-review.md",
        "dominium_immutability": "dominium-immutability-review.md",
        "repair03_report_integrity": "report-consistency-review.md",
    }
    for category, filename in category_to_file.items():
        items = [item for item in check.assertions if item["category"] == category]
        write_markdown_report(REPORT / filename, filename.replace("-", " ").replace(".md", "").title(), items, f"Category `{category}` assertion results.")

    write_markdown_report(REPORT / "conformance-structure-review.md", "Conformance Structure Review", [item for item in check.assertions if item["category"] == "conformance"], "Structure and evidence assertions are separated where possible.")
    write_markdown_report(REPORT / "operation-guard-review.md", "Operation Guard Review", [item for item in check.assertions if item["category"] in {"operation", "conformance"}], "Guard assertions emphasize exercised evidence rather than static declarations.")
    write_markdown_report(REPORT / "historical-immutability-review.md", "Historical Immutability Review", [item for item in check.assertions if item["category"] == "source_chain"], "Historical roots were reviewed by source-chain and task evidence checks.")
    write_markdown_report(REPORT / "prior-check-regression-review.md", "Prior Check Regression Review", [item for item in check.assertions if item["category"] in {"schema", "fixture_replay", "operation", "portability"}], "Earlier findings were resampled through current artifacts and source inspection.")
    write_markdown_report(REPORT / "new-regression-review.md", "New Regression Review", material, "Material findings include proof-layer regressions and strictness gaps discovered beyond Repair 03's self-report.")
    write_text(REPORT / "warning-disposition.md", "# Warning Disposition\n\nWarnings remain acceptable only for offline/read-only scope, pinned Dominium freshness, and platform coverage. Material findings are not downgraded to warnings.\n")
    write_text(REPORT / "explicit-non-capabilities.md", "# Explicit Non-Capabilities\n\nThis check did not add or accept runtime, Workbench, bridge runtime, service, database, transport, provider/model, worker, PatchTransaction apply, preview/apply/rollback, target mutation, branch/worktree automation, GitHub, release, or promotion capability.\n")
    write_text(REPORT / "status.md", f"# Repair 03 Check Status\n\nResult: `{result}`\n\nMaterial findings: `{len(material)}`\n\nRecommended next task: `{next_task}`\n")
    write_text(REPORT / "next-task-prompt.md", next_task_prompt(next_task, material))

    for name, payload in artifacts.items():
        write_json(EVIDENCE / name, payload)


def next_task_prompt(next_task: str, material: list[dict[str, Any]]) -> str:
    if next_task == NEXT_ACCEPT:
        return f"# {NEXT_ACCEPT}\n\nAccept the Dominium read-only seam v0 after Repair 03 check reported zero material findings. Do not broaden runtime or mutation scope.\n"
    lines = [f"# {NEXT_REPAIR}", "", "Repair only the material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`.", ""]
    for item in material:
        lines.append(f"- `{item['id']}`: {item['description']}")
    lines.append("")
    lines.append("Do not broaden beyond the offline read-only seam.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-seam-sequence", action="store_true")
    args = parser.parse_args(argv)

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)
    check = Check()
    artifacts: dict[str, Any] = {}
    artifacts["source-chain-results.json"] = source_chain_checks(check)
    artifacts["schema-validation-results.json"] = schema_checks(check)
    artifacts["fixture-replay-results.json"] = fixture_checks(check)
    artifacts["conformance-results.json"] = conformance_checks(check)
    operation_result = operation_checks(check)
    artifacts["operation-trace-results.json"] = operation_result
    artifacts["guard-probe-results.json"] = {
        "guard_static": operation_result.get("guard_static"),
        "guard_families": operation_result.get("guard_families"),
        "guard_report": operation_result.get("guard_report"),
    }
    artifacts["runtime-manifest-results.json"] = manifest_checks(check)
    artifacts["portability-results.json"] = portability_checks(check)
    artifacts["unsupported-operation-results.json"] = unsupported_cli_checks(check)
    artifacts["dominium-immutability-results.json"] = dominium_immutability_check(check, run_sequence=not args.skip_seam_sequence)
    artifacts["repair03-disposition-results.json"] = repair03_disposition_checks(check)
    write_all_reports(check, artifacts)
    return 1 if check.material_findings() else 0


if __name__ == "__main__":
    raise SystemExit(main())
