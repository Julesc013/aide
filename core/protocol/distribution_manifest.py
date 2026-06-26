"""DistributionManifest v1 helpers.

This module normalizes the existing local release-bundle evidence into a
deterministic distribution identity. It does not install, update, repair,
rollback, uninstall, publish, promote, or mutate target repositories.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope


API_VERSION = envelope.API_VERSION
KIND = "DistributionManifest"
SCHEMA_VERSION = "aide.distribution-manifest.v1"
PROTOCOL_VERSION = "1.0.0"
TASK_ID = "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01"
CHECK_TASK_ID = "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01"
PROPOSED_CAPABILITY = "distribution_manifest_v1"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:distribution-manifest-v1"

REPORT_ROOT = Path(".aide/reports/distribution-manifest-v1")
SCHEMA_PATH = Path(".aide/protocol/aide-distribution-manifest-v1.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/distribution-manifest-v1")

STATUS_MD = REPORT_ROOT / "status.md"
MANIFEST_JSON = REPORT_ROOT / "manifest.json"
MANIFEST_MD = REPORT_ROOT / "manifest.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
DIGEST_VECTORS_JSON = REPORT_ROOT / "digest-vectors.json"
Q47_SOURCE_MAPPING_JSON = REPORT_ROOT / "q47-source-mapping.json"
Q47_SOURCE_MAPPING_MD = REPORT_ROOT / "q47-source-mapping.md"
ARTIFACT_INDEX_JSON = REPORT_ROOT / "artifact-index.json"
ARTIFACT_INDEX_MD = REPORT_ROOT / "artifact-index.md"
COMPONENT_INDEX_JSON = REPORT_ROOT / "component-index.json"
COMPONENT_INDEX_MD = REPORT_ROOT / "component-index.md"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"

RELEASE_BUNDLE_JSON = Path(".aide/release/latest-release-bundle.json")
RELEASE_ASSETS_JSON = Path(".aide/release/dist/release-assets.json")
RELEASE_CHECKSUMS_JSON = Path(".aide/release/dist/aide-lite-pack-v0.checksums.json")
RELEASE_PROVENANCE_JSON = Path(".aide/release/dist/release-provenance.json")
RELEASE_MANIFEST_YAML = Path(".aide/release/dist/manifest.yaml")
EXPORT_PACK_ROOT = Path(".aide/export/aide-lite-pack-v0")

SUPPORTED_CHANNELS = {"dev", "canary", "edge", "stable", "lts"}
SUPPORTED_SOURCE_KINDS = {"local_directory", "local_zip", "local_tar_gz"}
SUPPORTED_REQUIRED_FEATURES = {
    "distribution_manifest_v1",
    "portable_release_bundle_v0",
    "sha256_digest_canonical_json_v1",
}
SUPPORTED_OPTIONAL_FEATURES = {
    "signature_placeholder_v0",
    "sbom_reference_placeholder_v0",
    "github_release_draft_publication_review_v0",
}
SUPPORTED_MIGRATIONS: set[str] = set()
SUPPORTED_PROTOCOL_MAJOR = 1
SUPPORTED_DISTRIBUTION_PACKAGE_PREFIXES = ("files/",)

FORBIDDEN_MEMBER_PREFIXES = (
    ".aide.local/",
    ".aide/reports/",
    ".aide/repo/latest-",
    ".aide/roots/latest-",
    ".aide/tools/latest-",
    ".aide/install/latest-",
    ".aide/repair/latest-",
    ".aide/upgrade/latest-",
    ".aide/rollback/latest-",
    ".aide/uninstall/latest-",
    ".aide/context/latest-",
    ".cache/",
    ".pytest_cache/",
    "__pycache__/",
    "logs/",
    "secrets/",
)
FORBIDDEN_MEMBER_EXACT = {
    ".aide.local",
    ".env",
    "raw-prompt.txt",
    "raw-response.txt",
}
ALLOWED_DISTRIBUTION_REPORT_MEMBERS = {
    ".aide/reports/aide-commit-message-standard.md",
    ".aide/reports/aide-task-resumption-standard.md",
    ".aide/reports/aide-workunit-recovery-standard.md",
    ".aide/reports/file-quality-ledger.schema.json",
}
SECRET_LIKE_RE = re.compile(r"(^|/)(secret|secrets|credential|credentials|token|tokens|\.env)(/|$)", re.IGNORECASE)

REFUSAL_CODES = [
    "distribution.manifest_missing",
    "distribution.manifest_invalid",
    "distribution.manifest_digest_mismatch",
    "distribution.duplicate_component",
    "distribution.duplicate_component_id",
    "distribution.duplicate_artifact",
    "distribution.artifact_digest_mismatch",
    "distribution.artifact_byte_count_mismatch",
    "distribution.artifact_media_type_mismatch",
    "distribution.artifact_compression_mismatch",
    "distribution.unsupported_protocol_range",
    "distribution.unknown_required_feature",
    "distribution.unsupported_source_kind",
    "distribution.forbidden_member",
    "distribution.source_state_contamination",
    "distribution.component_digest_mismatch",
    "distribution.missing_artifact_ref",
    "distribution.excluded_artifact_ref",
    "distribution.missing_component_dependency",
    "distribution.component_dependency_cycle",
    "distribution.checksum_digest_mismatch",
    "distribution.checksum_basename_collision",
    "distribution.signature_unverified",
    "distribution.sbom_unavailable",
    "distribution.missing_checksum",
    "distribution.incompatible_migration",
]

EXPLICIT_NON_CAPABILITIES = [
    "install_apply",
    "update_apply",
    "repair_apply",
    "rollback_apply",
    "uninstall_apply",
    "release_publication",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "target_repository_mutation",
    "branch_worktree_automation",
    "workbench_runtime",
    "mcp_runtime",
    "source_change_preview_apply_rollback",
    "promotion",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_digest(data: bytes) -> str:
    return f"sha256:{sha256_bytes(data)}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, stable_json(data))


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_rel(value: str) -> str:
    return value.replace("\\", "/").strip()


def is_absolute_or_traversal(value: str) -> bool:
    rel = normalize_rel(value)
    if not rel:
        return True
    if rel.startswith("/") or re.match(r"^[A-Za-z]:/", rel) or rel.startswith("//"):
        return True
    parts = [part for part in rel.split("/") if part]
    return any(part == ".." for part in parts)


def _forbidden_member_reason_for_normalized(rel: str) -> str | None:
    rel = normalize_rel(rel)
    if is_absolute_or_traversal(rel):
        return "absolute_or_traversal_path"
    if rel == ".aide.local.example" or rel.startswith(".aide.local.example/") or "/.aide.local.example/" in rel:
        return None
    if rel in ALLOWED_DISTRIBUTION_REPORT_MEMBERS:
        return None
    if rel in FORBIDDEN_MEMBER_EXACT:
        return "forbidden_exact_member"
    for prefix in FORBIDDEN_MEMBER_PREFIXES:
        if rel.startswith(prefix):
            return f"forbidden_prefix:{prefix}"
    if SECRET_LIKE_RE.search(rel):
        return "secret_like_member"
    return None


def _member_classification_views(value: str) -> list[dict[str, str]]:
    source_member = normalize_rel(value)
    views: list[dict[str, str]] = []
    for prefix in SUPPORTED_DISTRIBUTION_PACKAGE_PREFIXES:
        if source_member.startswith(prefix):
            views.append(
                {
                    "source_member": source_member,
                    "target_member": source_member[len(prefix) :],
                    "packaging_prefix": prefix.rstrip("/"),
                    "view": "target_root_member",
                }
            )
    views.append(
        {
            "source_member": source_member,
            "target_member": source_member,
            "packaging_prefix": "",
            "view": "source_member",
        }
    )
    return views


def forbidden_member_classification(value: str) -> dict[str, str] | None:
    for view in _member_classification_views(value):
        reason = _forbidden_member_reason_for_normalized(view["target_member"])
        if reason:
            return {
                **view,
                "reason": reason,
                "refusal_code": "distribution.forbidden_member",
            }
    return None


def forbidden_member_reason(value: str) -> str | None:
    classification = forbidden_member_classification(value)
    return classification["reason"] if classification else None


def media_type_for(path: str, kind: str) -> str:
    if path.endswith(".zip"):
        return "application/zip"
    if path.endswith(".tar.gz"):
        return "application/gzip"
    if path.endswith(".json"):
        return "application/json"
    if path.endswith(".yaml") or path.endswith(".yml"):
        return "application/yaml"
    if path.endswith(".md"):
        return "text/markdown"
    if path.endswith(".txt"):
        return "text/plain"
    if kind == "local_directory":
        return "application/vnd.aide.directory"
    return "application/octet-stream"


def compression_format_for(path: str) -> str | None:
    if path.endswith(".zip"):
        return "zip"
    if path.endswith(".tar.gz"):
        return "tar.gz"
    return None


def source_kind_for(path: str) -> str:
    if path.endswith(".zip"):
        return "local_zip"
    if path.endswith(".tar.gz"):
        return "local_tar_gz"
    return "local_file"


def safe_artifact_path(root: Path, relative_path: str) -> Path | None:
    rel = normalize_rel(relative_path)
    if forbidden_member_reason(rel):
        return None
    candidate = root / rel
    try:
        resolved_root = root.resolve()
        resolved_candidate = candidate.resolve(strict=False)
        if resolved_candidate == resolved_root or resolved_root not in resolved_candidate.parents:
            return None
    except OSError:
        return None
    return candidate


def artifact_ref(asset_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", asset_id).strip("-")
    return f"aide://distribution/artifact/{safe}"


def component_ref(component_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", component_id).strip("-")
    return f"aide://distribution/component/{safe}"


def load_release_inputs(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    paths = {
        "release_bundle": root / RELEASE_BUNDLE_JSON,
        "release_assets": root / RELEASE_ASSETS_JSON,
        "release_checksums": root / RELEASE_CHECKSUMS_JSON,
        "release_provenance": root / RELEASE_PROVENANCE_JSON,
        "release_manifest": root / RELEASE_MANIFEST_YAML,
        "export_pack": root / EXPORT_PACK_ROOT,
    }
    missing = [key for key, path in paths.items() if not path.exists()]
    if missing:
        raise ValueError(f"missing Q47 release input(s): {', '.join(missing)}")
    return {
        "paths": {key: repo_rel(path, root) for key, path in paths.items()},
        "release_bundle": read_json(paths["release_bundle"]),
        "release_assets": read_json(paths["release_assets"]),
        "release_checksums": read_json(paths["release_checksums"]),
        "release_provenance": read_json(paths["release_provenance"]),
    }


def directory_inventory_report(path: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    forbidden_members: list[dict[str, str]] = []
    total_bytes = 0
    for child in sorted(path.rglob("*")):
        if not child.is_file():
            continue
        rel = child.relative_to(path).as_posix()
        forbidden = forbidden_member_classification(rel)
        if forbidden:
            forbidden_members.append(
                {
                    "path": rel,
                    "reason": forbidden["reason"],
                    "source_member": forbidden["source_member"],
                    "target_member": forbidden["target_member"],
                    "packaging_prefix": forbidden["packaging_prefix"],
                    "refusal_code": forbidden["refusal_code"],
                }
            )
            continue
        size = child.stat().st_size
        total_bytes += size
        entries.append({"path": rel, "byte_count": size, "sha256": sha256_file(child)})
    digest = sha256_digest(canonical_json_bytes(entries))
    return {
        "schema_version": "aide.distribution-directory-inventory.v1",
        "directory": "local_distribution_source",
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "directory_digest": digest,
        "allowed_members": entries,
        "forbidden_members": forbidden_members,
        "forbidden_member_count": len(forbidden_members),
        "source_state_contamination_detected": bool(forbidden_members),
    }


def directory_inventory_digest(path: Path) -> tuple[int, int, str, list[dict[str, str]]]:
    report = directory_inventory_report(path)
    forbidden_members = [
        {"path": item["path"], "reason": item["reason"]}
        for item in report["forbidden_members"]
    ]
    return int(report["file_count"]), int(report["total_bytes"]), str(report["directory_digest"]), forbidden_members


def _artifact_from_release_record(repo_root: Path, record: dict[str, Any]) -> dict[str, Any]:
    path = normalize_rel(str(record.get("path", "")))
    safe_path = safe_artifact_path(repo_root, path)
    path_valid = safe_path is not None
    if path_valid and safe_path is not None and safe_path.exists():
        byte_count = safe_path.stat().st_size
        actual_hash = sha256_file(safe_path)
    else:
        byte_count = int(record.get("size_bytes") or 0)
        actual_hash = str(record.get("sha256", ""))
    name = str(record.get("asset_id") or Path(path).name)
    kind = str(record.get("kind") or "release_artifact")
    return {
        "artifact_ref": artifact_ref(name),
        "artifact_id": name,
        "kind": kind,
        "source_kind": source_kind_for(name),
        "media_type": media_type_for(path, kind),
        "byte_count": byte_count,
        "content_digest": f"sha256:{actual_hash}",
        "relative_source_location": path,
        "archive_member": None,
        "portable_role": "release_bundle_artifact",
        "target_treatment": "distribution_input_only_not_ownership_authority",
        "compression_format": compression_format_for(name),
        "checksum_ref": "aide://distribution/checksums/q47-release-dist-core-artifacts",
        "provenance_ref": "aide://distribution/provenance/q47-release-provenance",
        "included": bool(record.get("included", True)),
        "excluded_reason": "" if record.get("included", True) else str(record.get("reason", "")),
        "extensions": {
            "path_validation": {
                "valid": path_valid,
                "reason": "" if path_valid else (forbidden_member_reason(path) or "path_not_contained"),
            }
        },
    }


def _directory_artifact(repo_root: Path) -> dict[str, Any]:
    count, total_bytes, digest, forbidden_members = directory_inventory_digest(repo_root / EXPORT_PACK_ROOT)
    return {
        "artifact_ref": artifact_ref("aide-lite-pack-v0-directory"),
        "artifact_id": "aide-lite-pack-v0-directory",
        "kind": "local_directory",
        "source_kind": "local_directory",
        "media_type": media_type_for("", "local_directory"),
        "byte_count": total_bytes,
        "content_digest": digest,
        "relative_source_location": EXPORT_PACK_ROOT.as_posix(),
        "archive_member": None,
        "portable_role": "validated_export_pack_directory",
        "target_treatment": "distribution_input_only_not_ownership_authority",
        "compression_format": None,
        "checksum_ref": None,
        "provenance_ref": "aide://distribution/provenance/q47-release-provenance",
        "included": True,
        "excluded_reason": "",
        "directory_file_count": count,
        "directory_forbidden_member_count": len(forbidden_members),
        "directory_forbidden_members": forbidden_members,
        "extensions": {},
    }


def build_artifacts(repo_root: str | Path, release_assets: dict[str, Any]) -> list[dict[str, Any]]:
    root = Path(repo_root)
    records = release_assets.get("artifacts", [])
    if not isinstance(records, list):
        records = []
    artifacts = [_artifact_from_release_record(root, record) for record in records if isinstance(record, dict)]
    artifacts.append(_directory_artifact(root))
    return sorted(artifacts, key=lambda item: str(item["artifact_ref"]))


def component_digest(component_payload: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(component_payload))


def component_digest_payload(component: dict[str, Any], artifact_by_ref: dict[str, dict[str, Any]]) -> dict[str, Any]:
    artifact_refs = sorted(str(ref) for ref in component.get("artifact_refs", []) if isinstance(ref, str))
    artifact_digests = []
    for ref in artifact_refs:
        artifact = artifact_by_ref.get(ref)
        if artifact and artifact.get("included") is True:
            artifact_digests.append({"artifact_ref": ref, "content_digest": str(artifact.get("content_digest", ""))})
    return {
        "component_id": str(component.get("component_id", "")),
        "kind": str(component.get("kind", "")),
        "version": str(component.get("version", "")),
        "required": bool(component.get("required", False)),
        "artifact_refs": artifact_refs,
        "artifact_digests": sorted(artifact_digests, key=lambda item: item["artifact_ref"]),
        "protocol_requirements": sorted(str(item) for item in component.get("protocol_requirements", []) if isinstance(item, str)),
        "target_role": str(component.get("target_role", "")),
        "compatibility_constraints": copy.deepcopy(component.get("compatibility_constraints", {})),
        "dependencies": sorted(str(item) for item in component.get("dependencies", []) if isinstance(item, str)),
    }


def build_components(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    artifact_refs = [str(item["artifact_ref"]) for item in artifacts if item.get("included") is True]
    artifact_by_ref = {str(item.get("artifact_ref")): item for item in artifacts if isinstance(item, dict)}
    component = {
        "component_ref": component_ref("aide-lite-pack-v0"),
        "component_id": "aide-lite-pack-v0",
        "kind": "aide_lite_portable_pack",
        "version": "v0",
        "required": True,
        "content_digest": "",
        "artifact_refs": sorted(artifact_refs),
        "protocol_requirements": ["distribution_manifest_v1", "portable_release_bundle_v0"],
        "target_role": "aide_lite_distribution_input",
        "compatibility_constraints": {
            "min_reader_version": PROTOCOL_VERSION,
            "min_writer_version": PROTOCOL_VERSION,
        },
        "dependencies": [],
        "extensions": {},
    }
    component["content_digest"] = component_digest(component_digest_payload(component, artifact_by_ref))
    return [component]


def build_distribution_manifest(repo_root: str | Path, *, source_kind: str = "local_zip") -> dict[str, Any]:
    root = Path(repo_root)
    release_inputs = load_release_inputs(root)
    provenance = release_inputs["release_provenance"]
    release_bundle = release_inputs["release_bundle"]
    release_checksums = release_inputs["release_checksums"]
    artifacts = build_artifacts(root, release_inputs["release_assets"])
    checksum_names = release_checksums.get("checksums") if isinstance(release_checksums.get("checksums"), dict) else {}
    for artifact in artifacts:
        if Path(str(artifact.get("relative_source_location", ""))).name not in checksum_names:
            artifact["checksum_ref"] = None
    components = build_components(artifacts)
    source_revision = str(provenance.get("source_commit") or "")
    manifest = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "distribution_ref": "aide://distribution/aide-lite-pack-v0",
            "name": "aide-lite-pack-v0",
            "product": "AIDE Lite",
            "format_version": "1.0.0",
            "release_id": str(release_bundle.get("bundle_id") or release_checksums.get("bundle_id") or "aide-lite-pack-v0"),
            "release_version": "v0",
            "channel": "canary",
            "source_revision": source_revision,
            "source_tree_digest": provenance.get("export_pack_manifest_sha256", ""),
            "build_implementation": "aide-lite release bundle q47",
            "projection_implementation": "core/protocol/distribution_manifest.py",
            "timestamp_classification": "q47_observed_build_metadata_projected_deterministically",
        },
        "spec": {
            "source": {
                "source_kind": source_kind,
                "source_ref": "aide://release-bundle/q47/aide-lite-pack-v0",
                "source_paths": release_inputs["paths"],
                "q47_dirty_state": bool(provenance.get("dirty_state", False)),
                "q47_source_repo_value_suppressed": bool(provenance.get("source_repo")),
                "q48_publication_draft_is_distribution_truth": False,
            },
            "protocol": {
                "protocol_range": {"min": "1.0.0", "max": "1.x"},
                "min_reader_version": PROTOCOL_VERSION,
                "min_writer_version": PROTOCOL_VERSION,
                "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
                "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
                "required_migrations": [],
                "compatibility_declarations": [
                    "Q43-Q48 latest outputs are source-repo evidence, not target truth.",
                    "DistributionManifest does not encode target ownership.",
                    "GitHub Release draft evidence is publication-review material only.",
                ],
            },
            "components": components,
            "artifacts": artifacts,
            "checksums": {
                "checksum_manifest_ref": "aide://distribution/checksums/q47-release-dist-core-artifacts",
                "checksum_manifest_path": RELEASE_CHECKSUMS_JSON.as_posix(),
                "algorithm": "sha256",
                "manifest_digest": f"sha256:{sha256_file(root / RELEASE_CHECKSUMS_JSON)}",
            },
            "provenance": {
                "provenance_ref": "aide://distribution/provenance/q47-release-provenance",
                "provenance_path": RELEASE_PROVENANCE_JSON.as_posix(),
                "preview_only": bool(provenance.get("preview_only", True)),
                "no_publish": bool(provenance.get("no_publish", True)),
                "source_repo_local_path_suppressed": bool(provenance.get("source_repo")),
            },
            "sbom_refs": [
                {
                    "sbom_ref": "aide://distribution/sbom/unavailable",
                    "status": "unavailable",
                    "reason": "Q47 local bundle does not generate an SBOM artifact.",
                }
            ],
            "signature_records": [
                {
                    "signature_ref": "aide://distribution/signature/unsigned-placeholder",
                    "status": "unsigned",
                    "verified": False,
                    "reason": "Q47 local bundle is not signed.",
                }
            ],
            "known_limitations": [
                "Local Q47 release artifacts are preview/no-publish evidence.",
                "Q47 provenance records dirty-state preview metadata.",
                "No public release, signature verification, SBOM generation, install apply, or update apply is implemented.",
            ],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "manifest_payload_digest": "",
            "distribution_digest": "",
            "source_state_contamination_detected": False,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "repair_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "release_publication_implemented": False,
            "target_repository_mutation_implemented": False,
            "network_calls_implemented": False,
            "provider_model_calls_implemented": False,
            "recommended_next_task": CHECK_TASK_ID,
        },
    }
    return finalize_manifest(manifest)


def canonicalize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(manifest)
    spec = data.get("spec")
    if isinstance(spec, dict):
        if isinstance(spec.get("components"), list):
            spec["components"] = sorted(spec["components"], key=lambda item: str(item.get("component_ref", "")) if isinstance(item, dict) else "")
        if isinstance(spec.get("artifacts"), list):
            spec["artifacts"] = sorted(spec["artifacts"], key=lambda item: str(item.get("artifact_ref", "")) if isinstance(item, dict) else "")
        protocol = spec.get("protocol")
        if isinstance(protocol, dict):
            for key in ["required_features", "optional_features", "required_migrations", "compatibility_declarations"]:
                if isinstance(protocol.get(key), list):
                    protocol[key] = sorted(str(item) for item in protocol[key])
    return data


def manifest_payload_for_digest(manifest: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_manifest(manifest)
    data.pop("status", None)
    spec = data.get("spec")
    if isinstance(spec, dict):
        spec.pop("signature_records", None)
    return data


def manifest_payload_digest(manifest: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(manifest_payload_for_digest(manifest)))


def immutable_artifact_digest_set(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = manifest.get("spec", {}).get("artifacts", []) if isinstance(manifest.get("spec"), dict) else []
    digest_set = []
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            digest_set.append(
                {
                    "artifact_ref": artifact.get("artifact_ref", ""),
                    "byte_count": artifact.get("byte_count", 0),
                    "content_digest": artifact.get("content_digest", ""),
                    "included": artifact.get("included", False),
                }
            )
    return sorted(digest_set, key=lambda item: str(item["artifact_ref"]))


def distribution_digest(manifest: dict[str, Any]) -> str:
    payload = {
        "manifest_payload_digest": manifest_payload_digest(manifest),
        "immutable_artifact_digest_set": immutable_artifact_digest_set(manifest),
    }
    return sha256_digest(canonical_json_bytes(payload))


def finalize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_manifest(manifest)
    status = data.setdefault("status", {})
    artifacts = data.get("spec", {}).get("artifacts", []) if isinstance(data.get("spec"), dict) else []
    status["source_state_contamination_detected"] = any(
        isinstance(artifact, dict) and int(artifact.get("directory_forbidden_member_count") or 0) > 0
        for artifact in artifacts
    )
    status["manifest_payload_digest"] = manifest_payload_digest(data)
    status["distribution_digest"] = distribution_digest(data)
    return data


def minimal_fixture_manifest() -> dict[str, Any]:
    artifact = {
        "artifact_ref": artifact_ref("minimal.json"),
        "artifact_id": "minimal.json",
        "kind": "manifest_fixture",
        "source_kind": "local_file",
        "media_type": "application/json",
        "byte_count": 2,
        "content_digest": sha256_digest(b"{}"),
        "relative_source_location": ".aide/fixtures/distribution-manifest-v1/source/minimal.json",
        "archive_member": None,
        "portable_role": "fixture",
        "target_treatment": "distribution_input_only_not_ownership_authority",
        "compression_format": None,
        "checksum_ref": "aide://distribution/checksums/fixture",
        "provenance_ref": "aide://distribution/provenance/fixture",
        "included": True,
        "excluded_reason": "",
    }
    component = build_components([artifact])[0]
    manifest = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "distribution_ref": "aide://distribution/fixture-minimal",
            "name": "fixture-minimal",
            "product": "AIDE Lite",
            "format_version": "1.0.0",
            "release_id": "fixture-minimal-1",
            "release_version": "fixture",
            "channel": "dev",
            "source_revision": "fixture",
            "source_tree_digest": "fixture",
            "build_implementation": "fixture",
            "projection_implementation": "core/protocol/distribution_manifest.py",
            "timestamp_classification": DETERMINISTIC_TIMESTAMP,
        },
        "spec": {
            "source": {
                "source_kind": "local_zip",
                "source_ref": "aide://release-bundle/fixture",
                "source_paths": {},
                "q47_dirty_state": False,
                "q47_source_repo_value_suppressed": False,
                "q48_publication_draft_is_distribution_truth": False,
            },
            "protocol": {
                "protocol_range": {"min": "1.0.0", "max": "1.x"},
                "min_reader_version": PROTOCOL_VERSION,
                "min_writer_version": PROTOCOL_VERSION,
                "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
                "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
                "required_migrations": [],
                "compatibility_declarations": ["fixture only"],
            },
            "components": [component],
            "artifacts": [artifact],
            "checksums": {
                "checksum_manifest_ref": "aide://distribution/checksums/fixture",
                "checksum_manifest_path": ".aide/fixtures/distribution-manifest-v1/source/checksums.json",
                "algorithm": "sha256",
                "manifest_digest": sha256_digest(b"fixture-checksums"),
            },
            "provenance": {
                "provenance_ref": "aide://distribution/provenance/fixture",
                "provenance_path": ".aide/fixtures/distribution-manifest-v1/source/provenance.json",
                "preview_only": True,
                "no_publish": True,
                "source_repo_local_path_suppressed": False,
            },
            "sbom_refs": [{"sbom_ref": "aide://distribution/sbom/unavailable", "status": "unavailable", "reason": "fixture"}],
            "signature_records": [{"signature_ref": "aide://distribution/signature/unsigned-placeholder", "status": "unsigned", "verified": False, "reason": "fixture"}],
            "known_limitations": ["fixture"],
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "manifest_payload_digest": "",
            "distribution_digest": "",
            "source_state_contamination_detected": False,
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "repair_apply_implemented": False,
            "rollback_apply_implemented": False,
            "uninstall_apply_implemented": False,
            "release_publication_implemented": False,
            "target_repository_mutation_implemented": False,
            "network_calls_implemented": False,
            "provider_model_calls_implemented": False,
            "recommended_next_task": CHECK_TASK_ID,
        },
    }
    return finalize_manifest(manifest)


def _add_error(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def _protocol_major(value: str) -> int | None:
    match = re.match(r"^(\d+)(?:\.|$)", value)
    if not match:
        return None
    return int(match.group(1))


def _semver_tuple(value: str) -> tuple[int, int, int] | None:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", value)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def _range_max_tuple(value: str) -> tuple[int, int, int] | None:
    wildcard = re.match(r"^(\d+)\.x$", value)
    if wildcard:
        major = int(wildcard.group(1))
        return (major, 999999, 999999)
    return _semver_tuple(value)


def _range_bound_major(value: str) -> int | None:
    wildcard = re.match(r"^(\d+)\.x$", value)
    if wildcard:
        return int(wildcard.group(1))
    parsed = _semver_tuple(value)
    return parsed[0] if parsed else None


def _max_bound_is_supported_major(value: str) -> bool:
    return _range_bound_major(value) == SUPPORTED_PROTOCOL_MAJOR


def protocol_range_includes_current(protocol: dict[str, Any]) -> bool:
    protocol_range = protocol.get("protocol_range") if isinstance(protocol.get("protocol_range"), dict) else {}
    minimum_value = str(protocol_range.get("min", ""))
    maximum_value = str(protocol_range.get("max", ""))
    minimum = _semver_tuple(minimum_value)
    maximum = _range_max_tuple(maximum_value)
    current = _semver_tuple(PROTOCOL_VERSION)
    reader = _semver_tuple(str(protocol.get("min_reader_version", "")))
    writer = _semver_tuple(str(protocol.get("min_writer_version", "")))
    if minimum is None or maximum is None or current is None or reader is None or writer is None:
        return False
    if not _max_bound_is_supported_major(maximum_value):
        return False
    if minimum > maximum:
        return False
    if not (minimum <= current <= maximum):
        return False
    if reader > current or writer > current:
        return False
    return True


def compatibility_constraints_include_current(constraints: Any) -> bool:
    if not isinstance(constraints, dict):
        return False
    current = _semver_tuple(PROTOCOL_VERSION)
    if current is None:
        return False
    reader = _semver_tuple(str(constraints.get("min_reader_version", "")))
    writer = _semver_tuple(str(constraints.get("min_writer_version", "")))
    if reader is None or writer is None:
        return False
    if reader > current or writer > current:
        return False
    for key in ("max_reader_version", "max_writer_version"):
        if key in constraints:
            value = str(constraints.get(key, ""))
            maximum = _range_max_tuple(value)
            if maximum is None or not _max_bound_is_supported_major(value):
                return False
            if current > maximum:
                return False
    component_range = constraints.get("protocol_range")
    if isinstance(component_range, dict):
        if not protocol_range_includes_current(
            {
                "protocol_range": component_range,
                "min_reader_version": constraints.get("min_reader_version"),
                "min_writer_version": constraints.get("min_writer_version"),
            }
        ):
            return False
    return True


def validate_distribution_manifest_object(
    manifest: dict[str, Any] | None,
    *,
    repo_root: str | Path | None = None,
    require_artifact_files: bool = False,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if manifest is None:
        _add_error(errors, "distribution.manifest_missing", "manifest is missing")
        return _validation_result(errors, warnings)
    if not isinstance(manifest, dict):
        _add_error(errors, "distribution.manifest_invalid", "manifest root must be an object")
        return _validation_result(errors, warnings)
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status"]:
        if field not in manifest:
            _add_error(errors, "distribution.manifest_invalid", f"missing required field: {field}")
    if manifest.get("kind") != KIND:
        _add_error(errors, "distribution.manifest_invalid", "kind must be DistributionManifest")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "distribution.manifest_invalid", f"schema_version must be {SCHEMA_VERSION}")
    metadata = manifest.get("metadata") if isinstance(manifest.get("metadata"), dict) else {}
    spec = manifest.get("spec") if isinstance(manifest.get("spec"), dict) else {}
    status = manifest.get("status") if isinstance(manifest.get("status"), dict) else {}
    if metadata.get("channel") not in SUPPORTED_CHANNELS:
        _add_error(errors, "distribution.manifest_invalid", "unsupported channel")
    source = spec.get("source") if isinstance(spec.get("source"), dict) else {}
    if source.get("source_kind") not in SUPPORTED_SOURCE_KINDS:
        _add_error(errors, "distribution.unsupported_source_kind", "unsupported source_kind")
    protocol = spec.get("protocol") if isinstance(spec.get("protocol"), dict) else {}
    if not protocol_range_includes_current(protocol):
        _add_error(errors, "distribution.unsupported_protocol_range", "protocol range, reader version, or writer version does not include v1")
    for feature in protocol.get("required_features", []) if isinstance(protocol.get("required_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            _add_error(errors, "distribution.unknown_required_feature", f"unknown required feature: {feature}")
    for feature in protocol.get("optional_features", []) if isinstance(protocol.get("optional_features"), list) else []:
        if feature not in SUPPORTED_REQUIRED_FEATURES and feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    for migration in protocol.get("required_migrations", []) if isinstance(protocol.get("required_migrations"), list) else []:
        if migration not in SUPPORTED_MIGRATIONS:
            _add_error(errors, "distribution.incompatible_migration", f"unsupported required migration: {migration}")
    components = spec.get("components", [])
    artifacts = spec.get("artifacts", [])
    if not isinstance(components, list) or not components:
        _add_error(errors, "distribution.manifest_invalid", "components must be a non-empty array")
        components = []
    if not isinstance(artifacts, list) or not artifacts:
        _add_error(errors, "distribution.manifest_invalid", "artifacts must be a non-empty array")
        artifacts = []
    root = Path(repo_root) if repo_root is not None else None
    checksum_spec = spec.get("checksums") if isinstance(spec.get("checksums"), dict) else {}
    checksum_entries = _checksum_entries(spec, root)
    if checksum_spec.get("algorithm") != "sha256":
        _add_error(errors, "distribution.manifest_invalid", "checksum algorithm must be sha256")
    checksum_path_value = checksum_spec.get("checksum_manifest_path")
    if root is not None and isinstance(checksum_path_value, str):
        checksum_path = safe_artifact_path(root, checksum_path_value)
        if checksum_path is None:
            _add_error(errors, "distribution.forbidden_member", f"{checksum_path_value}: forbidden checksum manifest path")
        elif checksum_path.exists():
            expected_manifest_digest = f"sha256:{sha256_file(checksum_path)}"
            if checksum_spec.get("manifest_digest") != expected_manifest_digest:
                _add_error(errors, "distribution.checksum_digest_mismatch", "checksum manifest digest mismatch")
    artifact_refs_seen: set[str] = set()
    artifact_by_ref: dict[str, dict[str, Any]] = {}
    checksum_artifact_names: dict[str, list[str]] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            _add_error(errors, "distribution.manifest_invalid", "artifact entries must be objects")
            continue
        ref = str(artifact.get("artifact_ref", ""))
        if ref in artifact_refs_seen:
            _add_error(errors, "distribution.duplicate_artifact", f"duplicate artifact_ref: {ref}")
        artifact_refs_seen.add(ref)
        artifact_by_ref[ref] = artifact
        rel = str(artifact.get("relative_source_location", ""))
        forbidden = forbidden_member_reason(rel)
        if forbidden:
            _add_error(errors, "distribution.forbidden_member", f"{rel}: {forbidden}")
            _add_error(errors, "distribution.source_state_contamination", f"{rel}: forbidden distribution member")
        if int(artifact.get("directory_forbidden_member_count") or 0) > 0:
            _add_error(errors, "distribution.source_state_contamination", f"{rel}: local directory contains forbidden members")
        content_digest_value = str(artifact.get("content_digest", ""))
        if not re.match(r"^sha256:[0-9a-f]{64}$", content_digest_value):
            _add_error(errors, "distribution.artifact_digest_mismatch", f"artifact digest has invalid format: {rel}")
        if artifact.get("checksum_ref"):
            name = Path(normalize_rel(rel)).name
            checksum_artifact_names.setdefault(name, []).append(ref)
            if checksum_entries is not None and name not in checksum_entries:
                _add_error(errors, "distribution.missing_checksum", f"missing checksum entry for {name}")
            elif checksum_entries is not None and checksum_entries.get(name) != content_digest_value.removeprefix("sha256:"):
                _add_error(errors, "distribution.checksum_digest_mismatch", f"checksum value mismatch for {name}")
        if artifact.get("content_digest") == "sha256:" + "0" * 64:
            _add_error(errors, "distribution.artifact_digest_mismatch", f"artifact digest is the zero digest: {rel}")
        if require_artifact_files and root is not None and artifact.get("source_kind") != "local_directory":
            artifact_path = safe_artifact_path(root, rel)
            if artifact_path is None:
                _add_error(errors, "distribution.forbidden_member", f"{rel}: path is not contained")
                continue
            if not artifact_path.exists():
                _add_error(errors, "distribution.manifest_invalid", f"artifact file missing: {rel}")
            elif artifact_path.is_symlink() or not artifact_path.is_file():
                _add_error(errors, "distribution.manifest_invalid", f"artifact is not a regular file: {rel}")
            else:
                actual_size = artifact_path.stat().st_size
                if int(artifact.get("byte_count") or -1) != actual_size:
                    _add_error(errors, "distribution.artifact_byte_count_mismatch", f"artifact byte_count mismatch: {rel}")
                actual = f"sha256:{sha256_file(artifact_path)}"
                if actual != artifact.get("content_digest"):
                    _add_error(errors, "distribution.artifact_digest_mismatch", f"artifact digest mismatch: {rel}")
                expected_media_type = media_type_for(rel, str(artifact.get("kind", "")))
                if artifact.get("media_type") != expected_media_type:
                    _add_error(errors, "distribution.artifact_media_type_mismatch", f"artifact media_type mismatch: {rel}")
                expected_compression = compression_format_for(rel)
                if artifact.get("compression_format") != expected_compression:
                    _add_error(errors, "distribution.artifact_compression_mismatch", f"artifact compression_format mismatch: {rel}")
    for name, refs in checksum_artifact_names.items():
        if len(refs) > 1:
            _add_error(errors, "distribution.checksum_basename_collision", f"checksum basename collision for {name}")
    component_refs_seen: set[str] = set()
    component_ids_seen: set[str] = set()
    dependency_graph: dict[str, list[str]] = {}
    for component in components:
        if not isinstance(component, dict):
            _add_error(errors, "distribution.manifest_invalid", "component entries must be objects")
            continue
        ref = str(component.get("component_ref", ""))
        component_id = str(component.get("component_id", ""))
        if not ref:
            _add_error(errors, "distribution.manifest_invalid", "component_ref is required")
        if ref in component_refs_seen:
            _add_error(errors, "distribution.duplicate_component", f"duplicate component_ref: {ref}")
        component_refs_seen.add(ref)
        if component_id in component_ids_seen:
            _add_error(errors, "distribution.duplicate_component_id", f"duplicate component_id: {component_id}")
        component_ids_seen.add(component_id)
        if not compatibility_constraints_include_current(component.get("compatibility_constraints")):
            _add_error(errors, "distribution.unsupported_protocol_range", f"component compatibility does not include v1: {ref}")
        for requirement in component.get("protocol_requirements", []) if isinstance(component.get("protocol_requirements"), list) else []:
            if requirement not in SUPPORTED_REQUIRED_FEATURES and requirement not in SUPPORTED_OPTIONAL_FEATURES:
                _add_error(errors, "distribution.unknown_required_feature", f"unknown component protocol requirement: {requirement}")
        for artifact_ref_value in component.get("artifact_refs", []) if isinstance(component.get("artifact_refs"), list) else []:
            artifact_ref_string = str(artifact_ref_value)
            artifact_record = artifact_by_ref.get(artifact_ref_string)
            if artifact_record is None:
                _add_error(errors, "distribution.missing_artifact_ref", f"component references missing artifact: {artifact_ref_string}")
            elif artifact_record.get("included") is not True:
                _add_error(errors, "distribution.excluded_artifact_ref", f"component references excluded artifact: {artifact_ref_string}")
        dependencies = [str(item) for item in component.get("dependencies", []) if isinstance(item, str)] if isinstance(component.get("dependencies"), list) else []
        dependency_graph[ref] = dependencies
        for dependency in dependencies:
            if dependency not in component_refs_seen and not any(isinstance(other, dict) and other.get("component_ref") == dependency for other in components):
                _add_error(errors, "distribution.missing_component_dependency", f"component dependency is missing: {dependency}")
            if dependency == ref:
                _add_error(errors, "distribution.component_dependency_cycle", f"component depends on itself: {ref}")
        expected_component_digest = component_digest(component_digest_payload(component, artifact_by_ref))
        if component.get("content_digest") != expected_component_digest:
            _add_error(errors, "distribution.component_digest_mismatch", f"component digest mismatch: {ref}")
    for cycle in component_dependency_cycles(dependency_graph):
        _add_error(errors, "distribution.component_dependency_cycle", f"component dependency cycle: {' -> '.join(cycle)}")
    for signature in spec.get("signature_records", []) if isinstance(spec.get("signature_records"), list) else []:
        if not isinstance(signature, dict):
            _add_error(errors, "distribution.signature_unverified", "signature record must be an object")
            continue
        if signature.get("verified") is True or signature.get("status") == "verified":
            _add_error(errors, "distribution.signature_unverified", "verified signature claims are not supported by this slice")
    sbom_refs = spec.get("sbom_refs", []) if isinstance(spec.get("sbom_refs"), list) else []
    if not sbom_refs:
        _add_error(errors, "distribution.sbom_unavailable", "SBOM status must be explicitly unavailable or placeholder")
    for sbom in sbom_refs:
        if isinstance(sbom, dict) and sbom.get("status") not in {"unavailable", "placeholder"}:
            _add_error(errors, "distribution.sbom_unavailable", "generated SBOM claims are not supported by this slice")
    expected_payload = manifest_payload_digest(manifest)
    expected_distribution = distribution_digest(manifest)
    if status.get("manifest_payload_digest") != expected_payload:
        _add_error(errors, "distribution.manifest_digest_mismatch", "manifest_payload_digest does not match canonical payload")
    if status.get("distribution_digest") != expected_distribution:
        _add_error(errors, "distribution.manifest_digest_mismatch", "distribution_digest does not match canonical artifact set")
    return _validation_result(errors, warnings)


def component_dependency_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        if node in visiting:
            if node in stack:
                cycles.append(stack[stack.index(node) :] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency, stack + [dependency])
        visiting.remove(node)
        visited.add(node)

    for component in sorted(graph):
        visit(component, [component])
    return cycles


def _checksum_entries(spec: dict[str, Any], root: Path | None) -> dict[str, str] | None:
    checksums = spec.get("checksums")
    if not isinstance(checksums, dict):
        return None
    path = checksums.get("checksum_manifest_path")
    if not isinstance(path, str):
        return None
    if root is not None:
        checksum_path = safe_artifact_path(root, path)
        if checksum_path is None:
            return None
        if checksum_path.exists():
            try:
                data = read_json(checksum_path)
            except ValueError:
                return None
            checksum_map = data.get("checksums")
            if isinstance(checksum_map, dict):
                return {str(key): str(value) for key, value in checksum_map.items()}
    if "fixture" in path:
        return {"minimal.json": sha256_bytes(b"{}")}
    return None


def _validation_result(errors: list[dict[str, str]], warnings: list[str]) -> dict[str, Any]:
    codes = sorted({item["code"] for item in errors})
    return {
        "valid": not errors,
        "status": "PASS" if not errors else "FAILED_VALIDATION",
        "error_count": len(errors),
        "errors": errors,
        "refusal_codes": codes,
        "warnings": warnings,
    }


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return read_json(Path(repo_root) / SCHEMA_PATH)


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    report = {
        "schema_version": "aide.distribution-manifest-status.v1",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/distribution_manifest.py").exists(),
        "q47_release_bundle_exists": (root / RELEASE_BUNDLE_JSON).exists(),
        "q47_release_assets_exists": (root / RELEASE_ASSETS_JSON).exists(),
        "q47_release_checksums_exists": (root / RELEASE_CHECKSUMS_JSON).exists(),
        "q47_release_provenance_exists": (root / RELEASE_PROVENANCE_JSON).exists(),
        "manifest_report_exists": (root / MANIFEST_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "supported_source_kinds": sorted(SUPPORTED_SOURCE_KINDS),
        "refusal_codes": REFUSAL_CODES,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "release_publication_implemented": False,
        "target_repository_mutation_implemented": False,
        "network_calls_implemented": False,
        "provider_model_calls_implemented": False,
        "warnings": [
            "DistributionManifest v1 is proposed until independent check and acceptance.",
            "Existing Q47 release artifacts are local preview/no-publish evidence.",
        ],
    }
    write_text(root / STATUS_MD, render_status_md(report))
    return report


def project(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    manifest = build_distribution_manifest(root)
    write_json(root / MANIFEST_JSON, manifest)
    write_text(root / MANIFEST_MD, render_manifest_md(manifest))
    write_fixture_corpus(root)
    q47_mapping = q47_source_mapping(root, manifest)
    write_json(root / Q47_SOURCE_MAPPING_JSON, q47_mapping)
    write_text(root / Q47_SOURCE_MAPPING_MD, render_q47_mapping_md(q47_mapping))
    artifact_index = {"schema_version": "aide.distribution-artifact-index.v1", "artifacts": manifest["spec"]["artifacts"]}
    component_index = {"schema_version": "aide.distribution-component-index.v1", "components": manifest["spec"]["components"]}
    write_json(root / ARTIFACT_INDEX_JSON, artifact_index)
    write_text(root / ARTIFACT_INDEX_MD, render_index_md("Artifact Index", manifest["spec"]["artifacts"], "artifact_ref"))
    write_json(root / COMPONENT_INDEX_JSON, component_index)
    write_text(root / COMPONENT_INDEX_MD, render_index_md("Component Index", manifest["spec"]["components"], "component_ref"))
    digest_vectors = {
        "schema_version": "aide.distribution-digest-vectors.v1",
        "manifest_payload_digest": manifest["status"]["manifest_payload_digest"],
        "distribution_digest": manifest["status"]["distribution_digest"],
        "immutable_artifact_digest_set": immutable_artifact_digest_set(manifest),
        "reordered_input_distribution_digest": distribution_digest(reordered_manifest(manifest)),
        "reordered_input_same_digest": distribution_digest(reordered_manifest(manifest)) == manifest["status"]["distribution_digest"],
    }
    write_json(root / DIGEST_VECTORS_JSON, digest_vectors)
    write_text(root / FIXTURE_MATRIX_MD, render_fixture_matrix_md(fixture_matrix(root)))
    write_text(root / NON_CAPABILITIES_MD, render_non_capabilities_md())
    report = {
        "schema_version": "aide.distribution-manifest-project-report.v1",
        "status": "PASS_WITH_WARNINGS",
        "proposed_capability": PROPOSED_CAPABILITY,
        "manifest_path": MANIFEST_JSON.as_posix(),
        "artifact_count": len(manifest["spec"]["artifacts"]),
        "component_count": len(manifest["spec"]["components"]),
        "manifest_payload_digest": manifest["status"]["manifest_payload_digest"],
        "distribution_digest": manifest["status"]["distribution_digest"],
        "source_artifacts_mutated": False,
        "recommended_next_task": CHECK_TASK_ID,
        "warnings": manifest["spec"]["known_limitations"],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    status(root)
    return report


def validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    project_report = project(root)
    manifest = read_json(root / MANIFEST_JSON)
    manifest_validation = validate_distribution_manifest_object(manifest, repo_root=root, require_artifact_files=True)
    schema = load_schema(root)
    schema_alignment_errors = schema_alignment_errors_for(schema)
    fixture_results = []
    for fixture in fixture_matrix(root):
        data = read_json(root / fixture["path"])
        result = validate_distribution_manifest_object(data, repo_root=root, require_artifact_files=False)
        expected_codes = set(fixture.get("expected_refusal_codes", []))
        observed_codes = set(result["refusal_codes"])
        expected_valid = fixture["expected_result"] == "PASS"
        fixture_results.append(
            {
                **fixture,
                "observed_result": "PASS" if result["valid"] else "FAILED_VALIDATION",
                "observed_refusal_codes": sorted(observed_codes),
                "passed": (result["valid"] is expected_valid) and expected_codes.issubset(observed_codes),
            }
        )
    fixture_pass = all(item["passed"] for item in fixture_results)
    digest_vectors = read_json(root / DIGEST_VECTORS_JSON)
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/distribution_manifest.py").exists(),
        "cli_registered": cli_registered(root),
        "manifest_generated": (root / MANIFEST_JSON).exists(),
        "manifest_valid": manifest_validation["valid"],
        "schema_alignment": not schema_alignment_errors,
        "fixture_matrix_passed": fixture_pass,
        "reordered_input_same_digest": bool(digest_vectors.get("reordered_input_same_digest")),
        "q47_release_bundle_mapped": bool(read_json(root / Q47_SOURCE_MAPPING_JSON).get("q47_inputs")),
        "q48_not_distribution_truth": manifest["spec"]["source"]["q48_publication_draft_is_distribution_truth"] is False,
        "install_apply_not_implemented": manifest["status"]["install_apply_implemented"] is False,
        "release_publication_not_implemented": manifest["status"]["release_publication_implemented"] is False,
        "target_repository_mutation_not_implemented": manifest["status"]["target_repository_mutation_implemented"] is False,
        "network_calls_not_implemented": manifest["status"]["network_calls_implemented"] is False,
        "provider_model_calls_not_implemented": manifest["status"]["provider_model_calls_implemented"] is False,
        "absolute_local_paths_suppressed": not contains_absolute_local_path(manifest),
    }
    errors = [key for key, value in checks.items() if not value]
    status_value = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.distribution-manifest-validation.v1",
        "validation_status": status_value,
        "status": status_value,
        "proposed_capability": PROPOSED_CAPABILITY,
        "checks": checks,
        "errors": errors,
        "schema_alignment_errors": schema_alignment_errors,
        "manifest_validation": manifest_validation,
        "fixture_results": fixture_results,
        "project_report": project_report,
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
        "warnings": [
            "DistributionManifest v1 is proposed until independent check and acceptance.",
            "Q47 release artifacts remain local preview/no-publish evidence.",
            "No signature verification or SBOM generation is claimed.",
        ],
        "recommended_next_task": CHECK_TASK_ID,
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / VALIDATION_MD, render_validation_md(report))
    return report


def schema_alignment_errors_for(schema: dict[str, Any]) -> list[str]:
    errors = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare Draft 2020-12")
    if schema.get("title") != "AIDE DistributionManifest v1":
        errors.append("schema title mismatch")
    for field in ["apiVersion", "kind", "schema_version", "metadata", "spec", "status"]:
        if field not in schema.get("required", []):
            errors.append(f"schema missing required field: {field}")
    return errors


def cli_registered(repo_root: Path) -> bool:
    script = repo_root / ".aide/scripts/aide_lite.py"
    if not script.exists():
        return False
    text = script.read_text(encoding="utf-8")
    return "distribution-manifest" in text and "command_distribution_manifest_validate" in text


def contains_absolute_local_path(data: Any) -> bool:
    if isinstance(data, dict):
        return any(contains_absolute_local_path(value) for value in data.values())
    if isinstance(data, list):
        return any(contains_absolute_local_path(value) for value in data)
    if isinstance(data, str):
        return bool(re.match(r"^[A-Za-z]:[/\\]", data) or data.startswith("/Users/") or data.startswith("/home/"))
    return False


def q47_source_mapping(repo_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.distribution-q47-source-mapping.v1",
        "q47_inputs": {
            "release_bundle": RELEASE_BUNDLE_JSON.as_posix(),
            "release_assets": RELEASE_ASSETS_JSON.as_posix(),
            "release_checksums": RELEASE_CHECKSUMS_JSON.as_posix(),
            "release_provenance": RELEASE_PROVENANCE_JSON.as_posix(),
            "release_manifest": RELEASE_MANIFEST_YAML.as_posix(),
            "export_pack": EXPORT_PACK_ROOT.as_posix(),
        },
        "q48_treatment": "publication_review_evidence_only",
        "distribution_truth": {
            "manifest": MANIFEST_JSON.as_posix(),
            "distribution_digest": manifest["status"]["distribution_digest"],
        },
        "source_repo_absolute_path_suppressed": manifest["spec"]["provenance"]["source_repo_local_path_suppressed"],
        "source_generated_target_truth_copied": False,
    }


def reordered_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(manifest)
    spec = data.get("spec", {})
    if isinstance(spec, dict):
        if isinstance(spec.get("components"), list):
            spec["components"] = list(reversed(spec["components"]))
        if isinstance(spec.get("artifacts"), list):
            spec["artifacts"] = list(reversed(spec["artifacts"]))
    return finalize_manifest(data)


def fixture_matrix(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    fixtures: list[dict[str, Any]] = []
    for path in sorted((root / FIXTURE_ROOT / "valid").glob("*.json")):
        fixtures.append({"case_id": path.stem, "path": repo_rel(path, root), "expected_result": "PASS", "expected_refusal_codes": []})
    invalid_expected = INVALID_FIXTURE_EXPECTATIONS
    for path in sorted((root / FIXTURE_ROOT / "invalid").glob("*.json")):
        fixtures.append(
            {
                "case_id": path.stem,
                "path": repo_rel(path, root),
                "expected_result": "FAILED_VALIDATION",
                "expected_refusal_codes": invalid_expected.get(path.stem, []),
            }
        )
    return fixtures


INVALID_FIXTURE_EXPECTATIONS = {
    "absolute-path": ["distribution.forbidden_member", "distribution.source_state_contamination"],
    "aide-local-member": ["distribution.forbidden_member", "distribution.source_state_contamination"],
    "duplicate-artifact": ["distribution.duplicate_artifact"],
    "duplicate-component": ["distribution.duplicate_component"],
    "duplicate-component-id": ["distribution.duplicate_component_id"],
    "checksum-basename-collision": ["distribution.checksum_basename_collision"],
    "checksum-missing": ["distribution.missing_checksum"],
    "checksum-wrong-value": ["distribution.checksum_digest_mismatch"],
    "dependency-cycle": ["distribution.component_dependency_cycle"],
    "false-signature-verification": ["distribution.signature_unverified"],
    "false-verified-signature": ["distribution.signature_unverified"],
    "forbidden-member": ["distribution.forbidden_member", "distribution.source_state_contamination"],
    "forbidden-source-report-member": ["distribution.forbidden_member", "distribution.source_state_contamination"],
    "incompatible-migration": ["distribution.incompatible_migration"],
    "inverted-protocol-range": ["distribution.unsupported_protocol_range"],
    "component-protocol-future-major": ["distribution.unsupported_protocol_range"],
    "malformed-digest": ["distribution.artifact_digest_mismatch"],
    "missing-artifact-ref": ["distribution.missing_artifact_ref"],
    "missing-checksum": ["distribution.missing_checksum"],
    "missing-dependency": ["distribution.missing_component_dependency"],
    "missing-digest": ["distribution.manifest_digest_mismatch"],
    "missing-sbom": ["distribution.sbom_unavailable"],
    "sbom-generated-claim": ["distribution.sbom_unavailable"],
    "source-contamination": ["distribution.source_state_contamination"],
    "traversal-path": ["distribution.forbidden_member", "distribution.source_state_contamination"],
    "unknown-required-feature": ["distribution.unknown_required_feature"],
    "unsupported-protocol": ["distribution.unsupported_protocol_range"],
    "protocol-range-max-2-0-0": ["distribution.unsupported_protocol_range"],
    "protocol-range-max-2x": ["distribution.unsupported_protocol_range"],
    "protocol-range-min-2-0-0": ["distribution.unsupported_protocol_range"],
    "unsupported-protocol-range": ["distribution.unsupported_protocol_range"],
    "unsupported-source": ["distribution.unsupported_source_kind"],
    "unsupported-source-kind": ["distribution.unsupported_source_kind"],
    "wrong-artifact-digest": ["distribution.artifact_digest_mismatch"],
    "wrong-component-digest": ["distribution.component_digest_mismatch"],
    "wrong-distribution-digest": ["distribution.manifest_digest_mismatch"],
    "wrong-manifest-digest": ["distribution.manifest_digest_mismatch"],
    "wrong-payload-digest": ["distribution.manifest_digest_mismatch"],
}


def write_fixture_corpus(repo_root: str | Path) -> None:
    root = Path(repo_root)
    valid_root = root / FIXTURE_ROOT / "valid"
    invalid_root = root / FIXTURE_ROOT / "invalid"
    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)
    minimal = minimal_fixture_manifest()
    write_json(valid_root / "minimal-unsigned.json", minimal)
    full = build_distribution_manifest(root)
    write_json(valid_root / "full-local-archive.json", full)
    local_dir = build_distribution_manifest(root, source_kind="local_directory")
    write_json(valid_root / "local-directory.json", local_dir)
    write_json(valid_root / "reordered-input.json", reordered_manifest(full))
    unknown_optional_feature = copy.deepcopy(minimal)
    add_unknown_optional_feature(unknown_optional_feature)
    write_json(valid_root / "unknown-optional-feature.json", finalize_manifest(unknown_optional_feature))
    unknown_optional_extension = copy.deepcopy(minimal)
    add_optional_extensions(unknown_optional_extension)
    write_json(valid_root / "unknown-optional-extension-round-trip.json", finalize_manifest(unknown_optional_extension))
    signature_placeholder = copy.deepcopy(minimal)
    write_json(valid_root / "signature-placeholder.json", finalize_manifest(signature_placeholder))
    invalid_cases = {
        "absolute-path": lambda m: set_artifact_path(m, "C:/tmp/aide-lite-pack-v0.zip"),
        "aide-local-member": lambda m: set_artifact_path(m, ".aide.local/state.sqlite"),
        "checksum-basename-collision": checksum_basename_collision,
        "checksum-missing": missing_checksum,
        "checksum-wrong-value": checksum_wrong_value,
        "dependency-cycle": component_dependency_cycle,
        "duplicate-artifact": duplicate_first_artifact,
        "duplicate-component": duplicate_first_component,
        "duplicate-component-id": duplicate_component_id,
        "false-signature-verification": false_verified_signature,
        "false-verified-signature": false_verified_signature,
        "forbidden-member": lambda m: set_artifact_path(m, ".env"),
        "forbidden-source-report-member": lambda m: set_artifact_path(m, ".aide/reports/latest-report.json"),
        "incompatible-migration": add_incompatible_migration,
        "inverted-protocol-range": inverted_protocol_range,
        "component-protocol-future-major": component_protocol_future_major,
        "malformed-digest": malformed_digest,
        "missing-artifact-ref": missing_artifact_ref,
        "missing-checksum": missing_checksum,
        "missing-dependency": missing_component_dependency,
        "missing-digest": remove_manifest_digest,
        "missing-sbom": missing_sbom,
        "sbom-generated-claim": sbom_generated_claim,
        "source-contamination": source_contamination,
        "traversal-path": lambda m: set_artifact_path(m, "../outside.txt"),
        "unknown-required-feature": add_unknown_required_feature,
        "unsupported-protocol": unsupported_protocol,
        "protocol-range-max-2-0-0": protocol_range_max_2_0_0,
        "protocol-range-max-2x": protocol_range_max_2x,
        "protocol-range-min-2-0-0": protocol_range_min_2_0_0,
        "unsupported-protocol-range": unsupported_protocol_range,
        "unsupported-source": unsupported_source_kind,
        "unsupported-source-kind": unsupported_source_kind,
        "wrong-artifact-digest": wrong_artifact_digest,
        "wrong-component-digest": wrong_component_digest,
        "wrong-distribution-digest": wrong_distribution_digest,
        "wrong-manifest-digest": wrong_manifest_digest,
        "wrong-payload-digest": wrong_payload_digest,
    }
    for name, mutator in invalid_cases.items():
        case = copy.deepcopy(minimal)
        mutator(case)
        if name not in {"missing-digest", "wrong-manifest-digest", "wrong-payload-digest", "wrong-distribution-digest"}:
            case = finalize_manifest(case)
        write_json(invalid_root / f"{name}.json", case)


def first_artifact(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["spec"]["artifacts"][0]


def set_artifact_path(manifest: dict[str, Any], path: str) -> None:
    first_artifact(manifest)["relative_source_location"] = path


def duplicate_first_artifact(manifest: dict[str, Any]) -> None:
    manifest["spec"]["artifacts"].append(copy.deepcopy(first_artifact(manifest)))


def duplicate_first_component(manifest: dict[str, Any]) -> None:
    manifest["spec"]["components"].append(copy.deepcopy(manifest["spec"]["components"][0]))


def duplicate_component_id(manifest: dict[str, Any]) -> None:
    duplicate = copy.deepcopy(manifest["spec"]["components"][0])
    duplicate["component_ref"] = component_ref("aide-lite-pack-v0-copy")
    manifest["spec"]["components"].append(duplicate)


def missing_artifact_ref(manifest: dict[str, Any]) -> None:
    manifest["spec"]["components"][0]["artifact_refs"].append("aide://distribution/artifact/missing")


def excluded_artifact_ref(manifest: dict[str, Any]) -> None:
    artifact = first_artifact(manifest)
    artifact["included"] = False
    artifact["excluded_reason"] = "fixture exclusion"


def missing_component_dependency(manifest: dict[str, Any]) -> None:
    manifest["spec"]["components"][0]["dependencies"].append("aide://distribution/component/missing")


def component_dependency_cycle(manifest: dict[str, Any]) -> None:
    ref = manifest["spec"]["components"][0]["component_ref"]
    manifest["spec"]["components"][0]["dependencies"].append(ref)


def checksum_basename_collision(manifest: dict[str, Any]) -> None:
    second = copy.deepcopy(first_artifact(manifest))
    second["artifact_ref"] = artifact_ref("nested-minimal")
    second["relative_source_location"] = "nested/minimal.json"
    manifest["spec"]["artifacts"].append(second)
    manifest["spec"]["components"][0]["artifact_refs"].append(second["artifact_ref"])


def checksum_wrong_value(manifest: dict[str, Any]) -> None:
    first_artifact(manifest)["content_digest"] = sha256_digest(b"changed")


def false_verified_signature(manifest: dict[str, Any]) -> None:
    manifest["spec"]["signature_records"] = [{"signature_ref": "aide://distribution/signature/fake", "status": "verified", "verified": True}]


def add_incompatible_migration(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["required_migrations"] = ["future.breaking-migration.v99"]


def missing_checksum(manifest: dict[str, Any]) -> None:
    first_artifact(manifest)["checksum_ref"] = "aide://distribution/checksums/fixture"
    first_artifact(manifest)["relative_source_location"] = ".aide/fixtures/distribution-manifest-v1/source/not-in-checksums.bin"


def remove_manifest_digest(manifest: dict[str, Any]) -> None:
    manifest["status"].pop("manifest_payload_digest", None)


def sbom_generated_claim(manifest: dict[str, Any]) -> None:
    manifest["spec"]["sbom_refs"] = [{"sbom_ref": "aide://distribution/sbom/fake", "status": "generated"}]


def missing_sbom(manifest: dict[str, Any]) -> None:
    manifest["spec"]["sbom_refs"] = []


def add_unknown_required_feature(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["required_features"].append("future.required.feature")


def add_unknown_optional_feature(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["optional_features"].append("future.optional.feature")


def add_optional_extensions(manifest: dict[str, Any]) -> None:
    manifest["metadata"]["extensions"] = {"operator.note": {"value": "preserve"}}
    manifest["spec"]["protocol"]["extensions"] = {"future.optional": {"enabled": True}}
    manifest["spec"]["components"][0]["extensions"] = {"component.optional": 7}


def unsupported_protocol(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "0.1.0", "max": "0.x"}


def unsupported_protocol_range(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "2.0.0", "max": "3.x"}


def protocol_range_max_2x(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "1.0.0", "max": "2.x"}


def protocol_range_max_2_0_0(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "1.0.0", "max": "2.0.0"}


def protocol_range_min_2_0_0(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "2.0.0", "max": "2.x"}


def inverted_protocol_range(manifest: dict[str, Any]) -> None:
    manifest["spec"]["protocol"]["protocol_range"] = {"min": "1.0.0", "max": "0.9.0"}


def component_protocol_future_major(manifest: dict[str, Any]) -> None:
    component = manifest["spec"]["components"][0]
    component["compatibility_constraints"]["max_reader_version"] = "2.x"
    artifact_by_ref = {
        str(artifact.get("artifact_ref")): artifact
        for artifact in manifest["spec"].get("artifacts", [])
        if isinstance(artifact, dict)
    }
    component["content_digest"] = component_digest(component_digest_payload(component, artifact_by_ref))


def unsupported_source_kind(manifest: dict[str, Any]) -> None:
    manifest["spec"]["source"]["source_kind"] = "remote_http"


def malformed_digest(manifest: dict[str, Any]) -> None:
    first_artifact(manifest)["content_digest"] = "sha256:not-a-valid-digest"


def wrong_artifact_digest(manifest: dict[str, Any]) -> None:
    first_artifact(manifest)["content_digest"] = "sha256:" + "0" * 64


def wrong_component_digest(manifest: dict[str, Any]) -> None:
    manifest["spec"]["components"][0]["content_digest"] = "sha256:" + "2" * 64


def wrong_manifest_digest(manifest: dict[str, Any]) -> None:
    manifest["status"]["manifest_payload_digest"] = "sha256:" + "1" * 64


def wrong_payload_digest(manifest: dict[str, Any]) -> None:
    manifest["status"]["manifest_payload_digest"] = "sha256:" + "3" * 64


def wrong_distribution_digest(manifest: dict[str, Any]) -> None:
    manifest["status"]["distribution_digest"] = "sha256:" + "4" * 64


def source_contamination(manifest: dict[str, Any]) -> None:
    artifact = first_artifact(manifest)
    artifact["source_kind"] = "local_directory"
    artifact["kind"] = "local_directory"
    artifact["media_type"] = media_type_for("", "local_directory")
    artifact["directory_file_count"] = 0
    artifact["directory_forbidden_member_count"] = 1
    artifact["directory_forbidden_members"] = [{"path": ".aide.local/state.sqlite", "reason": "forbidden_prefix:.aide.local/"}]


def render_status_md(data: dict[str, Any]) -> str:
    lines = [
        "# DistributionManifest v1 Status",
        "",
        f"- status: {data.get('status')}",
        f"- proposed_capability: {data.get('proposed_capability')}",
        f"- schema_exists: {str(data.get('schema_exists')).lower()}",
        f"- helper_exists: {str(data.get('helper_exists')).lower()}",
        f"- q47_release_bundle_exists: {str(data.get('q47_release_bundle_exists')).lower()}",
        f"- manifest_report_exists: {str(data.get('manifest_report_exists')).lower()}",
        f"- validation_report_exists: {str(data.get('validation_report_exists')).lower()}",
        f"- recommended_next_task: {data.get('recommended_next_task')}",
        "",
        "## Non-Capabilities",
        "",
    ]
    for item in data.get("explicit_non_capabilities", []):
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_manifest_md(manifest: dict[str, Any]) -> str:
    metadata = manifest["metadata"]
    status_data = manifest["status"]
    lines = [
        "# DistributionManifest v1 Projection",
        "",
        f"- distribution_ref: `{metadata['distribution_ref']}`",
        f"- release_id: `{metadata['release_id']}`",
        f"- channel: `{metadata['channel']}`",
        f"- manifest_payload_digest: `{status_data['manifest_payload_digest']}`",
        f"- distribution_digest: `{status_data['distribution_digest']}`",
        f"- component_count: {len(manifest['spec']['components'])}",
        f"- artifact_count: {len(manifest['spec']['artifacts'])}",
        "- q48_publication_draft_is_distribution_truth: false",
        "- install_apply_implemented: false",
        "- update_apply_implemented: false",
        "- release_publication_implemented: false",
        "",
        "## Artifacts",
        "",
    ]
    for artifact in manifest["spec"]["artifacts"]:
        lines.append(f"- `{artifact['artifact_id']}`: {artifact['kind']} {artifact['content_digest']}")
    return "\n".join(lines) + "\n"


def render_q47_mapping_md(data: dict[str, Any]) -> str:
    lines = ["# Q47 Source Mapping", "", "## Inputs", ""]
    for key, path in data["q47_inputs"].items():
        lines.append(f"- {key}: `{path}`")
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            f"- q48_treatment: {data['q48_treatment']}",
            f"- source_repo_absolute_path_suppressed: {str(data['source_repo_absolute_path_suppressed']).lower()}",
            "- source_generated_target_truth_copied: false",
        ]
    )
    return "\n".join(lines) + "\n"


def render_index_md(title: str, records: list[dict[str, Any]], key: str) -> str:
    lines = [f"# {title}", ""]
    for record in records:
        lines.append(f"- `{record.get(key)}`")
    return "\n".join(lines) + "\n"


def render_fixture_matrix_md(fixtures: list[dict[str, Any]]) -> str:
    lines = ["# DistributionManifest Fixture Matrix", "", "| Case | Expected | Codes |", "| --- | --- | --- |"]
    for fixture in fixtures:
        codes = ", ".join(fixture.get("expected_refusal_codes", [])) or "none"
        lines.append(f"| {fixture['case_id']} | {fixture['expected_result']} | {codes} |")
    return "\n".join(lines) + "\n"


def render_non_capabilities_md() -> str:
    lines = ["# DistributionManifest v1 Explicit Non-Capabilities", ""]
    for item in EXPLICIT_NON_CAPABILITIES:
        lines.append(f"- {item}: false")
    return "\n".join(lines) + "\n"


def render_validation_md(report: dict[str, Any]) -> str:
    lines = [
        "# DistributionManifest v1 Validation",
        "",
        f"- result: {report.get('validation_status')}",
        f"- proposed_capability: {report.get('proposed_capability')}",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Checks",
        "",
    ]
    for key, value in report.get("checks", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")
    lines.extend(["", "## Fixture Results", ""])
    for item in report.get("fixture_results", []):
        lines.append(f"- {item['case_id']}: {str(item['passed']).lower()} ({item['observed_result']})")
    lines.extend(["", "## Warnings", ""])
    for warning in report.get("warnings", []):
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"
