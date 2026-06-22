from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04"
SOURCE_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04"
SOURCE_COMMIT = "270b97dc66e477cd37a2f863c8604854a5e90bdf"
PREVIOUS_CHECK_TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03"
PREVIOUS_CHECK_COMMIT = "8d5cb86fa7f82d3da9d4856fa43b7102e0f16286"
NEXT_ACCEPT = "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"
NEXT_REPAIR = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05"
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

REPAIR_04_FINDINGS = [
    "schema.kind_specific_defs_present",
    "schema.authority_extensions_bounded",
    "fixture.production_requires_value",
    "fixture.production_rejects_unicode_decimal_indexes",
    "fixture.production_forbidden_key_set_complete",
    "conformance.unsupported_uses_actual_cli_dispatch",
    "conformance.no_write_surrounds_actual_operations",
    "conformance.guard_evidence_is_exercised",
    "operation.aggregate_key_preserves_semantics",
    "operation.guard_report_is_not_static",
    "portability.required_child_output_set_complete",
    "cli.unsupported_verbs_typed_refusal",
]

RECORD_DEFS = {
    "HostManifest": "HostManifestRecord",
    "HostCapabilitySet": "HostCapabilitySetRecord",
    "WorkspaceDescriptor": "WorkspaceDescriptorRecord",
    "ContextDescriptor": "ContextDescriptorRecord",
    "ArtifactReference": "ArtifactReferenceRecord",
    "DiagnosticProjection": "DiagnosticProjectionRecord",
    "RefusalProjection": "RefusalProjectionRecord",
    "EvidenceReferenceSet": "EvidenceReferenceSetRecord",
    "EventEnvelope": "EventEnvelopeRecord",
    "DominiumBridgeManifest": "DominiumBridgeManifestRecord",
}

RECORD_CONTAINERS = {
    "HostManifest": ("host_manifest", None),
    "HostCapabilitySet": ("host_capability_set", None),
    "WorkspaceDescriptor": ("workspace_descriptor", None),
    "ContextDescriptor": ("context_descriptor", None),
    "ArtifactReference": ("artifact_references", 0),
    "DiagnosticProjection": ("diagnostic_projections", 0),
    "RefusalProjection": ("refusal_projections", 0),
    "EvidenceReferenceSet": ("evidence_reference_set", None),
    "EventEnvelope": ("event_envelopes", 0),
    "DominiumBridgeManifest": ("dominium_bridge_manifest", None),
}

CROSS_KIND_SUBSTITUTIONS = [
    ("HostManifest", "ContextDescriptor"),
    ("ContextDescriptor", "HostManifest"),
    ("ArtifactReference", "DiagnosticProjection"),
    ("DiagnosticProjection", "RefusalProjection"),
    ("EventEnvelope", "ArtifactReference"),
    ("DominiumBridgeManifest", "HostCapabilitySet"),
]

AUTHORITY_EXTENSION_NAMES = [
    "authoritative",
    "canonical",
    "trusted",
    "admitted",
    "workbench_is_authority",
    "runtime_started",
    "private_tool_bypass",
    "command_invocation_implemented",
    "network_allowed",
    "provider_enabled",
    "worker_enabled",
    "mutation_allowed",
    "apply_allowed",
    "release_allowed",
]

FIXTURE_FORBIDDEN_KEYS = [
    "import",
    "args",
    "kwargs",
    "callable",
    "module",
    "command",
    "shell",
    "eval",
    "exec",
    "python",
    "entrypoint",
    "script",
    "function",
    "method",
    "code",
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
    "random-unknown-verb-1",
    "random-unknown-verb-2",
    "unknown-123",
    "future-operation",
    "xyzzy",
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

EXPLICIT_NON_CAPABILITIES = [
    "dominium_command_invocation",
    "host_runtime",
    "host_sdk",
    "workbench_implementation",
    "bridge_runtime",
    "service",
    "database_runtime",
    "transport",
    "network_call",
    "provider_model_call",
    "worker_execution",
    "patch_transaction_apply",
    "preview_apply_rollback",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").exists() and (parent / ".aide").is_dir():
            return parent
    raise RuntimeError("could not locate repo root")


ROOT = find_repo_root()
EVIDENCE = ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04-check"


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


def compact_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str], *, cwd: Path | None = None, timeout: int = 120, env: dict[str, str] | None = None) -> dict[str, Any]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd or ROOT),
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        timed_out = False
        returncode = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        returncode = 124
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
    return {
        "args": args,
        "cwd": rel(cwd or ROOT),
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_seconds": round(time.monotonic() - start, 3),
        "stdout": stdout,
        "stderr": stderr,
        "stdout_lines": stdout.splitlines(),
        "stderr_lines": stderr.splitlines(),
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


def walk(value: Any, path: str = ""):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}/{index}")


def resolve_ref(schema: dict[str, Any], ref_value: str) -> Any:
    if not ref_value.startswith("#/"):
        raise KeyError(ref_value)
    current: Any = schema
    for raw in ref_value[2:].split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        current = current[part]
    return current


def ref_exists(schema: dict[str, Any], ref_value: str) -> bool:
    try:
        resolve_ref(schema, ref_value)
        return True
    except Exception:
        return False


def schema_errors(schema: dict[str, Any], node: dict[str, Any], value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "$ref" in node:
        try:
            return schema_errors(schema, resolve_ref(schema, str(node["$ref"])), value, path)
        except Exception as exc:
            return [f"{path}: unresolved ref {node.get('$ref')}: {exc}"]
    if "allOf" in node:
        for index, child in enumerate(node["allOf"]):
            errors.extend(schema_errors(schema, child, value, f"{path}.allOf[{index}]"))
    if "oneOf" in node:
        matches = [index for index, child in enumerate(node["oneOf"]) if not schema_errors(schema, child, value, f"{path}.oneOf[{index}]")]
        if len(matches) != 1:
            errors.append(f"{path}: oneOf expected exactly one match, observed {matches}")
    if "not" in node and not schema_errors(schema, node["not"], value, path):
        errors.append(f"{path}: value matched forbidden not-schema")
    if "const" in node and value != node["const"]:
        errors.append(f"{path}: expected const {node['const']!r}, observed {value!r}")
    if "enum" in node and value not in node["enum"]:
        errors.append(f"{path}: expected enum {node['enum']!r}, observed {value!r}")
    typ = node.get("type")
    if typ:
        type_ok = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": (isinstance(value, int | float) and not isinstance(value, bool)),
            "boolean": isinstance(value, bool),
            "null": value is None,
        }.get(str(typ), True)
        if not type_ok:
            errors.append(f"{path}: expected type {typ}, observed {type(value).__name__}")
            return errors
    if "pattern" in node and isinstance(value, str) and not re.fullmatch(str(node["pattern"]), value):
        errors.append(f"{path}: pattern mismatch {node['pattern']!r}: {value!r}")
    if "minimum" in node and isinstance(value, int | float) and value < node["minimum"]:
        errors.append(f"{path}: minimum {node['minimum']} violated by {value}")
    if isinstance(value, dict):
        props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
        for field in node.get("required", []) if isinstance(node.get("required"), list) else []:
            if field not in value:
                errors.append(f"{path}: missing required field {field}")
        for field, child in props.items():
            if field in value:
                errors.extend(schema_errors(schema, child, value[field], f"{path}.{field}"))
        if "propertyNames" in node:
            for field in value:
                errors.extend(schema_errors(schema, node["propertyNames"], field, f"{path}.{field}<propertyName>"))
        additional = node.get("additionalProperties", None)
        extras = [field for field in value if field not in props]
        if additional is False and extras:
            errors.append(f"{path}: additional properties not allowed: {extras}")
        elif isinstance(additional, dict):
            for field in extras:
                errors.extend(schema_errors(schema, additional, value[field], f"{path}.{field}"))
    if isinstance(value, list) and isinstance(node.get("items"), dict):
        for index, item in enumerate(value):
            errors.extend(schema_errors(schema, node["items"], item, f"{path}[{index}]"))
    return errors


def record_from_bundle(bundle: dict[str, Any], kind: str) -> dict[str, Any]:
    container, index = RECORD_CONTAINERS[kind]
    value = bundle["records"][container]
    if index is None:
        return copy.deepcopy(value)
    return copy.deepcopy(value[index])


def validate_record(schema: dict[str, Any], record: dict[str, Any], kind: str) -> list[str]:
    return schema_errors(schema, schema["$defs"][RECORD_DEFS[kind]], record, f"record[{kind}]")


def mutate_path(document: Any, parts: list[str], value: Any, *, remove: bool = False) -> Any:
    candidate = copy.deepcopy(document)
    current = candidate
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    final = parts[-1]
    if remove:
        if isinstance(current, list):
            current.pop(int(final))
        else:
            current.pop(final, None)
    else:
        if isinstance(current, list):
            current[int(final)] = value
        else:
            current[final] = value
    return candidate


def source_baseline(check: Check) -> dict[str, Any]:
    git_status = run(["git", "status", "--short", "--branch"])
    head = run(["git", "log", "-1", "--format=%H %s"])
    repair03 = load_json(ROOT / ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/evidence/result.json")
    repair04 = load_json(ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/evidence/result.json")
    dispositions = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04/finding-disposition.json")
    downstream = {
        "check_04": (ROOT / ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04").exists(),
        "repair_05": (ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05").exists(),
        "acceptance": (ROOT / ".aide/queue/AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01").exists(),
    }
    check.add(
        "baseline.branch_and_head",
        "source_chain",
        "Branch is main and live head is the verified Repair 04 commit.",
        git_status["stdout"].splitlines()[0].startswith("## main...origin/main") and head["stdout"].startswith(SOURCE_COMMIT),
        expected={"branch": "main", "head": SOURCE_COMMIT},
        observed={"status": git_status["stdout"].strip(), "head": head["stdout"].strip()},
        evidence_refs=["git status --short --branch", "git log -1 --format=%H"],
    )
    check.add(
        "baseline.repair03_and_repair04_results",
        "source_chain",
        "Repair 03 check and Repair 04 result match expected routing.",
        repair03.get("result") == "REQUEST_CHANGES"
        and repair03.get("material_finding_count") == 12
        and repair04.get("result") in {"PASS", "PASS_WITH_WARNINGS"}
        and repair04.get("recommended_next_task") == TASK_ID,
        expected={"repair03": "REQUEST_CHANGES/12", "repair04": "PASS_WITH_WARNINGS routes here"},
        observed={"repair03": repair03, "repair04": repair04},
        evidence_refs=[
            ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03/evidence/result.json",
            ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/evidence/result.json",
        ],
    )
    check.add(
        "baseline.repair04_disposition_count",
        "report_consistency",
        "Repair 04 has exactly 12 repaired-pending-check finding dispositions matching Repair 03 findings.",
        len(dispositions) == 12
        and [item.get("finding_id") for item in dispositions] == REPAIR_04_FINDINGS
        and all(item.get("disposition") == "REPAIRED_PENDING_INDEPENDENT_CHECK" for item in dispositions),
        expected=REPAIR_04_FINDINGS,
        observed=dispositions,
        evidence_refs=[".aide/reports/dominium-readonly-seam-v0-repair-04/finding-disposition.json"],
    )
    check.add(
        "baseline.no_downstream_superseding_task",
        "source_chain",
        "No downstream Repair 04 check, Repair 05, or acceptance task existed before this check scaffold.",
        downstream["repair_05"] is False and downstream["acceptance"] is False,
        expected={"repair_05": False, "acceptance": False},
        observed=downstream,
        evidence_refs=["Test-Path downstream queue directories"],
    )
    return {"git_status": git_status, "head": head, "repair03": repair03, "repair04": repair04, "dispositions": dispositions, "downstream": downstream}


def schema_checks(check: Check) -> dict[str, Any]:
    schema_path = ROOT / ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json"
    bundle_path = ROOT / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json"
    schema = load_json(schema_path)
    bundle = load_json(bundle_path)
    refs = [node.get("$ref") for _path, node in walk(schema) if isinstance(node, dict) and "$ref" in node]
    dangling = [ref for ref in refs if not isinstance(ref, str) or not ref_exists(schema, ref)]
    seam_record = schema.get("$defs", {}).get("SeamRecord", {})
    oneof_refs = [item.get("$ref") for item in seam_record.get("oneOf", []) if isinstance(item, dict)]
    expected_refs = [f"#/$defs/{RECORD_DEFS[kind]}" for kind in RECORD_DEFS]
    record_def_results = {}
    for kind, def_name in RECORD_DEFS.items():
        node = schema["$defs"].get(def_name, {})
        composed = node.get("allOf", [])
        overlay = composed[1] if len(composed) > 1 and isinstance(composed[1], dict) else {}
        props = overlay.get("properties", {})
        record_def_results[kind] = {
            "has_allOf": "allOf" in node,
            "kind_const": props.get("kind", {}).get("const"),
            "spec_ref": props.get("spec", {}).get("$ref"),
            "status_ref": props.get("status", {}).get("$ref"),
        }
    check.add(
        "schema.seam_record_union",
        "schema",
        "Schema declares a canonical SeamRecord oneOf with all ten record kinds exactly once.",
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        and not dangling
        and oneof_refs == expected_refs
        and len(set(oneof_refs)) == 10,
        expected={"draft": "2020-12", "oneOf": expected_refs, "dangling_refs": []},
        observed={"draft": schema.get("$schema"), "oneOf": oneof_refs, "dangling_refs": dangling},
        evidence_refs=[rel(schema_path)],
        source_finding_id="schema.kind_specific_defs_present",
    )
    composition_ok = all(
        item["has_allOf"]
        and item["kind_const"] == kind
        and item["spec_ref"] == f"#/$defs/{kind}Spec"
        and item["status_ref"] in {"#/$defs/ProjectionStatus", "#/$defs/FalseStatus"}
        for kind, item in record_def_results.items()
    )
    check.add(
        "schema.kind_composition",
        "schema",
        "Each record kind ties kind const, matching spec, and status schema through composition.",
        composition_ok,
        expected="all ten record defs use allOf with matching kind/spec/status",
        observed=record_def_results,
        evidence_refs=[rel(schema_path)],
        source_finding_id="schema.kind_specific_defs_present",
    )
    cross_results = []
    for target_kind, donor_kind in CROSS_KIND_SUBSTITUTIONS:
        candidate = record_from_bundle(bundle, target_kind)
        candidate["spec"] = record_from_bundle(bundle, donor_kind)["spec"]
        errors = validate_record(schema, candidate, target_kind)
        cross_results.append({"target_kind": target_kind, "donor_spec": donor_kind, "failed": bool(errors), "errors": errors[:5]})
    check.add(
        "schema.cross_kind_substitutions_fail",
        "schema",
        "Cross-kind record/spec substitutions fail independent schema validation.",
        all(item["failed"] for item in cross_results),
        expected="all specified cross-kind substitutions fail",
        observed=cross_results,
        evidence_refs=[rel(schema_path), rel(bundle_path)],
        source_finding_id="schema.kind_specific_defs_present",
    )
    mutation_cases = [
        ("commit_sha_pattern", "WorkspaceDescriptor", ["spec", "selected_revision"], "not-a-sha"),
        ("sha256_pattern", "ArtifactReference", ["spec", "sha256"], "sha256:nothex"),
        ("reference_id_pattern", "ArtifactReference", ["spec", "artifact_ref"], "not-a-ref"),
        ("repo_relative_path", "ArtifactReference", ["spec", "source_path"], "../escape"),
        ("nonnegative_count", "ArtifactReference", ["spec", "size_bytes"], -1),
        ("sequence_minimum", "EventEnvelope", ["spec", "sequence"], 0),
        ("identity_is_file_path_false", "WorkspaceDescriptor", ["spec", "identity_is_file_path"], True),
        ("file_path_is_locator_true", "ArtifactReference", ["spec", "file_path_is_locator"], False),
        ("runtime_flag_false", "DominiumBridgeManifest", ["spec", "bridge_runtime_implemented"], True),
        ("apply_status_false", "HostManifest", ["status", "patch_transaction_applied"], True),
    ]
    mutation_results = []
    for case_id, kind, parts, value in mutation_cases:
        candidate = mutate_path(record_from_bundle(bundle, kind), parts, value)
        errors = validate_record(schema, candidate, kind)
        mutation_results.append({"case_id": case_id, "kind": kind, "failed": bool(errors), "errors": errors[:5]})
    check.add(
        "schema.required_constraints_are_meaningful",
        "schema",
        "Representative required canonical fields have meaningful type, pattern, const, and minimum constraints.",
        all(item["failed"] for item in mutation_results),
        expected="all representative schema mutations fail",
        observed=mutation_results,
        evidence_refs=[rel(schema_path), rel(bundle_path)],
        source_finding_id="schema.kind_specific_defs_present",
    )
    open_surfaces = []
    for path, node in walk(schema):
        if isinstance(node, dict) and "additionalProperties" in node and node.get("additionalProperties") is not False:
            open_surfaces.append(path)
    allowed_open = [
        path
        for path in open_surfaces
        if "/ExtensionMap" in path or "/ExtensionValue" in path
    ]
    check.add(
        "schema.open_object_surfaces_bounded",
        "extension_boundary",
        "Canonical objects are closed; non-false additionalProperties appears only under explicit extension value containers.",
        sorted(open_surfaces) == sorted(allowed_open),
        expected="only ExtensionMap/ExtensionValue open-object surfaces",
        observed=open_surfaces,
        evidence_refs=[rel(schema_path)],
        source_finding_id="schema.authority_extensions_bounded",
    )
    return {
        "dangling_refs": dangling,
        "oneof_refs": oneof_refs,
        "record_def_results": record_def_results,
        "cross_results": cross_results,
        "mutation_results": mutation_results,
        "open_surfaces": open_surfaces,
    }


def production_validation_probe(extension_key: str, *, value: Any = True) -> dict[str, Any]:
    script = r"""
import copy, json, sys
from pathlib import Path
root = Path(sys.argv[1])
key = sys.argv[2]
value = json.loads(sys.argv[3])
sys.path.insert(0, str(root))
from core.interop.dominium import validation
bundle = json.loads((root / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json").read_text(encoding="utf-8"))
candidate = copy.deepcopy(bundle)
candidate["records"]["host_manifest"]["spec"]["extensions"] = {key: value}
report = validation.validate_bundle(candidate, dominium_root=Path("C:/Projects/Dominium/dominium"))
print(json.dumps({"status": report.get("validation_status"), "codes": [item.get("code") for item in report.get("error_records", [])]}, sort_keys=True))
"""
    result = run([sys.executable, "-c", script, str(ROOT), extension_key, json.dumps(value)], timeout=60)
    try:
        parsed = json.loads(result["stdout"])
    except json.JSONDecodeError:
        parsed = {"status": "HARNESS_ERROR", "codes": [], "stdout": result["stdout"], "stderr": result["stderr"]}
    return {"extension_key": extension_key, "returncode": result["returncode"], **parsed}


def extension_checks(check: Check) -> dict[str, Any]:
    validation_source = (ROOT / "core/interop/dominium/validation.py").read_text(encoding="utf-8")
    source_names = {name: name in validation_source for name in AUTHORITY_EXTENSION_NAMES}
    variants = []
    for name in AUTHORITY_EXTENSION_NAMES:
        variants.extend([name, name.upper(), f"safe.{name}", f"{name}-flag"])
    probe_results = [production_validation_probe(name) for name in variants]
    benign = production_validation_probe("safe_metadata_note", value="preserved")
    authority_closed = all("schema.authority_extension" in item.get("codes", []) or "extension.authority_change" in item.get("codes", []) for item in probe_results)
    benign_ok = not any(code in {"schema.authority_extension", "extension.authority_change"} for code in benign.get("codes", []))
    check.add(
        "extension.authority_names_semantically_refused",
        "extension_boundary",
        "Authority-changing extension names and normalized variants fail semantic validation.",
        authority_closed and all(source_names.values()),
        expected={"all_names_in_validator": True, "all_variants_rejected": True},
        observed={"names_in_validator": source_names, "probe_failures": [item for item in probe_results if not ("schema.authority_extension" in item.get("codes", []) or "extension.authority_change" in item.get("codes", []))]},
        evidence_refs=["core/interop/dominium/validation.py", "evidence/extension-probes.json"],
        source_finding_id="schema.authority_extensions_bounded",
    )
    check.add(
        "extension.benign_metadata_allowed",
        "extension_boundary",
        "Benign metadata extension remains accepted by semantic validation.",
        benign_ok,
        expected="safe metadata extension does not raise authority-change code",
        observed=benign,
        evidence_refs=["evidence/extension-probes.json"],
        severity="WARNING",
    )
    payload = {"authority_probes": probe_results, "benign_probe": benign}
    write_json(EVIDENCE / "extension-probes.json", payload)
    return payload


def production_fixture_probe(operations: list[dict[str, Any]], document: dict[str, Any] | None = None) -> dict[str, Any]:
    script = r"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root))
from core.interop.dominium import fixture_replay
document = json.loads(sys.stdin.readline())
operations = json.loads(sys.stdin.readline())
try:
    result = fixture_replay.apply_operations(document, operations)
    print(json.dumps({"ok": True, "result": result}, sort_keys=True))
except Exception as exc:
    print(json.dumps({"ok": False, "error_type": type(exc).__name__, "error": str(exc)}, sort_keys=True))
"""
    base = document if document is not None else {"items": [{"name": "a"}], "obj": {"x": 1}}
    proc = subprocess.run(
        [sys.executable, "-c", script, str(ROOT)],
        input=json.dumps(base) + "\n" + json.dumps(operations) + "\n",
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(ROOT),
        check=False,
        timeout=60,
    )
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        parsed = {"ok": False, "error": "invalid probe output", "stdout": proc.stdout, "stderr": proc.stderr}
    parsed["returncode"] = proc.returncode
    return parsed


def pointer_parts(pointer: str) -> list[str]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON pointer path must start with /")
    parts = pointer.split("/")[1:]
    if not parts:
        raise ValueError("root mutation is not allowed")
    result = []
    for part in parts:
        index = 0
        while index < len(part):
            if part[index] == "~" and (index + 1 >= len(part) or part[index + 1] not in {"0", "1"}):
                raise ValueError("malformed JSON pointer escape")
            index += 1
        result.append(part.replace("~1", "/").replace("~0", "~"))
    return result


def canonical_index(value: str, *, limit: int, allow_end: bool, allow_dash: bool) -> int:
    if value == "-":
        if allow_dash:
            return limit
        raise ValueError("dash not allowed")
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9][0-9]*)", value):
        raise ValueError("array index must be ASCII canonical decimal")
    index = int(value)
    maximum = limit if allow_end else limit - 1
    if index < 0 or index > maximum:
        raise ValueError("array index out of range")
    return index


def independent_apply(document: Any, operations: list[dict[str, Any]]) -> Any:
    candidate = copy.deepcopy(document)
    for op in operations:
        if not isinstance(op, dict):
            raise ValueError("operation must be object")
        if set(op) & set(FIXTURE_FORBIDDEN_KEYS):
            raise ValueError("forbidden operation key")
        kind = op.get("op")
        allowed_keys = {"op", "path"}
        if kind in {"add", "replace", "append"}:
            if "value" not in op:
                raise ValueError("missing required value")
            allowed_keys.add("value")
        if kind not in {"add", "remove", "replace", "append"}:
            raise ValueError("unsupported op")
        extra = set(op) - allowed_keys
        if extra:
            raise ValueError("extra operation key")
        parts = pointer_parts(op.get("path"))
        parent = candidate
        for part in parts[:-1]:
            if isinstance(parent, list):
                parent = parent[canonical_index(part, limit=len(parent), allow_end=False, allow_dash=False)]
            elif isinstance(parent, dict) and part in parent:
                parent = parent[part]
            else:
                raise ValueError("missing intermediate")
        key = parts[-1]
        if isinstance(parent, list):
            if kind == "remove":
                parent.pop(canonical_index(key, limit=len(parent), allow_end=False, allow_dash=False))
            elif kind == "replace":
                parent[canonical_index(key, limit=len(parent), allow_end=False, allow_dash=False)] = copy.deepcopy(op["value"])
            elif kind == "add":
                parent.insert(canonical_index(key, limit=len(parent), allow_end=True, allow_dash=True), copy.deepcopy(op["value"]))
            elif kind == "append":
                if key != "-":
                    canonical_index(key, limit=len(parent), allow_end=True, allow_dash=False)
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
                    raise ValueError("add key exists")
                parent[key] = copy.deepcopy(op["value"])
            elif kind == "append":
                if key not in parent or not isinstance(parent[key], list):
                    raise ValueError("append target is not array")
                parent[key].append(copy.deepcopy(op["value"]))
        else:
            raise ValueError("parent is not container")
    return candidate


def fixture_checks(check: Check) -> dict[str, Any]:
    source = (ROOT / "core/interop/dominium/fixture_replay.py").read_text(encoding="utf-8")
    missing_value_ops = {
        "add": production_fixture_probe([{"op": "add", "path": "/obj/y"}]),
        "replace": production_fixture_probe([{"op": "replace", "path": "/obj/x"}]),
        "append": production_fixture_probe([{"op": "append", "path": "/items"}]),
    }
    explicit_null = production_fixture_probe([{"op": "replace", "path": "/obj/x", "value": None}])
    check.add(
        "fixture.value_presence",
        "fixture_replay",
        "Production replay requires explicit value for add, replace, and append while accepting explicit JSON null.",
        all(not item.get("ok") for item in missing_value_ops.values()) and explicit_null.get("ok") is True,
        expected={"missing_value": "fail", "explicit_null": "pass"},
        observed={"missing_value_ops": missing_value_ops, "explicit_null": explicit_null},
        evidence_refs=["evidence/fixture-probes.json"],
        source_finding_id="fixture.production_requires_value",
    )
    bad_indexes = ["-1", "+1", "00", "01", "1.0", "1e2", "\u0661", "\uff11", " ", ""]
    index_results = {idx.encode("unicode_escape").decode("ascii"): production_fixture_probe([{"op": "replace", "path": f"/items/{idx}", "value": {}}]) for idx in bad_indexes}
    good_indexes = {"0": production_fixture_probe([{"op": "replace", "path": "/items/0", "value": {}}])}
    check.add(
        "fixture.ascii_canonical_indexes",
        "fixture_replay",
        "Array indexes accept only ASCII canonical non-negative decimal strings.",
        all(not item.get("ok") for item in index_results.values()) and all(item.get("ok") for item in good_indexes.values()) and "isdecimal()" not in source,
        expected={"bad_indexes": "fail", "0": "pass", "no_isdecimal": True},
        observed={"bad_indexes": index_results, "good_indexes": good_indexes, "uses_isdecimal": "isdecimal()" in source},
        evidence_refs=["core/interop/dominium/fixture_replay.py", "evidence/fixture-probes.json"],
        source_finding_id="fixture.production_rejects_unicode_decimal_indexes",
    )
    key_results = {key: production_fixture_probe([{"op": "replace", "path": "/obj/x", "value": 2, key: "x"}]) for key in FIXTURE_FORBIDDEN_KEYS}
    check.add(
        "fixture.forbidden_key_set",
        "fixture_replay",
        "Production replay rejects every executable or out-of-contract operation key.",
        all(not item.get("ok") for item in key_results.values()) and all(f'"{key}"' in source for key in FIXTURE_FORBIDDEN_KEYS),
        expected=FIXTURE_FORBIDDEN_KEYS,
        observed={"probe_failures": [key for key, item in key_results.items() if item.get("ok")], "source_missing": [key for key in FIXTURE_FORBIDDEN_KEYS if f'"{key}"' not in source]},
        evidence_refs=["core/interop/dominium/fixture_replay.py", "evidence/fixture-probes.json"],
        source_finding_id="fixture.production_forbidden_key_set_complete",
    )
    boundary_cases = {
        "remove_missing": production_fixture_probe([{"op": "remove", "path": "/obj/missing"}]),
        "replace_missing": production_fixture_probe([{"op": "replace", "path": "/obj/missing", "value": 1}]),
        "add_existing": production_fixture_probe([{"op": "add", "path": "/obj/x", "value": 1}]),
        "append_non_array": production_fixture_probe([{"op": "append", "path": "/obj/x", "value": 1}]),
        "root_mutation": production_fixture_probe([{"op": "replace", "path": "", "value": {}}]),
        "malformed_pointer": production_fixture_probe([{"op": "replace", "path": "/obj/~2", "value": 1}]),
    }
    check.add(
        "fixture.boundary_failures",
        "fixture_replay",
        "Production replay rejects missing targets, add-existing, append non-array, root mutation, and malformed pointers.",
        all(not item.get("ok") for item in boundary_cases.values()),
        expected="all boundary probes fail",
        observed=boundary_cases,
        evidence_refs=["evidence/fixture-probes.json"],
        severity="WARNING",
    )
    bundle = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json")
    fixture_dir = ROOT / ".aide/fixtures/dominium-readonly-seam/negative"
    replay_results = []
    for path in sorted(fixture_dir.glob("*.json")):
        fixture = load_json(path)
        try:
            invalid = independent_apply(bundle, fixture.get("operations", []))
            digest = stable_digest(invalid)
            ok = digest == fixture.get("invalid_bundle_sha256")
            error = None
        except Exception as exc:
            digest = None
            ok = False
            error = str(exc)
        replay_results.append({"fixture": path.name, "digest_matches": ok, "expected": fixture.get("invalid_bundle_sha256"), "observed": digest, "error": error})
    check.add(
        "fixture.negative_fixture_digests",
        "fixture_replay",
        "Every committed negative fixture independently replays to its recorded invalid payload hash.",
        all(item["digest_matches"] for item in replay_results),
        expected="all negative fixture invalid_bundle_sha256 values match independent replay",
        observed=[item for item in replay_results if not item["digest_matches"]],
        evidence_refs=[".aide/fixtures/dominium-readonly-seam/negative/**", "evidence/fixture-replay.json"],
        severity="WARNING",
    )
    payload = {
        "missing_value_ops": missing_value_ops,
        "explicit_null": explicit_null,
        "index_results": index_results,
        "good_indexes": good_indexes,
        "key_results": key_results,
        "boundary_cases": boundary_cases,
        "negative_fixture_replay": replay_results,
    }
    write_json(EVIDENCE / "fixture-probes.json", payload)
    write_json(EVIDENCE / "fixture-replay.json", replay_results)
    return payload


def cli_probe(verb: str) -> dict[str, Any]:
    result = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", verb], timeout=60)
    output = result["stdout"] + result["stderr"]
    false_values = {}
    for field in FALSE_BOUNDARY_FIELDS:
        match = re.search(rf"^{re.escape(field)}:\s*(\w+)", output, re.MULTILINE)
        false_values[field] = match.group(1).lower() if match else None
    return {
        "verb": verb,
        "returncode": result["returncode"],
        "typed_refusal": result["returncode"] == 2
        and "result: REFUSED" in output
        and "reason_code: AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION" in output
        and f"operation: {verb}" in output,
        "false_values": false_values,
        "all_false_boundaries": all(value == "false" for value in false_values.values()),
        "stdout_preview": result["stdout_lines"][:40],
        "stderr_preview": result["stderr_lines"][:20],
    }


def cli_checks(check: Check) -> dict[str, Any]:
    source = (ROOT / ".aide/scripts/aide_lite.py").read_text(encoding="utf-8")
    results = [cli_probe(verb) for verb in UNSUPPORTED_VERBS]
    help_result = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", "--help"], timeout=60)
    status_result = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", "status"], timeout=90)
    unknown_option = run(["py", "-3", ".aide/scripts/aide_lite.py", "dominium-seam", "--unknown-option"], timeout=60)
    all_typed = all(item["typed_refusal"] for item in results)
    all_false = all(item["all_false_boundaries"] for item in results)
    arbitrary = [item for item in results if item["verb"] in {"obliterate", "random-unknown-verb-1", "random-unknown-verb-2", "unknown-123", "future-operation", "xyzzy"}]
    generic_fallback = all(item["typed_refusal"] for item in arbitrary) and "known_dominium_seam_commands" in source and "operation not in known_dominium_seam_commands" in source
    check.add(
        "cli.actual_dispatch_unsupported_matrix",
        "typed_refusal",
        "Unsupported and arbitrary dominium-seam verbs return typed refusal through actual CLI parsing and dispatch.",
        all_typed and generic_fallback,
        expected={"exit_code": 2, "reason_code": "AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION", "generic_unknowns": "typed refusal"},
        observed={"failures": [item for item in results if not item["typed_refusal"]], "generic_fallback_source": generic_fallback},
        evidence_refs=["evidence/unsupported-cli-results.json"],
        source_finding_id="cli.unsupported_verbs_typed_refusal",
    )
    check.add(
        "cli.false_boundary_exactness",
        "typed_refusal",
        "Every typed refusal includes the complete false-boundary field set with false values.",
        all_false,
        expected=FALSE_BOUNDARY_FIELDS,
        observed=[{"verb": item["verb"], "false_values": item["false_values"]} for item in results if not item["all_false_boundaries"]],
        evidence_refs=["evidence/unsupported-cli-results.json"],
        source_finding_id="cli.unsupported_verbs_typed_refusal",
    )
    check.add(
        "cli.known_help_status_and_option_errors",
        "typed_refusal",
        "Help and known read-only status remain usable; unknown options remain option errors rather than operations.",
        help_result["returncode"] == 0 and status_result["returncode"] == 0 and unknown_option["returncode"] != 2,
        expected={"help": 0, "status": 0, "unknown_option": "argparse option error"},
        observed={"help": help_result["returncode"], "status": status_result["returncode"], "unknown_option": unknown_option["returncode"], "unknown_stderr": unknown_option["stderr_lines"][:5]},
        evidence_refs=["evidence/unsupported-cli-results.json"],
        severity="WARNING",
    )
    payload = {"results": results, "help": help_result, "status": status_result, "unknown_option": unknown_option}
    write_json(EVIDENCE / "unsupported-cli-results.json", payload)
    return payload


def copy_manifest_dependencies(source_root: Path, target_root: Path, manifest: dict[str, Any]) -> None:
    for entry in manifest.get("dependencies", []):
        rel_path = Path(str(entry.get("path", "")))
        if rel_path.is_absolute() or ".." in rel_path.parts:
            raise ValueError(f"unsafe manifest path: {rel_path}")
        src = source_root / rel_path
        dst = target_root / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def dominium_state(label: str, selected_paths: list[str] | None = None) -> dict[str, Any]:
    commands = {
        "head": ["git", "rev-parse", "HEAD"],
        "refs": ["git", "for-each-ref", "--format=%(refname) %(objectname)"],
        "index": ["git", "ls-files", "-s"],
        "config": ["git", "config", "--list", "--show-origin"],
        "tracked_tree": ["git", "ls-tree", "-r", "HEAD"],
        "untracked_inventory": ["git", "ls-files", "--others", "--exclude-standard"],
        "ignored_inventory": ["git", "ls-files", "--others", "--ignored", "--exclude-standard"],
        "worktree_status": ["git", "status", "--short", "--branch"],
    }
    state: dict[str, Any] = {"label": label, "available": DOMINIUM_ROOT.exists(), "path": str(DOMINIUM_ROOT)}
    if not DOMINIUM_ROOT.exists():
        return state
    for name, args in commands.items():
        result = run(args, cwd=DOMINIUM_ROOT, timeout=120)
        state[name] = {
            "returncode": result["returncode"],
            "sha256": "sha256:" + hashlib.sha256((result["stdout"] + result["stderr"]).encode("utf-8")).hexdigest(),
            "preview": (result["stdout_lines"] + result["stderr_lines"])[:30],
        }
    hashes = {}
    for rel_path in selected_paths or []:
        path = DOMINIUM_ROOT / rel_path
        hashes[rel_path] = file_digest(path) if path.exists() else None
    state["selected_source_hashes"] = hashes
    return state


def run_temp_seam_sequence(commands: list[str], *, timeout_per_command: int = 180) -> dict[str, Any]:
    manifest = load_json(ROOT / ".aide/interop/dominium/runtime-dependency-manifest.json")
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        temp_root = base / "aide-portable"
        cwd = base / "unrelated-cwd"
        cwd.mkdir()
        copy_manifest_dependencies(ROOT, temp_root, manifest)
        results = []
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONUSERBASE", None)
        env["PYTHONNOUSERSITE"] = "1"
        env["AIDE_DOMINIUM_PORTABILITY_CHILD"] = "1"
        for command in commands:
            args = [
                sys.executable,
                "-I",
                str(temp_root / ".aide/scripts/aide_lite.py"),
                "--repo-root",
                str(temp_root),
                "dominium-seam",
                command,
                "--dominium-root",
                str(DOMINIUM_ROOT),
            ]
            results.append(run(args, cwd=cwd, env=env, timeout=timeout_per_command))
        output_set = sorted(path for path in REQUIRED_PORTABLE_OUTPUTS if (temp_root / path).exists())
        hashes = {path: file_digest(temp_root / path) for path in output_set}
        return {"commands": results, "output_set": output_set, "hashes": hashes}


def no_write_checks(check: Check, bundle: dict[str, Any]) -> dict[str, Any]:
    selected_paths = [str(item.get("path")) for item in bundle.get("source_snapshot", {}).get("selected_files", []) if isinstance(item, dict)]
    before = dominium_state("before-no-write", selected_paths)
    sequence = run_temp_seam_sequence(["snapshot", "project", "validate", "diff", "demo"], timeout_per_command=240)
    after = dominium_state("after-no-write", selected_paths)
    comparable = ["head", "refs", "index", "config", "tracked_tree", "untracked_inventory", "ignored_inventory", "worktree_status", "selected_source_hashes"]
    changed = []
    if before.get("available") and after.get("available"):
        for key in comparable:
            if before.get(key) != after.get(key):
                changed.append(key)
    command_ok = all(item["returncode"] == 0 for item in sequence["commands"])
    actual_ops = [item["args"][-3] if len(item["args"]) >= 3 else "" for item in sequence["commands"]]
    check.add(
        "conformance.no_write_actual_sequence",
        "conformance",
        "Dominium state is unchanged after actual snapshot/project/validate/diff/demo seam commands run between before/after captures.",
        before.get("available") is True and command_ok and not changed and len(sequence["commands"]) == 5,
        expected={"commands": ["snapshot", "project", "validate", "diff", "demo"], "changed_state": []},
        observed={"command_returncodes": [item["returncode"] for item in sequence["commands"]], "changed_state": changed, "actual_ops": actual_ops},
        evidence_refs=["evidence/dominium-state-before.json", "evidence/dominium-state-after.json", "evidence/no-write-sequence.json"],
        source_finding_id="conformance.no_write_surrounds_actual_operations",
    )
    write_json(EVIDENCE / "dominium-state-before.json", before)
    write_json(EVIDENCE / "dominium-state-after.json", after)
    write_json(EVIDENCE / "no-write-sequence.json", sequence)
    return {"before": before, "after": after, "changed": changed, "sequence": sequence}


def conformance_checks(check: Check) -> dict[str, Any]:
    source = (ROOT / "core/interop/dominium/conformance.py").read_text(encoding="utf-8")
    evidence = load_json(ROOT / ".aide/interop/dominium/conformance-evidence.json")
    direct_helper = "unsupported_operation_refusal(verb)" in source or "unsupported_operation_probe_matrix(None)" in source
    probes = evidence.get("unsupported_operation_probes", {})
    actual_cli_preview = any("AIDE Lite dominium-seam unsupported" in "\n".join(item.get("preview", [])) for item in probes.get("results", []) if isinstance(item, dict))
    check.add(
        "conformance.unsupported_cli_evidence",
        "conformance",
        "Unsupported-operation conformance consumes actual CLI dispatch evidence, not direct refusal constructor output.",
        not direct_helper and probes.get("all_typed_refusals") is True and actual_cli_preview,
        expected={"no_direct_helper": True, "all_typed_refusals": True, "cli_preview": True},
        observed={"direct_helper_source": direct_helper, "all_typed_refusals": probes.get("all_typed_refusals"), "cli_preview": actual_cli_preview},
        evidence_refs=["core/interop/dominium/conformance.py", ".aide/interop/dominium/conformance-evidence.json"],
        source_finding_id="conformance.unsupported_uses_actual_cli_dispatch",
    )
    return {"direct_helper": direct_helper, "unsupported_probes": probes}


def guard_checks(check: Check) -> dict[str, Any]:
    source = (ROOT / "core/interop/dominium/operations.py").read_text(encoding="utf-8")
    guard = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json")
    guard_slice = source[source.find("def exercise_guard") : source.find("def guard_conformance")]
    dispatcher_tokens = ["subprocess.run", "run_git", "open(", "write_text", "executor", "dispatch", "classify_git_args("]
    exercised = any(token in guard_slice for token in dispatcher_tokens)
    static_pass_literals = '"guard_invoked": True' in source or "guard_invoked = True" in source
    families = {item.get("family") for item in guard.get("probes", []) if isinstance(item, dict)}
    required = {"filesystem_writes", "branch_worktree_ref_ops", "network_attempts", "provider_model_attempts", "worker_dispatch", "mutation_apply"}
    check.add(
        "conformance.guard_evidence_exercised",
        "guard",
        "Guard evidence reaches actual guard or dispatcher paths for safe forbidden requests rather than only constructing pass dictionaries.",
        exercised and guard.get("result") == "PASS" and required.issubset(families),
        expected={"guard_path_reached": True, "required_families": sorted(required)},
        observed={"guard_path_tokens_present": exercised, "static_pass_literals": static_pass_literals, "families": sorted(families), "guard_slice": guard_slice[:1200]},
        evidence_refs=["core/interop/dominium/operations.py", ".aide/reports/dominium-readonly-seam-v0/operation-guard-conformance.json"],
        source_finding_id="conformance.guard_evidence_is_exercised",
    )
    check.add(
        "operation.guard_report_not_static",
        "operation",
        "Operation guard report is not static pass data and records exercised evidence.",
        exercised and not static_pass_literals,
        expected="actual guard/dispatcher invocation evidence, no static guard_invoked=True pass dictionary",
        observed={"guard_path_tokens_present": exercised, "static_pass_literals": static_pass_literals},
        evidence_refs=["core/interop/dominium/operations.py"],
        source_finding_id="operation.guard_report_is_not_static",
    )
    return {"guard": guard, "guard_path_tokens_present": exercised, "static_pass_literals": static_pass_literals}


def aggregate_from_raw(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aggregate: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in raw:
        key = (
            item.get("family"),
            item.get("operation"),
            item.get("target"),
            item.get("classification"),
            item.get("allowed"),
            item.get("source"),
            item.get("observation_method"),
        )
        entry = aggregate.setdefault(
            key,
            {
                "family": item.get("family"),
                "operation": item.get("operation"),
                "target": item.get("target"),
                "classification": item.get("classification"),
                "allowed": item.get("allowed"),
                "source": item.get("source"),
                "observation_method": item.get("observation_method"),
                "count": 0,
                "return_codes": [],
            },
        )
        entry["count"] += 1
        if item.get("return_code") not in entry["return_codes"]:
            entry["return_codes"].append(item.get("return_code"))
    return sorted(
        aggregate.values(),
        key=lambda item: (
            str(item["family"]),
            str(item["operation"]),
            str(item["target"]),
            str(item["classification"]),
            str(item["source"]),
            str(item["observation_method"]),
        ),
    )


def operation_checks(check: Check) -> dict[str, Any]:
    operations_source = (ROOT / "core/interop/dominium/operations.py").read_text(encoding="utf-8")
    trace = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/operation-trace.json")
    demo = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/demo-result.json")
    raw = trace.get("observations", [])
    recomputed_hash = compact_digest(raw)
    contiguous = [item.get("sequence") for item in raw] == list(range(1, len(raw) + 1))
    recomputed_aggregate = aggregate_from_raw(raw)
    ledger = demo.get("operation_ledger", {})
    aggregate_count_sum = sum(int(item.get("count", 0)) for item in ledger.get("operations", []) if isinstance(item, dict))
    allowed_count = sum(1 for item in raw if item.get("allowed") is True)
    forbidden_count = sum(1 for item in raw if item.get("allowed") is False)
    source_key_lossy = "key = (item.family, item.operation, item.allowed, item.observation_method)" in operations_source
    synthetic_raw = [
        {"sequence": 1, "family": "filesystem_writes", "operation": "probe", "target": "A", "classification": "write_a", "allowed": False, "source": "one", "observation_method": "guard", "return_code": None},
        {"sequence": 2, "family": "filesystem_writes", "operation": "probe", "target": "B", "classification": "write_b", "allowed": False, "source": "two", "observation_method": "guard", "return_code": None},
        {"sequence": 3, "family": "filesystem_writes", "operation": "probe", "target": "B", "classification": "write_b", "allowed": True, "source": "two", "observation_method": "wrapper", "return_code": 0},
    ]
    synthetic_aggregate = aggregate_from_raw(synthetic_raw)
    check.add(
        "operation.lossless_aggregate_dimensions",
        "operation",
        "Operation aggregation preserves target, classification, source, observation method, and allowed distinctions.",
        not source_key_lossy and len(synthetic_aggregate) == 3 and all(token in operations_source for token in ["item.target", "item.classification", "item.source"]),
        expected="synthetic same-operation observations remain separate aggregate records",
        observed={"source_key_lossy": source_key_lossy, "synthetic_aggregate": synthetic_aggregate},
        evidence_refs=["core/interop/dominium/operations.py", "evidence/operation-recompute.json"],
        source_finding_id="operation.aggregate_key_preserves_semantics",
    )
    check.add(
        "operation.raw_trace_reconciles",
        "operation",
        "Raw operation trace has contiguous sequence, valid hash, valid counts, and aggregate counts reconcile.",
        contiguous
        and recomputed_hash == trace.get("raw_trace_sha256")
        and len(raw) == ledger.get("raw_observation_count")
        and allowed_count + forbidden_count == len(raw)
        and aggregate_count_sum == len(raw)
        and ledger.get("operation_count") == len(ledger.get("operations", [])),
        expected="raw trace hash/counts/aggregate all reconcile",
        observed={
            "contiguous": contiguous,
            "recomputed_hash": recomputed_hash,
            "stored_hash": trace.get("raw_trace_sha256"),
            "raw_count": len(raw),
            "ledger_raw_count": ledger.get("raw_observation_count"),
            "allowed_plus_forbidden": allowed_count + forbidden_count,
            "aggregate_count_sum": aggregate_count_sum,
            "operation_count": ledger.get("operation_count"),
            "aggregate_length": len(ledger.get("operations", [])),
        },
        evidence_refs=[".aide/reports/dominium-readonly-seam-v0/operation-trace.json", ".aide/reports/dominium-readonly-seam-v0/demo-result.json", "evidence/operation-recompute.json"],
        severity="WARNING",
    )
    payload = {"recomputed_hash": recomputed_hash, "recomputed_aggregate_sample": recomputed_aggregate[:50], "synthetic_aggregate": synthetic_aggregate}
    write_json(EVIDENCE / "operation-recompute.json", payload)
    return payload


def manifest_digest_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in manifest.items() if key != "manifest_digest"}


def derive_ast_import_closure(root: Path) -> set[str]:
    import ast

    manifest = load_json(root / ".aide/interop/dominium/runtime-dependency-manifest.json")
    files = [root / str(entry["path"]) for entry in manifest.get("dependencies", []) if str(entry.get("path", "")).endswith(".py")]
    local: set[str] = set()
    for path in files:
        rel_path = path.relative_to(root).as_posix()
        local.add(rel_path)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if node.level and rel_path.startswith("core/interop/dominium/"):
                    for alias in node.names:
                        candidate = root / "core/interop/dominium" / f"{alias.name}.py"
                        if candidate.exists():
                            local.add(candidate.relative_to(root).as_posix())
                elif module.startswith("core."):
                    candidate = root / (module.replace(".", "/") + ".py")
                    if candidate.exists():
                        local.add(candidate.relative_to(root).as_posix())
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("core."):
                        candidate = root / (alias.name.replace(".", "/") + ".py")
                        if candidate.exists():
                            local.add(candidate.relative_to(root).as_posix())
    return local


def independent_portability_run() -> dict[str, Any]:
    manifest = load_json(ROOT / ".aide/interop/dominium/runtime-dependency-manifest.json")
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        roots = [base / "portable-a", base / "portable-b"]
        root_reports = []
        for index, temp_root in enumerate(roots):
            copy_manifest_dependencies(ROOT, temp_root, manifest)
            cwd = base / f"cwd-{index}"
            cwd.mkdir()
            env = os.environ.copy()
            env.pop("PYTHONPATH", None)
            env.pop("PYTHONHOME", None)
            env.pop("PYTHONUSERBASE", None)
            env["PYTHONNOUSERSITE"] = "1"
            env["PYTHONHASHSEED"] = str(index + 17)
            env["AIDE_DOMINIUM_PORTABILITY_CHILD"] = "1"
            command_results = []
            for command in ["status", "snapshot", "project", "validate", "diff", "demo"]:
                args = [
                    sys.executable,
                    "-I",
                    str(temp_root / ".aide/scripts/aide_lite.py"),
                    "--repo-root",
                    str(temp_root),
                    "dominium-seam",
                    command,
                    "--dominium-root",
                    str(DOMINIUM_ROOT),
                ]
                command_results.append(run(args, cwd=cwd, env=env, timeout=240))
            output_set = sorted(path for path in REQUIRED_PORTABLE_OUTPUTS if (temp_root / path).exists())
            output_hashes = {path: file_digest(temp_root / path) for path in output_set}
            leak_needles = [str(ROOT.resolve()), str(base.resolve()), os.path.expanduser("~")]
            leak_hits = []
            for path in sorted(p for p in temp_root.rglob("*") if p.is_file()):
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                for needle in leak_needles:
                    if needle and needle in text:
                        leak_hits.append({"path": path.relative_to(temp_root).as_posix(), "needle": needle})
            root_reports.append(
                {
                    "root": temp_root.name,
                    "commands": command_results,
                    "output_set": output_set,
                    "output_hashes": output_hashes,
                    "leak_hits": leak_hits,
                }
            )
        return {"roots": root_reports}


def portability_checks(check: Check, *, run_heavy: bool) -> dict[str, Any]:
    manifest = load_json(ROOT / ".aide/interop/dominium/runtime-dependency-manifest.json")
    entries = manifest.get("dependencies", [])
    digest_ok = stable_digest(manifest_digest_payload(manifest)) == manifest.get("manifest_digest")
    paths = [str(entry.get("path")) for entry in entries]
    unique = len(paths) == len(set(paths))
    path_safe = all(not Path(path).is_absolute() and ".." not in Path(path).parts for path in paths)
    hash_results = [
        {"path": path, "ok": (ROOT / path).exists() and file_digest(ROOT / path) == entry.get("sha256")}
        for path, entry in zip(paths, entries, strict=True)
    ]
    closure = derive_ast_import_closure(ROOT)
    missing_closure = sorted(path for path in closure if path not in paths and not path.endswith("__init__.py"))
    current = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/portability-result.json")
    current_compared = set(current.get("compared_outputs", []))
    current_complete = set(REQUIRED_PORTABLE_OUTPUTS) == current_compared
    independent = independent_portability_run() if run_heavy else {"skipped": True, "reason": "heavy portability disabled"}
    if run_heavy:
        roots = independent["roots"]
        root_sets = [set(root["output_set"]) for root in roots]
        root_hashes = [root["output_hashes"] for root in roots]
        commands_ok = all(all(cmd["returncode"] == 0 for cmd in root["commands"]) for root in roots)
        sets_complete = all(root_set == set(REQUIRED_PORTABLE_OUTPUTS) for root_set in root_sets)
        bytes_equal = len(root_hashes) == 2 and root_hashes[0] == root_hashes[1]
        leak_free = all(not root["leak_hits"] for root in roots)
    else:
        commands_ok = sets_complete = bytes_equal = leak_free = False
    check.add(
        "portability.manifest_valid",
        "portability",
        "Runtime dependency manifest digest, path safety, uniqueness, file hashes, and AST import closure validate independently.",
        digest_ok and unique and path_safe and all(item["ok"] for item in hash_results) and not missing_closure,
        expected={"digest": True, "unique": True, "path_safe": True, "hashes": True, "missing_ast_imports": []},
        observed={"digest_ok": digest_ok, "unique": unique, "path_safe": path_safe, "bad_hashes": [item for item in hash_results if not item["ok"]], "missing_ast_imports": missing_closure},
        evidence_refs=[".aide/interop/dominium/runtime-dependency-manifest.json", "evidence/portability-review.json"],
        severity="WARNING",
    )
    check.add(
        "portability.required_output_set_complete",
        "portability",
        "Portable output comparison includes exactly the accepted required child output set before hash comparison.",
        current.get("status") == "PASS" and current_complete and (not run_heavy or sets_complete),
        expected=REQUIRED_PORTABLE_OUTPUTS,
        observed={"current_status": current.get("status"), "current_compared": sorted(current_compared), "independent_sets_complete": sets_complete if run_heavy else "not_run"},
        evidence_refs=[".aide/reports/dominium-readonly-seam-v0/portability-result.json", "evidence/portability-review.json"],
        source_finding_id="portability.required_child_output_set_complete",
    )
    check.add(
        "portability.fresh_process_determinism",
        "portability",
        "At least two isolated portable roots produce complete deterministic outputs byte-for-byte without local path leaks.",
        run_heavy and commands_ok and sets_complete and bytes_equal and leak_free,
        expected={"commands": "0", "complete_sets": True, "bytes_equal": True, "path_leaks": 0},
        observed={"run_heavy": run_heavy, "commands_ok": commands_ok, "sets_complete": sets_complete, "bytes_equal": bytes_equal, "leak_free": leak_free},
        evidence_refs=["evidence/portability-review.json"],
        severity="WARNING" if run_heavy else "MATERIAL",
    )
    payload = {
        "manifest": {"digest_ok": digest_ok, "unique": unique, "path_safe": path_safe, "bad_hashes": [item for item in hash_results if not item["ok"]], "missing_ast_imports": missing_closure},
        "current_portability": current,
        "independent": independent,
    }
    write_json(EVIDENCE / "portability-review.json", payload)
    return payload


def regression_sampling(check: Check, schema: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    validation = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/validation.json")
    demo = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/demo-result.json")
    conformance_results = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/conformance-results.json")
    identity_ok = bundle.get("source_snapshot", {}).get("repository_identity", {}).get("canonical_identity") == "github.com/julesc013/dominium"
    digest_ok = bundle.get("content_digests", {}).get("seam_bundle_without_self_digest") is not None
    provenance_ok = all(key in bundle.get("registry_projection_summary", {}) for key in ["diagnostics", "refusals"])
    validation_ok = validation.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"} and not validation.get("errors")
    demo_truth_ok = demo.get("elapsed_time", {}).get("status") == "not_measured" and demo.get("source_mutation_count") == 0
    conformance_ok = conformance_results.get("status") in {"PASS", "PASS_WITH_WARNINGS"} and conformance_results.get("passed_count") == conformance_results.get("expectation_count")
    check.add(
        "regression.sampled_prior_invariants",
        "regression",
        "Sampled prior invariants remain closed: identity, digest presence, registry provenance, validation, conformance, and elapsed-time truthfulness.",
        identity_ok and digest_ok and provenance_ok and validation_ok and demo_truth_ok and conformance_ok,
        expected="sampled invariants remain passing",
        observed={
            "identity_ok": identity_ok,
            "digest_ok": digest_ok,
            "provenance_ok": provenance_ok,
            "validation_ok": validation_ok,
            "demo_truth_ok": demo_truth_ok,
            "conformance_ok": conformance_ok,
        },
        evidence_refs=[
            ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json",
            ".aide/reports/dominium-readonly-seam-v0/validation.json",
            ".aide/reports/dominium-readonly-seam-v0/demo-result.json",
            ".aide/reports/dominium-readonly-seam-v0/conformance-results.json",
        ],
        severity="WARNING",
    )
    noncaps = bundle.get("explicit_non_capabilities", [])
    false_status_ok = all(bundle.get("status", {}).get(field) is False for field in FALSE_BOUNDARY_FIELDS)
    check.add(
        "regression.no_capability_expansion",
        "non_capabilities",
        "Explicit non-capabilities and false-boundary status fields preserve the offline read-only boundary.",
        set(EXPLICIT_NON_CAPABILITIES).issubset(set(noncaps)) and false_status_ok,
        expected={"explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES, "false_fields": FALSE_BOUNDARY_FIELDS},
        observed={"missing_noncaps": sorted(set(EXPLICIT_NON_CAPABILITIES) - set(noncaps)), "false_status_ok": false_status_ok},
        evidence_refs=[".aide/reports/dominium-readonly-seam-v0/seam-bundle.json"],
        severity="WARNING",
    )
    return {"identity_ok": identity_ok, "validation_ok": validation_ok, "conformance_ok": conformance_ok}


def report_integrity_checks(check: Check) -> dict[str, Any]:
    disposition_path = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04/finding-disposition.json"
    repair_report_path = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04/repair-report.json"
    self_check_path = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04/self-adversarial-check.json"
    test_summary_path = ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-04/test-summary.json"
    status_path = ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04/status.yaml"
    dispositions = load_json(disposition_path)
    repair_report = load_json(repair_report_path)
    self_check = load_json(self_check_path)
    test_summary = load_json(test_summary_path)
    evidence_refs_exist = []
    for row in dispositions:
        for ref in row.get("evidence_refs", []):
            evidence_refs_exist.append({"ref": ref, "exists": (ROOT / ref).exists()})
    named_tests_exist = (ROOT / ".aide/scripts/tests/test_aide_dominium_readonly_seam_repair_04.py").exists()
    check.add(
        "report.repair04_consistency",
        "report_consistency",
        "Repair 04 reports and status agree on 12 repaired-pending-check findings and correct routing.",
        len(dispositions) == 12
        and [item.get("finding_id") for item in dispositions] == REPAIR_04_FINDINGS
        and repair_report.get("material_findings_repaired") == 12
        and repair_report.get("recommended_next_task") == TASK_ID
        and self_check.get("result") == "PASS"
        and test_summary.get("result") == "PASS_WITH_WARNINGS"
        and named_tests_exist
        and all(item["exists"] for item in evidence_refs_exist),
        expected="Repair 04 reports are internally consistent and evidence refs exist",
        observed={
            "disposition_count": len(dispositions),
            "ids": [item.get("finding_id") for item in dispositions],
            "repair_report_next": repair_report.get("recommended_next_task"),
            "self_check_result": self_check.get("result"),
            "test_summary_result": test_summary.get("result"),
            "status_exists": status_path.exists(),
            "missing_evidence_refs": [item for item in evidence_refs_exist if not item["exists"]],
        },
        evidence_refs=[rel(disposition_path), rel(repair_report_path), rel(self_check_path), rel(test_summary_path), rel(status_path)],
        severity="WARNING",
    )
    return {"dispositions": dispositions, "repair_report": repair_report, "self_check": self_check, "test_summary": test_summary}


def closure_matrix(assertions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for finding_id in REPAIR_04_FINDINGS:
        related = [item for item in assertions if item.get("source_finding_id") == finding_id and item.get("severity") == "MATERIAL"]
        failures = [item for item in related if item.get("outcome") != "PASS"]
        if failures:
            disposition = "OPEN"
        elif related:
            disposition = "CLOSED"
        else:
            disposition = "SUPERSEDED_BY_STRONGER_PASSING_CHECK"
        rows.append(
            {
                "finding_id": finding_id,
                "original_observed_defect": "See AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03 check report.",
                "repair_04_change": "See Repair 04 implementation commit and report.",
                "independent_test": [item["id"] for item in related] or ["covered by stronger sampled invariant"],
                "expected": [item.get("expected") for item in related],
                "observed": failures or [item.get("observed") for item in related if item.get("outcome") == "PASS"],
                "evidence_refs": sorted({ref for item in related for ref in item.get("evidence_refs", [])}),
                "disposition": disposition,
            }
        )
    return rows


def write_category_report(filename: str, title: str, assertions: list[dict[str, Any]]) -> None:
    lines = [f"# {title}", "", "| Assertion | Outcome | Severity | Source Finding |", "| --- | --- | --- | --- |"]
    for item in assertions:
        lines.append(f"| `{item['id']}` | {item['outcome']} | {item['severity']} | `{item.get('source_finding_id')}` |")
    lines.append("")
    write_text(REPORT / filename, "\n".join(lines))


def write_reports(check: Check, artifacts: dict[str, Any]) -> dict[str, Any]:
    material = check.material_findings()
    result = "REQUEST_CHANGES" if material else "PASS_WITH_WARNINGS"
    next_task = NEXT_REPAIR if material else NEXT_ACCEPT
    warning_count = sum(1 for item in check.assertions if item["severity"] == "WARNING" and item["outcome"] != "PASS")
    report = {
        "schema_version": "aide.dominium-readonly-seam.repair-04-check-report.v0",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "material_finding_count": len(material),
        "warning_count": warning_count,
        "recommended_next_task": next_task,
        "assertions": check.assertions,
        "material_findings": material,
    }
    matrix = closure_matrix(check.assertions)
    write_json(REPORT / "check-report.json", report)
    write_json(REPORT / "twelve-finding-closure.json", matrix)
    write_json(EVIDENCE / "independent-repair-04-check.json", report)
    write_json(EVIDENCE / "twelve-finding-closure.json", matrix)
    lines = ["# Twelve Finding Closure", "", "| Finding | Disposition |", "| --- | --- |"]
    for row in matrix:
        lines.append(f"| `{row['finding_id']}` | {row['disposition']} |")
    write_text(REPORT / "twelve-finding-closure.md", "\n".join(lines) + "\n")
    write_text(
        REPORT / "status.md",
        "\n".join(
            [
                "# Repair 04 Check Status",
                "",
                f"- task_id: `{TASK_ID}`",
                f"- status: `needs_review`",
                f"- result: `{result}`",
                f"- material_finding_count: {len(material)}",
                f"- warning_count: {warning_count}",
                f"- recommended_next_task: `{next_task}`",
                "",
            ]
        ),
    )
    category_files = {
        "source_chain": "source-chain-review.md",
        "historical": "historical-immutability-review.md",
        "schema": "schema-contract-review.md",
        "extension_boundary": "extension-boundary-review.md",
        "fixture_replay": "fixture-replay-review.md",
        "conformance": "conformance-evidence-review.md",
        "guard": "conformance-evidence-review.md",
        "operation": "operation-auditability-review.md",
        "portability": "portability-review.md",
        "typed_refusal": "typed-refusal-review.md",
        "regression": "regression-sampling.md",
        "report_consistency": "report-consistency-review.md",
        "non_capabilities": "explicit-non-capabilities.md",
    }
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in check.assertions:
        grouped.setdefault(category_files.get(item["category"], "report-consistency-review.md"), []).append(item)
    for filename in sorted(set(category_files.values())):
        write_category_report(filename, filename.replace("-", " ").replace(".md", "").title(), grouped.get(filename, []))
    write_text(
        REPORT / "warning-disposition.md",
        "# Warning Disposition\n\n"
        + "\n".join(f"- `{item['id']}`: {item['observed']}" for item in check.assertions if item["severity"] == "WARNING" and item["outcome"] != "PASS")
        + "\n",
    )
    write_text(
        REPORT / "explicit-non-capabilities.md",
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- `{item}`" for item in EXPLICIT_NON_CAPABILITIES) + "\n",
    )
    next_title = next_task
    write_text(
        REPORT / "next-task-prompt.md",
        f"# {next_title}\n\nCreate and process `{next_title}` as the next serialized Dominium read-only seam task selected by `{TASK_ID}`. Do not begin it from this check task.\n",
    )
    write_json(EVIDENCE / "result.json", {
        "schema_version": "aide.dominium-readonly-seam.repair-04-check-result.v0",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "status": "needs_review",
        "material_finding_count": len(material),
        "warning_count": warning_count,
        "recommended_next_task": next_task,
        "check_report": ".aide/reports/dominium-readonly-seam-v0-repair-04-check/check-report.json",
        "next_task_prompt": ".aide/reports/dominium-readonly-seam-v0-repair-04-check/next-task-prompt.md",
    })
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-heavy-portability", action="store_true")
    args = parser.parse_args(argv)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)
    check = Check()
    artifacts: dict[str, Any] = {}
    artifacts["baseline"] = source_baseline(check)
    schema = load_json(ROOT / ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json")
    bundle = load_json(ROOT / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json")
    artifacts["schema"] = schema_checks(check)
    artifacts["extensions"] = extension_checks(check)
    artifacts["fixtures"] = fixture_checks(check)
    artifacts["cli"] = cli_checks(check)
    artifacts["conformance"] = conformance_checks(check)
    artifacts["no_write"] = no_write_checks(check, bundle)
    artifacts["guard"] = guard_checks(check)
    artifacts["operation"] = operation_checks(check)
    artifacts["portability"] = portability_checks(check, run_heavy=not args.skip_heavy_portability)
    artifacts["regression"] = regression_sampling(check, schema, bundle)
    artifacts["report_integrity"] = report_integrity_checks(check)
    report = write_reports(check, artifacts)
    write_json(EVIDENCE / "harness-artifacts.json", artifacts)
    print(json.dumps({"result": report["result"], "material_finding_count": report["material_finding_count"], "warning_count": report["warning_count"], "recommended_next_task": report["recommended_next_task"]}, sort_keys=True))
    return 0 if report["result"] == "PASS_WITH_WARNINGS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
