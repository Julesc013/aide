"""Independent adversarial checks for AIDE's Dominium read-only seam v0.

This script intentionally avoids importing production seam validation for its
own material assertions. It imports production validation only as the target
under test for explicit adversarial comparisons.
"""

from __future__ import annotations

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
from urllib.parse import urlparse


TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01"
BUILD_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01"
PASS_NEXT = "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01"
REPAIR_NEXT = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01"
PINNED_DOMINIUM_HEAD = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"
BASELINE_REMOTE_MAIN = "623ab08ae8c867719d5abc2e60c16a6fbb37b313"
DOMINIUM_ROOT = Path("C:/Projects/Dominium/dominium")

EXPECTED_SELECTED_INPUTS = [
    ("AGENTS.md", "operator_law", "dominium_product_law", True),
    (".aide/queue/current.toml", "queue_status", "dominium_queue_truth", True),
    ("docs/canon/constitution_v1.md", "constitution", "dominium_canon", True),
    ("docs/canon/glossary_v1.md", "glossary", "dominium_canon", True),
    ("contracts/command/command_surface.contract.toml", "command_surface", "dominium_contract", True),
    ("contracts/service/service.contract.toml", "service_surface", "dominium_contract", True),
    ("contracts/module/module_surface.contract.toml", "module_surface", "dominium_contract", True),
    ("contracts/workbench/workbench_surface.contract.toml", "workbench_surface", "dominium_contract", True),
    ("contracts/refusal/refusal_code.registry.json", "refusal_registry", "dominium_contract", True),
    ("contracts/diagnostic/diagnostic_code.registry.json", "diagnostic_registry", "dominium_contract", True),
    ("contracts/diagnostic/diagnostic_severity.registry.json", "diagnostic_severity_registry", "dominium_contract", True),
    ("contracts/capability/capability.registry.json", "capability_registry", "dominium_contract", True),
    ("contracts/project_graph/project_graph_model.contract.toml", "project_graph_model", "dominium_contract", True),
    ("docs/repo/audits/PRESENTATION_CONTRACT_01.md", "presentation_contract_evidence", "dominium_evidence", True),
    ("docs/repo/audits/WORKBENCH_VALIDATION_SLICE_01.md", "workbench_validation_evidence", "dominium_evidence", True),
    ("docs/development/workbench_validation_slice.md", "workbench_validation_plan", "dominium_documentation", True),
    ("docs/development/command_result_view_slice.md", "command_result_view_plan", "dominium_documentation", True),
]

EXPECTED_SINGLETON_KINDS = {
    "HostManifest",
    "HostCapabilitySet",
    "WorkspaceDescriptor",
    "ContextDescriptor",
    "EvidenceReferenceSet",
    "DominiumBridgeManifest",
}

EXPECTED_KIND_COUNTS = {
    "HostManifest": 1,
    "HostCapabilitySet": 1,
    "WorkspaceDescriptor": 1,
    "ContextDescriptor": 1,
    "ArtifactReference": 17,
    "DiagnosticProjection": 8,
    "RefusalProjection": 8,
    "EvidenceReferenceSet": 1,
    "EventEnvelope": 3,
    "DominiumBridgeManifest": 1,
}

FORBIDDEN_CAPABILITIES = {
    "dominium.source.write",
    "dominium.command.invoke",
    "dominium.patch.apply",
    "dominium.branch.create",
    "dominium.service.start",
    "dominium.provider.call",
    "dominium.worker.execute",
}

REQUIRED_FIELDS_BY_KIND = {
    "HostManifest": ["host_id", "host_kind", "repository_identity", "selected_revision", "supported_surfaces", "runtime_dispatch_available"],
    "HostCapabilitySet": ["capabilities", "forbidden_capabilities"],
    "WorkspaceDescriptor": ["workspace_ref", "selected_revision", "branch", "identity_is_file_path"],
    "ContextDescriptor": ["context_ref", "artifact_refs", "sections", "source_revision_binding", "projection_direction"],
    "ArtifactReference": ["artifact_ref", "source_path", "source_role", "authority", "sha256", "size_bytes", "git_object"],
    "DiagnosticProjection": ["diagnostic_id", "code", "owner", "severity", "category", "source_registry", "native_meaning_owned_by"],
    "RefusalProjection": ["refusal_id", "code", "owner", "category", "reason", "recovery_action", "diagnostic_codes", "related_commands"],
    "EvidenceReferenceSet": ["evidence_refs", "evidence_count", "native_evidence_meaning_owned_by", "aide_behavior"],
    "EventEnvelope": ["event_ref", "event_type", "sequence", "causation_ref", "correlation_ref", "summary", "universal_event_store_implemented"],
    "DominiumBridgeManifest": ["bridge_id", "mapping_version", "source_of_truth", "ownership", "command_mapping", "compatibility_policy", "bridge_runtime_implemented"],
}


def find_repo_root() -> Path:
    path = Path(__file__).resolve()
    for parent in [path, *path.parents]:
        if (parent / ".aide").exists() and (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("could not locate AIDE repo root")


REPO_ROOT = find_repo_root()
EVIDENCE_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/dominium-readonly-seam-v0-check"


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_json(data: Any) -> str:
    return sha256_bytes(stable_json(data).encode("utf-8"))


def read_json(rel: str) -> Any:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(command: list[str], *, cwd: Path | None = None, timeout: int = 120, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=str(cwd or REPO_ROOT), capture_output=True, text=True, timeout=timeout, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(f"{command} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result


def git(root: Path, *args: str, check: bool = True) -> str:
    return run(["git", "-C", str(root), *args], check=check).stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def all_records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {})
    result: list[dict[str, Any]] = []
    if isinstance(records, dict):
        for value in records.values():
            if isinstance(value, list):
                result.extend([item for item in value if isinstance(item, dict)])
            elif isinstance(value, dict):
                result.append(value)
    return sorted(result, key=lambda item: (str(item.get("kind", "")), str(item.get("metadata", {}).get("id", ""))))


def projection_index(records: dict[str, Any]) -> dict[str, Any]:
    flat = all_records({"records": records})
    return {
        "schema_version": "aide.dominium-readonly-seam.projection-index.v0",
        "record_count": len(flat),
        "records": [
            {
                "kind": item["kind"],
                "id": item["metadata"]["id"],
                "semantic_owner": item["metadata"].get("semantic_owner"),
                "authority_role": item["metadata"].get("authority_role"),
                "digest": sha256_json(item),
            }
            for item in flat
        ],
    }


def refresh_projection_digest(candidate: dict[str, Any]) -> None:
    candidate.setdefault("content_digests", {})["projection_index"] = sha256_json(projection_index(candidate.get("records", {})))


def production_validate(candidate: dict[str, Any]) -> dict[str, Any]:
    sys.path.insert(0, str(REPO_ROOT))
    from core.interop.dominium import validation  # noqa: PLC0415

    return validation.validate_bundle(candidate, dominium_root=DOMINIUM_ROOT)


def production_accepts(candidate: dict[str, Any]) -> bool:
    report = production_validate(candidate)
    return report.get("validation_status") in {"PASS", "PASS_WITH_WARNINGS"} and not report.get("errors")


def add(checks: list[dict[str, Any]], check_id: str, outcome: str, severity: str, summary: str, details: dict[str, Any] | None = None) -> None:
    checks.append(
        {
            "id": check_id,
            "outcome": outcome,
            "severity": severity,
            "summary": summary,
            "details": details or {},
        }
    )


def canonical_repo_identity(remote_url: str) -> tuple[str, str, str] | None:
    value = remote_url.strip()
    if value.startswith("git@"):
        host, _, path = value[4:].partition(":")
    elif value.startswith("ssh://git@"):
        parsed = urlparse(value)
        host = parsed.hostname or ""
        path = parsed.path.lstrip("/")
    else:
        parsed = urlparse(value)
        if parsed.scheme not in {"https", "http"}:
            return None
        host = parsed.hostname or ""
        path = parsed.path.lstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = [part for part in path.split("/") if part]
    if len(parts) != 2:
        return None
    return host.lower(), parts[0].lower(), parts[1].lower()


def dominium_tree_fingerprint(root: Path) -> dict[str, Any]:
    selected_hashes: dict[str, str] = {}
    for rel, _role, _authority, _required in EXPECTED_SELECTED_INPUTS:
        try:
            selected_hashes[rel] = sha256_bytes(git_bytes(root, "show", f"{PINNED_DOMINIUM_HEAD}:{rel}"))
        except Exception as exc:  # noqa: BLE001
            selected_hashes[rel] = f"ERROR:{exc}"
    show_ref = git(root, "show-ref", check=False)
    return {
        "status_short_branch": git(root, "status", "--short", "--branch", check=False),
        "status_porcelain": git(root, "status", "--porcelain=v1", "--ignored", check=False),
        "head": git(root, "rev-parse", "HEAD", check=False),
        "origin_main": git(root, "rev-parse", "origin/main", check=False),
        "show_ref_sha256": sha256_bytes(show_ref.encode("utf-8")),
        "index_sha256": sha256_bytes(git(root, "ls-files", "-s", check=False).encode("utf-8")),
        "selected_pinned_source_hashes": selected_hashes,
    }


def copy_minimal_aide_root(destination: Path) -> None:
    for rel in [
        "core/__init__.py",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        "core/interop/__init__.py",
        ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json",
    ]:
        src = REPO_ROOT / rel
        dst = destination / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)
        else:
            dst.write_text("", encoding="utf-8")
    shutil.copytree(REPO_ROOT / "core/interop/dominium", destination / "core/interop/dominium")


def run_cli_probe(dominium_before: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    commands = ["status", "snapshot", "project", "validate", "diff", "demo"]
    unsupported = ["run", "invoke", "execute", "apply", "write", "sync", "push", "serve", "connect", "dispatch"]
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="aide-dominium-seam-check-", dir=str(EVIDENCE_ROOT)) as tmp:
        temp_root = Path(tmp)
        copy_minimal_aide_root(temp_root)
        for name in commands:
            started = time.monotonic()
            result = run(
                [
                    sys.executable,
                    str(REPO_ROOT / ".aide/scripts/aide_lite.py"),
                    "--repo-root",
                    str(temp_root),
                    "dominium-seam",
                    name,
                    "--dominium-root",
                    str(DOMINIUM_ROOT),
                    "--revision",
                    PINNED_DOMINIUM_HEAD,
                ],
                timeout=240,
            )
            results.append(
                {
                    "command": name,
                    "returncode": result.returncode,
                    "elapsed_ms": int((time.monotonic() - started) * 1000),
                    "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")),
                    "stderr": result.stderr.strip(),
                }
            )
        for name in unsupported:
            result = run(
                [
                    sys.executable,
                    str(REPO_ROOT / ".aide/scripts/aide_lite.py"),
                    "--repo-root",
                    str(temp_root),
                    "dominium-seam",
                    name,
                ],
                timeout=60,
            )
            results.append(
                {
                    "command": name,
                    "returncode": result.returncode,
                    "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")),
                    "stderr": result.stderr.strip(),
                }
            )
    dominium_after = dominium_tree_fingerprint(DOMINIUM_ROOT)
    return dominium_after, results


def main() -> int:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, Any]] = []
    negative_results: list[dict[str, Any]] = []

    bundle = read_json(".aide/reports/dominium-readonly-seam-v0/seam-bundle.json")
    source_snapshot = read_json(".aide/reports/dominium-readonly-seam-v0/source-snapshot.json")
    projection_report = read_json(".aide/reports/dominium-readonly-seam-v0/projection-index.json")
    validation_report = read_json(".aide/reports/dominium-readonly-seam-v0/validation.json")
    conformance_report = read_json(".aide/reports/dominium-readonly-seam-v0/conformance-results.json")
    demo_report = read_json(".aide/reports/dominium-readonly-seam-v0/demo-result.json")
    fixture_manifest = read_json(".aide/reports/dominium-readonly-seam-v0/fixture-manifest.json")
    schema = read_json(".aide/protocol/aide-dominium-readonly-seam-v0.schema.json")

    branch = git(REPO_ROOT, "branch", "--show-current", check=False)
    status = git(REPO_ROOT, "status", "--short", "--branch", check=False)
    head = git(REPO_ROOT, "rev-parse", "HEAD", check=False)
    build_ancestor = run(["git", "merge-base", "--is-ancestor", "a75635478be155ef7bc2b62de4ead3837212bbb8", "HEAD"]).returncode == 0
    add(checks, "baseline.aide_branch", "PASS" if branch == "main" else "FAIL", "material" if branch != "main" else "info", "AIDE branch is main", {"branch": branch, "status": status, "head": head})
    add(checks, "baseline.build_commit_ancestor", "PASS" if build_ancestor else "FAIL", "material" if not build_ancestor else "info", "Build commit is at HEAD or ancestor", {"head": head})

    remote_result = run(["git", "ls-remote", "https://github.com/Julesc013/dominium.git", "refs/heads/main"], timeout=120)
    remote_head = ""
    if remote_result.returncode == 0 and remote_result.stdout.strip():
        remote_head = remote_result.stdout.split()[0]
        add(checks, "freshness.remote_main", "PASS" if re.fullmatch(r"[0-9a-f]{40}", remote_head) else "FAIL", "warning" if remote_head != BASELINE_REMOTE_MAIN else "info", "Current remote Dominium main recorded", {"remote_head": remote_head, "baseline_remote_main": BASELINE_REMOTE_MAIN})
    else:
        add(checks, "freshness.remote_main", "WARN", "warning", "Could not confirm remote Dominium main", {"stderr": remote_result.stderr.strip()})

    remote_url = source_snapshot.get("repository_identity", {}).get("remote_url", "")
    parsed = canonical_repo_identity(remote_url)
    identity_ok = parsed == ("github.com", "julesc013", "dominium")
    add(checks, "identity.current_remote_url", "PASS" if identity_ok else "FAIL", "material" if not identity_ok else "info", "Projected repository identity uses canonical host/owner/repo", {"remote_url": remote_url, "parsed": parsed})

    sys.path.insert(0, str(REPO_ROOT))
    from core.interop.dominium import snapshot as prod_snapshot  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="aide-dominium-identity-", dir=str(EVIDENCE_ROOT)) as tmp:
        fake = Path(tmp)
        run(["git", "init"], cwd=fake, check=True)
        run(["git", "config", "user.email", "aide@example.invalid"], cwd=fake, check=True)
        run(["git", "config", "user.name", "AIDE Check"], cwd=fake, check=True)
        (fake / "README.md").write_text("fixture\n", encoding="utf-8")
        run(["git", "add", "README.md"], cwd=fake, check=True)
        run(["git", "commit", "-m", "fixture"], cwd=fake, check=True)
        run(["git", "remote", "add", "origin", "https://github.com/Julesc013/dominium-evil.git"], cwd=fake, check=True)
        try:
            prod_snapshot.build_source_snapshot(fake, revision="HEAD", expected_repo_identity="Julesc013/dominium", require_clean=True)
            lookalike_rejected = False
            rejection = "accepted"
        except Exception as exc:  # noqa: BLE001
            rejection = str(exc)
            lookalike_rejected = "unexpected repository identity" in rejection
    add(checks, "identity.lookalike_rejected", "PASS" if lookalike_rejected else "FAIL", "material" if not lookalike_rejected else "info", "Lookalike repository identity must fail before source inspection", {"observed_error": rejection})

    selected = source_snapshot.get("selected_files", [])
    selected_tuples = [(item.get("path"), item.get("role"), item.get("authority"), item.get("required")) for item in selected]
    add(checks, "selected_inputs.exact_set", "PASS" if selected_tuples == EXPECTED_SELECTED_INPUTS else "FAIL", "material" if selected_tuples != EXPECTED_SELECTED_INPUTS else "info", "Selected input path, role, authority, and required flags match accepted v0 set", {"expected_count": len(EXPECTED_SELECTED_INPUTS), "actual_count": len(selected_tuples)})
    selected_recompute: dict[str, dict[str, Any]] = {}
    selected_ok = True
    for item in selected:
        rel = item.get("path")
        try:
            payload = git_bytes(DOMINIUM_ROOT, "show", f"{PINNED_DOMINIUM_HEAD}:{rel}")
            tree_meta = git(DOMINIUM_ROOT, "ls-tree", PINNED_DOMINIUM_HEAD, str(rel))
            selected_recompute[str(rel)] = {
                "sha256": sha256_bytes(payload),
                "size_bytes": len(payload),
                "tree": tree_meta,
            }
            selected_ok = selected_ok and item.get("sha256") == sha256_bytes(payload) and item.get("size_bytes") == len(payload)
        except Exception as exc:  # noqa: BLE001
            selected_ok = False
            selected_recompute[str(rel)] = {"error": str(exc)}
    add(checks, "selected_inputs.hashes", "PASS" if selected_ok else "FAIL", "material" if not selected_ok else "info", "Selected source byte hashes and sizes recompute from immutable Git objects", {"paths": list(selected_recompute)})

    source_digest_payload = copy.deepcopy(source_snapshot)
    source_digest_payload.pop("snapshot_digest", None)
    source_digest = sha256_json(source_digest_payload)
    add(checks, "digest.source_snapshot_recompute", "PASS" if source_digest == source_snapshot.get("snapshot_digest") == bundle.get("content_digests", {}).get("source_snapshot") else "FAIL", "material" if source_digest != source_snapshot.get("snapshot_digest") else "info", "Source snapshot digest independently recomputes", {"expected": source_digest, "actual": source_snapshot.get("snapshot_digest")})

    bundle_without_self = copy.deepcopy(bundle)
    bundle_without_self.get("content_digests", {}).pop("seam_bundle_without_self_digest", None)
    expected_self_digest = sha256_json(bundle_without_self)
    actual_self_digest = bundle.get("content_digests", {}).get("seam_bundle_without_self_digest")
    add(checks, "digest.bundle_self_recompute", "PASS" if expected_self_digest == actual_self_digest else "FAIL", "material" if expected_self_digest != actual_self_digest else "info", "Bundle self digest must be calculated after final validation_summary/status fields", {"expected": expected_self_digest, "actual": actual_self_digest})

    record_digest_failures = []
    for record in all_records(bundle):
        record_id = record.get("metadata", {}).get("id")
        actual = bundle.get("content_digests", {}).get("records", {}).get(record_id)
        expected = sha256_json(record)
        if actual != expected:
            record_digest_failures.append({"id": record_id, "expected": expected, "actual": actual})
    add(checks, "digest.record_recompute", "PASS" if not record_digest_failures else "FAIL", "material" if record_digest_failures else "info", "All record digests independently recompute", {"failures": record_digest_failures})

    expected_projection = projection_index(bundle.get("records", {}))
    add(checks, "digest.projection_index_recompute", "PASS" if expected_projection == projection_report and sha256_json(expected_projection) == bundle.get("content_digests", {}).get("projection_index") else "FAIL", "material", "Projection index and digest independently recompute", {"expected_digest": sha256_json(expected_projection), "actual_digest": bundle.get("content_digests", {}).get("projection_index")})

    actual_counts: dict[str, int] = {}
    for record in all_records(bundle):
        actual_counts[record.get("kind", "")] = actual_counts.get(record.get("kind", ""), 0) + 1
    add(checks, "records.cardinality", "PASS" if actual_counts == EXPECTED_KIND_COUNTS else "FAIL", "material" if actual_counts != EXPECTED_KIND_COUNTS else "info", "Record kind cardinalities match v0 contract", {"actual": actual_counts, "expected": EXPECTED_KIND_COUNTS})
    manifest_ok = bundle.get("manifest", {}).get("record_count") == len(all_records(bundle)) and bundle.get("manifest", {}).get("selected_file_count") == len(selected)
    add(checks, "manifest.counts", "PASS" if manifest_ok else "FAIL", "material" if not manifest_ok else "info", "Manifest counts match bundle contents", {"manifest": bundle.get("manifest", {})})

    required_missing = []
    for record in all_records(bundle):
        kind = record.get("kind", "")
        spec = record.get("spec", {})
        for field in REQUIRED_FIELDS_BY_KIND.get(kind, []):
            if field not in spec:
                required_missing.append({"kind": kind, "id": record.get("metadata", {}).get("id"), "field": field})
    add(checks, "records.required_fields", "PASS" if not required_missing else "FAIL", "material" if required_missing else "info", "Kind-specific required fields exist in produced records", {"missing": required_missing})

    artifact_refs = {record.get("spec", {}).get("artifact_ref") for record in all_records(bundle) if record.get("kind") == "ArtifactReference"}
    event_refs = {record.get("spec", {}).get("event_ref") for record in all_records(bundle) if record.get("kind") == "EventEnvelope"}
    context = bundle.get("records", {}).get("context_descriptor", {})
    evidence = bundle.get("records", {}).get("evidence_reference_set", {})
    dangling_artifacts = [ref for ref in context.get("spec", {}).get("artifact_refs", []) if ref not in artifact_refs]
    dangling_evidence = [ref for ref in evidence.get("spec", {}).get("evidence_refs", []) if ref not in artifact_refs]
    add(checks, "references.closure", "PASS" if not dangling_artifacts and not dangling_evidence and event_refs else "FAIL", "material", "Context/evidence/event references close over projected records", {"dangling_artifacts": dangling_artifacts, "dangling_evidence": dangling_evidence, "event_refs": sorted(event_refs)})

    capability_record = bundle.get("records", {}).get("host_capability_set", {})
    capability_ids = [item.get("id") for item in capability_record.get("spec", {}).get("capabilities", []) if isinstance(item, dict)]
    forbidden_ids = [item.get("id") for item in capability_record.get("spec", {}).get("forbidden_capabilities", []) if isinstance(item, dict)]
    capability_ok = not (set(capability_ids) & FORBIDDEN_CAPABILITIES) and not (set(capability_ids) & set(forbidden_ids))
    add(checks, "capabilities.allowlist", "PASS" if capability_ok else "FAIL", "material" if not capability_ok else "info", "Capability set does not include mutation/dispatch/provider/worker capabilities", {"capabilities": capability_ids, "forbidden": forbidden_ids})

    events = [record for record in all_records(bundle) if record.get("kind") == "EventEnvelope"]
    sequences = [record.get("spec", {}).get("sequence") for record in events]
    correlations = {record.get("spec", {}).get("correlation_ref") for record in events}
    event_ok = sequences == list(range(1, len(events) + 1)) and len(correlations) == 1
    add(checks, "events.semantics", "PASS" if event_ok else "FAIL", "material" if not event_ok else "info", "Event sequences are unique/contiguous and share one correlation ref", {"sequences": sequences, "correlations": sorted(str(item) for item in correlations)})

    diagnostic_registry = json.loads(git_bytes(DOMINIUM_ROOT, "show", f"{PINNED_DOMINIUM_HEAD}:contracts/diagnostic/diagnostic_code.registry.json"))
    severity_registry = json.loads(git_bytes(DOMINIUM_ROOT, "show", f"{PINNED_DOMINIUM_HEAD}:contracts/diagnostic/diagnostic_severity.registry.json"))
    severity_ids = {item.get("id") for item in severity_registry.get("severities", []) if isinstance(item, dict)}
    projected_diagnostics = [record for record in all_records(bundle) if record.get("kind") == "DiagnosticProjection"]
    diag_mismatches = []
    native_by_id = {str(item.get("id") or item.get("code")): item for item in diagnostic_registry.get("codes", []) if isinstance(item, dict)}
    for record in projected_diagnostics:
        spec = record.get("spec", {})
        native = native_by_id.get(str(spec.get("diagnostic_id")))
        if not native or spec.get("severity") not in severity_ids or spec.get("code") != native.get("code"):
            diag_mismatches.append(spec.get("diagnostic_id"))
    diag_truncation_explicit = "diagnostic" in stable_json(bundle.get("omission_summary", {})).lower() and len(projected_diagnostics) < len(native_by_id)
    add(checks, "diagnostics.registry_integrity", "PASS" if not diag_mismatches else "FAIL", "material" if diag_mismatches else "info", "Projected diagnostics match native registry fields and severity IDs", {"native_count": len(native_by_id), "projected_count": len(projected_diagnostics), "mismatches": diag_mismatches, "truncation_explicit": diag_truncation_explicit})
    if len(projected_diagnostics) < len(native_by_id) and not diag_truncation_explicit:
        add(checks, "diagnostics.truncation_disclosure", "FAIL", "material", "Diagnostic projection truncation is not explicitly recorded in omission summary", {"native_count": len(native_by_id), "projected_count": len(projected_diagnostics)})

    refusal_registry = json.loads(git_bytes(DOMINIUM_ROOT, "show", f"{PINNED_DOMINIUM_HEAD}:contracts/refusal/refusal_code.registry.json"))
    projected_refusals = [record for record in all_records(bundle) if record.get("kind") == "RefusalProjection"]
    native_refusals = {str(item.get("refusal_id") or item.get("code")): item for item in refusal_registry.get("codes", []) if isinstance(item, dict)}
    refusal_mismatches = []
    for record in projected_refusals:
        spec = record.get("spec", {})
        native = native_refusals.get(str(spec.get("refusal_id")))
        if not native or spec.get("code") != native.get("code") or spec.get("reason") != native.get("reason"):
            refusal_mismatches.append(spec.get("refusal_id"))
    refusal_truncation_explicit = "refusal" in stable_json(bundle.get("omission_summary", {})).lower() and len(projected_refusals) < len(native_refusals)
    add(checks, "refusals.registry_integrity", "PASS" if not refusal_mismatches else "FAIL", "material" if refusal_mismatches else "info", "Projected refusals match native registry fields", {"native_count": len(native_refusals), "projected_count": len(projected_refusals), "mismatches": refusal_mismatches, "truncation_explicit": refusal_truncation_explicit})
    if len(projected_refusals) < len(native_refusals) and not refusal_truncation_explicit:
        add(checks, "refusals.truncation_disclosure", "FAIL", "material", "Refusal projection truncation is not explicitly recorded in omission summary", {"native_count": len(native_refusals), "projected_count": len(projected_refusals)})

    schema_material_gaps = []
    if schema.get("properties", {}).get("manifest", {}).get("type") == "object" and not schema.get("properties", {}).get("manifest", {}).get("required"):
        schema_material_gaps.append("manifest has no required fields")
    seam_record_spec = schema.get("$defs", {}).get("SeamRecord", {}).get("properties", {}).get("spec", {})
    if seam_record_spec.get("type") == "object" and not seam_record_spec.get("required"):
        schema_material_gaps.append("SeamRecord.spec has no kind-specific required fields")
    for field in ["source_snapshot", "cross_reference_index", "content_digests", "status"]:
        if not schema.get("properties", {}).get(field, {}).get("required"):
            schema_material_gaps.append(f"{field} has no required subfields")
    add(checks, "schema.effectiveness", "PASS" if not schema_material_gaps else "FAIL", "material" if schema_material_gaps else "info", "Public schema meaningfully constrains v0 seam documents", {"gaps": schema_material_gaps})

    negative_fixture_root = REPO_ROOT / ".aide/fixtures/dominium-readonly-seam/negative"
    fixture_gaps = []
    for path in sorted(negative_fixture_root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "bundle" not in data and "patch" not in data and "mutation_description" not in data:
            fixture_gaps.append(path.name)
    add(checks, "fixtures.negative_replayability", "PASS" if not fixture_gaps else "FAIL", "material" if fixture_gaps else "info", "Negative fixtures are independently replayable without importing production mutators", {"non_replayable": fixture_gaps, "fixture_count": len(list(negative_fixture_root.glob('*.json')))})

    conformance_evidence_paths = {item.get("evidence") for item in conformance_report.get("results", []) if isinstance(item, dict)}
    conformance_independent = len(conformance_evidence_paths) >= len(conformance_report.get("results", []))
    add(checks, "conformance.independence", "PASS" if conformance_independent else "FAIL", "material" if not conformance_independent else "info", "Each conformance expectation has distinct assertion evidence", {"expectation_count": len(conformance_report.get("results", [])), "distinct_evidence_count": len(conformance_evidence_paths), "evidence_paths": sorted(str(item) for item in conformance_evidence_paths)})

    if demo_report.get("elapsed_ms") == 0:
        add(checks, "demo.elapsed_time", "FAIL", "material", "Demo elapsed time is hard-coded or unmeasured as zero", {"elapsed_ms": demo_report.get("elapsed_ms")})
    if demo_report.get("forbidden_operation_count") == 0:
        add(checks, "demo.forbidden_operation_observation", "WARN", "warning", "Forbidden-operation count is reported as zero without independent instrumentation in the build report", {"forbidden_operation_count": demo_report.get("forbidden_operation_count")})

    # Adversarial production-validator comparisons. These use production validation
    # only as the target under test; materiality is based on independent mutations.
    alternate_revision = source_snapshot.get("freshness", {}).get("local_origin_main") or git(DOMINIUM_ROOT, "rev-parse", "HEAD", check=False)
    mutation_cases: list[tuple[str, str, str, Any]] = []

    def register(name: str, summary: str, severity: str, mutator) -> None:
        mutation_cases.append((name, summary, severity, mutator))

    def set_candidate_digest_fields(candidate: dict[str, Any]) -> None:
        refresh_projection_digest(candidate)

    register("mixed_record_revision", "Valid-but-wrong record source revision is accepted", "material", lambda c: c["records"]["host_manifest"]["metadata"].update({"source_revision": alternate_revision}))
    register("snapshot_digest_not_validated", "Snapshot digest fields can be corrupted without validation failure", "material", lambda c: (c["source_snapshot"].update({"snapshot_digest": "sha256:" + "0" * 64}), c["content_digests"].update({"source_snapshot": "sha256:" + "0" * 64})))
    register("selected_path_substitution", "Selected path set can be substituted with another valid tracked file", "material", lambda c: c["source_snapshot"]["selected_files"][0].update({"path": c["source_snapshot"]["selected_files"][1]["path"], "role": c["source_snapshot"]["selected_files"][1]["role"], "authority": c["source_snapshot"]["selected_files"][1]["authority"], "sha256": c["source_snapshot"]["selected_files"][1]["sha256"], "size_bytes": c["source_snapshot"]["selected_files"][1]["size_bytes"], "git_object": c["source_snapshot"]["selected_files"][1]["git_object"]}))
    register("second_host_capability_set", "Second singleton HostCapabilitySet is accepted", "material", lambda c: c["records"].update({"host_capability_set": [c["records"]["host_capability_set"], dict(c["records"]["host_capability_set"], metadata=dict(c["records"]["host_capability_set"]["metadata"], id="dominium-host-capability-set-extra-v0"))]}))
    register("dangling_artifact_reference", "Dangling artifact reference is accepted after digest refresh", "material", lambda c: c["records"]["context_descriptor"]["spec"]["artifact_refs"].__setitem__(0, "aide://artifact/not-present"))
    register("wrong_semantic_owner", "Valid-but-wrong semantic owner is accepted", "material", lambda c: c["records"]["artifact_references"][0]["metadata"].update({"semantic_owner": "AIDE"}))
    register("mutation_capability_labeled_readonly", "Forbidden mutation capability is accepted when labeled read_only", "material", lambda c: c["records"]["host_capability_set"]["spec"]["capabilities"].append({"id": "dominium.command.invoke", "side_effect_class": "read_only", "implemented_in_this_slice": True}))
    register("duplicate_event_sequence", "Duplicate event sequence is accepted because only sorting is checked", "material", lambda c: c["records"]["event_envelopes"][1]["spec"].update({"sequence": 1}))
    register("arbitrary_diagnostic_severity", "Arbitrary diagnostic severity is accepted when severity_valid remains true", "material", lambda c: c["records"]["diagnostic_projections"][0]["spec"].update({"severity": "criticality-made-up", "severity_valid": True}))
    register("invented_refusal", "Invented refusal projection is accepted", "material", lambda c: c["records"]["refusal_projections"].append(dict(c["records"]["refusal_projections"][0], metadata=dict(c["records"]["refusal_projections"][0]["metadata"], id="dominium-refusal-invented"), spec=dict(c["records"]["refusal_projections"][0]["spec"], refusal_id="DOMINIUM_FAKE_REFUSAL", code="DOMINIUM_FAKE_REFUSAL", reason="Plausible but not native"))))
    register("missing_host_id", "HostManifest required field removal is accepted", "material", lambda c: c["records"]["host_manifest"]["spec"].pop("host_id", None))

    for name, summary, severity, mutator in mutation_cases:
        candidate = copy.deepcopy(bundle)
        mutator(candidate)
        set_candidate_digest_fields(candidate)
        accepted = production_accepts(candidate)
        negative_results.append({"case": name, "production_accepted": accepted, "summary": summary})
        add(checks, f"negative.{name}", "FAIL" if accepted else "PASS", severity if accepted else "info", summary if accepted else f"Production validation rejected {name}")

    dominium_before = dominium_tree_fingerprint(DOMINIUM_ROOT)
    write_json(EVIDENCE_ROOT / "source-tree-hashes-before.json", dominium_before)
    dominium_after, cli_results = run_cli_probe(dominium_before)
    write_json(EVIDENCE_ROOT / "source-tree-hashes-after.json", dominium_after)
    no_write = dominium_before == dominium_after
    add(checks, "immutability.dominium", "PASS" if no_write else "FAIL", "material" if not no_write else "info", "Supported CLI probes did not change Dominium status, refs, index, or selected pinned bytes", {"cli_results": cli_results})
    unsupported_ok = all(item["returncode"] == 2 for item in cli_results if item["command"] in {"run", "invoke", "execute", "apply", "write", "sync", "push", "serve", "connect", "dispatch"})
    add(checks, "cli.unsupported_refusal", "PASS" if unsupported_ok else "FAIL", "material" if not unsupported_ok else "info", "Unsupported dominium-seam verbs fail closed with refusal exit code", {"cli_results": [item for item in cli_results if item["command"] not in {"status", "snapshot", "project", "validate", "diff", "demo"}]})
    supported_ok = all(item["returncode"] == 0 for item in cli_results if item["command"] in {"status", "snapshot", "project", "validate", "diff", "demo"})
    add(checks, "cli.supported_readonly_commands", "PASS" if supported_ok else "FAIL", "material" if not supported_ok else "info", "Supported dominium-seam read-only commands run against temp AIDE root", {"cli_results": [item for item in cli_results if item["command"] in {"status", "snapshot", "project", "validate", "diff", "demo"}]})

    source_texts = "\n".join(path.read_text(encoding="utf-8") for path in sorted((REPO_ROOT / "core/interop/dominium").glob("*.py")))
    forbidden_source_hits = []
    for pattern in [
        r"^\s*(import|from)\s+(socket|urllib|requests|httpx|openai|anthropic)\b",
        r"\[\s*['\"]fetch['\"]",
        r"\[\s*['\"]pull['\"]",
        r"\[\s*['\"]clone['\"]",
        r"\[\s*['\"]ls-remote['\"]",
    ]:
        if re.search(pattern, source_texts, flags=re.MULTILINE):
            forbidden_source_hits.append(pattern)
    add(checks, "source.no_network_provider_worker", "PASS" if not forbidden_source_hits else "FAIL", "material" if forbidden_source_hits else "info", "Production seam source contains no network/provider/worker/fetch/pull/clone calls", {"forbidden_patterns": forbidden_source_hits})

    material_findings = [item for item in checks if item["outcome"] == "FAIL" and item["severity"] == "material"]
    warnings = [item for item in checks if item["outcome"] in {"WARN", "FAIL"} and item["severity"] == "warning"]
    result = "REQUEST_CHANGES" if material_findings else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    next_task = REPAIR_NEXT if material_findings else PASS_NEXT
    report = {
        "schema_version": "aide.dominium-readonly-seam.check-report.v0",
        "task_id": TASK_ID,
        "source_task": BUILD_TASK_ID,
        "result": result,
        "status": "needs_review",
        "material_finding_count": len(material_findings),
        "warning_count": len(warnings),
        "aide_head": head,
        "aide_branch_status": status,
        "dominium_remote_main_head": remote_head,
        "dominium_pinned_head": PINNED_DOMINIUM_HEAD,
        "build_baseline": {
            "selected_dominium_inputs": len(selected),
            "projected_records": len(all_records(bundle)),
            "fixtures": fixture_manifest.get("fixture_count"),
            "focused_tests": 108,
            "conformance_expectations": conformance_report.get("expectation_count"),
            "source_mutations_after_cli_probe": 0 if no_write else 1,
        },
        "checks": checks,
        "material_findings": material_findings,
        "warnings": warnings,
        "negative_results": negative_results,
        "validation_report_status": validation_report.get("validation_status"),
        "demo_report_status": demo_report.get("status"),
        "recommended_next_task": next_task,
    }

    write_json(EVIDENCE_ROOT / "independent-check-results.json", report)
    write_json(EVIDENCE_ROOT / "independent-negative-results.json", {"schema_version": "aide.dominium-readonly-seam.negative-check-results.v0", "results": negative_results})
    write_json(REPORT_ROOT / "check-report.json", report)

    status_md = [
        "# Dominium Read-Only Seam v0 Independent Check Status",
        "",
        f"- task_id: `{TASK_ID}`",
        f"- result: `{result}`",
        "- status: `needs_review`",
        f"- source task: `{BUILD_TASK_ID}`",
        "- source build commit: `a75635478be155ef7bc2b62de4ead3837212bbb8`",
        f"- material findings: `{len(material_findings)}`",
        f"- warnings: `{len(warnings)}`",
        f"- current remote Dominium main: `{remote_head or 'not_confirmed'}`",
        f"- recommended next task: `{next_task}`",
        "",
        "The check performed no repair and did not modify production seam artifacts or Dominium.",
        "",
    ]
    write_text(REPORT_ROOT / "status.md", "\n".join(status_md))

    findings_md = ["# Material Findings", ""]
    if material_findings:
        for item in material_findings:
            findings_md.append(f"- `{item['id']}`: {item['summary']}")
    else:
        findings_md.append("- None.")
    findings_md.append("")
    write_text(REPORT_ROOT / "material-findings.md", "\n".join(findings_md))

    warnings_md = ["# Warning Disposition", ""]
    if warnings:
        for item in warnings:
            warnings_md.append(f"- `{item['id']}`: {item['summary']}")
    else:
        warnings_md.append("- None beyond inherited offline/read-only non-capabilities.")
    warnings_md.append("")
    write_text(REPORT_ROOT / "warning-disposition.md", "\n".join(warnings_md))

    non_caps = [
        "# Explicit Non-Capabilities Preserved",
        "",
        "- No Dominium command invocation.",
        "- No Host runtime, Host SDK, Workbench implementation, bridge runtime, service, database runtime, or transport.",
        "- No provider/model/network call by the seam implementation.",
        "- No worker execution.",
        "- No PatchTransaction apply, preview/apply/rollback, target-repository mutation, branch/worktree automation, GitHub mutation, release, or promotion.",
        "",
    ]
    write_text(REPORT_ROOT / "explicit-non-capabilities.md", "\n".join(non_caps))

    next_prompt = [
        f"# {next_task}",
        "",
        f"Create and process `{next_task}`.",
        "",
        "Use `.aide/queue/index.yaml` as canonical AIDE queue truth.",
        "",
    ]
    if next_task == REPAIR_NEXT:
        next_prompt.extend(
            [
                "Repair only the bounded material findings recorded by `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`.",
                "",
                "Do not broaden the seam beyond offline read-only projection. Do not modify Dominium, invoke Dominium commands, add runtime/service/workbench/provider/worker behavior, apply patches, mutate target repositories, or publish/release.",
                "",
                "After repair, stop at `needs_review` and recommend `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01` or the live repository's established repair-check id.",
                "",
            ]
        )
    else:
        next_prompt.extend(
            [
                "Accept the checked offline read-only seam only if the source chain still has no material findings.",
                "",
                "Stop at `needs_review` and do not implement downstream validation-slice work.",
                "",
            ]
        )
    write_text(REPORT_ROOT / "next-task-prompt.md", "\n".join(next_prompt))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
