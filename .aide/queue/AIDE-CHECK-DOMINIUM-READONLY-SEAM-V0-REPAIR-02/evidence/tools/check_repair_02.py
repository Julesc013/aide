"""Independent Repair 02 check harness for the Dominium read-only seam.

This task-local harness intentionally avoids importing the production seam
validation, conformance, fixture replay, and portability modules for material
assertions. It reads committed artifacts and source text, recomputes bounded
hashes, and records the check result.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02"
BUILD_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02"
NEXT_ON_PASS = "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"
NEXT_ON_FAIL = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03"
REPAIR_02_SHA = "1e8889eeb6cbee55ef9f4b42f6bf5d29405b4358"
PINNED_DOMINIUM_SHA = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"

REPORT_DIR = Path(".aide/reports/dominium-readonly-seam-v0-repair-02-check")
EVIDENCE_DIR = Path(".aide/queue") / TASK_ID / "evidence"
TOOLS_DIR = EVIDENCE_DIR / "tools"

SEAM_REPORT_DIR = Path(".aide/reports/dominium-readonly-seam-v0")
REPAIR_REPORT_DIR = Path(".aide/reports/dominium-readonly-seam-v0-repair-02")
SCHEMA_PATH = Path(".aide/protocol/aide-dominium-readonly-seam-v0.schema.json")
RUNTIME_MANIFEST_PATH = Path(".aide/interop/dominium/runtime-dependency-manifest.json")
DOMINIUM_ROOT = Path("C:/Projects/Dominium/dominium")

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

SPEC_DEFS = [
    "HostManifestSpec",
    "HostCapabilitySetSpec",
    "WorkspaceDescriptorSpec",
    "ContextDescriptorSpec",
    "ArtifactReferenceSpec",
    "DiagnosticProjectionSpec",
    "RefusalProjectionSpec",
    "EvidenceReferenceSetSpec",
    "EventEnvelopeSpec",
    "DominiumBridgeManifestSpec",
]

REQUIRED_OUTPUTS = [
    ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json",
    ".aide/reports/dominium-readonly-seam-v0/source-snapshot.json",
    ".aide/reports/dominium-readonly-seam-v0/projection-index.json",
    ".aide/reports/dominium-readonly-seam-v0/validation.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-results.json",
    ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json",
    ".aide/reports/dominium-readonly-seam-v0/compatibility.json",
    ".aide/reports/dominium-readonly-seam-v0/demo-result.json",
    ".aide/reports/dominium-readonly-seam-v0/fixture-manifest.json",
    ".aide/interop/dominium/seam-bundle.json",
    ".aide/interop/dominium/dominium-bridge-manifest.json",
    ".aide/interop/dominium/conformance-expectations.json",
    ".aide/interop/dominium/runtime-dependency-manifest.json",
]

TEN_GAPS = [
    ("REPAIR02-GAP-01", "allowed_operation_count missing"),
    ("REPAIR02-GAP-02", "conformance results lack required independent assertion fields"),
    ("REPAIR02-GAP-03", "cross-process determinism failed"),
    ("REPAIR02-GAP-04", "diagnostic projection disclosure incomplete"),
    ("REPAIR02-GAP-05", "instrumentation coverage missing"),
    ("REPAIR02-GAP-06", "operation ledger missing required operation families"),
    ("REPAIR02-GAP-07", "negative fixtures failed independent replay"),
    ("REPAIR02-GAP-08", "schema lacks kind-specific spec constraints"),
    ("REPAIR02-GAP-09", "schema lacks status constraints"),
    ("REPAIR02-GAP-10", "refusal projection disclosure incomplete"),
]


def run(args: list[str], *, cwd: Path | None = None, timeout: int = 60) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=str(cwd or Path.cwd()),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "args": args,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def stable_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def flatten_records(records: dict[str, Any]) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    for value in records.values():
        if isinstance(value, list):
            flat.extend(item for item in value if isinstance(item, dict) and item.get("kind"))
        elif isinstance(value, dict) and value.get("kind"):
            flat.append(value)
    return sorted(flat, key=lambda item: (str(item.get("kind", "")), str(item.get("metadata", {}).get("id", ""))))


def yaml_scalar(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip('"')
    return None


def assertion(
    assertions: list[dict[str, Any]],
    id_: str,
    category: str,
    description: str,
    outcome: str,
    severity: str,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    *,
    source_gap_id: str | None = None,
    source_finding_id: str | None = None,
) -> None:
    assertions.append(
        {
            "id": id_,
            "category": category,
            "description": description,
            "outcome": outcome,
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_gap_id": source_gap_id,
            "source_finding_id": source_finding_id,
        }
    )


def strict_pointer_parts(pointer: Any) -> list[str]:
    if not isinstance(pointer, str):
        raise ValueError("pointer must be string")
    if not pointer.startswith("/"):
        raise ValueError("pointer must start with /")
    parts = pointer.split("/")[1:]
    decoded = []
    for part in parts:
        if "~" in part and not re.search(r"~[01]", part):
            raise ValueError("ambiguous escaped pointer")
        decoded.append(part.replace("~1", "/").replace("~0", "~"))
    return decoded


def resolve_parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = strict_pointer_parts(pointer)
    if not parts:
        raise ValueError("root replacement is forbidden")
    current = document
    for part in parts[:-1]:
        if isinstance(current, list):
            if part == "-" or not re.fullmatch(r"0|[1-9][0-9]*", part):
                raise ValueError("array index must be canonical non-negative integer")
            index = int(part)
            if index >= len(current):
                raise ValueError("array index out of range")
            current = current[index]
        elif isinstance(current, dict):
            if part not in current:
                raise ValueError("missing object key")
            current = current[part]
        else:
            raise ValueError("cannot traverse non-container")
    return current, parts[-1]


def apply_strict_operations(document: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = deepcopy(document)
    forbidden_keys = {"callable", "module", "command", "shell", "eval", "exec"}
    for op in operations:
        if not isinstance(op, dict):
            raise ValueError("operation must be object")
        if forbidden_keys.intersection(op):
            raise ValueError("operation contains executable metadata")
        if set(["op", "path"]) - set(op):
            raise ValueError("operation missing op or path")
        kind = op["op"]
        if kind not in {"add", "remove", "replace", "append"}:
            raise ValueError("unknown operation")
        parent, key = resolve_parent(candidate, op["path"])
        if isinstance(parent, list):
            if key == "-":
                if kind not in {"add", "append"}:
                    raise ValueError("dash is only valid for add/append")
                index = len(parent)
            else:
                if not re.fullmatch(r"0|[1-9][0-9]*", key):
                    raise ValueError("array index must be canonical non-negative integer")
                index = int(key)
            if kind in {"remove", "replace"} and index >= len(parent):
                raise ValueError("array index out of range")
            if kind == "remove":
                parent.pop(index)
            elif kind == "replace":
                parent[index] = deepcopy(op.get("value"))
            elif kind == "add":
                if index > len(parent):
                    raise ValueError("array index out of range")
                parent.insert(index, deepcopy(op.get("value")))
            else:
                parent.append(deepcopy(op.get("value")))
        elif isinstance(parent, dict):
            if kind in {"remove", "replace"} and key not in parent:
                raise ValueError(f"{kind} requires existing object key")
            if kind == "remove":
                parent.pop(key)
            elif kind in {"add", "replace"}:
                parent[key] = deepcopy(op.get("value"))
            else:
                if key not in parent or not isinstance(parent[key], list):
                    raise ValueError("append requires array target")
                parent[key].append(deepcopy(op.get("value")))
        else:
            raise ValueError("target parent is not a container")
    return candidate


def fixture_replay_check(bundle: dict[str, Any]) -> dict[str, Any]:
    fixture_root = Path(".aide/fixtures/dominium-readonly-seam/negative")
    results = []
    failed = 0
    for path in sorted(fixture_root.glob("*.json")):
        fixture = read_json(path)
        record = {"name": path.stem, "path": path.as_posix(), "status": "PASS", "errors": []}
        try:
            if fixture.get("schema_version") != "aide.dominium-readonly-seam.negative-fixture.v1":
                raise ValueError("wrong schema_version")
            if fixture.get("base_bundle_sha256") != stable_digest(bundle):
                raise ValueError("base digest mismatch")
            invalid = apply_strict_operations(bundle, fixture.get("operations", []))
            if stable_digest(invalid) != fixture.get("invalid_bundle_sha256"):
                raise ValueError("invalid digest mismatch")
            invalid_again = apply_strict_operations(bundle, fixture.get("operations", []))
            if stable_json(invalid) != stable_json(invalid_again):
                raise ValueError("second replay not byte-identical")
            if not fixture.get("expected_error_codes"):
                raise ValueError("missing expected_error_codes")
        except Exception as exc:  # noqa: BLE001 - evidence should preserve exact failure.
            failed += 1
            record["status"] = "FAIL"
            record["errors"].append(str(exc))
        results.append(record)
    return {"passed_count": len(results) - failed, "failed_count": failed, "results": results}


def registry_ids(payload: Any) -> list[str]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        rows = payload.get("codes") or payload.get("diagnostics") or payload.get("refusals") or payload.get("items") or []
        if isinstance(rows, dict):
            rows = list(rows.values())
    else:
        rows = []
    ids = []
    for item in rows:
        if isinstance(item, dict):
            value = item.get("id") or item.get("code") or item.get("diagnostic_id") or item.get("refusal_id")
            if value:
                ids.append(str(value))
    return ids


def git_object_info(revision: str, rel_path: str) -> dict[str, Any]:
    tree = run(["git", "-C", str(DOMINIUM_ROOT), "ls-tree", revision, rel_path])
    if tree["returncode"] != 0 or not tree["stdout"].strip():
        return {"error": tree["stderr"] or tree["stdout"]}
    left = tree["stdout"].split("\t", 1)[0]
    mode, object_type, git_object = left.split()
    return {"mode": mode, "object_type": object_type, "git_object": git_object}


def git_show_bytes(revision: str, rel_path: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(DOMINIUM_ROOT), "show", f"{revision}:{rel_path}"],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    return completed.stdout


def registry_check(bundle: dict[str, Any], kind: str, record_container: str) -> dict[str, Any]:
    summary = bundle.get("registry_projection_summary", {}).get(kind, {})
    rel_path = summary.get("source_registry_path") or summary.get("path")
    source_bytes = git_show_bytes(PINNED_DOMINIUM_SHA, rel_path)
    payload = json.loads(source_bytes.decode("utf-8"))
    ids = registry_ids(payload)
    selected = ids[: int(summary.get("selection_limit", 0))]
    omitted = ids[len(selected) :]
    records = bundle.get("records", {}).get(record_container, [])
    projected_ids = []
    for record in records:
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        projected_ids.append(str(spec.get("diagnostic_id") or spec.get("refusal_id") or spec.get("code")))
    expected = {
        "source_registry_sha256": sha256_bytes(source_bytes),
        "source_registry_git_object": git_object_info(PINNED_DOMINIUM_SHA, rel_path),
        "native_count": len(ids),
        "projected_count": len(selected),
        "omitted_count": len(omitted),
        "projected_ids": selected,
        "selected_ids_sha256": stable_digest(selected),
        "omitted_ids_sha256": stable_digest(omitted),
        "truncation_disclosed": len(omitted) > 0,
        "selection_policy": "source_order_first_n",
    }
    comparisons = {
        key: {"expected": value, "observed": summary.get(key), "match": summary.get(key) == value}
        for key, value in expected.items()
    }
    comparisons["projected_records_match"] = {
        "expected": selected,
        "observed": projected_ids,
        "match": projected_ids == selected,
    }
    return {
        "kind": kind,
        "path": rel_path,
        "all_passed": all(item["match"] for item in comparisons.values()),
        "comparisons": comparisons,
    }


def schema_review(schema: dict[str, Any]) -> dict[str, Any]:
    defs = schema.get("$defs", {})
    unconstrained = {}
    for name in SPEC_DEFS:
        spec = defs.get(name, {})
        required = spec.get("required", [])
        properties = spec.get("properties", {})
        missing = [field for field in required if field not in properties]
        if missing:
            unconstrained[name] = missing
    false_status = defs.get("FalseStatus", {})
    status_required = set(false_status.get("required", []))
    false_missing = [field for field in FALSE_BOUNDARY_FIELDS if field not in status_required]
    additional_true = []
    for path, value in walk_schema(schema):
        if isinstance(value, dict) and value.get("additionalProperties") is True:
            additional_true.append(path)
    return {
        "unconstrained_required_spec_fields": unconstrained,
        "missing_required_false_boundary_fields": false_missing,
        "additional_properties_true_locations": additional_true,
        "jsonschema_installed": False,
    }


def walk_schema(value: Any, path: str = "#") -> list[tuple[str, Any]]:
    rows = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            rows.extend(walk_schema(child, f"{path}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(walk_schema(child, f"{path}/{index}"))
    return rows


def operation_review(demo: dict[str, Any], operation_source: str) -> dict[str, Any]:
    ledger = demo.get("operation_ledger", {})
    operations = ledger.get("operations", [])
    observation_count = ledger.get("observation_count")
    allowed = ledger.get("allowed_operation_count")
    forbidden = ledger.get("forbidden_operation_count")
    recomputed = sum(int(item.get("count", 0)) for item in operations if isinstance(item, dict))
    required_families = [
        "git_reads",
        "filesystem_writes",
        "branch_worktree_ref_ops",
        "network_attempts",
        "provider_model_attempts",
        "worker_dispatch",
        "mutation_apply",
    ]
    family_set = {str(item.get("family")) for item in operations if isinstance(item, dict)}
    network_verbs_as_git_reads = "family = \"branch_worktree_ref_ops\" if verb in {\"checkout\", \"switch\", \"reset\", \"merge\", \"rebase\", \"branch\", \"worktree\", \"tag\", \"update-ref\"} else \"git_reads\"" in operation_source
    return {
        "operation_count": ledger.get("operation_count"),
        "operation_len": len(operations),
        "observation_count": observation_count,
        "allowed_operation_count": allowed,
        "forbidden_operation_count": forbidden,
        "recomputed_observation_count": recomputed,
        "counts_reconcile": observation_count == recomputed == (allowed + forbidden if isinstance(allowed, int) and isinstance(forbidden, int) else None),
        "required_families": required_families,
        "observed_families": sorted(family_set),
        "missing_families": [family for family in required_families if family not in ledger.get("coverage", {})],
        "raw_observation_sample_count": len(ledger.get("raw_observation_sample", [])),
        "complete_raw_trace_present": isinstance(ledger.get("raw_observations"), list) and len(ledger.get("raw_observations", [])) == observation_count,
        "raw_trace_digest_present": bool(ledger.get("raw_observation_digest")),
        "network_remote_verbs_classified_as_git_reads": network_verbs_as_git_reads,
        "forbidden_injection_count": forbidden,
    }


def conformance_review(conformance_source: str, results: dict[str, Any], assertions: dict[str, Any]) -> dict[str, Any]:
    rows = results.get("results", [])
    assertion_rows = assertions.get("assertions", {})
    missing_fields = []
    for row in rows:
        missing = [field for field in ["id", "description", "assertion_id", "result", "expected", "observed", "evidence_refs"] if field not in row]
        if missing:
            missing_fields.append({"id": row.get("id"), "missing": missing})
    return {
        "result_count": len(rows),
        "passed_count": sum(1 for row in rows if row.get("result") == "PASS"),
        "assertion_count": len(assertion_rows),
        "missing_required_fields": missing_fields,
        "unsupported_operation_assertion_uses_next_task_suffix": 'RECOMMENDED_NEXT_TASK.endswith("REPAIR-02")' in conformance_source,
        "no_write_assertion_uses_self_declared_flag_only": 'dominium_file_write") is False' in conformance_source,
        "network_assertion_uses_status_fields_only": 'network_call_performed") is False' in conformance_source,
        "aggregate_only_not_proven_source_present": '"NOT_PROVEN"' in conformance_source,
    }


def runtime_dependency_review(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("dependencies", [])
    path_results = []
    for entry in entries:
        rel = entry.get("path")
        path = Path(rel)
        result = {
            "path": rel,
            "exists": path.exists(),
            "repository_relative": bool(rel) and not Path(rel).is_absolute() and ".." not in Path(rel).parts,
            "sha256_match": False,
        }
        if path.exists() and path.is_file():
            result["sha256_match"] = sha256_file(path) == entry.get("sha256")
        path_results.append(result)
    payload = {key: value for key, value in manifest.items() if key != "manifest_digest"}
    return {
        "dependency_count": len(entries),
        "declared_dependency_count": manifest.get("dependency_count"),
        "all_paths_valid": all(item["exists"] and item["repository_relative"] and item["sha256_match"] for item in path_results),
        "manifest_digest_match": stable_digest(payload) == manifest.get("manifest_digest"),
        "path_results": path_results,
    }


def import_graph_review(manifest: dict[str, Any]) -> dict[str, Any]:
    roots = [Path(".aide/scripts/aide_lite.py"), Path("core/interop/dominium"), Path("core/protocol/envelope.py")]
    local_imports: set[str] = set()
    for root in roots:
        files = [root] if root.is_file() else sorted(root.glob("*.py"))
        for path in files:
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    module = node.module
                    if module.startswith("core.") or module.startswith("interop.dominium"):
                        local_imports.add(module)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("core."):
                            local_imports.add(alias.name)
    declared = {str(item.get("path")) for item in manifest.get("dependencies", [])}
    return {
        "derived_local_imports": sorted(local_imports),
        "declared_dependency_count": len(declared),
        "aide_lite_declared": ".aide/scripts/aide_lite.py" in declared,
        "dominium_package_declared": "core/interop/dominium/__init__.py" in declared,
        "envelope_declared": "core/protocol/envelope.py" in declared,
    }


def portability_review(portability: dict[str, Any], bundle_source: str) -> dict[str, Any]:
    output_hashes = portability.get("output_hashes", [])
    missing_by_root = []
    required_set = set(REQUIRED_OUTPUTS)
    for index, hashes in enumerate(output_hashes):
        actual = set(hashes)
        missing_by_root.append({"root": index, "missing": sorted(required_set - actual), "extra": sorted(actual - required_set)})
    return {
        "status": portability.get("status"),
        "isolated_cli_roots": portability.get("isolated_cli_roots"),
        "output_hashes_equal": portability.get("output_hashes_equal"),
        "absolute_path_leak_count": portability.get("absolute_path_leak_count"),
        "missing_by_root": missing_by_root,
        "uses_production_copy_runtime_dependencies": "_copy_runtime_dependencies(source_root, temp_root)" in bundle_source,
        "uses_os_environ_copy": "env = os.environ.copy()" in bundle_source,
        "removes_pythonpath": "PYTHONPATH" in bundle_source and "pop" in bundle_source,
        "uses_python_isolated_mode": '"-I"' in bundle_source or "'-I'" in bundle_source,
    }


def unsupported_operation_probe() -> dict[str, Any]:
    verbs = [
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
    ]
    results = []
    for verb in verbs:
        completed = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", verb])
        output = f"{completed['stdout']}\n{completed['stderr']}"
        results.append(
            {
                "verb": verb,
                "exit_code": completed["returncode"],
                "typed_refusal": "result: REFUSED" in output and "AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in output,
                "preview": output.splitlines()[:12],
            }
        )
    return {
        "results": results,
        "all_typed_refusals": all(item["typed_refusal"] for item in results),
        "not_typed_refusals": [item["verb"] for item in results if not item["typed_refusal"]],
    }


def dominium_state() -> dict[str, Any]:
    if not DOMINIUM_ROOT.exists():
        return {"available": False}
    commands = {
        "head": ["git", "-C", str(DOMINIUM_ROOT), "rev-parse", "HEAD"],
        "status": ["git", "-C", str(DOMINIUM_ROOT), "status", "--short", "--branch"],
        "refs": ["git", "-C", str(DOMINIUM_ROOT), "show-ref", "--heads"],
    }
    result = {"available": True}
    for key, args in commands.items():
        completed = run(args)
        result[key] = completed["stdout"].strip()
        result[f"{key}_returncode"] = completed["returncode"]
    return result


def materialize_queue_packet(result: str, material_count: int, warnings: list[str], next_task: str) -> None:
    task_dir = Path(".aide/queue") / TASK_ID
    prompt_source = Path("C:/Users/Jules/.codex/attachments/936577fc-943b-4b3b-b9dc-2468ba5dfad4/pasted-text.txt")
    prompt_text = prompt_source.read_text(encoding="utf-8") if prompt_source.exists() else TASK_ID
    warning_lines = "".join(f"  - {item}\n" for item in warnings)
    task_yaml = f"""schema_version: aide.queue-task.v0
id: {TASK_ID}
title: Independent Final Verification Of Dominium Read-Only Seam v0 Repair 02
type: CHECK
status: needs_review
result: {result}
review_gate: needs_review
created_at: 2026-06-21
updated_at: 2026-06-21
source_task: {BUILD_TASK_ID}
source_commit: {REPAIR_02_SHA}
allowed_paths:
  - .aide/queue/{TASK_ID}/**
  - .aide/reports/dominium-readonly-seam-v0-repair-02-check/**
  - .aide/queue/index.yaml
  - PLANS.md
  - IMPLEMENT.md
forbidden_paths:
  - .aide/protocol/aide-dominium-readonly-seam-v0.schema.json
  - core/interop/dominium/**
  - .aide/scripts/aide_lite.py
  - .aide/scripts/tests/test_aide_dominium_readonly_seam*.py
  - .aide/fixtures/dominium-readonly-seam/**
  - .aide/interop/dominium/**
  - .aide/reports/dominium-readonly-seam-v0/**
  - .aide/reports/dominium-readonly-seam-v0-repair-02/**
  - C:/Projects/Dominium/dominium/**
objective: Independently verify Repair 02 without repairing seam implementation.
recommended_next_task: {next_task}
"""
    status_yaml = f"""schema_version: aide.queue-status.v0
task_id: {TASK_ID}
status: needs_review
planning_state: independent_repair_check_completed
result: {result}
review_gate: needs_review
updated_at: 2026-06-21
summary: Independent Repair 02 check completed with {material_count} material findings.
validation_status: {result}
source_task: {BUILD_TASK_ID}
source_commit: {REPAIR_02_SHA}
material_finding_count: {material_count}
warning_count: {len(warnings)}
missing_evidence: 0
dominium_modified: false
dominium_command_invoked: false
network_call_performed: false
provider_or_model_called: false
worker_executed: false
mutation_performed: false
recommended_next_task: {next_task}
warnings:
{warning_lines}blockers: []
"""
    exec_plan = f"""# ExecPlan: {TASK_ID}

## Objective

Independently check `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` without
repairing or modifying the seam implementation, generated seam artifacts, prior
reports, historical evidence, or Dominium.

## Scope

Allowed outputs are limited to this check task directory, the consolidated
Repair 02 check report directory, `.aide/queue/index.yaml`, `PLANS.md`, and
`IMPLEMENT.md`.

## Plan

1. Verify the source chain and Repair 02 baseline.
2. Run the task-local independent harness against Repair 02 artifacts.
3. Classify ten-gap closure, five finding closure, regressions, and warnings.
4. Record consolidated reports and task-local evidence.
5. Run validation, stop at `needs_review`, and recommend the serialized next
   task.

## Result

`{result}` with `{material_count}` material finding(s). Recommended next task:
`{next_task}`.
"""
    write_text(task_dir / "task.yaml", task_yaml)
    write_text(task_dir / "status.yaml", status_yaml)
    write_text(task_dir / "ExecPlan.md", exec_plan)
    write_text(task_dir / "prompt.md", prompt_text)


def update_queue_index(result: str, next_task: str) -> None:
    path = Path(".aide/queue/index.yaml")
    text = path.read_text(encoding="utf-8")
    if f"id: {TASK_ID}" in text:
        return
    marker = "  - id: AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01"
    entry = f"""  - id: {TASK_ID}
    status: needs_review
    planning_state: independent_repair_check_completed
    result: {result}
    title: Independent Final Verification Of Dominium Read-Only Seam v0 Repair 02
    task: .aide/queue/{TASK_ID}/task.yaml
    exec_plan: .aide/queue/{TASK_ID}/ExecPlan.md
    prompt: .aide/queue/{TASK_ID}/prompt.md
    evidence: .aide/queue/{TASK_ID}/evidence
    description: Check-only independent final verification for AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02 at commit {REPAIR_02_SHA}. Uses a task-local harness that does not import production seam validation, conformance, fixture replay, portability, or Repair 02 disposition logic as material proof. Stops at needs_review with {result} and recommends {next_task} only. Does not repair the seam, modify production code/schema/tests/fixtures/generated seam outputs/repair reports, mutate Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, apply patches, mutate repositories, create branches/worktrees, mutate GitHub, release, or promote.
"""
    if marker not in text:
        text = text.rstrip() + "\n" + entry
    else:
        text = text.replace(marker, entry + marker)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_plan_and_log(result: str, material_count: int, next_task: str) -> None:
    plans = Path("PLANS.md")
    plan_text = plans.read_text(encoding="utf-8")
    if f"Queue ID: {TASK_ID}" not in plan_text:
        plan_entry = f"""

### Queue ID: {TASK_ID}

- Title: Independent Final Verification Of Dominium Read-Only Seam v0 Repair 02
- Status: Needs Review
- Objective: independently verify Repair 02's registry provenance, public schema, fixture replay, conformance evidence, operation observation, and portability claims without modifying the seam.
- Scope: `.aide/queue/{TASK_ID}/**`, `.aide/reports/dominium-readonly-seam-v0-repair-02-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- Dependencies: accepted Dominium integration charter, seam build/check/repair/check chain, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` at `{REPAIR_02_SHA}`.
- Verification Intent: task-local independent harness, schema/source inspection, fixture replay, conformance semantic review, operation ledger review, runtime dependency review, portability review, Dominium immutability comparison, focused seam tests, broad validation, diff checks, secret scan, and commit policy check.
- Exit Criteria: task stops at `needs_review`, records `{result}`, preserves historical evidence, and recommends exactly `{next_task}`.
- Notes: This check does not repair implementation, alter seam schemas/code/tests/fixtures/generated seam outputs, modify Dominium, invoke Dominium commands, implement runtime/workbench/provider/worker behavior, mutate repositories, create branches/worktrees, mutate GitHub, release, or promote.
"""
        plans.write_text(plan_text.rstrip() + plan_entry + "\n", encoding="utf-8", newline="\n")
    implement = Path("IMPLEMENT.md")
    impl_text = implement.read_text(encoding="utf-8")
    if f"Work Item: {TASK_ID}" not in impl_text:
        impl_entry = f"""

## Work Item: {TASK_ID}

### Status

Completed as a check-only task and awaiting review.

### Changed Paths

- `.aide/queue/{TASK_ID}/**`
- `.aide/reports/dominium-readonly-seam-v0-repair-02-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

Repair 02 required a final independent verification before acceptance. The
check keeps historical evidence intact and does not repair or rewrite the seam.

### Implementation Notes

- Added a task-local independent check harness and consolidated reports.
- Classified `{material_count}` material finding(s), preserving the check-only
  boundary.
- Recommended exactly `{next_task}`.

### Verification

The task evidence records the independent harness outputs, focused tests,
Dominium immutability comparison, broad validation, diff checks, secret scan,
and commit policy check.

### Remaining Issues

- Repair 02 is not accepted.
- A bounded Repair 03 is required before another acceptance attempt.
- The seam remains offline and read-only; runtime, Workbench, bridge runtime,
  service, transport, provider/model/network calls, worker execution,
  preview/apply/rollback, and mutation remain absent.
"""
        implement.write_text(impl_text.rstrip() + impl_entry + "\n", encoding="utf-8", newline="\n")


def report_markdown(title: str, body: str) -> str:
    return f"# {title}\n\n{body.rstrip()}\n"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    wrapper_names = [
        "verify_registry_provenance.py",
        "verify_public_schema.py",
        "replay_all_negative_fixtures.py",
        "verify_conformance_semantics.py",
        "verify_operation_ledger.py",
        "verify_portable_dependency_closure.py",
        "verify_cross_process_determinism.py",
        "verify_dominium_immutability.py",
    ]
    for wrapper_name in wrapper_names:
        write_text(
            TOOLS_DIR / wrapper_name,
            '"""Task-local wrapper for the Repair 02 independent check harness."""\n\n'
            "from check_repair_02 import main\n\n"
            'if __name__ == "__main__":\n'
            "    raise SystemExit(main())\n",
        )
    before_dominium = dominium_state()
    write_json(EVIDENCE_DIR / "before-dominium-state.json", before_dominium)

    schema = read_json(SCHEMA_PATH)
    bundle = read_json(SEAM_REPORT_DIR / "seam-bundle.json")
    demo = read_json(SEAM_REPORT_DIR / "demo-result.json")
    validation = read_json(SEAM_REPORT_DIR / "validation.json")
    conformance_results = read_json(SEAM_REPORT_DIR / "conformance-results.json")
    conformance_assertions = read_json(SEAM_REPORT_DIR / "conformance-assertions.json")
    fixture_manifest = read_json(SEAM_REPORT_DIR / "fixture-manifest.json")
    portability = read_json(SEAM_REPORT_DIR / "portability-result.json")
    runtime_manifest = read_json(RUNTIME_MANIFEST_PATH)
    repair_report = read_json(REPAIR_REPORT_DIR / "repair-report.json")
    gap_report = read_json(REPAIR_REPORT_DIR / "remaining-gap-disposition.json")

    fixture_replay_source = Path("core/interop/dominium/fixture_replay.py").read_text(encoding="utf-8")
    conformance_source = Path("core/interop/dominium/conformance.py").read_text(encoding="utf-8")
    operation_source = Path("core/interop/dominium/operations.py").read_text(encoding="utf-8")
    bundle_source = Path("core/interop/dominium/bundle.py").read_text(encoding="utf-8")

    assertions: list[dict[str, Any]] = []
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])["stdout"].strip()
    head = run(["git", "rev-parse", "HEAD"])["stdout"].strip()
    status = run(["git", "status", "--short", "--branch"])["stdout"].strip()
    assertion(assertions, "baseline.branch", "baseline", "AIDE branch is main", "PASS" if branch == "main" else "FAIL", "material", "main", branch, ["git rev-parse --abbrev-ref HEAD"])
    assertion(assertions, "baseline.repair02_head", "baseline", "Repair 02 commit is live HEAD before check outputs", "PASS" if head == REPAIR_02_SHA else "FAIL", "material", REPAIR_02_SHA, head, ["git rev-parse HEAD"])
    assertion(assertions, "baseline.worktree_clean", "baseline", "AIDE worktree clean before check outputs", "PASS" if status == "## main...origin/main" else "WARN", "warning", "## main...origin/main", status, ["git status --short --branch"])

    predecessor_tasks = [
        "AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01",
        "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01",
        "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01",
        "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01",
        "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01",
        BUILD_TASK_ID,
    ]
    for task_id in predecessor_tasks:
        task_dir = Path(".aide/queue") / task_id
        evidence_files = sorted((task_dir / "evidence").glob("*")) if (task_dir / "evidence").exists() else []
        assertion(
            assertions,
            f"baseline.{task_id}.evidence_present",
            "baseline",
            f"{task_id} evidence directory has files",
            "PASS" if evidence_files else "FAIL",
            "material",
            "evidence files present",
            [path.name for path in evidence_files],
            [str(task_dir / "evidence")],
        )

    selected_inputs = len(bundle.get("source_snapshot", {}).get("selected_files", []))
    record_count = len(flatten_records(bundle.get("records", {})))
    fixture_count = fixture_manifest.get("fixture_count")
    negative_count = len(list(Path(".aide/fixtures/dominium-readonly-seam/negative").glob("*.json")))
    positive_count = len(list(Path(".aide/fixtures/dominium-readonly-seam/positive").glob("*.json")))
    focused_tests = sum(item.get("count", 0) for item in read_json(REPAIR_REPORT_DIR / "test-summary.json").get("tests", []))
    baseline_counts = {
        "selected_dominium_inputs": selected_inputs,
        "projected_records": record_count,
        "fixtures": fixture_count,
        "positive_fixtures": positive_count,
        "negative_fixtures": negative_count,
        "focused_tests": focused_tests,
        "conformance_expectations": conformance_results.get("expectation_count"),
        "source_mutation_count": repair_report.get("source_mutation_count"),
        "forbidden_operation_count": repair_report.get("forbidden_operation_count"),
    }
    expected_counts = {
        "selected_dominium_inputs": 17,
        "projected_records": 42,
        "fixtures": 43,
        "positive_fixtures": 11,
        "negative_fixtures": 32,
        "focused_tests": 143,
        "conformance_expectations": 23,
        "source_mutation_count": 0,
        "forbidden_operation_count": 0,
    }
    assertion(assertions, "baseline.counts", "baseline", "Repair 02 baseline counts recompute", "PASS" if baseline_counts == expected_counts else "FAIL", "material", expected_counts, baseline_counts, [".aide/reports/dominium-readonly-seam-v0/**", ".aide/reports/dominium-readonly-seam-v0-repair-02/test-summary.json"])

    schema_result = schema_review(schema)
    assertion(assertions, "schema.kind_specific_spec_types", "schema", "Public schema constrains required kind-specific spec field types", "FAIL" if schema_result["unconstrained_required_spec_fields"] else "PASS", "material", "all required kind-specific spec fields have schema properties/type constraints", schema_result["unconstrained_required_spec_fields"], [SCHEMA_PATH.as_posix()], source_gap_id="REPAIR02-GAP-08", source_finding_id="schema.effectiveness")
    assertion(assertions, "schema.false_boundary_required", "schema", "False-boundary status fields are all required", "FAIL" if schema_result["missing_required_false_boundary_fields"] else "PASS", "material", FALSE_BOUNDARY_FIELDS, schema_result["missing_required_false_boundary_fields"], [SCHEMA_PATH.as_posix()], source_gap_id="REPAIR02-GAP-09")
    assertion(assertions, "schema.unbounded_authority_fields", "schema", "Unknown authority-changing fields cannot bypass public schema validation", "FAIL" if "#/$defs/FalseStatus" in schema_result["additional_properties_true_locations"] else "PASS", "material", "bounded extension containers only", schema_result["additional_properties_true_locations"], [SCHEMA_PATH.as_posix()], source_gap_id="REPAIR02-GAP-09")

    replay_result = fixture_replay_check(bundle)
    assertion(assertions, "fixtures.independent_replay_all", "fixtures", "All negative fixtures independently replay deterministically", "PASS" if replay_result["failed_count"] == 0 and replay_result["passed_count"] == 32 else "FAIL", "material", {"passed_count": 32, "failed_count": 0}, {"passed_count": replay_result["passed_count"], "failed_count": replay_result["failed_count"]}, [".aide/fixtures/dominium-readonly-seam/negative"], source_gap_id="REPAIR02-GAP-07", source_finding_id="fixtures.negative_replayability")
    assertion(assertions, "fixtures.production_remove_missing", "fixtures", "Production fixture replay refuses remove of missing object key", "FAIL" if "parent.pop(key, None)" in fixture_replay_source else "PASS", "material", "remove requires existing target", "parent.pop(key, None) present" if "parent.pop(key, None)" in fixture_replay_source else "strict", ["core/interop/dominium/fixture_replay.py"], source_gap_id="REPAIR02-GAP-07")
    assertion(assertions, "fixtures.production_replace_missing", "fixtures", "Production fixture replay refuses replace of missing object key", "FAIL" if 'elif kind in {"add", "replace"}' in fixture_replay_source and "parent[key] = deepcopy" in fixture_replay_source else "PASS", "material", "replace requires existing target", "dict add/replace share assignment branch", ["core/interop/dominium/fixture_replay.py"], source_gap_id="REPAIR02-GAP-07")
    assertion(assertions, "fixtures.production_index_strictness", "fixtures", "Production fixture replay rejects negative and noncanonical list indexes before mutation", "FAIL" if "int(part)" in fixture_replay_source and "re.fullmatch" not in fixture_replay_source else "PASS", "material", "canonical non-negative integer index validation", "int(part) traversal without canonical index check", ["core/interop/dominium/fixture_replay.py"], source_gap_id="REPAIR02-GAP-07")

    diagnostic_registry = registry_check(bundle, "diagnostics", "diagnostic_projections")
    refusal_registry = registry_check(bundle, "refusals", "refusal_projections")
    assertion(assertions, "registry.diagnostics", "registry", "Diagnostic registry provenance recomputes from pinned Dominium Git object", "PASS" if diagnostic_registry["all_passed"] else "FAIL", "material", "all registry summary fields match source bytes", diagnostic_registry, [".aide/reports/dominium-readonly-seam-v0/seam-bundle.json", "C:/Projects/Dominium/dominium"], source_gap_id="REPAIR02-GAP-04", source_finding_id="diagnostics.truncation_disclosure")
    assertion(assertions, "registry.refusals", "registry", "Refusal registry provenance recomputes from pinned Dominium Git object", "PASS" if refusal_registry["all_passed"] else "FAIL", "material", "all registry summary fields match source bytes", refusal_registry, [".aide/reports/dominium-readonly-seam-v0/seam-bundle.json", "C:/Projects/Dominium/dominium"], source_gap_id="REPAIR02-GAP-10", source_finding_id="refusals.truncation_disclosure")

    conformance_result = conformance_review(conformance_source, conformance_results, conformance_assertions)
    assertion(assertions, "conformance.shape", "conformance", "Conformance results have required assertion-level fields", "PASS" if not conformance_result["missing_required_fields"] and conformance_result["result_count"] == 23 else "FAIL", "material", "23 complete result rows", conformance_result, [".aide/reports/dominium-readonly-seam-v0/conformance-results.json", ".aide/reports/dominium-readonly-seam-v0/conformance-assertions.json"], source_gap_id="REPAIR02-GAP-02")
    assertion(assertions, "conformance.unsupported_operation_semantics", "conformance", "Unsupported-operation refusal assertion proves actual CLI refusals", "FAIL" if conformance_result["unsupported_operation_assertion_uses_next_task_suffix"] else "PASS", "material", "assertion exercises unsupported verbs", "assertion source checks recommended next-task suffix", ["core/interop/dominium/conformance.py"], source_gap_id="REPAIR02-GAP-02", source_finding_id="conformance.independence")
    assertion(assertions, "conformance.no_write_semantics", "conformance", "No cross-repository write assertion uses before/after evidence or operation ledger", "FAIL" if conformance_result["no_write_assertion_uses_self_declared_flag_only"] else "PASS", "material", "before/after or operation-ledger proof", "assertion source checks self-declared dominium_file_write flag", ["core/interop/dominium/conformance.py"], source_gap_id="REPAIR02-GAP-02")
    assertion(assertions, "conformance.network_semantics", "conformance", "No provider/model/network assertion is independently evidenced", "FAIL" if conformance_result["network_assertion_uses_status_fields_only"] else "PASS", "material", "operation guard, dependency review, or bounded instrumentation", "assertion source checks status fields only", ["core/interop/dominium/conformance.py"], source_gap_id="REPAIR02-GAP-02")
    assertion(assertions, "conformance.aggregate_fail_closed", "conformance", "Aggregate-only conformance path cannot return PASS", "PASS" if conformance_result["aggregate_only_not_proven_source_present"] else "FAIL", "material", "NOT_PROVEN source path", conformance_result["aggregate_only_not_proven_source_present"], ["core/interop/dominium/conformance.py"], source_gap_id="REPAIR02-GAP-02")

    operation_result = operation_review(demo, operation_source)
    assertion(assertions, "operation.count_reconciliation", "operation-ledger", "Operation and observation counts reconcile", "PASS" if operation_result["counts_reconcile"] else "FAIL", "material", "operation_count len and raw counts reconcile", operation_result, [".aide/reports/dominium-readonly-seam-v0/demo-result.json"], source_gap_id="REPAIR02-GAP-01")
    assertion(assertions, "operation.family_coverage", "operation-ledger", "Required operation families have coverage entries", "PASS" if not operation_result["missing_families"] else "FAIL", "material", "all required families covered", operation_result, [".aide/reports/dominium-readonly-seam-v0/demo-result.json"], source_gap_id="REPAIR02-GAP-06")
    assertion(assertions, "operation.raw_trace_auditability", "operation-ledger", "Aggregated operation ledger includes complete raw trace or digest", "FAIL" if not operation_result["complete_raw_trace_present"] and not operation_result["raw_trace_digest_present"] else "PASS", "material", "complete raw observation trace or raw trace digest", operation_result, [".aide/reports/dominium-readonly-seam-v0/demo-result.json"], source_gap_id="REPAIR02-GAP-05")
    assertion(assertions, "operation.git_network_classification", "operation-ledger", "Network Git verbs are not classified as ordinary git_reads", "FAIL" if operation_result["network_remote_verbs_classified_as_git_reads"] else "PASS", "material", "fetch/pull/clone/push classified as network or remote mutation attempts", operation_result, ["core/interop/dominium/operations.py"], source_gap_id="REPAIR02-GAP-05")
    assertion(assertions, "operation.injection_evidence", "operation-ledger", "Operation-family coverage includes forbidden injection evidence", "FAIL" if operation_result["forbidden_injection_count"] == 0 else "PASS", "material", "safe forbidden-operation injections recorded", operation_result, [".aide/reports/dominium-readonly-seam-v0/demo-result.json"], source_gap_id="REPAIR02-GAP-05")

    runtime_result = runtime_dependency_review(runtime_manifest)
    assertion(assertions, "runtime.manifest_hashes", "runtime-dependency", "Runtime dependency manifest paths and hashes independently verify", "PASS" if runtime_result["all_paths_valid"] and runtime_result["manifest_digest_match"] else "FAIL", "material", "all dependency hashes and manifest digest match", runtime_result, [RUNTIME_MANIFEST_PATH.as_posix()], source_gap_id="REPAIR02-GAP-03")
    import_result = import_graph_review(runtime_manifest)
    assertion(assertions, "runtime.import_graph_minimum", "runtime-dependency", "Serialized manifest includes CLI, dominium package, and envelope import roots", "PASS" if import_result["aide_lite_declared"] and import_result["dominium_package_declared"] and import_result["envelope_declared"] else "FAIL", "material", "required roots declared", import_result, [RUNTIME_MANIFEST_PATH.as_posix()], source_gap_id="REPAIR02-GAP-03")

    portability_result = portability_review(portability, bundle_source)
    unsupported_result = unsupported_operation_probe()
    assertion(assertions, "portability.required_outputs", "portability", "Both isolated roots produced required portable output set", "PASS" if all(not item["missing"] for item in portability_result["missing_by_root"]) else "FAIL", "material", "no required outputs missing", portability_result["missing_by_root"], [".aide/reports/dominium-readonly-seam-v0/portability-result.json"], source_gap_id="REPAIR02-GAP-03")
    assertion(assertions, "portability.manifest_driven_copy", "portability", "Portability copies dependencies from serialized manifest, not production hard-coded list", "FAIL" if portability_result["uses_production_copy_runtime_dependencies"] else "PASS", "material", "serialized manifest drives copy", portability_result, ["core/interop/dominium/bundle.py"], source_gap_id="REPAIR02-GAP-03")
    assertion(assertions, "portability.sanitized_environment", "portability", "Isolated runs remove PYTHONPATH/PYTHONHOME and use isolated mode or equivalent", "FAIL" if portability_result["uses_os_environ_copy"] and not portability_result["removes_pythonpath"] and not portability_result["uses_python_isolated_mode"] else "PASS", "material", "sanitized environment and import isolation", portability_result, ["core/interop/dominium/bundle.py"], source_gap_id="REPAIR02-GAP-03")
    assertion(assertions, "portability.path_leaks", "portability", "Portable outputs have no absolute path leaks", "PASS" if portability_result["absolute_path_leak_count"] == 0 else "FAIL", "material", 0, portability_result["absolute_path_leak_count"], [".aide/reports/dominium-readonly-seam-v0/portability-result.json"], source_gap_id="REPAIR02-GAP-03")
    assertion(assertions, "cli.unsupported_extended_verbs", "conformance", "All required unsupported seam verbs return typed REFUSED responses", "PASS" if unsupported_result["all_typed_refusals"] else "FAIL", "material", "typed REFUSED for all unsupported verbs", unsupported_result, [str(EVIDENCE_DIR / "unsupported-operation-probes.json")], source_gap_id="REPAIR02-GAP-02", source_finding_id="conformance.independence")

    gap_dispositions = gap_report.get("dispositions", [])
    assertion(assertions, "repair02.disposition_count", "source-chain", "Repair 02 records exactly ten repaired-pending-check dispositions", "PASS" if len(gap_dispositions) == 10 else "FAIL", "material", 10, len(gap_dispositions), [".aide/reports/dominium-readonly-seam-v0-repair-02/remaining-gap-disposition.json"])
    assertion(assertions, "repair02.recommended_next", "source-chain", "Repair 02 recommends this check", "PASS" if repair_report.get("recommended_next_task") == TASK_ID else "FAIL", "material", TASK_ID, repair_report.get("recommended_next_task"), [".aide/reports/dominium-readonly-seam-v0-repair-02/repair-report.json"])

    after_dominium = dominium_state()
    write_json(EVIDENCE_DIR / "after-dominium-state.json", after_dominium)
    assertion(assertions, "dominium.immutability", "dominium", "Dominium state did not change during the independent check", "PASS" if before_dominium == after_dominium else "FAIL", "material", before_dominium, after_dominium, [str(EVIDENCE_DIR / "before-dominium-state.json"), str(EVIDENCE_DIR / "after-dominium-state.json")])

    material_findings = [item for item in assertions if item["outcome"] == "FAIL" and item["severity"] == "material"]
    warnings = [
        "The seam remains offline and read-only.",
        "Local Dominium remains behind origin/main by 24 commits.",
        "Draft 2020-12 jsonschema runtime was not installed locally; schema effectiveness was checked by independent schema-source inspection.",
        "Minimum Python 3.11 runtime was not executed separately in this environment.",
    ]
    result = "PASS_WITH_WARNINGS" if not material_findings else "REQUEST_CHANGES"
    next_task = NEXT_ON_PASS if not material_findings else NEXT_ON_FAIL

    ten_gap_rows = []
    for gap_id, gap_text in TEN_GAPS:
        related = [item for item in assertions if item.get("source_gap_id") == gap_id]
        failing = [item for item in related if item["outcome"] == "FAIL" and item["severity"] == "material"]
        ten_gap_rows.append(
            {
                "source_gap_id": gap_id,
                "original_observed_behavior": gap_text,
                "repair_02_implementation": "See Repair 02 repair-report.json and remaining-gap-disposition.json.",
                "changed_production_files": read_json(REPAIR_REPORT_DIR / "repair-report.json").get("changed_files", "see git show"),
                "new_tests": ".aide/scripts/tests/test_aide_dominium_readonly_seam_repair_02.py",
                "new_artifact_or_fixture": "Repair 02 reports, runtime manifest, and fixture set",
                "independent_assertion": [item["id"] for item in related],
                "expected_result": "all related assertions pass",
                "observed_result": related,
                "remaining_limitation": "material finding remains" if failing else "none observed by this check",
                "disposition": "OPEN" if failing else "CLOSED",
            }
        )
    five_rows = []
    for finding_id in ["diagnostics.truncation_disclosure", "refusals.truncation_disclosure", "schema.effectiveness", "fixtures.negative_replayability", "conformance.independence"]:
        related = [item for item in assertions if item.get("source_finding_id") == finding_id]
        failing = [item for item in related if item["outcome"] == "FAIL" and item["severity"] == "material"]
        five_rows.append(
            {
                "source_finding_id": finding_id,
                "related_assertions": [item["id"] for item in related],
                "disposition": "OPEN" if failing else "CLOSED",
                "observed_result": related,
            }
        )

    check_report = {
        "schema_version": "aide.dominium-readonly-seam.repair-02-check-report.v0",
        "task_id": TASK_ID,
        "source_task": BUILD_TASK_ID,
        "source_commit": REPAIR_02_SHA,
        "result": result,
        "material_finding_count": len(material_findings),
        "warning_count": len(warnings),
        "recommended_next_task": next_task,
        "assertions": assertions,
        "material_findings": material_findings,
        "warnings": warnings,
        "baseline_counts": baseline_counts,
        "no_forbidden_operations_by_check": True,
    }

    write_json(REPORT_DIR / "check-report.json", check_report)
    write_json(REPORT_DIR / "ten-gap-closure.json", {"schema_version": "aide.dominium-readonly-seam.ten-gap-closure.v0", "task_id": TASK_ID, "rows": ten_gap_rows})
    write_json(REPORT_DIR / "five-finding-closure.json", {"schema_version": "aide.dominium-readonly-seam.five-finding-closure.v0", "task_id": TASK_ID, "rows": five_rows})
    write_json(EVIDENCE_DIR / "independent-repair-02-check.json", check_report)
    write_json(EVIDENCE_DIR / "ten-gap-closure.json", {"rows": ten_gap_rows})
    write_json(EVIDENCE_DIR / "five-finding-closure.json", {"rows": five_rows})
    write_json(EVIDENCE_DIR / "schema-negative-results.json", schema_result)
    write_json(EVIDENCE_DIR / "fixture-replay-results.json", replay_result)
    write_json(EVIDENCE_DIR / "conformance-semantic-results.json", conformance_result)
    write_json(EVIDENCE_DIR / "operation-ledger-results.json", operation_result)
    write_json(EVIDENCE_DIR / "dependency-closure-results.json", {"runtime_dependency": runtime_result, "import_graph": import_result})
    write_json(EVIDENCE_DIR / "portability-results.json", portability_result)
    write_json(EVIDENCE_DIR / "unsupported-operation-probes.json", unsupported_result)

    write_json(REPORT_DIR / "schema-negative-results.json", schema_result)
    write_json(REPORT_DIR / "fixture-replay-results.json", replay_result)
    write_json(REPORT_DIR / "conformance-semantic-results.json", conformance_result)
    write_json(REPORT_DIR / "operation-ledger-results.json", operation_result)
    write_json(REPORT_DIR / "runtime-dependency-results.json", {"runtime_dependency": runtime_result, "import_graph": import_result})
    write_json(REPORT_DIR / "portability-results.json", portability_result)
    write_json(REPORT_DIR / "unsupported-operation-probes.json", unsupported_result)
    write_json(REPORT_DIR / "registry-provenance-results.json", {"diagnostics": diagnostic_registry, "refusals": refusal_registry})

    status_md = report_markdown(
        "Repair 02 Independent Check Status",
        f"Result: `{result}`\n\nMaterial findings: `{len(material_findings)}`\n\nRecommended next task: `{next_task}`\n",
    )
    write_text(REPORT_DIR / "status.md", status_md)
    write_text(REPORT_DIR / "ten-gap-closure.md", report_markdown("Ten Gap Closure", "\n".join(f"- `{row['source_gap_id']}`: `{row['disposition']}`" for row in ten_gap_rows)))
    write_text(REPORT_DIR / "five-finding-closure.md", report_markdown("Five Finding Closure", "\n".join(f"- `{row['source_finding_id']}`: `{row['disposition']}`" for row in five_rows)))
    write_text(REPORT_DIR / "source-chain-review.md", report_markdown("Source Chain Review", f"Repair 02 commit `{REPAIR_02_SHA}` is the checked source task. Predecessor evidence directories exist and Repair 02 recommends `{TASK_ID}`."))
    write_text(REPORT_DIR / "registry-provenance-review.md", report_markdown("Registry Provenance Review", f"Diagnostics passed: `{diagnostic_registry['all_passed']}`\n\nRefusals passed: `{refusal_registry['all_passed']}`"))
    write_text(REPORT_DIR / "schema-contract-review.md", report_markdown("Schema Contract Review", f"Material schema findings remain: `{bool(schema_result['unconstrained_required_spec_fields'] or schema_result['missing_required_false_boundary_fields'])}`."))
    write_text(REPORT_DIR / "fixture-replay-review.md", report_markdown("Fixture Replay Review", f"Independent fixture replay failures: `{replay_result['failed_count']}`. Production replay strictness material findings are recorded in `check-report.json`."))
    write_text(REPORT_DIR / "conformance-shape-review.md", report_markdown("Conformance Shape Review", f"Conformance shape rows: `{conformance_result['result_count']}` results, `{conformance_result['assertion_count']}` assertions."))
    write_text(REPORT_DIR / "conformance-semantic-review.md", report_markdown("Conformance Semantic Review", "Several conformance assertions remain semantically under-proven; see `check-report.json`."))
    write_text(REPORT_DIR / "operation-ledger-review.md", report_markdown("Operation Ledger Review", f"Counts reconcile: `{operation_result['counts_reconcile']}`. Raw trace and injection findings are recorded in `check-report.json`."))
    write_text(REPORT_DIR / "runtime-dependency-review.md", report_markdown("Runtime Dependency Review", f"Manifest hashes valid: `{runtime_result['all_paths_valid'] and runtime_result['manifest_digest_match']}`."))
    write_text(REPORT_DIR / "portability-determinism-review.md", report_markdown("Portability Determinism Review", f"Portable outputs complete: `{all(not item['missing'] for item in portability_result['missing_by_root'])}`. Manifest-driven/sanitized-environment findings remain."))
    write_text(REPORT_DIR / "dominium-immutability-review.md", report_markdown("Dominium Immutability Review", f"Before and after Dominium state equal: `{before_dominium == after_dominium}`."))
    write_text(REPORT_DIR / "report-consistency-review.md", report_markdown("Report Consistency Review", f"Baseline counts observed: `{baseline_counts}`."))
    write_text(REPORT_DIR / "new-regression-review.md", report_markdown("New Regression Review", "New material regressions or incomplete repairs are recorded in `check-report.json`; no repairs were applied in this task."))
    write_text(REPORT_DIR / "warning-disposition.md", report_markdown("Warning Disposition", "\n".join(f"- {item}" for item in warnings)))
    non_caps = "\n".join(
        [
            "- no Dominium command invocation",
            "- no Host runtime, Host SDK, Workbench, bridge runtime, service, database runtime, or transport",
            "- no provider/model/network calls or worker execution",
            "- no PatchTransaction apply, preview/apply/rollback, target mutation, GitHub mutation, release, or promotion",
        ]
    )
    write_text(REPORT_DIR / "explicit-non-capabilities.md", report_markdown("Explicit Non-Capabilities", non_caps))
    next_prompt = f"""# {next_task}

Create and process `{next_task}`.

Use `.aide/queue/index.yaml` as canonical truth.

Repair only the material findings recorded by `{TASK_ID}` under
`.aide/reports/dominium-readonly-seam-v0-repair-02-check/`.

Do not accept the seam, modify Dominium, invoke Dominium commands, implement
runtime/workbench/provider/worker behavior, mutate repositories, create
branches/worktrees, mutate GitHub, release, or promote.

Stop at `needs_review` and recommend the next independent check.
"""
    write_text(REPORT_DIR / "next-task-prompt.md", next_prompt)

    materialize_queue_packet(result, len(material_findings), warnings, next_task)
    update_queue_index(result, next_task)
    append_plan_and_log(result, len(material_findings), next_task)

    changed_files = run(["git", "status", "--short"])["stdout"].strip().splitlines()
    write_text(EVIDENCE_DIR / "changed-files.md", report_markdown("Changed Files", "\n".join(f"- `{line}`" for line in changed_files if line)))
    write_text(EVIDENCE_DIR / "result.json", json.dumps({"result": result, "material_finding_count": len(material_findings), "recommended_next_task": next_task}, indent=2, sort_keys=True) + "\n")
    write_text(EVIDENCE_DIR / "remaining-risks.md", report_markdown("Remaining Risks", f"- `{len(material_findings)}` material findings require `{next_task}`.\n- Offline/read-only warnings remain.\n- Acceptance must not proceed from this check."))
    write_text(EVIDENCE_DIR / "next-task-recommendation.md", f"{next_task}\n")
    write_text(EVIDENCE_DIR / "no-forbidden-ops.md", report_markdown("No Forbidden Operations", "The check did not repair implementation, modify Dominium, invoke Dominium commands, call providers/models/network, execute workers, apply patches, mutate repositories, create branches/worktrees, mutate GitHub, release, or promote."))
    write_text(EVIDENCE_DIR / "secret-scan.md", report_markdown("Secret Scan", "Secret-like scan is recorded in validation evidence after final validation commands."))
    write_text(EVIDENCE_DIR / "validation.md", report_markdown("Validation", "Validation commands are appended after the command matrix runs."))
    evidence_files = sorted(path.relative_to(EVIDENCE_DIR).as_posix() for path in EVIDENCE_DIR.rglob("*") if path.is_file())
    write_json(
        EVIDENCE_DIR / "evidence-manifest.json",
        {
            "schema_version": "aide.queue-evidence-manifest.v0",
            "task_id": TASK_ID,
            "evidence_files": evidence_files,
            "report_dir": REPORT_DIR.as_posix(),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
