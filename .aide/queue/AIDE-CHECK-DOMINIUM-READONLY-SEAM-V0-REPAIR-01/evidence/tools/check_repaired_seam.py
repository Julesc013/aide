"""Independent repair check for AIDE's Dominium read-only seam v0 repair.

This harness intentionally does not import production Dominium seam validation,
production conformance, production negative-fixture mutators, or repair
finding-disposition logic. It treats committed JSON/schema/report artifacts and
Git object content as the target under review.
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
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01"
REPAIR_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01"
ORIGINAL_BUILD_TASK_ID = "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01"
ORIGINAL_CHECK_TASK_ID = "AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01"
ACCEPT_TASK_ID = "AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01"
REPAIR_COMMIT_SHORT = "30931ba"
ORIGINAL_BUILD_COMMIT = "a75635478be155ef7bc2b62de4ead3837212bbb8"
ORIGINAL_CHECK_COMMIT = "692b4b3469e80a67f3f2f98612ec66c86b7394e9"
PINNED_DOMINIUM_HEAD = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"
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

EXPECTED_FINDINGS = [
    "identity.lookalike_rejected",
    "digest.bundle_self_recompute",
    "diagnostics.truncation_disclosure",
    "refusals.truncation_disclosure",
    "schema.effectiveness",
    "fixtures.negative_replayability",
    "conformance.independence",
    "demo.elapsed_time",
    "negative.mixed_record_revision",
    "negative.snapshot_digest_not_validated",
    "negative.second_host_capability_set",
    "negative.dangling_artifact_reference",
    "negative.wrong_semantic_owner",
    "negative.mutation_capability_labeled_readonly",
    "negative.duplicate_event_sequence",
    "negative.arbitrary_diagnostic_severity",
    "negative.invented_refusal",
    "negative.missing_host_id",
]

KIND_CONTAINERS = {
    "HostManifest": "host_manifest",
    "HostCapabilitySet": "host_capability_set",
    "WorkspaceDescriptor": "workspace_descriptor",
    "ContextDescriptor": "context_descriptor",
    "ArtifactReference": "artifact_references",
    "DiagnosticProjection": "diagnostic_projections",
    "RefusalProjection": "refusal_projections",
    "EvidenceReferenceSet": "evidence_reference_set",
    "EventEnvelope": "event_envelopes",
    "DominiumBridgeManifest": "dominium_bridge_manifest",
}

SINGLETON_CONTAINERS = {
    "host_manifest",
    "host_capability_set",
    "workspace_descriptor",
    "context_descriptor",
    "evidence_reference_set",
    "dominium_bridge_manifest",
}

LIST_CONTAINERS = {
    "artifact_references",
    "diagnostic_projections",
    "refusal_projections",
    "event_envelopes",
}

KIND_RULES = {
    "HostManifest": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "aide_read_only_host_projection",
        "required": {"host_id": str, "host_kind": str, "repository_identity": dict, "selected_revision": str, "supported_surfaces": list},
    },
    "HostCapabilitySet": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "aide_read_only_capability_projection",
        "required": {"capabilities": list, "forbidden_capabilities": list},
    },
    "WorkspaceDescriptor": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "workspace_projection_not_product_truth",
        "required": {"workspace_ref": str, "selected_revision": str, "branch": str, "identity_is_file_path": bool},
    },
    "ContextDescriptor": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "bounded_context_projection",
        "required": {"context_ref": str, "artifact_refs": list, "sections": list, "source_revision_binding": str},
    },
    "ArtifactReference": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "artifact_reference_to_dominium_source_bytes",
        "required": {"artifact_ref": str, "source_path": str, "source_role": str, "authority": str, "sha256": str, "source_revision": str},
    },
    "DiagnosticProjection": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "read_only_projection_of_dominium_diagnostic_contract",
        "required": {"diagnostic_id": str, "code": str, "owner": str, "severity": str, "category": str, "summary": str},
    },
    "RefusalProjection": {
        "semantic_owner": "Dominium",
        "identity_owner": "AIDE",
        "authority_role": "read_only_projection_of_dominium_refusal_contract",
        "required": {"refusal_id": str, "code": str, "owner": str, "category": str, "summary": str, "reason": str},
    },
    "EvidenceReferenceSet": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "evidence_reference_aggregation",
        "required": {"evidence_refs": list, "evidence_count": int, "native_evidence_meaning_owned_by": str, "aide_behavior": str},
    },
    "EventEnvelope": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "event_projection_not_event_store",
        "required": {"event_ref": str, "event_type": str, "sequence": int, "causation_ref": str, "correlation_ref": str, "summary": str},
    },
    "DominiumBridgeManifest": {
        "semantic_owner": "AIDE",
        "identity_owner": "AIDE",
        "authority_role": "mapping_version_law_projection",
        "required": {"bridge_id": str, "mapping_version": str, "source_revision": str, "source_of_truth": dict, "ownership": dict},
    },
}

IMPLEMENTED_CAPABILITIES = {
    "dominium.snapshot.read",
    "dominium.selected_files.hash",
    "dominium.contract_inventory.project",
    "dominium.diagnostic_registry.project",
    "dominium.refusal_registry.project",
    "dominium.evidence_refs.project",
    "dominium.event_envelopes.project",
}

FORBIDDEN_CAPABILITIES = {
    "dominium.command.invoke",
    "dominium.source.write",
    "dominium.service.start",
    "dominium.provider.call",
    "dominium.worker.execute",
    "dominium.patch.apply",
    "dominium.branch.create",
    "dominium.worktree.create",
    "dominium.release.publish",
}


def find_repo_root() -> Path:
    path = Path(__file__).resolve()
    for parent in [path, *path.parents]:
        if (parent / ".aide").exists() and (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("could not locate AIDE repo root")


REPO_ROOT = find_repo_root()
TASK_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID
EVIDENCE_ROOT = TASK_ROOT / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/dominium-readonly-seam-v0-repair-check"
SEAM_REPORT_ROOT = REPO_ROOT / ".aide/reports/dominium-readonly-seam-v0"
FIXTURE_ROOT = REPO_ROOT / ".aide/fixtures/dominium-readonly-seam"


def run(command: list[str], *, cwd: Path | None = None, check: bool = False, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=str(cwd or REPO_ROOT), capture_output=True, text=True, check=False, timeout=timeout)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result


def git(root: Path, *args: str, check: bool = True) -> str:
    return run(["git", "-C", str(root), *args], check=check).stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_json(data: Any) -> str:
    return sha256_bytes(stable_json(data).encode("utf-8"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def status_value(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.+?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip('"')
    return ""


def evidence_missing(task_id: str) -> int | None:
    result = run(["py", "-3", ".aide/scripts/aide_lite.py", "task", "inspect", "--task-id", task_id], timeout=120)
    if result.returncode != 0:
        return None
    match = re.search(r"missing_evidence:\s*(\d+)", result.stdout)
    return int(match.group(1)) if match else None


def add_assertion(assertions: list[dict[str, Any]], check_id: str, category: str, description: str, outcome: str, severity: str, expected: Any, observed: Any, evidence_refs: list[str], source_finding_id: str | None = None) -> None:
    assertions.append(
        {
            "id": check_id,
            "category": category,
            "description": description,
            "outcome": outcome,
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def all_records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    records = bundle.get("records", {})
    result: list[dict[str, Any]] = []
    if isinstance(records, dict):
        for value in records.values():
            if isinstance(value, list):
                result.extend(item for item in value if isinstance(item, dict))
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


def snapshot_payload_for_digest(snapshot: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(snapshot)
    payload.pop("snapshot_digest", None)
    return payload


def bundle_payload_for_self_digest(bundle: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(bundle)
    digests = payload.get("content_digests")
    if isinstance(digests, dict):
        digests.pop("seam_bundle_without_self_digest", None)
    return payload


def parse_ref(value: Any) -> tuple[str, str] | None:
    if not isinstance(value, str) or "?" in value or "#" in value or "\\" in value:
        return None
    match = re.match(r"^aide://([A-Za-z0-9._~-]+)/([A-Za-z0-9._~@+=:,-]+)$", value)
    if not match:
        return None
    if ".." in match.group(2) or "/" in match.group(2):
        return None
    return match.group(1), match.group(2)


def normalize_remote(remote_url: str) -> tuple[str, str, str, str] | None:
    raw = str(remote_url or "").strip()
    if not raw or "?" in raw or "#" in raw:
        return None
    if raw.startswith("git@"):
        host_part, sep, path_part = raw[4:].partition(":")
        if not sep:
            return None
        transport = "ssh"
        host = host_part.lower()
        path = path_part
    else:
        parsed = urlparse(raw)
        if parsed.scheme not in {"https", "ssh"}:
            return None
        if parsed.username not in {None, "", "git"}:
            return None
        transport = parsed.scheme
        host = (parsed.hostname or "").lower()
        path = parsed.path.lstrip("/")
    parts = [part for part in path.strip("/").split("/") if part]
    if len(parts) != 2:
        return None
    repo = parts[1][:-4] if parts[1].endswith(".git") else parts[1]
    return host, parts[0].lower(), repo.lower(), transport


def git_object_json(root: Path, revision: str, rel: str) -> dict[str, Any]:
    return json.loads(git_bytes(root, "show", f"{revision}:{rel}").decode("utf-8"))


def native_registries() -> tuple[dict[str, dict[str, Any]], set[str], dict[str, dict[str, Any]]]:
    diagnostics = git_object_json(DOMINIUM_ROOT, PINNED_DOMINIUM_HEAD, "contracts/diagnostic/diagnostic_code.registry.json")
    severities = git_object_json(DOMINIUM_ROOT, PINNED_DOMINIUM_HEAD, "contracts/diagnostic/diagnostic_severity.registry.json")
    refusals = git_object_json(DOMINIUM_ROOT, PINNED_DOMINIUM_HEAD, "contracts/refusal/refusal_code.registry.json")
    native_diagnostics = {str(item.get("id") or item.get("code")): item for item in diagnostics.get("codes", []) if isinstance(item, dict)}
    native_severities = {str(item.get("id")) for item in severities.get("severities", []) if isinstance(item, dict)}
    native_refusals = {str(item.get("refusal_id") or item.get("code")): item for item in refusals.get("codes", []) if isinstance(item, dict)}
    return native_diagnostics, native_severities, native_refusals


def independent_validate(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    def err(code: str, path: str, message: str, expected: Any = None, observed: Any = None) -> None:
        errors.append({"code": code, "path": path, "message": message, "expected": expected, "observed": observed})

    source = bundle.get("source_snapshot", {}) if isinstance(bundle.get("source_snapshot"), dict) else {}
    manifest = bundle.get("manifest", {}) if isinstance(bundle.get("manifest"), dict) else {}
    metadata = bundle.get("metadata", {}) if isinstance(bundle.get("metadata"), dict) else {}
    records = bundle.get("records", {}) if isinstance(bundle.get("records"), dict) else {}
    revision = source.get("source_revision")
    if not isinstance(revision, str) or not re.match(r"^[0-9a-f]{40}$", revision):
        err("revision.syntax", "/source_snapshot/source_revision", "source revision must be a commit SHA")
    repo_identity = source.get("repository_identity", {}) if isinstance(source.get("repository_identity"), dict) else {}
    if repo_identity.get("canonical_identity") != "github.com/julesc013/dominium":
        err("repository.identity", "/source_snapshot/repository_identity/canonical_identity", "unexpected canonical identity", "github.com/julesc013/dominium", repo_identity.get("canonical_identity"))
    expected_paths = [item[0] for item in EXPECTED_SELECTED_INPUTS]
    selected = source.get("selected_files", []) if isinstance(source.get("selected_files"), list) else []
    actual_paths = []
    for index, item in enumerate(selected):
        if not isinstance(item, dict):
            err("selected_files.item", f"/source_snapshot/selected_files/{index}", "selected file entry must be object")
            continue
        path = item.get("path")
        if not isinstance(path, str) or not path:
            err("path.syntax", f"/source_snapshot/selected_files/{index}/path", "source path must be a string")
            continue
        if path.startswith("/") or re.match(r"^[A-Za-z]:", path):
            err("path.absolute", f"/source_snapshot/selected_files/{index}/path", "absolute path is forbidden")
        if ".." in path.replace("\\", "/").split("/"):
            err("path.traversal", f"/source_snapshot/selected_files/{index}/path", "path traversal is forbidden")
        actual_paths.append(path.replace("\\", "/"))
        if not isinstance(item.get("sha256"), str) or not re.match(r"^sha256:[0-9a-f]{64}$", item.get("sha256", "")):
            err("digest.source.syntax", f"/source_snapshot/selected_files/{index}/sha256", "source digest must be sha256")
    if actual_paths != expected_paths:
        err("selected_files.exact_set", "/source_snapshot/selected_files", "selected files differ from expected ordered set", expected_paths, actual_paths)

    if manifest.get("source_revision") != revision:
        err("revision.binding", "/manifest/source_revision", "manifest revision mismatch", revision, manifest.get("source_revision"))
    if metadata.get("source_revision") != revision:
        err("revision.binding", "/metadata/source_revision", "bundle metadata revision mismatch", revision, metadata.get("source_revision"))
    freshness = bundle.get("freshness", {}) if isinstance(bundle.get("freshness"), dict) else {}
    if freshness.get("selected_revision") != revision:
        err("revision.binding", "/freshness/selected_revision", "freshness revision mismatch", revision, freshness.get("selected_revision"))

    for container in SINGLETON_CONTAINERS:
        if not isinstance(records.get(container), dict):
            err("cardinality.singleton", f"/records/{container}", "singleton container must be one object")
    for container in LIST_CONTAINERS:
        if not isinstance(records.get(container), list) or not records.get(container):
            err("cardinality.list", f"/records/{container}", "list container must be a non-empty list")

    flat = all_records(bundle)
    ids = [item.get("metadata", {}).get("id") for item in flat if isinstance(item.get("metadata"), dict)]
    if len(ids) != len(set(ids)):
        err("identity.duplicate", "/records", "record ids must be unique")
    if len(flat) != manifest.get("record_count"):
        err("record_count", "/manifest/record_count", "manifest record count mismatch", manifest.get("record_count"), len(flat))

    for record in flat:
        kind = record.get("kind")
        rule = KIND_RULES.get(str(kind))
        if not rule:
            err("kind.unsupported", "/records", "unsupported record kind", list(KIND_RULES), kind)
            continue
        meta = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
        spec = record.get("spec", {}) if isinstance(record.get("spec"), dict) else {}
        if meta.get("source_revision") != revision:
            err("revision.binding", f"/records/{kind}/metadata/source_revision", "record revision mismatch", revision, meta.get("source_revision"))
        if meta.get("semantic_owner") != rule["semantic_owner"]:
            err("ownership.semantic", f"/records/{kind}/metadata/semantic_owner", "semantic owner mismatch", rule["semantic_owner"], meta.get("semantic_owner"))
        if meta.get("identity_owner") != rule["identity_owner"]:
            err("ownership.identity", f"/records/{kind}/metadata/identity_owner", "identity owner mismatch", rule["identity_owner"], meta.get("identity_owner"))
        if meta.get("authority_role") != rule["authority_role"]:
            err("authority.role", f"/records/{kind}/metadata/authority_role", "authority role mismatch", rule["authority_role"], meta.get("authority_role"))
        if meta.get("schema_version") != "aide.dominium-readonly-seam.v0":
            err("schema.version", f"/records/{kind}/metadata/schema_version", "schema version mismatch")
        for field, expected_type in rule["required"].items():
            if field not in spec:
                err("spec.required", f"/records/{kind}/spec/{field}", "required spec field missing")
            elif not isinstance(spec[field], expected_type):
                err("spec.type", f"/records/{kind}/spec/{field}", "required spec field has wrong type", expected_type.__name__, type(spec[field]).__name__)
        for key in ["selected_revision", "source_revision", "source_revision_binding"]:
            if key in spec and spec[key] != revision:
                err("revision.binding", f"/records/{kind}/spec/{key}", "spec revision mismatch", revision, spec[key])

    source_digest = sha256_json(snapshot_payload_for_digest(source))
    digests = bundle.get("content_digests", {}) if isinstance(bundle.get("content_digests"), dict) else {}
    if source.get("snapshot_digest") != source_digest:
        err("digest.snapshot", "/source_snapshot/snapshot_digest", "source snapshot digest mismatch", source_digest, source.get("snapshot_digest"))
    if digests.get("source_snapshot") != source_digest:
        err("digest.source", "/content_digests/source_snapshot", "content source digest mismatch", source_digest, digests.get("source_snapshot"))
    expected_projection = projection_index(records)
    if digests.get("projection_index") != sha256_json(expected_projection):
        err("digest.projection_index", "/content_digests/projection_index", "projection index digest mismatch")
    record_digests = digests.get("records", {}) if isinstance(digests.get("records"), dict) else {}
    for record in flat:
        record_id = record.get("metadata", {}).get("id")
        if record_digests.get(record_id) != sha256_json(record):
            err("digest.record", f"/content_digests/records/{record_id}", "record digest mismatch")
    expected_self = sha256_json(bundle_payload_for_self_digest(bundle))
    if digests.get("seam_bundle_without_self_digest") != expected_self:
        err("digest.bundle_self", "/content_digests/seam_bundle_without_self_digest", "bundle self digest mismatch", expected_self, digests.get("seam_bundle_without_self_digest"))

    cross = bundle.get("cross_reference_index", {}) if isinstance(bundle.get("cross_reference_index"), dict) else {}
    bundle_ref = cross.get("bundle_ref")
    artifact_refs = set(cross.get("artifact_refs", []) if isinstance(cross.get("artifact_refs"), list) else [])
    event_refs = set(cross.get("event_refs", []) if isinstance(cross.get("event_refs"), list) else [])
    for ref_path, ref_value in [
        ("/cross_reference_index/bundle_ref", bundle_ref),
        ("/cross_reference_index/workspace_ref", cross.get("workspace_ref")),
        ("/cross_reference_index/context_ref", cross.get("context_ref")),
    ]:
        if parse_ref(ref_value) is None:
            err("reference.syntax", ref_path, "invalid ReferenceID syntax")
    workspace = records.get("workspace_descriptor", {}) if isinstance(records.get("workspace_descriptor"), dict) else {}
    context = records.get("context_descriptor", {}) if isinstance(records.get("context_descriptor"), dict) else {}
    if workspace.get("spec", {}).get("workspace_ref") != cross.get("workspace_ref"):
        err("reference.closure", "/cross_reference_index/workspace_ref", "workspace index target mismatch")
    if context.get("spec", {}).get("context_ref") != cross.get("context_ref"):
        err("reference.closure", "/cross_reference_index/context_ref", "context index target mismatch")
    for ref in context.get("spec", {}).get("artifact_refs", []) if isinstance(context.get("spec"), dict) else []:
        parsed = parse_ref(ref)
        if parsed is None:
            err("reference.syntax", "/records/context_descriptor/spec/artifact_refs", "invalid artifact ref syntax")
        elif parsed[0] != "artifact" or ref not in artifact_refs:
            err("reference.closure", "/records/context_descriptor/spec/artifact_refs", "artifact ref is dangling or wrong kind", "artifact ref in index", ref)
    evidence = records.get("evidence_reference_set", {}) if isinstance(records.get("evidence_reference_set"), dict) else {}
    evidence_spec = evidence.get("spec", {}) if isinstance(evidence.get("spec"), dict) else {}
    if evidence_spec.get("native_evidence_meaning_owned_by") != "Dominium":
        err("ownership.native_evidence", "/records/evidence_reference_set/spec/native_evidence_meaning_owned_by", "native evidence owner mismatch", "Dominium", evidence_spec.get("native_evidence_meaning_owned_by"))
    for ref in evidence_spec.get("evidence_refs", []) if isinstance(evidence_spec.get("evidence_refs"), list) else []:
        parsed = parse_ref(ref)
        if parsed is None:
            err("reference.syntax", "/records/evidence_reference_set/spec/evidence_refs", "invalid evidence ref syntax")
        elif parsed[0] != "artifact" or ref not in artifact_refs:
            err("reference.closure", "/records/evidence_reference_set/spec/evidence_refs", "evidence ref is dangling or wrong kind", "artifact ref in index", ref)

    capabilities = records.get("host_capability_set", {}) if isinstance(records.get("host_capability_set"), dict) else {}
    capability_spec = capabilities.get("spec", {}) if isinstance(capabilities.get("spec"), dict) else {}
    implemented = [item for item in capability_spec.get("capabilities", []) if isinstance(item, dict)]
    forbidden = [item for item in capability_spec.get("forbidden_capabilities", []) if isinstance(item, dict)]
    implemented_ids = {str(item.get("id")) for item in implemented}
    forbidden_ids = {str(item.get("id")) for item in forbidden}
    if implemented_ids != IMPLEMENTED_CAPABILITIES:
        err("capability.implemented_set", "/records/host_capability_set/spec/capabilities", "implemented capability set mismatch", sorted(IMPLEMENTED_CAPABILITIES), sorted(implemented_ids))
    if forbidden_ids != FORBIDDEN_CAPABILITIES:
        err("capability.forbidden_set", "/records/host_capability_set/spec/forbidden_capabilities", "forbidden capability set mismatch", sorted(FORBIDDEN_CAPABILITIES), sorted(forbidden_ids))
    if implemented_ids & FORBIDDEN_CAPABILITIES:
        err("capability.mutation", "/records/host_capability_set/spec/capabilities", "forbidden ID implemented as read-only", sorted(FORBIDDEN_CAPABILITIES), sorted(implemented_ids & FORBIDDEN_CAPABILITIES))
    for item in implemented:
        if item.get("side_effect_class") != "read_only" or item.get("implemented_in_this_slice") is not True:
            err("capability.readonly", "/records/host_capability_set/spec/capabilities", "implemented capability is not read-only")
    if any(item.get("implemented_in_this_slice") is True for item in forbidden):
        err("capability.mutation", "/records/host_capability_set/spec/forbidden_capabilities", "forbidden capability marked implemented")

    events = records.get("event_envelopes", []) if isinstance(records.get("event_envelopes"), list) else []
    sequences = [item.get("spec", {}).get("sequence") for item in events if isinstance(item, dict)]
    if sequences != list(range(1, len(sequences) + 1)):
        err("event.sequence", "/records/event_envelopes/spec/sequence", "event sequence must be contiguous 1..N", list(range(1, len(sequences) + 1)), sequences)
    refs = [item.get("spec", {}).get("event_ref") for item in events if isinstance(item, dict)]
    if len(refs) != len(set(refs)):
        err("event.identity", "/records/event_envelopes/spec/event_ref", "event refs must be unique")
    expected_causation = f"aide://source/dominium-{str(revision)[:12]}"
    for index, event in enumerate(events):
        spec = event.get("spec", {}) if isinstance(event, dict) else {}
        if spec.get("event_ref") not in event_refs:
            err("reference.closure", f"/records/event_envelopes/{index}/spec/event_ref", "event ref is not indexed")
        if spec.get("correlation_ref") != bundle_ref:
            err("event.correlation", f"/records/event_envelopes/{index}/spec/correlation_ref", "event correlation must target bundle")
        if spec.get("causation_ref") != expected_causation:
            err("event.causation", f"/records/event_envelopes/{index}/spec/causation_ref", "event causation must target source observation", expected_causation, spec.get("causation_ref"))
        if spec.get("universal_event_store_implemented") is not False:
            err("event.store", f"/records/event_envelopes/{index}/spec/universal_event_store_implemented", "event store must remain false")
        if not spec.get("event_type") or not spec.get("summary"):
            err("event.required", f"/records/event_envelopes/{index}/spec", "event type and summary must be non-empty")

    native_diagnostics, native_severities, native_refusals = native_registries()
    for index, record in enumerate(records.get("diagnostic_projections", []) if isinstance(records.get("diagnostic_projections"), list) else []):
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        native = native_diagnostics.get(str(spec.get("diagnostic_id", "")))
        if native is None:
            err("diagnostic.registry", f"/records/diagnostic_projections/{index}/spec/diagnostic_id", "diagnostic is not native")
        else:
            for field in ["code", "owner", "severity", "category", "summary"]:
                if spec.get(field) != native.get(field):
                    err("diagnostic.registry", f"/records/diagnostic_projections/{index}/spec/{field}", f"diagnostic {field} mismatch", native.get(field), spec.get(field))
        if spec.get("severity") not in native_severities:
            err("diagnostic.registry", f"/records/diagnostic_projections/{index}/spec/severity", "diagnostic severity is not native")
    for index, record in enumerate(records.get("refusal_projections", []) if isinstance(records.get("refusal_projections"), list) else []):
        spec = record.get("spec", {}) if isinstance(record, dict) else {}
        native = native_refusals.get(str(spec.get("refusal_id", "")))
        if native is None:
            err("refusal.registry", f"/records/refusal_projections/{index}/spec/refusal_id", "refusal is not native")
        else:
            for field in ["code", "owner", "category", "summary", "reason", "diagnostic_codes", "related_commands"]:
                if spec.get(field) != native.get(field):
                    err("refusal.registry", f"/records/refusal_projections/{index}/spec/{field}", f"refusal {field} mismatch", native.get(field), spec.get(field))
            native_recovery = native.get("recovery", {}) if isinstance(native.get("recovery"), dict) else {}
            if spec.get("recovery_action") != native_recovery.get("action"):
                err("refusal.registry", f"/records/refusal_projections/{index}/spec/recovery_action", "refusal recovery action mismatch", native_recovery.get("action"), spec.get("recovery_action"))

    if bundle.get("status", {}).get("generated_projection_marked_canonical") is not False:
        err("authority.canonical_overclaim", "/status/generated_projection_marked_canonical", "generated projection marked canonical")
    for field in [
        "network_call_performed",
        "provider_or_model_called",
        "worker_executed",
        "target_repository_mutated",
        "branch_or_worktree_created",
        "github_mutation_performed",
    ]:
        if bundle.get("status", {}).get(field) is not False:
            err("status.false_boundary", f"/status/{field}", "forbidden status fact must be false")
    return errors


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with /: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]


def apply_operations(document: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    for op in operations:
        parts = pointer_parts(op["path"])
        parent: Any = candidate
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = parts[-1]
        if isinstance(parent, list):
            index = len(parent) if key == "-" else int(key)
            if op["op"] == "remove":
                parent.pop(index)
            elif op["op"] == "add":
                parent.insert(index, copy.deepcopy(op.get("value")))
            elif op["op"] == "replace":
                parent[index] = copy.deepcopy(op.get("value"))
            else:
                raise ValueError(f"unsupported list op {op['op']}")
        elif isinstance(parent, dict):
            if op["op"] == "remove":
                parent.pop(key, None)
            elif op["op"] in {"add", "replace"}:
                parent[key] = copy.deepcopy(op.get("value"))
            else:
                raise ValueError(f"unsupported object op {op['op']}")
        else:
            raise ValueError("operation parent is not a container")
    return candidate


def tree_state(root: Path) -> dict[str, Any]:
    refs = git(root, "show-ref", check=False)
    index = git(root, "ls-files", "-s", check=False)
    selected_hashes = {}
    for rel, _role, _authority, _required in EXPECTED_SELECTED_INPUTS:
        try:
            selected_hashes[rel] = sha256_bytes(git_bytes(root, "show", f"{PINNED_DOMINIUM_HEAD}:{rel}"))
        except Exception as exc:  # noqa: BLE001
            selected_hashes[rel] = f"ERROR:{exc}"
    return {
        "head": git(root, "rev-parse", "HEAD", check=False),
        "status_short_branch": git(root, "status", "--short", "--branch", check=False),
        "status_porcelain": git(root, "status", "--porcelain=v1", "--ignored", check=False),
        "refs_sha256": sha256_bytes(refs.encode("utf-8")),
        "index_sha256": sha256_bytes(index.encode("utf-8")),
        "config_sha256": sha256_bytes((root / ".git/config").read_bytes()) if (root / ".git/config").exists() else "",
        "selected_pinned_source_hashes": selected_hashes,
    }


def replay_negative_fixtures(bundle: dict[str, Any]) -> dict[str, Any]:
    results = []
    for path in sorted((FIXTURE_ROOT / "negative").glob("*.json")):
        fixture = read_json(path)
        operations = fixture.get("operations", [])
        expected_codes = set(fixture.get("expected_error_codes", []))
        try:
            base_digest_ok = fixture.get("base_bundle_sha256") == sha256_json(bundle)
            first = apply_operations(bundle, operations)
            second = apply_operations(bundle, operations)
            deterministic = first == second
            invalid_digest_ok = fixture.get("invalid_bundle_sha256") == sha256_json(first)
            errors = independent_validate(first)
            observed_codes = {item["code"] for item in errors}
            code_match = bool(expected_codes & observed_codes)
            result = "PASS" if base_digest_ok and deterministic and invalid_digest_ok and code_match else "FAILED_VALIDATION"
            detail = None
        except Exception as exc:  # noqa: BLE001
            first = {}
            deterministic = False
            invalid_digest_ok = False
            observed_codes = set()
            base_digest_ok = False
            code_match = False
            result = "FAILED_VALIDATION"
            detail = str(exc)
        results.append(
            {
                "fixture_path": path.relative_to(REPO_ROOT).as_posix(),
                "name": fixture.get("name", path.stem),
                "base_digest_ok": base_digest_ok,
                "operation_count": len(operations),
                "deterministic_replay": deterministic,
                "invalid_digest_ok": invalid_digest_ok,
                "expected_error_codes": sorted(expected_codes),
                "observed_error_codes": sorted(observed_codes),
                "result": result,
                "detail": detail,
            }
        )
    return {
        "schema_version": "aide.dominium-readonly-seam.repair-check.negative-results.v0",
        "fixture_count": len(results),
        "passed_count": sum(1 for item in results if item["result"] == "PASS"),
        "failed_count": sum(1 for item in results if item["result"] != "PASS"),
        "results": results,
    }


def schema_review(schema: dict[str, Any]) -> dict[str, Any]:
    seam_record = schema.get("$defs", {}).get("SeamRecord", {})
    records = schema.get("properties", {}).get("records", {})
    source = schema.get("properties", {}).get("source_snapshot", {})
    spec = seam_record.get("properties", {}).get("spec", {})
    required = set(schema.get("required", []))
    required_ok = {
        "manifest": "manifest" in required,
        "source_snapshot": "source_snapshot" in required,
        "cross_reference_index": "cross_reference_index" in required,
        "content_digests": "content_digests" in required,
        "status": "status" in required,
        "registry_projection_summary": "registry_projection_summary" in required,
    }
    invalid_cases = {
        "empty_manifest": "manifest" in required and "manifest" in schema.get("properties", {}),
        "empty_source_snapshot": bool(source.get("required")),
        "empty_cross_reference_index": bool(schema.get("properties", {}).get("cross_reference_index", {}).get("required")),
        "empty_content_digests": bool(schema.get("properties", {}).get("content_digests", {}).get("required")),
        "empty_status": bool(schema.get("properties", {}).get("status", {}).get("required")),
        "kind_specific_spec_constraints": any(key in spec for key in ["oneOf", "anyOf", "allOf", "required"]),
        "records_additional_properties_closed": records.get("additionalProperties") is False,
    }
    material_gaps = []
    if not all(required_ok.values()):
        material_gaps.append("top-level required bundle sections are incomplete")
    if not invalid_cases["kind_specific_spec_constraints"]:
        material_gaps.append("public schema does not constrain kind-specific spec fields")
    if not schema.get("properties", {}).get("status", {}).get("required"):
        material_gaps.append("public schema does not constrain status facts")
    return {
        "required_sections": required_ok,
        "invalid_case_coverage": invalid_cases,
        "material_gaps": material_gaps,
        "result": "PASS" if not material_gaps else "REQUEST_CHANGES",
    }


def conformance_review(report: dict[str, Any]) -> dict[str, Any]:
    results = report.get("results", []) if isinstance(report.get("results"), list) else []
    details = []
    missing_required_fields = 0
    observations = set()
    for item in results:
        missing = [field for field in ["id", "description", "result"] if field not in item]
        for field in ["assertion_id", "expected", "observed", "evidence_refs"]:
            if field not in item:
                missing.append(field)
        observations.add(str(item.get("observation", "")))
        if missing:
            missing_required_fields += 1
        details.append({"id": item.get("id"), "result": item.get("result"), "missing_fields": missing})
    aggregate_only = len(observations) <= 1
    return {
        "expectation_count": len(results),
        "passed_count": sum(1 for item in results if item.get("result") == "PASS"),
        "results_have_required_assertion_fields": missing_required_fields == 0,
        "missing_required_field_count": missing_required_fields,
        "aggregate_only_pattern_detected": aggregate_only,
        "details": details,
        "result": "PASS" if missing_required_fields == 0 and not aggregate_only else "REQUEST_CHANGES",
    }


def operation_ledger_review(demo: dict[str, Any]) -> dict[str, Any]:
    ledger = demo.get("operation_ledger", {}) if isinstance(demo.get("operation_ledger"), dict) else {}
    operations = ledger.get("observations", []) if isinstance(ledger.get("observations"), list) else []
    operation_count = ledger.get("observation_count")
    forbidden_count = ledger.get("forbidden_operation_count")
    allowed_count = sum(1 for item in operations if item.get("allowed") is True)
    required_fields = {"operation", "target", "classification", "allowed", "source"}
    missing_fields = [index for index, item in enumerate(operations) if not required_fields.issubset(set(item))]
    coverage_terms = " ".join(str(item.get("operation", "")) for item in operations).lower()
    coverage = {
        "git_reads": all(term in coverage_terms for term in ["status", "rev-parse", "remote get-url", "branch", "show"]),
        "filesystem_writes": "file write" in coverage_terms or "filesystem write" in coverage_terms,
        "network_attempts": "network" in coverage_terms or "socket" in coverage_terms,
        "provider_model_attempts": "provider" in coverage_terms or "model" in coverage_terms,
        "worker_dispatch": "worker" in coverage_terms,
        "mutation_apply": "apply" in coverage_terms or "mutation" in coverage_terms,
        "branch_worktree_ref_ops": "worktree" in coverage_terms or "checkout" in coverage_terms or "fetch" in coverage_terms,
    }
    injected = copy.deepcopy(demo)
    injected.setdefault("operation_ledger", {}).setdefault("observations", []).append(
        {
            "operation": "git fetch",
            "target": "Dominium",
            "classification": "forbidden_remote_ref_update",
            "allowed": False,
            "source": "repair_check_injection",
        }
    )
    injected["operation_ledger"]["observation_count"] = len(injected["operation_ledger"]["observations"])
    injected["operation_ledger"]["forbidden_operation_count"] = sum(1 for item in injected["operation_ledger"]["observations"] if item.get("allowed") is False)
    injection_detected = injected["operation_ledger"]["forbidden_operation_count"] > forbidden_count
    material_gaps = []
    if operation_count != len(operations):
        material_gaps.append("operation_count mismatch")
    if forbidden_count != sum(1 for item in operations if item.get("allowed") is False):
        material_gaps.append("forbidden_operation_count mismatch")
    if "allowed_operation_count" not in ledger:
        material_gaps.append("allowed_operation_count missing")
    if "instrumentation_coverage" not in ledger:
        material_gaps.append("instrumentation coverage missing")
    if not all(coverage.values()):
        material_gaps.append("ledger does not describe every required operation family")
    if missing_fields:
        material_gaps.append("operation entries missing required fields")
    if not injection_detected:
        material_gaps.append("forbidden operation injection not detected")
    return {
        "operation_count": operation_count,
        "allowed_operation_count": allowed_count,
        "forbidden_operation_count": forbidden_count,
        "coverage": coverage,
        "missing_field_entries": missing_fields,
        "injection_detected": injection_detected,
        "material_gaps": material_gaps,
        "result": "PASS" if not material_gaps else "REQUEST_CHANGES",
    }


def deterministic_copy_files(source_root: Path, dest_root: Path) -> None:
    rels = [
        ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json",
        ".aide/scripts/aide_lite.py",
        "core/__init__.py",
        "core/interop/__init__.py",
    ]
    rels.extend(path.relative_to(source_root).as_posix() for path in (source_root / "core/interop/dominium").glob("*.py"))
    for rel in rels:
        src = source_root / rel
        if not src.is_file():
            continue
        dst = dest_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def cross_process_determinism() -> dict[str, Any]:
    outputs = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        for index in range(2):
            aide_root = base / f"aide-{index}"
            deterministic_copy_files(REPO_ROOT, aide_root)
            result = run(
                [
                    "py",
                    "-3",
                    str(aide_root / ".aide/scripts/aide_lite.py"),
                    "--repo-root",
                    str(aide_root),
                    "dominium-seam",
                    "project",
                    "--dominium-root",
                    str(DOMINIUM_ROOT),
                    "--revision",
                    PINNED_DOMINIUM_HEAD,
                ],
                cwd=base,
                timeout=180,
            )
            bundle_path = aide_root / ".aide/reports/dominium-readonly-seam-v0/seam-bundle.json"
            outputs.append(
                {
                    "index": index,
                    "returncode": result.returncode,
                    "bundle_sha256": sha256_bytes(bundle_path.read_bytes()) if bundle_path.exists() else "",
                    "stderr": result.stderr.strip(),
                    "absolute_path_leak": str(base).replace("\\", "/") in bundle_path.read_text(encoding="utf-8") if bundle_path.exists() else True,
                }
            )
    passed = len(outputs) == 2 and outputs[0]["returncode"] == 0 and outputs[1]["returncode"] == 0 and outputs[0]["bundle_sha256"] == outputs[1]["bundle_sha256"] and not any(item["absolute_path_leak"] for item in outputs)
    return {"result": "PASS" if passed else "FAILED_VALIDATION", "outputs": outputs}


def report_consistency(bundle: dict[str, Any], validation: dict[str, Any], conformance: dict[str, Any], fixture_manifest: dict[str, Any], demo: dict[str, Any], repair_report: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "record_count": len(all_records(bundle)) == bundle.get("manifest", {}).get("record_count") == validation.get("record_count") == demo.get("record_counts", {}).get("records") == repair_report.get("projected_records"),
        "fixture_count": fixture_manifest.get("fixture_count") == demo.get("record_counts", {}).get("fixtures") == repair_report.get("fixture_count"),
        "validation_status": validation.get("validation_status") == demo.get("validation_result") == repair_report.get("validation_status"),
        "conformance_count": conformance.get("expectation_count") == repair_report.get("conformance_expectations"),
        "next_task": bundle.get("manifest", {}).get("recommended_next_task") == validation.get("recommended_next_task") == conformance.get("recommended_next_task") == demo.get("recommended_next_task") == repair_report.get("recommended_next_task"),
        "source_revision": bundle.get("manifest", {}).get("source_revision") == bundle.get("source_snapshot", {}).get("source_revision") == demo.get("input_revision"),
        "operation_count": demo.get("forbidden_operation_count") == repair_report.get("forbidden_operation_count"),
    }
    return {"checks": checks, "result": "PASS" if all(checks.values()) else "REQUEST_CHANGES"}


def direct_injection_results(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    injections: list[tuple[str, str, list[dict[str, Any]]]] = [
        ("mixed_record_revision", "revision.binding", [{"op": "replace", "path": "/records/host_manifest/metadata/source_revision", "value": "0" * 40}]),
        ("snapshot_digest", "digest.snapshot", [{"op": "replace", "path": "/source_snapshot/snapshot_digest", "value": "sha256:" + "1" * 64}]),
        ("second_host_capability_set", "cardinality.singleton", [{"op": "replace", "path": "/records/host_capability_set", "value": [bundle["records"]["host_capability_set"], bundle["records"]["host_capability_set"]]}]),
        ("dangling_artifact", "reference.closure", [{"op": "add", "path": "/records/context_descriptor/spec/artifact_refs/-", "value": "aide://artifact/dangling"}]),
        ("wrong_owner", "ownership.semantic", [{"op": "replace", "path": "/records/artifact_references/0/metadata/semantic_owner", "value": "AIDE"}]),
        ("forbidden_capability", "capability.mutation", [{"op": "replace", "path": "/records/host_capability_set/spec/capabilities/0/id", "value": "dominium.patch.apply"}]),
        ("duplicate_event_sequence", "event.sequence", [{"op": "replace", "path": "/records/event_envelopes/1/spec/sequence", "value": 1}]),
        ("bad_diagnostic_severity", "diagnostic.registry", [{"op": "replace", "path": "/records/diagnostic_projections/0/spec/severity", "value": "notice"}]),
        ("invented_refusal", "refusal.registry", [{"op": "replace", "path": "/records/refusal_projections/0/spec/refusal_id", "value": "dominium.refusal.invented"}]),
        ("missing_host_id", "spec.required", [{"op": "remove", "path": "/records/host_manifest/spec/host_id"}]),
        ("wrong_causation", "event.causation", [{"op": "replace", "path": "/records/event_envelopes/0/spec/causation_ref", "value": "aide://event/unrelated"}]),
        ("wrong_diagnostic_summary", "diagnostic.registry", [{"op": "replace", "path": "/records/diagnostic_projections/0/spec/summary", "value": "Wrong"}]),
        ("wrong_refusal_recovery", "refusal.registry", [{"op": "replace", "path": "/records/refusal_projections/0/spec/recovery_action", "value": "wrong"}]),
        ("wrong_host_id_type", "spec.type", [{"op": "replace", "path": "/records/host_manifest/spec/host_id", "value": 123}]),
    ]
    results = []
    for name, expected_code, operations in injections:
        candidate = apply_operations(bundle, operations)
        errors = independent_validate(candidate)
        codes = {item["code"] for item in errors}
        results.append(
            {
                "name": name,
                "expected_code": expected_code,
                "observed_codes": sorted(codes),
                "result": "PASS" if expected_code in codes else "FAILED_VALIDATION",
            }
        )
    return results


def build_closure_matrix(independent: dict[str, Any]) -> list[dict[str, Any]]:
    injections_by_name = {item["name"]: item for item in independent["direct_injections"]}
    fixture_names = {item["name"]: item for item in independent["negative_results"]["results"]}
    schema_result = independent["schema_review"]["result"]
    conformance_result = independent["conformance_review"]["result"]
    operation_result = independent["operation_ledger_review"]["result"]
    registry_review = independent["registry_review"]
    rows = []
    mapping = {
        "identity.lookalike_rejected": ("exact repository identity parser rejects lookalikes before source inspection", "identity code and repository matrix", independent["identity_matrix"]["result"] == "PASS", "identity"),
        "digest.bundle_self_recompute": ("final bundle digest recomputes over final payload", "digest review and mutation injections", independent["digest_review"]["result"] == "PASS", "digest"),
        "diagnostics.truncation_disclosure": ("diagnostic truncation is disclosed", "registry projection summary", registry_review["diagnostics"]["result"] == "PASS", "registry"),
        "refusals.truncation_disclosure": ("refusal truncation is disclosed", "registry projection summary", registry_review["refusals"]["result"] == "PASS", "registry"),
        "schema.effectiveness": ("public schema and semantic rules reject empty public objects", "schema review", schema_result == "PASS", "schema"),
        "fixtures.negative_replayability": ("negative fixtures replay from serialized operations", "fixture replay", independent["negative_results"]["failed_count"] == 0, "fixtures"),
        "conformance.independence": ("conformance has expectation-level evidence", "conformance review", conformance_result == "PASS", "conformance"),
        "demo.elapsed_time": ("demo no longer records placeholder elapsed_ms zero", "demo report", independent["demo_timing"]["result"] == "PASS", "demo"),
        "negative.mixed_record_revision": ("mixed record revision rejected", "direct injection", injections_by_name["mixed_record_revision"]["result"] == "PASS", "revision"),
        "negative.snapshot_digest_not_validated": ("snapshot digest corruption rejected", "direct injection", injections_by_name["snapshot_digest"]["result"] == "PASS", "digest"),
        "negative.second_host_capability_set": ("second singleton container rejected", "direct injection", injections_by_name["second_host_capability_set"]["result"] == "PASS", "cardinality"),
        "negative.dangling_artifact_reference": ("dangling artifact reference rejected", "direct injection", injections_by_name["dangling_artifact"]["result"] == "PASS", "reference"),
        "negative.wrong_semantic_owner": ("wrong kind-specific semantic owner rejected", "direct injection", injections_by_name["wrong_owner"]["result"] == "PASS", "ownership"),
        "negative.mutation_capability_labeled_readonly": ("mutation capability ID rejected regardless of read-only label", "direct injection", injections_by_name["forbidden_capability"]["result"] == "PASS", "capability"),
        "negative.duplicate_event_sequence": ("duplicate event sequence rejected", "direct injection", injections_by_name["duplicate_event_sequence"]["result"] == "PASS", "event"),
        "negative.arbitrary_diagnostic_severity": ("diagnostic severity compared against native registry", "direct injection", injections_by_name["bad_diagnostic_severity"]["result"] == "PASS", "diagnostic"),
        "negative.invented_refusal": ("invented refusal rejected by native registry comparison", "direct injection", injections_by_name["invented_refusal"]["result"] == "PASS", "refusal"),
        "negative.missing_host_id": ("missing HostManifest.host_id rejected", "direct injection", injections_by_name["missing_host_id"]["result"] == "PASS", "required-fields"),
    }
    for index, finding_id in enumerate(EXPECTED_FINDINGS, start=1):
        summary, evidence, closed, category = mapping[finding_id]
        fixture = fixture_names.get(finding_id.split(".")[-1], {})
        rows.append(
            {
                "index": index,
                "finding_id": finding_id,
                "original_observed_behavior": summary,
                "repair_implementation": "see repair commit and changed-file review",
                "changed_production_files": "core/interop/dominium/** and public schema where applicable",
                "new_or_updated_tests": "repair regression suite and replayable negative fixtures",
                "replayable_fixture": fixture.get("fixture_path", ""),
                "independent_repair_check_assertion": evidence,
                "observed_repaired_behavior": "closed" if closed else "remaining material gap",
                "remaining_limitation": "" if closed else "independent repair check found required evidence or behavior gap",
                "result": "CLOSED" if closed else "OPEN",
                "category": category,
            }
        )
    return rows


def main() -> int:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    tools_root = EVIDENCE_ROOT / "tools"
    before = {"aide": tree_state(REPO_ROOT), "dominium": tree_state(DOMINIUM_ROOT)}
    write_json(EVIDENCE_ROOT / "before-tree-state.json", before)

    bundle = read_json(SEAM_REPORT_ROOT / "seam-bundle.json")
    validation_report = read_json(SEAM_REPORT_ROOT / "validation.json")
    conformance_report = read_json(SEAM_REPORT_ROOT / "conformance-results.json")
    fixture_manifest = read_json(SEAM_REPORT_ROOT / "fixture-manifest.json")
    demo = read_json(SEAM_REPORT_ROOT / "demo-result.json")
    repair_report = read_json(REPO_ROOT / ".aide/reports/dominium-readonly-seam-v0-repair/repair-report.json")
    schema = read_json(REPO_ROOT / ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json")

    assertions: list[dict[str, Any]] = []
    repair_full_sha = git(REPO_ROOT, "rev-parse", REPAIR_COMMIT_SHORT)
    current_branch = git(REPO_ROOT, "branch", "--show-current")
    status_lines = git(REPO_ROOT, "status", "--short").splitlines()
    allowed_output_prefixes = (
        f"?? .aide/queue/{TASK_ID}/",
        "?? .aide/reports/dominium-readonly-seam-v0-repair-check/",
    )
    unexpected_status_lines = [
        line for line in status_lines if not any(line.startswith(prefix) for prefix in allowed_output_prefixes)
    ]
    worktree_clean = not unexpected_status_lines
    add_assertion(assertions, "baseline.branch", "baseline", "current branch is main", "PASS" if current_branch == "main" else "FAIL", "material", "main", current_branch, ["git status --short --branch"])
    add_assertion(assertions, "baseline.worktree_clean", "baseline", "worktree clean before check outputs except this task's allowed outputs", "PASS" if worktree_clean else "FAIL", "material", True, {"clean": worktree_clean, "unexpected_status_lines": unexpected_status_lines}, ["git status --short --branch"])
    add_assertion(assertions, "baseline.repair_sha", "baseline", "repair commit resolves locally", "PASS" if repair_full_sha.startswith(REPAIR_COMMIT_SHORT) else "FAIL", "material", REPAIR_COMMIT_SHORT, repair_full_sha, ["git rev-parse 30931ba"])
    add_assertion(assertions, "baseline.repair_ancestor", "baseline", "repair commit is at HEAD or ancestor", "PASS" if run(["git", "merge-base", "--is-ancestor", repair_full_sha, "HEAD"]).returncode == 0 else "FAIL", "material", "ancestor", repair_full_sha, ["git merge-base --is-ancestor"])
    for task_id, expected_missing in [
        (ACCEPT_TASK_ID, 0),
        (ORIGINAL_BUILD_TASK_ID, 0),
        (ORIGINAL_CHECK_TASK_ID, 0),
        (REPAIR_TASK_ID, 0),
    ]:
        missing = evidence_missing(task_id)
        add_assertion(assertions, f"baseline.{task_id}.evidence", "baseline", f"{task_id} missing evidence is zero", "PASS" if missing == expected_missing else "FAIL", "material", expected_missing, missing, [f"task inspect --task-id {task_id}"])

    original_check_status = status_value(REPO_ROOT / ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/status.yaml", "result")
    original_material_count = status_value(REPO_ROOT / ".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/status.yaml", "material_finding_count")
    repair_result = status_value(REPO_ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/status.yaml", "result")
    repair_next = status_value(REPO_ROOT / ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/status.yaml", "recommended_next_task")
    add_assertion(assertions, "baseline.original_check_result", "baseline", "original check remains REQUEST_CHANGES", "PASS" if original_check_status == "REQUEST_CHANGES" else "FAIL", "material", "REQUEST_CHANGES", original_check_status, [".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/status.yaml"])
    add_assertion(assertions, "baseline.original_material_count", "baseline", "original check material count remains 18", "PASS" if original_material_count == "18" else "FAIL", "material", "18", original_material_count, [".aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/status.yaml"])
    add_assertion(assertions, "baseline.repair_result", "baseline", "repair result is PASS or PASS_WITH_WARNINGS", "PASS" if repair_result in {"PASS", "PASS_WITH_WARNINGS"} else "FAIL", "material", "PASS or PASS_WITH_WARNINGS", repair_result, [".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/status.yaml"])
    add_assertion(assertions, "baseline.repair_next", "baseline", "repair recommends this check", "PASS" if repair_next == TASK_ID else "FAIL", "material", TASK_ID, repair_next, [".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/status.yaml"])

    historical_diffs = {
        "original_build_queue": git(REPO_ROOT, "diff", "--name-only", ORIGINAL_BUILD_COMMIT, "HEAD", "--", f".aide/queue/{ORIGINAL_BUILD_TASK_ID}", check=False).splitlines(),
        "original_failed_check_queue": git(REPO_ROOT, "diff", "--name-only", ORIGINAL_CHECK_COMMIT, "HEAD", "--", f".aide/queue/{ORIGINAL_CHECK_TASK_ID}", check=False).splitlines(),
        "original_failed_check_reports": git(REPO_ROOT, "diff", "--name-only", ORIGINAL_CHECK_COMMIT, "HEAD", "--", ".aide/reports/dominium-readonly-seam-v0-check", check=False).splitlines(),
    }
    for key, paths in historical_diffs.items():
        add_assertion(assertions, f"history.{key}", "source-chain", f"{key} unchanged from source commit", "PASS" if not paths else "FAIL", "material", [], paths, ["git diff --name-only"])

    allowed_prefixes = [
        ".aide/protocol/aide-dominium-readonly-seam-v0.schema.json",
        "core/interop/dominium/",
        ".aide/scripts/tests/test_aide_dominium_readonly_seam.py",
        ".aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py",
        ".aide/fixtures/dominium-readonly-seam/",
        ".aide/interop/dominium/",
        ".aide/reports/dominium-readonly-seam-v0/",
        ".aide/reports/dominium-readonly-seam-v0-repair/",
        ".aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01/",
        ".aide/queue/index.yaml",
        "PLANS.md",
        "IMPLEMENT.md",
    ]
    repair_changed = git(REPO_ROOT, "diff", "--name-only", ORIGINAL_CHECK_COMMIT, REPAIR_COMMIT_SHORT, check=False).splitlines()
    out_of_scope = [path for path in repair_changed if not any(path == prefix or path.startswith(prefix) for prefix in allowed_prefixes)]
    add_assertion(assertions, "source-chain.changed_files", "source-chain", "repair changed files are within authorized surfaces", "PASS" if not out_of_scope else "FAIL", "material", "authorized surfaces only", out_of_scope, ["git diff --name-only 692b4b..30931ba"])

    identity_inputs = {
        "https://github.com/Julesc013/dominium.git": True,
        "https://github.com/Julesc013/dominium": True,
        "git@github.com:Julesc013/dominium.git": True,
        "ssh://git@github.com/Julesc013/dominium.git": True,
        "https://github.com/Julesc013/dominium-evil.git": False,
        "https://github.com/Julesc013/dominium.git.evil.example": False,
        "https://github.com/attacker/Julesc013/dominium.git": False,
        "https://example.com/Julesc013/dominium.git": False,
        "file:///tmp/Julesc013/dominium": False,
        "C:/tmp/Julesc013/dominium": False,
        "https://user:secret@github.com/Julesc013/dominium.git": False,
        "https://github.com/Julesc013/dominium.git?redirect=evil": False,
        "https://github.com/Julesc013/dominium.git#other": False,
    }
    identity_results = []
    for remote, should_accept in identity_inputs.items():
        parsed = normalize_remote(remote)
        accepted = parsed is not None and parsed[:3] == ("github.com", "julesc013", "dominium") and parsed[3] in {"https", "ssh"}
        identity_results.append({"remote": remote, "expected_accept": should_accept, "observed_accept": accepted, "result": "PASS" if accepted == should_accept else "FAIL"})
    identity_matrix = {"result": "PASS" if all(item["result"] == "PASS" for item in identity_results) else "FAILED_VALIDATION", "results": identity_results}

    independent_errors = independent_validate(bundle)
    add_assertion(assertions, "bundle.independent_validate", "semantic", "independent validator accepts committed repaired bundle", "PASS" if not independent_errors else "FAIL", "material", [], independent_errors, [".aide/reports/dominium-readonly-seam-v0/seam-bundle.json"])

    digest_mutations = []
    for name, path, value in [
        ("validation_summary.validated", "/validation_summary/validated", False),
        ("validation_summary.error_count", "/validation_summary/error_count", 99),
        ("status.network_call_performed", "/status/network_call_performed", True),
        ("manifest.record_count", "/manifest/record_count", 999),
        ("omission_summary.reason", "/omission_summary/reason", "changed"),
        ("authority_classification.conflict_policy", "/authority_classification/conflict_policy", "ignore"),
        ("registry_projection_summary.diagnostics.projected_count", "/registry_projection_summary/diagnostics/projected_count", 999),
    ]:
        candidate = apply_operations(bundle, [{"op": "replace", "path": path, "value": value}])
        codes = {item["code"] for item in independent_validate(candidate)}
        digest_mutations.append({"name": name, "observed_codes": sorted(codes), "result": "PASS" if "digest.bundle_self" in codes or "digest.projection_index" in codes or "record_count" in codes or "status.false_boundary" in codes else "FAILED_VALIDATION"})
    digest_review = {"result": "PASS" if all(item["result"] == "PASS" for item in digest_mutations) and not independent_errors else "FAILED_VALIDATION", "mutations": digest_mutations}

    schema_result = schema_review(schema)
    conformance_result = conformance_review(conformance_report)
    op_result = operation_ledger_review(demo)
    negative_results = replay_negative_fixtures(bundle)
    injections = direct_injection_results(bundle)

    native_diagnostics, _native_severities, native_refusals = native_registries()
    registry_summary = bundle.get("registry_projection_summary", {})
    diag_summary = registry_summary.get("diagnostics", {}) if isinstance(registry_summary, dict) else {}
    ref_summary = registry_summary.get("refusals", {}) if isinstance(registry_summary, dict) else {}
    registry_review = {
        "diagnostics": {
            "native_count": len(native_diagnostics),
            "projected_count": len(bundle.get("records", {}).get("diagnostic_projections", [])),
            "summary": diag_summary,
            "has_source_registry_digest": "source_registry_digest" in diag_summary,
            "result": "PASS" if diag_summary.get("native_count") == len(native_diagnostics) and diag_summary.get("projected_count") == len(bundle.get("records", {}).get("diagnostic_projections", [])) and "source_registry_digest" in diag_summary else "REQUEST_CHANGES",
        },
        "refusals": {
            "native_count": len(native_refusals),
            "projected_count": len(bundle.get("records", {}).get("refusal_projections", [])),
            "summary": ref_summary,
            "has_source_registry_digest": "source_registry_digest" in ref_summary,
            "result": "PASS" if ref_summary.get("native_count") == len(native_refusals) and ref_summary.get("projected_count") == len(bundle.get("records", {}).get("refusal_projections", [])) and "source_registry_digest" in ref_summary else "REQUEST_CHANGES",
        },
    }

    elapsed = demo.get("elapsed_time", {}) if isinstance(demo.get("elapsed_time"), dict) else {}
    demo_timing = {
        "result": "PASS" if elapsed.get("status") == "not_measured" and elapsed.get("elapsed_ms") is None and "elapsed_ms" not in demo else "FAILED_VALIDATION",
        "observed": elapsed,
    }

    consistency = report_consistency(bundle, validation_report, conformance_report, fixture_manifest, demo, repair_report)
    determinism = cross_process_determinism()

    independent = {
        "identity_matrix": identity_matrix,
        "digest_review": digest_review,
        "schema_review": schema_result,
        "negative_results": negative_results,
        "conformance_review": conformance_result,
        "operation_ledger_review": op_result,
        "registry_review": registry_review,
        "demo_timing": demo_timing,
        "direct_injections": injections,
        "report_consistency": consistency,
        "cross_process_determinism": determinism,
    }
    closure = build_closure_matrix(independent)

    material_assertion_failures = [
        item for item in assertions if item["severity"] == "material" and item["outcome"] != "PASS"
    ]
    material_gaps = []
    if identity_matrix["result"] != "PASS":
        material_gaps.append("exact repository identity matrix failed")
    if digest_review["result"] != "PASS":
        material_gaps.append("digest integrity review failed")
    if schema_result["result"] != "PASS":
        material_gaps.extend(schema_result["material_gaps"])
    if negative_results["failed_count"]:
        material_gaps.append("one or more replayable negative fixtures failed independent replay")
    if conformance_result["result"] != "PASS":
        material_gaps.append("conformance results lack required independent assertion fields")
    if op_result["result"] != "PASS":
        material_gaps.extend(op_result["material_gaps"])
    if registry_review["diagnostics"]["result"] != "PASS":
        material_gaps.append("diagnostic projection disclosure is incomplete")
    if registry_review["refusals"]["result"] != "PASS":
        material_gaps.append("refusal projection disclosure is incomplete")
    if demo_timing["result"] != "PASS":
        material_gaps.append("demo timing representation is not accepted")
    if any(item["result"] != "PASS" for item in injections):
        material_gaps.append("one or more direct semantic injections was not detected")
    if consistency["result"] != "PASS":
        material_gaps.append("report consistency failed")
    if determinism["result"] != "PASS":
        material_gaps.append("cross-process determinism failed")
    material_gaps.extend(item["description"] for item in material_assertion_failures)

    result = "PASS_WITH_WARNINGS" if not material_gaps else "REQUEST_CHANGES"
    recommended_next = "AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01" if result == "PASS_WITH_WARNINGS" else "AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02"

    after = {"aide": tree_state(REPO_ROOT), "dominium": tree_state(DOMINIUM_ROOT)}
    write_json(EVIDENCE_ROOT / "after-tree-state.json", after)
    no_write = before["dominium"] == after["dominium"]
    add_assertion(assertions, "immutability.dominium", "immutability", "Dominium tree state unchanged", "PASS" if no_write else "FAIL", "material", before["dominium"], after["dominium"], ["before-tree-state.json", "after-tree-state.json"])

    check_report = {
        "schema_version": "aide.dominium-readonly-seam.repair-check.v0",
        "task_id": TASK_ID,
        "source_repair_task": REPAIR_TASK_ID,
        "repair_commit": repair_full_sha,
        "result": result,
        "material_finding_count": len(material_gaps),
        "material_gaps": sorted(set(material_gaps)),
        "assertions": assertions,
        "independent": independent,
        "finding_closure_count": len(closure),
        "finding_closure_open_count": sum(1 for item in closure if item["result"] != "CLOSED"),
        "dominium_no_write": no_write,
        "recommended_next_task": recommended_next,
    }

    write_json(EVIDENCE_ROOT / "independent-repair-check.json", check_report)
    write_json(EVIDENCE_ROOT / "independent-negative-results.json", negative_results)
    write_json(EVIDENCE_ROOT / "independent-conformance-results.json", conformance_result)
    write_json(EVIDENCE_ROOT / "finding-closure-matrix.json", {"schema_version": "aide.dominium-readonly-seam.finding-closure-matrix.v0", "findings": closure})
    write_json(REPORT_ROOT / "check-report.json", check_report)
    write_json(REPORT_ROOT / "finding-closure-matrix.json", {"schema_version": "aide.dominium-readonly-seam.finding-closure-matrix.v0", "findings": closure})

    status_md = [
        "# Dominium Read-Only Seam v0 Repair Check Status",
        "",
        f"- result: `{result}`",
        f"- material_finding_count: `{len(material_gaps)}`",
        f"- repair_commit: `{repair_full_sha}`",
        f"- finding rows: `{len(closure)}`",
        f"- recommended_next_task: `{recommended_next}`",
        "",
    ]
    write_text(REPORT_ROOT / "status.md", "\n".join(status_md))

    rows = ["# Finding Closure Matrix", ""]
    for item in closure:
        rows.append(f"- `{item['finding_id']}`: `{item['result']}` - {item['observed_repaired_behavior']}")
    rows.append("")
    write_text(REPORT_ROOT / "finding-closure-matrix.md", "\n".join(rows))

    def topical(name: str, title: str, data: Any) -> None:
        write_text(REPORT_ROOT / name, f"# {title}\n\n```json\n{stable_json(data)}```\n")

    topical("source-chain-review.md", "Source Chain Review", {"repair_commit": repair_full_sha, "historical_diffs": historical_diffs, "changed_file_out_of_scope": out_of_scope})
    topical("identity-and-revision-review.md", "Identity And Revision Review", {"identity_matrix": identity_matrix, "revision_errors": [item for item in independent_errors if item["code"].startswith("revision")]})
    topical("digest-integrity-review.md", "Digest Integrity Review", digest_review)
    topical("schema-contract-review.md", "Schema Contract Review", schema_result)
    topical("reference-cardinality-ownership-review.md", "Reference Cardinality Ownership Review", {"independent_errors": [item for item in independent_errors if item["code"].startswith(("reference", "cardinality", "ownership"))]})
    topical("registry-projection-review.md", "Registry Projection Review", registry_review)
    topical("fixture-replay-review.md", "Fixture Replay Review", negative_results)
    topical("conformance-independence-review.md", "Conformance Independence Review", conformance_result)
    topical("demo-operation-ledger-review.md", "Demo Operation Ledger Review", op_result)
    topical("determinism-immutability-review.md", "Determinism Immutability Review", {"determinism": determinism, "dominium_no_write": no_write, "before": before["dominium"], "after": after["dominium"]})
    topical("report-consistency-review.md", "Report Consistency Review", consistency)
    topical("new-regression-review.md", "New Regression Review", {"material_gaps": sorted(set(material_gaps)), "direct_injections": injections})
    topical("warning-disposition.md", "Warning Disposition", {"warnings": ["seam remains offline/read-only", "local Dominium remains behind origin/main", "operation ledger instrumentation remains incomplete when result is REQUEST_CHANGES"]})
    write_text(REPORT_ROOT / "explicit-non-capabilities.md", "# Explicit Non-Capabilities\n\n- No Dominium command invocation.\n- No Host runtime or Host SDK.\n- No Workbench implementation.\n- No bridge runtime, service, database runtime, or transport.\n- No network-backed seam operation.\n- No provider/model call.\n- No worker execution.\n- No PatchTransaction apply.\n- No DevelopmentTransaction or PreviewSession.\n- No preview/apply/rollback.\n- No target-repository mutation.\n- No branch/worktree automation.\n- No GitHub mutation.\n- No release or promotion.\n")
    write_text(REPORT_ROOT / "next-task-prompt.md", f"# {recommended_next}\n\nCreate and process `{recommended_next}`.\n\nUse `.aide/queue/index.yaml` as canonical queue truth.\n\nThis repair check result was `{result}`. Do not begin this task from the repair-check turn.\n")

    print(stable_json({"result": result, "material_finding_count": len(material_gaps), "recommended_next_task": recommended_next}))
    return 0 if result in {"PASS_WITH_WARNINGS", "REQUEST_CHANGES"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
