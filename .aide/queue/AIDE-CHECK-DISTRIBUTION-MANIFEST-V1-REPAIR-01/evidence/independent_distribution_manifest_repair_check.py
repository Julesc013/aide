"""Independent check harness for DistributionManifest v1 Repair 01.

This script is task-local evidence. It treats core/protocol/distribution_manifest.py
as the system under test and keeps independent recomputation/probe logic here.
It does not repair implementation or write production manifest outputs.
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
from unittest.mock import patch


TASK_ID = "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
SOURCE_TASK_ID = "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
SOURCE_CHECK_TASK_ID = "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01"
SOURCE_COMMIT = "77ac6c2facddbd343479e269b841070602d5f047"
CAPABILITY = "distribution_manifest_v1"
PASS_NEXT = "AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01"
FAIL_NEXT = "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02"

REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID
EVIDENCE_ROOT = TASK_ROOT / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/distribution-manifest-v1-repair-01-check"
SOURCE_REPORT_ROOT = REPO_ROOT / ".aide/reports/distribution-manifest-v1"
FIXTURE_ROOT = REPO_ROOT / ".aide/fixtures/distribution-manifest-v1"
SOURCE_TASK_ROOT = REPO_ROOT / ".aide/queue" / SOURCE_TASK_ID
MATERIAL_FINDING_IDS = [
    "schema.optional_extension_boundary_missing",
    "identity.mutable_status_changes_distribution_digest",
    "component.graph_integrity_not_validated",
    "artifact.integrity_metadata_not_validated",
    "path.preaccess_validation_order_violation",
    "checksum.value_not_verified",
    "protocol.range_semantics_incomplete",
    "contamination.forbidden_members_silently_filtered",
    "fixture.required_coverage_incomplete",
]

sys.path.insert(0, str(REPO_ROOT))
from core.protocol import distribution_manifest as sut  # noqa: E402


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": "), ensure_ascii=False) + "\n"


def canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_obj(data: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(data)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    write_text(path, stable_json(data))


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def excerpt(value: str, limit: int = 1800) -> str:
    text = value.replace("\r\n", "\n")
    if len(text) > limit:
        return text[:limit] + "\n...[truncated]"
    return text


def run_cmd(command: list[str], timeout: int = 180) -> dict[str, Any]:
    actual_command = list(command)
    # On this Windows host, launching `py` directly as a child of Python can
    # exercise different stdlib path behavior than the shell command users run.
    # Use the same PowerShell path for validation receipts when available.
    if os.name == "nt" and command and command[0] == "py":
        pwsh = shutil.which("pwsh")
        if pwsh:
            actual_command = [pwsh, "-NoProfile", "-Command", subprocess.list2cmdline(command)]
    try:
        completed = subprocess.run(
            actual_command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=False,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        return {
            "command": command,
            "actual_command": actual_command,
            "exit_code": completed.returncode,
            "result": "PASS" if completed.returncode == 0 else "FAIL",
            "stdout_excerpt": excerpt(completed.stdout),
            "stderr_excerpt": excerpt(completed.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "actual_command": actual_command,
            "exit_code": None,
            "result": "TIMEOUT",
            "stdout_excerpt": excerpt(exc.stdout or ""),
            "stderr_excerpt": excerpt(exc.stderr or ""),
        }


def independent_canonicalize(manifest: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(manifest)
    spec = data.get("spec")
    if isinstance(spec, dict):
        if isinstance(spec.get("components"), list):
            spec["components"] = sorted(spec["components"], key=lambda item: str(item.get("component_ref", "")))
        if isinstance(spec.get("artifacts"), list):
            spec["artifacts"] = sorted(spec["artifacts"], key=lambda item: str(item.get("artifact_ref", "")))
        protocol = spec.get("protocol")
        if isinstance(protocol, dict):
            for key in ["required_features", "optional_features", "required_migrations", "compatibility_declarations"]:
                if isinstance(protocol.get(key), list):
                    protocol[key] = sorted(str(item) for item in protocol[key])
    return data


def independent_payload_for_digest(manifest: dict[str, Any]) -> dict[str, Any]:
    data = independent_canonicalize(manifest)
    data.pop("status", None)
    spec = data.get("spec")
    if isinstance(spec, dict):
        spec.pop("signature_records", None)
    return data


def independent_artifact_digest_set(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = manifest.get("spec", {}).get("artifacts", []) if isinstance(manifest.get("spec"), dict) else []
    result = []
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if isinstance(artifact, dict):
                result.append(
                    {
                        "artifact_ref": artifact.get("artifact_ref", ""),
                        "byte_count": artifact.get("byte_count", 0),
                        "content_digest": artifact.get("content_digest", ""),
                        "included": artifact.get("included", False),
                    }
                )
    return sorted(result, key=lambda item: str(item["artifact_ref"]))


def independent_manifest_payload_digest(manifest: dict[str, Any]) -> str:
    return digest_obj(independent_payload_for_digest(manifest))


def independent_distribution_digest(manifest: dict[str, Any]) -> str:
    return digest_obj(
        {
            "manifest_payload_digest": independent_manifest_payload_digest(manifest),
            "immutable_artifact_digest_set": independent_artifact_digest_set(manifest),
        }
    )


def independent_component_payload(component: dict[str, Any], artifact_by_ref: dict[str, dict[str, Any]]) -> dict[str, Any]:
    artifact_refs = sorted(str(item) for item in component.get("artifact_refs", []) if isinstance(item, str))
    artifact_digests = [
        {
            "artifact_ref": ref,
            "content_digest": artifact_by_ref[ref].get("content_digest", ""),
        }
        for ref in artifact_refs
        if isinstance(artifact_by_ref.get(ref), dict) and artifact_by_ref[ref].get("included") is True
    ]
    return {
        "component_id": component.get("component_id", ""),
        "kind": component.get("kind", ""),
        "version": component.get("version", ""),
        "required": component.get("required", False),
        "artifact_refs": artifact_refs,
        "artifact_digests": sorted(artifact_digests, key=lambda item: item["artifact_ref"]),
        "protocol_requirements": sorted(str(item) for item in component.get("protocol_requirements", []) if isinstance(item, str)),
        "target_role": component.get("target_role", ""),
        "compatibility_constraints": component.get("compatibility_constraints", {}),
        "dependencies": sorted(str(item) for item in component.get("dependencies", []) if isinstance(item, str)),
    }


def independent_component_digest(component: dict[str, Any], artifact_by_ref: dict[str, dict[str, Any]]) -> str:
    return digest_obj(independent_component_payload(component, artifact_by_ref))


def codes(result: dict[str, Any]) -> set[str]:
    return set(str(item) for item in result.get("refusal_codes", []))


def validate_manifest(manifest: dict[str, Any], *, root: Path | None = None, require_files: bool = False) -> dict[str, Any]:
    return sut.validate_distribution_manifest_object(copy.deepcopy(manifest), repo_root=root, require_artifact_files=require_files)


def finalized(manifest: dict[str, Any]) -> dict[str, Any]:
    return sut.finalize_manifest(copy.deepcopy(manifest))


class Recorder:
    def __init__(self) -> None:
        self.assertions: list[dict[str, Any]] = []
        self.material_findings: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    def check(
        self,
        assertion_id: str,
        *,
        category: str,
        description: str,
        expected: str,
        observed: Any,
        passed: bool,
        source_finding_id: str | None = None,
        evidence_refs: list[str] | None = None,
        material: bool = True,
    ) -> None:
        severity = "info" if passed else ("material" if material else "warning")
        outcome = "PASS" if passed else ("FAIL" if material else "WARNING")
        record = {
            "id": assertion_id,
            "category": category,
            "description": description,
            "outcome": outcome,
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs or [],
            "source_finding_id": source_finding_id,
        }
        self.assertions.append(record)
        if not passed and material:
            self.material_findings.append(record)
        elif not passed:
            self.warnings.append(f"{assertion_id}: {observed}")


def mutate(base: dict[str, Any], func) -> dict[str, Any]:
    data = copy.deepcopy(base)
    func(data)
    return data


def validate_probe(rec: Recorder, assertion_id: str, base: dict[str, Any], func, expected_code: str, source: str, *, finalize_after: bool = True, root: Path | None = None, require_files: bool = False) -> None:
    data = mutate(base, func)
    if finalize_after:
        data = finalized(data)
    result = validate_manifest(data, root=root, require_files=require_files)
    actual_codes = sorted(codes(result))
    rec.check(
        assertion_id,
        category="behavior_probe",
        description=f"Probe must fail with {expected_code}",
        expected=expected_code,
        observed={"valid": result.get("valid"), "codes": actual_codes},
        passed=expected_code in codes(result),
        source_finding_id=source,
        evidence_refs=["validation-results.md"],
    )


def set_status_field(manifest: dict[str, Any], key: str, value: Any) -> None:
    manifest.setdefault("status", {})[key] = value


def set_protocol(manifest: dict[str, Any], key: str, value: Any) -> None:
    manifest["spec"]["protocol"][key] = value


def material_finding_source_summary() -> dict[str, Any]:
    path = SOURCE_TASK_ROOT / "evidence/finding-matrix.json"
    if not path.exists():
        return {"exists": False, "ids": [], "closed_pending_count": 0}
    data = read_json(path)
    findings = data.get("findings", [])
    ids = [item.get("finding_id") for item in findings if isinstance(item, dict)]
    closed = [item for item in findings if isinstance(item, dict) and item.get("completion_state") == "closed_pending_independent_check"]
    return {"exists": True, "ids": ids, "closed_pending_count": len(closed)}


def run_extension_checks(rec: Recorder, minimal: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    schema_text = stable_json(schema)
    extension_paths = re.findall(r'"extensions"', schema_text)
    rec.check(
        "extension.schema_surfaces_present",
        category="extension_boundary",
        description="Schema has explicit extensions maps.",
        expected="at least metadata/spec/status/protocol/component/artifact extension surfaces",
        observed={"extension_property_count": len(extension_paths)},
        passed=len(extension_paths) >= 8,
        source_finding_id="schema.optional_extension_boundary_missing",
        evidence_refs=["extension-boundary-review.md"],
    )
    data = copy.deepcopy(minimal)
    data["metadata"]["extensions"] = {"check.optional": {"value": "preserved"}}
    data["spec"]["extensions"] = {"check.spec": [1, 2, 3]}
    data["status"]["extensions"] = {"check.status": True}
    data["spec"]["protocol"]["extensions"] = {"check.protocol": "kept"}
    data["spec"]["components"][0]["extensions"] = {"check.component": {"nested": True}}
    data["spec"]["artifacts"][0]["extensions"] = {"check.artifact": "value"}
    data = finalized(data)
    result = validate_manifest(data)
    preserved = (
        data["metadata"]["extensions"]["check.optional"]["value"] == "preserved"
        and data["spec"]["extensions"]["check.spec"] == [1, 2, 3]
        and data["status"]["extensions"]["check.status"] is True
        and data["spec"]["protocol"]["extensions"]["check.protocol"] == "kept"
        and data["spec"]["components"][0]["extensions"]["check.component"]["nested"] is True
        and data["spec"]["artifacts"][0]["extensions"]["check.artifact"] == "value"
    )
    rec.check(
        "extension.optional_round_trip",
        category="extension_boundary",
        description="Unknown optional extension maps survive finalize and validation.",
        expected="valid manifest with preserved extension values",
        observed={"valid": result.get("valid"), "codes": sorted(codes(result)), "preserved": preserved},
        passed=bool(result.get("valid")) and preserved,
        source_finding_id="schema.optional_extension_boundary_missing",
        evidence_refs=["extension-boundary-review.md"],
    )
    validate_probe(
        rec,
        "extension.unknown_required_feature_refuses",
        minimal,
        lambda m: m["spec"]["protocol"]["required_features"].append("future.required.extension"),
        "distribution.unknown_required_feature",
        "schema.optional_extension_boundary_missing",
    )
    return {"schema_extension_property_count": len(extension_paths), "round_trip_valid": result.get("valid"), "round_trip_preserved": preserved}


def run_identity_checks(rec: Recorder, manifest: dict[str, Any]) -> dict[str, Any]:
    status = manifest.get("status", {})
    base_payload = status.get("manifest_payload_digest")
    base_distribution = status.get("distribution_digest")
    independent_payload = independent_manifest_payload_digest(manifest)
    independent_distribution = independent_distribution_digest(manifest)
    rec.check(
        "digest.independent_payload_matches",
        category="digest",
        description="Independent canonical payload digest matches manifest status.",
        expected=str(base_payload),
        observed=independent_payload,
        passed=independent_payload == base_payload,
        source_finding_id="identity.mutable_status_changes_distribution_digest",
        evidence_refs=["digest-recomputation.md"],
    )
    rec.check(
        "digest.independent_distribution_matches",
        category="digest",
        description="Independent distribution digest matches manifest status.",
        expected=str(base_distribution),
        observed=independent_distribution,
        passed=independent_distribution == base_distribution,
        source_finding_id="identity.mutable_status_changes_distribution_digest",
        evidence_refs=["digest-recomputation.md"],
    )
    status_mutations = {
        "status.status": lambda m: set_status_field(m, "status", "PASS"),
        "status.recommended_next_task": lambda m: set_status_field(m, "recommended_next_task", "AIDE-NOOP-STATUS-MUTATION"),
        "status.proposed_capability": lambda m: set_status_field(m, "proposed_capability", "status_mutation_only"),
        "status.validation_boolean": lambda m: set_status_field(m, "network_calls_implemented", True),
        "status.warning_extension": lambda m: set_status_field(m, "extensions", {"warning": "mutable status-only note"}),
    }
    status_results: dict[str, Any] = {}
    for name, func in status_mutations.items():
        changed = finalized(mutate(manifest, func))
        status_results[name] = changed["status"]["distribution_digest"]
        rec.check(
            f"identity.{name}.does_not_change",
            category="identity_boundary",
            description=f"{name} must not affect distribution identity.",
            expected=base_distribution,
            observed=changed["status"]["distribution_digest"],
            passed=changed["status"]["distribution_digest"] == base_distribution,
            source_finding_id="identity.mutable_status_changes_distribution_digest",
            evidence_refs=["identity-boundary-review.md"],
        )
    spec_mutations = {
        "metadata.distribution_ref": lambda m: m["metadata"].__setitem__("distribution_ref", "aide://distribution/changed"),
        "metadata.release_id": lambda m: m["metadata"].__setitem__("release_id", "changed-release-id"),
        "metadata.source_revision": lambda m: m["metadata"].__setitem__("source_revision", "changed-source-revision"),
        "metadata.source_tree_digest": lambda m: m["metadata"].__setitem__("source_tree_digest", "sha256:" + "1" * 64),
        "artifact.digest": lambda m: m["spec"]["artifacts"][0].__setitem__("content_digest", "sha256:" + "2" * 64),
        "artifact.byte_count": lambda m: m["spec"]["artifacts"][0].__setitem__("byte_count", int(m["spec"]["artifacts"][0].get("byte_count", 0)) + 1),
        "component.digest": lambda m: m["spec"]["components"][0].__setitem__("content_digest", "sha256:" + "3" * 64),
        "protocol.required_feature": lambda m: m["spec"]["protocol"]["required_features"].append("distribution_manifest_identity_probe"),
        "protocol.required_migration": lambda m: m["spec"]["protocol"]["required_migrations"].append("future-migration"),
        "protocol.range": lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "1.0.0", "max": "1.0.0"}),
        "artifact.included_set": lambda m: m["spec"]["artifacts"][0].__setitem__("included", not bool(m["spec"]["artifacts"][0].get("included"))),
    }
    spec_results: dict[str, Any] = {}
    for name, func in spec_mutations.items():
        changed = finalized(mutate(manifest, func))
        spec_results[name] = changed["status"]["distribution_digest"]
        rec.check(
            f"identity.{name}.changes",
            category="identity_boundary",
            description=f"{name} must affect distribution identity.",
            expected="digest differs from base",
            observed={"base": base_distribution, "changed": changed["status"]["distribution_digest"]},
            passed=changed["status"]["distribution_digest"] != base_distribution,
            source_finding_id="identity.mutable_status_changes_distribution_digest",
            evidence_refs=["identity-boundary-review.md"],
        )
    return {
        "base_payload": base_payload,
        "base_distribution": base_distribution,
        "independent_payload": independent_payload,
        "independent_distribution": independent_distribution,
        "status_mutations": status_results,
        "spec_mutations": spec_results,
    }


def run_component_checks(rec: Recorder, minimal: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    artifact_by_ref = {artifact["artifact_ref"]: artifact for artifact in manifest["spec"]["artifacts"]}
    component_digest_matches = []
    for component in manifest["spec"]["components"]:
        expected = independent_component_digest(component, artifact_by_ref)
        component_digest_matches.append({"component_ref": component["component_ref"], "expected": expected, "observed": component.get("content_digest")})
    rec.check(
        "component.independent_digest_recompute",
        category="component_graph",
        description="Every component content digest recomputes independently.",
        expected="all component digests match independent payload",
        observed=component_digest_matches,
        passed=all(item["expected"] == item["observed"] for item in component_digest_matches),
        source_finding_id="component.graph_integrity_not_validated",
        evidence_refs=["component-graph-review.md"],
    )
    validate_probe(
        rec,
        "component.wrong_digest_refuses",
        minimal,
        lambda m: m["spec"]["components"][0].__setitem__("content_digest", "sha256:" + "4" * 64),
        "distribution.component_digest_mismatch",
        "component.graph_integrity_not_validated",
        finalize_after=False,
    )
    validate_probe(
        rec,
        "component.missing_artifact_ref_refuses",
        minimal,
        lambda m: m["spec"]["components"][0].__setitem__("artifact_refs", ["aide://distribution/artifact/missing"]),
        "distribution.missing_artifact_ref",
        "component.graph_integrity_not_validated",
    )
    validate_probe(
        rec,
        "component.excluded_artifact_ref_refuses",
        minimal,
        lambda m: m["spec"]["artifacts"][0].__setitem__("included", False),
        "distribution.excluded_artifact_ref",
        "component.graph_integrity_not_validated",
    )
    validate_probe(
        rec,
        "component.missing_dependency_refuses",
        minimal,
        lambda m: m["spec"]["components"][0].__setitem__("dependencies", ["aide://distribution/component/missing"]),
        "distribution.missing_component_dependency",
        "component.graph_integrity_not_validated",
    )
    validate_probe(
        rec,
        "component.self_dependency_refuses",
        minimal,
        lambda m: m["spec"]["components"][0].__setitem__("dependencies", [m["spec"]["components"][0]["component_ref"]]),
        "distribution.component_dependency_cycle",
        "component.graph_integrity_not_validated",
    )
    validate_probe(
        rec,
        "component.duplicate_ref_refuses",
        minimal,
        lambda m: m["spec"]["components"].append(copy.deepcopy(m["spec"]["components"][0])),
        "distribution.duplicate_component",
        "component.graph_integrity_not_validated",
    )
    def duplicate_component_id(m: dict[str, Any]) -> None:
        duplicate = copy.deepcopy(m["spec"]["components"][0])
        duplicate["component_ref"] = "aide://distribution/component/duplicate-id"
        m["spec"]["components"].append(duplicate)
    validate_probe(
        rec,
        "component.duplicate_id_refuses",
        minimal,
        duplicate_component_id,
        "distribution.duplicate_component_id",
        "component.graph_integrity_not_validated",
    )
    validate_probe(
        rec,
        "component.required_component_omitted_refuses",
        minimal,
        lambda m: m["spec"].__setitem__("components", []),
        "distribution.manifest_invalid",
        "component.graph_integrity_not_validated",
    )
    reordered = copy.deepcopy(manifest)
    reordered["spec"]["components"] = list(reversed(reordered["spec"]["components"]))
    reordered["spec"]["artifacts"] = list(reversed(reordered["spec"]["artifacts"]))
    reordered = finalized(reordered)
    rec.check(
        "component.reordered_equivalent_digest_stable",
        category="component_graph",
        description="Reordering components/artifacts does not change distribution digest.",
        expected=manifest["status"]["distribution_digest"],
        observed=reordered["status"]["distribution_digest"],
        passed=reordered["status"]["distribution_digest"] == manifest["status"]["distribution_digest"],
        source_finding_id="component.graph_integrity_not_validated",
        evidence_refs=["component-graph-review.md"],
    )
    return {"component_digest_matches": component_digest_matches}


def make_temp_checksum_root(manifest: dict[str, Any], modifier) -> tuple[tempfile.TemporaryDirectory[str], Path, dict[str, Any]]:
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    checksum_path = root / manifest["spec"]["checksums"]["checksum_manifest_path"]
    checksum_path.parent.mkdir(parents=True, exist_ok=True)
    source_checksums = REPO_ROOT / manifest["spec"]["checksums"]["checksum_manifest_path"]
    shutil.copy2(source_checksums, checksum_path)
    data = read_json(checksum_path)
    modifier(data)
    write_json(checksum_path, data)
    updated = copy.deepcopy(manifest)
    updated["spec"]["checksums"]["manifest_digest"] = digest_file(checksum_path)
    updated = finalized(updated)
    return temp, root, updated


def run_artifact_checks(rec: Recorder, minimal: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    source_validate = validate_manifest(manifest, root=REPO_ROOT, require_files=True)
    rec.check(
        "artifact.q47_files_recompute",
        category="artifact_integrity",
        description="Included Q47 artifacts recompute with byte count, content digest, media type, compression type, checksums, and provenance.",
        expected="valid when artifact files are required",
        observed={"valid": source_validate.get("valid"), "codes": sorted(codes(source_validate))},
        passed=bool(source_validate.get("valid")),
        source_finding_id="artifact.integrity_metadata_not_validated",
        evidence_refs=["artifact-integrity-review.md"],
    )
    validate_probe(
        rec,
        "artifact.missing_file_refuses",
        manifest,
        lambda m: m["spec"]["artifacts"][0].__setitem__("relative_source_location", ".aide/release/dist/missing-artifact.zip"),
        "distribution.manifest_invalid",
        "artifact.integrity_metadata_not_validated",
        root=REPO_ROOT,
        require_files=True,
    )
    validate_probe(
        rec,
        "artifact.wrong_digest_refuses",
        manifest,
        lambda m: m["spec"]["artifacts"][0].__setitem__("content_digest", "sha256:" + "5" * 64),
        "distribution.artifact_digest_mismatch",
        "artifact.integrity_metadata_not_validated",
        root=REPO_ROOT,
        require_files=True,
    )
    validate_probe(
        rec,
        "artifact.wrong_byte_count_refuses",
        manifest,
        lambda m: m["spec"]["artifacts"][0].__setitem__("byte_count", int(m["spec"]["artifacts"][0].get("byte_count", 0)) + 7),
        "distribution.artifact_byte_count_mismatch",
        "artifact.integrity_metadata_not_validated",
        root=REPO_ROOT,
        require_files=True,
    )
    validate_probe(
        rec,
        "artifact.absolute_path_refuses",
        minimal,
        lambda m: m["spec"]["artifacts"][0].__setitem__("relative_source_location", "C:/outside/aide.zip"),
        "distribution.forbidden_member",
        "artifact.integrity_metadata_not_validated",
    )
    validate_probe(
        rec,
        "artifact.traversal_path_refuses",
        minimal,
        lambda m: m["spec"]["artifacts"][0].__setitem__("relative_source_location", "../outside/aide.zip"),
        "distribution.forbidden_member",
        "artifact.integrity_metadata_not_validated",
    )
    validate_probe(
        rec,
        "artifact.unsupported_source_kind_refuses",
        minimal,
        lambda m: m["spec"]["source"].__setitem__("source_kind", "remote_http"),
        "distribution.unsupported_source_kind",
        "artifact.integrity_metadata_not_validated",
    )
    validate_probe(
        rec,
        "artifact.duplicate_ref_refuses",
        minimal,
        lambda m: m["spec"]["artifacts"].append(copy.deepcopy(m["spec"]["artifacts"][0])),
        "distribution.duplicate_artifact",
        "artifact.integrity_metadata_not_validated",
    )
    rec.check(
        "artifact.duplicate_id_non_identity",
        category="artifact_integrity",
        description="artifact_ref is the artifact identity; duplicate artifact_id is not treated as separate identity law in v1.",
        expected="no material duplicate artifact_id requirement unless identity law changes",
        observed="artifact_ref is checked; artifact_id is descriptive",
        passed=True,
        source_finding_id="artifact.integrity_metadata_not_validated",
        evidence_refs=["artifact-integrity-review.md"],
        material=False,
    )
    directory_artifacts = [a for a in manifest["spec"]["artifacts"] if a.get("source_kind") == "local_directory"]
    directory_summary: list[dict[str, Any]] = []
    for artifact in directory_artifacts:
        path = REPO_ROOT / artifact["relative_source_location"]
        count, total, digest, forbidden = sut.directory_inventory_digest(path)
        directory_summary.append(
            {
                "artifact_ref": artifact["artifact_ref"],
                "reported_count": artifact.get("directory_file_count"),
                "observed_count": count,
                "reported_byte_count": artifact.get("byte_count"),
                "observed_byte_count": total,
                "reported_digest": artifact.get("content_digest"),
                "observed_digest": digest,
                "reported_forbidden": artifact.get("directory_forbidden_member_count"),
                "observed_forbidden": len(forbidden),
            }
        )
    rec.check(
        "artifact.local_directory_recomputed",
        category="artifact_integrity",
        description="Local directory artifact inventory recomputes.",
        expected="reported count, bytes, digest, and forbidden count match observed inventory",
        observed=directory_summary,
        passed=all(
            item["reported_count"] == item["observed_count"]
            and item["reported_byte_count"] == item["observed_byte_count"]
            and item["reported_digest"] == item["observed_digest"]
            and item["reported_forbidden"] == item["observed_forbidden"]
            for item in directory_summary
        ),
        source_finding_id="artifact.integrity_metadata_not_validated",
        evidence_refs=["artifact-integrity-review.md"],
    )
    return {"q47_validate": source_validate, "directory_summary": directory_summary}


def run_preaccess_checks(rec: Recorder) -> dict[str, Any]:
    invalid_paths = [
        "/tmp/outside/aide.zip",
        "C:/outside/aide.zip",
        "\\\\server\\share\\aide.zip",
        "../outside/aide.zip",
        ".aide.local/state.sqlite",
        ".env",
    ]
    path_access_results: list[dict[str, Any]] = []
    for path_value in invalid_paths:
        accessed: list[str] = []

        def fail_exists(self):  # type: ignore[no-untyped-def]
            accessed.append(f"exists:{self}")
            raise AssertionError(f"Path.exists called before containment for {path_value}")

        def fail_stat(self):  # type: ignore[no-untyped-def]
            accessed.append(f"stat:{self}")
            raise AssertionError(f"Path.stat called before containment for {path_value}")

        def fail_open(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            accessed.append(f"open:{self}")
            raise AssertionError(f"Path.open called before containment for {path_value}")

        def fail_sha(path: Path):  # type: ignore[no-untyped-def]
            accessed.append(f"sha256:{path}")
            raise AssertionError(f"sha256_file called before containment for {path_value}")

        record = {"path": path_value, "accessed": accessed, "raised": None}
        with patch.object(Path, "exists", fail_exists), patch.object(Path, "stat", fail_stat), patch.object(Path, "open", fail_open), patch.object(sut, "sha256_file", fail_sha):
            try:
                sut._artifact_from_release_record(REPO_ROOT, {"path": path_value, "asset_id": "bad.zip", "sha256": "0" * 64, "size_bytes": 1})
            except AssertionError as exc:
                record["raised"] = str(exc)
        path_access_results.append(record)
    rec.check(
        "path.preaccess_invalid_records_do_not_probe",
        category="path_safety",
        description="Invalid release artifact paths are rejected before stat/open/hash.",
        expected="no Path.exists, Path.stat, Path.open, or sha256_file calls for invalid records",
        observed=path_access_results,
        passed=all(not item["accessed"] and item["raised"] is None for item in path_access_results),
        source_finding_id="path.preaccess_validation_order_violation",
        evidence_refs=["preaccess-path-safety.md"],
    )
    symlink_result = {"attempted": False, "valid": None, "reason": ""}
    with tempfile.TemporaryDirectory() as temp_name:
        temp_root = Path(temp_name)
        outside = temp_root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        link = temp_root / "link-outside.txt"
        try:
            os.symlink(outside, link)
            symlink_result["attempted"] = True
            artifact = sut._artifact_from_release_record(temp_root, {"path": "link-outside.txt", "asset_id": "link-outside.txt", "sha256": "0" * 64, "size_bytes": 7})
            validation = validate_manifest(
                finalized(
                    mutate(
                        sut.minimal_fixture_manifest(),
                        lambda m: m["spec"]["artifacts"].__setitem__(0, {**m["spec"]["artifacts"][0], **artifact}),
                    )
                ),
                root=temp_root,
                require_files=True,
            )
            symlink_result["valid"] = validation.get("valid")
            symlink_result["reason"] = ",".join(sorted(codes(validation)))
        except (OSError, NotImplementedError) as exc:
            symlink_result["reason"] = f"symlink unavailable: {exc}"
    rec.check(
        "path.symlink_escape_rejected_where_practical",
        category="path_safety",
        description="Symlink/reparse escape is rejected where the platform permits a symlink probe.",
        expected="invalid or unavailable with warning",
        observed=symlink_result,
        passed=(not symlink_result["attempted"]) or symlink_result["valid"] is False,
        source_finding_id="path.preaccess_validation_order_violation",
        evidence_refs=["preaccess-path-safety.md"],
        material=False if not symlink_result["attempted"] else True,
    )
    return {"invalid_path_results": path_access_results, "symlink_result": symlink_result}


def run_checksum_checks(rec: Recorder, manifest: dict[str, Any]) -> dict[str, Any]:
    checksum_path = REPO_ROOT / manifest["spec"]["checksums"]["checksum_manifest_path"]
    checksum_data = read_json(checksum_path)
    checksum_entries = checksum_data.get("checksums", {})
    included_names = [
        Path(str(artifact.get("relative_source_location", ""))).name
        for artifact in manifest["spec"]["artifacts"]
        if artifact.get("included") is True and artifact.get("checksum_ref")
    ]
    missing = [name for name in included_names if name not in checksum_entries]
    wrong = [
        name
        for name in included_names
        for artifact in manifest["spec"]["artifacts"]
        if Path(str(artifact.get("relative_source_location", ""))).name == name
        and checksum_entries.get(name) != str(artifact.get("content_digest", "")).removeprefix("sha256:")
    ]
    rec.check(
        "checksum.q47_values_match",
        category="checksum",
        description="Every included Q47 file artifact has an exact checksum entry matching content_digest.",
        expected="no missing or wrong checksums",
        observed={"missing": missing, "wrong": wrong, "included_names": included_names},
        passed=not missing and not wrong,
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    rec.check(
        "checksum.manifest_digest_matches",
        category="checksum",
        description="Checksum manifest digest matches the referenced file.",
        expected=manifest["spec"]["checksums"]["manifest_digest"],
        observed=digest_file(checksum_path),
        passed=manifest["spec"]["checksums"]["manifest_digest"] == digest_file(checksum_path),
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    first_name = included_names[0]
    temp, temp_root, wrong_value_manifest = make_temp_checksum_root(
        manifest,
        lambda d: d["checksums"].__setitem__(first_name, "0" * 64),
    )
    with temp:
        wrong_value_result = validate_manifest(wrong_value_manifest, root=temp_root)
    rec.check(
        "checksum.correct_name_wrong_value_refuses",
        category="checksum",
        description="Correct checksum filename with wrong checksum value fails.",
        expected="distribution.checksum_digest_mismatch",
        observed={"valid": wrong_value_result.get("valid"), "codes": sorted(codes(wrong_value_result))},
        passed="distribution.checksum_digest_mismatch" in codes(wrong_value_result),
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    temp, temp_root, missing_manifest = make_temp_checksum_root(
        manifest,
        lambda d: d["checksums"].pop(first_name, None),
    )
    with temp:
        missing_result = validate_manifest(missing_manifest, root=temp_root)
    rec.check(
        "checksum.missing_entry_refuses",
        category="checksum",
        description="Missing checksum entry fails.",
        expected="distribution.missing_checksum",
        observed={"valid": missing_result.get("valid"), "codes": sorted(codes(missing_result))},
        passed="distribution.missing_checksum" in codes(missing_result),
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    duplicate_basename_manifest = mutate(
        sut.minimal_fixture_manifest(),
        lambda m: m["spec"]["artifacts"].append({**copy.deepcopy(m["spec"]["artifacts"][0]), "artifact_ref": "aide://distribution/artifact/duplicate-name", "relative_source_location": "elsewhere/minimal.json"}),
    )
    duplicate_basename_manifest = finalized(duplicate_basename_manifest)
    duplicate_result = validate_manifest(duplicate_basename_manifest)
    rec.check(
        "checksum.basename_collision_refuses",
        category="checksum",
        description="Two included artifacts with the same checksum basename fail.",
        expected="distribution.checksum_basename_collision",
        observed={"valid": duplicate_result.get("valid"), "codes": sorted(codes(duplicate_result))},
        passed="distribution.checksum_basename_collision" in codes(duplicate_result),
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    wrong_algorithm = finalized(mutate(sut.minimal_fixture_manifest(), lambda m: m["spec"]["checksums"].__setitem__("algorithm", "sha512")))
    wrong_algorithm_result = validate_manifest(wrong_algorithm)
    rec.check(
        "checksum.wrong_algorithm_refuses",
        category="checksum",
        description="Checksum algorithm must be exactly sha256.",
        expected="distribution.manifest_invalid",
        observed={"valid": wrong_algorithm_result.get("valid"), "codes": sorted(codes(wrong_algorithm_result))},
        passed="distribution.manifest_invalid" in codes(wrong_algorithm_result),
        source_finding_id="checksum.value_not_verified",
        evidence_refs=["checksum-value-review.md"],
    )
    return {
        "checksum_file": rel(checksum_path),
        "included_names": included_names,
        "wrong_value_codes": sorted(codes(wrong_value_result)),
        "missing_codes": sorted(codes(missing_result)),
    }


def run_protocol_checks(rec: Recorder, minimal: dict[str, Any]) -> dict[str, Any]:
    probes = {
        "protocol.min_above_v1_refuses": (
            lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "2.0.0", "max": "3.x"}),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.max_below_v1_refuses": (
            lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "1.0.0", "max": "0.x"}),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.inverted_range_refuses": (
            lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "1.1.0", "max": "1.0.0"}),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.malformed_range_refuses": (
            lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "1.0", "max": "one.x"}),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.missing_reader_refuses": (
            lambda m: m["spec"]["protocol"].pop("min_reader_version", None),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.missing_writer_refuses": (
            lambda m: m["spec"]["protocol"].pop("min_writer_version", None),
            "distribution.unsupported_protocol_range",
        ),
        "protocol.unsupported_migration_refuses": (
            lambda m: m["spec"]["protocol"]["required_migrations"].append("future-migration-v9"),
            "distribution.incompatible_migration",
        ),
        "protocol.unknown_required_feature_refuses": (
            lambda m: m["spec"]["protocol"]["required_features"].append("future-required-feature"),
            "distribution.unknown_required_feature",
        ),
        "protocol.component_incompatible_refuses": (
            lambda m: m["spec"]["components"][0].__setitem__("compatibility_constraints", {"min_reader_version": "2.0.0", "min_writer_version": "2.0.0"}),
            "distribution.unsupported_protocol_range",
        ),
    }
    protocol_results: dict[str, Any] = {}
    for assertion_id, (func, expected_code) in probes.items():
        data = finalized(mutate(minimal, func))
        result = validate_manifest(data)
        protocol_results[assertion_id] = sorted(codes(result))
        rec.check(
            assertion_id,
            category="protocol_range",
            description=f"{assertion_id} must fail closed.",
            expected=expected_code,
            observed={"valid": result.get("valid"), "codes": sorted(codes(result))},
            passed=expected_code in codes(result),
            source_finding_id="protocol.range_semantics_incomplete",
            evidence_refs=["protocol-range-review.md"],
        )
    future_major = finalized(mutate(minimal, lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "1.0.0", "max": "2.x"})))
    future_major_result = validate_manifest(future_major)
    rec.check(
        "protocol.future_major_not_implicitly_accepted",
        category="protocol_range",
        description="A future-major maximum must not be accepted merely because current v1 is inside the numeric interval.",
        expected="distribution.unsupported_protocol_range unless explicit future-major support exists",
        observed={"valid": future_major_result.get("valid"), "codes": sorted(codes(future_major_result)), "range": future_major["spec"]["protocol"]["protocol_range"]},
        passed="distribution.unsupported_protocol_range" in codes(future_major_result),
        source_finding_id="protocol.range_semantics_incomplete",
        evidence_refs=["protocol-range-review.md"],
    )
    optional = finalized(mutate(minimal, lambda m: m["spec"]["protocol"]["optional_features"].append("future.optional.feature")))
    optional_result = validate_manifest(optional)
    preserved = "future.optional.feature" in optional["spec"]["protocol"]["optional_features"]
    rec.check(
        "protocol.unknown_optional_feature_tolerated",
        category="protocol_range",
        description="Unknown optional features are tolerated and preserved.",
        expected="valid with warning and preserved optional feature",
        observed={"valid": optional_result.get("valid"), "warnings": optional_result.get("warnings"), "preserved": preserved},
        passed=bool(optional_result.get("valid")) and preserved,
        source_finding_id="protocol.range_semantics_incomplete",
        evidence_refs=["protocol-range-review.md"],
    )
    return {"protocol_probe_codes": protocol_results, "future_major_codes": sorted(codes(future_major_result))}


def independent_forbidden_reason(value: str) -> str | None:
    normalized = value.replace("\\", "/").strip()
    if not normalized:
        return "empty"
    lower = normalized.lower()
    if lower.startswith("/") or re.match(r"^[a-z]:/", lower) or lower.startswith("//"):
        return "absolute_or_drive"
    if any(part == ".." for part in normalized.split("/")):
        return "traversal"
    target_like = lower
    if target_like.startswith("files/"):
        target_like = target_like.removeprefix("files/")
    if target_like in {".aide.local", ".env", "raw-prompt.txt", "raw-response.txt"}:
        return "forbidden_exact"
    prefixes = (
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
    if target_like.startswith(prefixes):
        return "forbidden_prefix"
    if re.search(r"(^|/)(secret|secrets|credential|credentials|token|tokens|\.env)(/|$)", target_like, re.IGNORECASE):
        return "secret_like"
    return None


def run_contamination_checks(rec: Recorder, minimal: dict[str, Any]) -> dict[str, Any]:
    direct_paths = [
        ".aide.local/state.sqlite",
        ".env",
        "raw-prompt.txt",
        "raw-response.txt",
        ".aide/context/latest-task-packet.md",
        ".aide/reports/distribution-manifest-v1/manifest.json",
        ".aide/repo/latest-inventory.json",
        ".aide/roots/latest-classification.json",
        ".aide/tools/latest-tools.json",
        ".aide/install/latest-plan.json",
        ".aide/repair/latest-plan.json",
        ".aide/upgrade/latest-plan.json",
        ".aide/rollback/latest-plan.json",
        ".aide/uninstall/latest-plan.json",
        "logs/run.log",
        ".cache/cache.bin",
        "secrets/token.txt",
    ]
    nested_paths = [
        "files/.aide.local/state.sqlite",
        "files/.env",
        "files/raw-prompt.txt",
        "files/raw-response.txt",
        "files/.aide/context/latest-task-packet.md",
        "files/.aide/reports/distribution-manifest-v1/manifest.json",
        "files/.aide/repo/latest-inventory.json",
        "files/.aide/roots/latest-classification.json",
        "files/.aide/tools/latest-tools.json",
        "files/.aide/install/latest-plan.json",
        "files/.aide/repair/latest-plan.json",
        "files/.aide/upgrade/latest-plan.json",
        "files/.aide/rollback/latest-plan.json",
        "files/.aide/uninstall/latest-plan.json",
        "files/logs/run.log",
        "files/.cache/cache.bin",
        "files/secrets/token.txt",
    ]
    classification = []
    for path in direct_paths + nested_paths:
        actual = sut.forbidden_member_reason(path)
        expected = independent_forbidden_reason(path)
        classification.append({"path": path, "expected": expected, "observed": actual})
    rec.check(
        "contamination.forbidden_path_classification_complete",
        category="contamination",
        description="Forbidden source-state categories are classified, including export-pack target-root members under files/.",
        expected="observed forbidden reason for every independently forbidden path",
        observed=classification,
        passed=all(item["observed"] for item in classification if item["expected"]),
        source_finding_id="contamination.forbidden_members_silently_filtered",
        evidence_refs=["contamination-review.md"],
    )
    with tempfile.TemporaryDirectory() as temp_name:
        temp_root = Path(temp_name)
        clean_root = temp_root / "clean"
        dirty_root = temp_root / "dirty"
        nested_dirty_root = temp_root / "nested-dirty"
        (clean_root / "files").mkdir(parents=True)
        (clean_root / "files/README.md").write_text("ok", encoding="utf-8")
        (dirty_root / ".aide.local").mkdir(parents=True)
        (dirty_root / ".aide.local/state.sqlite").write_text("dirty", encoding="utf-8")
        (nested_dirty_root / "files/.aide.local").mkdir(parents=True)
        (nested_dirty_root / "files/.aide.local/state.sqlite").write_text("dirty", encoding="utf-8")
        clean = sut.directory_inventory_digest(clean_root)
        dirty = sut.directory_inventory_digest(dirty_root)
        nested_dirty = sut.directory_inventory_digest(nested_dirty_root)
    directory_summary = {
        "clean_forbidden": len(clean[3]),
        "dirty_forbidden": len(dirty[3]),
        "nested_dirty_forbidden": len(nested_dirty[3]),
    }
    rec.check(
        "contamination.directory_forbidden_members_recorded",
        category="contamination",
        description="Local-directory forbidden members are recorded instead of silently producing a clean digest.",
        expected="dirty and nested-dirty directories have forbidden members",
        observed=directory_summary,
        passed=directory_summary["dirty_forbidden"] > 0 and directory_summary["nested_dirty_forbidden"] > 0,
        source_finding_id="contamination.forbidden_members_silently_filtered",
        evidence_refs=["contamination-review.md"],
    )
    contaminated_artifact = finalized(
        mutate(
            minimal,
            lambda m: (
                m["spec"]["artifacts"][0].__setitem__("source_kind", "local_directory"),
                m["spec"]["artifacts"][0].__setitem__("directory_forbidden_member_count", 1),
                m["spec"]["artifacts"][0].__setitem__("directory_forbidden_members", [{"path": ".aide.local/state.sqlite", "reason": "forbidden"}]),
            ),
        )
    )
    contaminated_result = validate_manifest(contaminated_artifact)
    rec.check(
        "contamination.directory_artifact_refuses",
        category="contamination",
        description="Manifest with reported local-directory forbidden members fails validation.",
        expected="distribution.source_state_contamination",
        observed={"valid": contaminated_result.get("valid"), "codes": sorted(codes(contaminated_result))},
        passed="distribution.source_state_contamination" in codes(contaminated_result),
        source_finding_id="contamination.forbidden_members_silently_filtered",
        evidence_refs=["contamination-review.md"],
    )
    return {"classification": classification, "directory_summary": directory_summary}


def run_fixture_checks(rec: Recorder) -> dict[str, Any]:
    required_valid = {
        "minimal valid unsigned": FIXTURE_ROOT / "valid/minimal-unsigned.json",
        "full Q47/local archive": FIXTURE_ROOT / "valid/full-local-archive.json",
        "local directory": FIXTURE_ROOT / "valid/local-directory.json",
        "reordered equivalent": FIXTURE_ROOT / "valid/reordered-input.json",
        "unknown optional feature": FIXTURE_ROOT / "valid/unknown-optional-feature.json",
        "unknown optional extension round-trip": FIXTURE_ROOT / "valid/unknown-optional-extension-round-trip.json",
    }
    required_invalid = {
        "duplicate component_ref": FIXTURE_ROOT / "invalid/duplicate-component.json",
        "duplicate component_id": FIXTURE_ROOT / "invalid/duplicate-component-id.json",
        "duplicate artifact_ref": FIXTURE_ROOT / "invalid/duplicate-artifact.json",
        "missing digest": FIXTURE_ROOT / "invalid/missing-digest.json",
        "malformed digest": FIXTURE_ROOT / "invalid/malformed-digest.json",
        "wrong artifact digest": FIXTURE_ROOT / "invalid/wrong-artifact-digest.json",
        "wrong component digest": FIXTURE_ROOT / "invalid/wrong-component-digest.json",
        "wrong manifest payload digest": FIXTURE_ROOT / "invalid/wrong-payload-digest.json",
        "wrong distribution digest": FIXTURE_ROOT / "invalid/wrong-distribution-digest.json",
        "missing artifact ref": FIXTURE_ROOT / "invalid/missing-artifact-ref.json",
        "missing dependency": FIXTURE_ROOT / "invalid/missing-dependency.json",
        "dependency cycle": FIXTURE_ROOT / "invalid/dependency-cycle.json",
        "unsupported source kind": FIXTURE_ROOT / "invalid/unsupported-source-kind.json",
        "unknown required feature": FIXTURE_ROOT / "invalid/unknown-required-feature.json",
        "unsupported protocol range": FIXTURE_ROOT / "invalid/unsupported-protocol-range.json",
        "inverted protocol range": FIXTURE_ROOT / "invalid/inverted-protocol-range.json",
        "forbidden member": FIXTURE_ROOT / "invalid/forbidden-member.json",
        "source contamination": FIXTURE_ROOT / "invalid/source-contamination.json",
        ".aide.local": FIXTURE_ROOT / "invalid/aide-local-member.json",
        "absolute path": FIXTURE_ROOT / "invalid/absolute-path.json",
        "traversal": FIXTURE_ROOT / "invalid/traversal-path.json",
        "checksum missing": FIXTURE_ROOT / "invalid/checksum-missing.json",
        "checksum wrong value": FIXTURE_ROOT / "invalid/checksum-wrong-value.json",
        "checksum basename collision": FIXTURE_ROOT / "invalid/checksum-basename-collision.json",
        "signature placeholder false verified": FIXTURE_ROOT / "invalid/false-verified-signature.json",
        "false signature verification": FIXTURE_ROOT / "invalid/false-signature-verification.json",
        "missing SBOM": FIXTURE_ROOT / "invalid/missing-sbom.json",
        "incompatible migration": FIXTURE_ROOT / "invalid/incompatible-migration.json",
        "source report member": FIXTURE_ROOT / "invalid/forbidden-source-report-member.json",
    }
    missing_valid = {name: rel(path) for name, path in required_valid.items() if not path.exists()}
    missing_invalid = {name: rel(path) for name, path in required_invalid.items() if not path.exists()}
    rec.check(
        "fixture.required_files_exist",
        category="fixture_coverage",
        description="Required valid and invalid fixture files exist.",
        expected="all required fixtures present",
        observed={"missing_valid": missing_valid, "missing_invalid": missing_invalid},
        passed=not missing_valid and not missing_invalid,
        source_finding_id="fixture.required_coverage_incomplete",
        evidence_refs=["fixture-coverage-review.md"],
    )
    valid_results = {}
    for name, path in required_valid.items():
        if path.exists():
            result = validate_manifest(read_json(path))
            valid_results[name] = {"valid": result.get("valid"), "codes": sorted(codes(result))}
    invalid_results = {}
    for name, path in required_invalid.items():
        if path.exists():
            result = validate_manifest(read_json(path))
            invalid_results[name] = {"valid": result.get("valid"), "codes": sorted(codes(result))}
    rec.check(
        "fixture.valid_behavior",
        category="fixture_coverage",
        description="Valid fixture corpus passes semantic validation.",
        expected="all valid fixtures valid",
        observed=valid_results,
        passed=all(item["valid"] for item in valid_results.values()),
        source_finding_id="fixture.required_coverage_incomplete",
        evidence_refs=["fixture-coverage-review.md"],
    )
    rec.check(
        "fixture.invalid_behavior",
        category="fixture_coverage",
        description="Invalid fixture corpus fails semantic validation.",
        expected="all invalid fixtures invalid",
        observed=invalid_results,
        passed=all(not item["valid"] for item in invalid_results.values()),
        source_finding_id="fixture.required_coverage_incomplete",
        evidence_refs=["fixture-coverage-review.md"],
    )
    future_major_fixture_candidates = list((FIXTURE_ROOT / "invalid").glob("*future*major*.json"))
    rec.check(
        "fixture.future_major_protocol_fixture_present",
        category="fixture_coverage",
        description="Fixture corpus covers future-major protocol max declarations.",
        expected="direct invalid future-major protocol fixture",
        observed=[rel(path) for path in future_major_fixture_candidates],
        passed=bool(future_major_fixture_candidates),
        source_finding_id="fixture.required_coverage_incomplete",
        evidence_refs=["fixture-coverage-review.md"],
    )
    return {"valid_results": valid_results, "invalid_results": invalid_results, "future_major_fixtures": [rel(path) for path in future_major_fixture_candidates]}


def run_q47_mapping_checks(rec: Recorder, manifest: dict[str, Any]) -> dict[str, Any]:
    release_assets_path = REPO_ROOT / ".aide/release/dist/release-assets.json"
    release_provenance_path = REPO_ROOT / ".aide/release/dist/release-provenance.json"
    q48_draft_path = REPO_ROOT / ".aide/release/latest-github-release-draft.json"
    assets = read_json(release_assets_path)
    provenance = read_json(release_provenance_path)
    asset_records = assets.get("artifacts", []) if isinstance(assets.get("artifacts"), list) else []
    included_asset_names = sorted(str(item.get("asset_id") or Path(str(item.get("path", ""))).name) for item in asset_records if item.get("included", True))
    manifest_asset_names = sorted(
        str(artifact.get("artifact_id", ""))
        for artifact in manifest["spec"]["artifacts"]
        if artifact.get("portable_role") == "release_bundle_artifact" and artifact.get("included") is True
    )
    source = manifest["spec"]["source"]
    rec.check(
        "q47.included_assets_represented_once",
        category="q47_mapping",
        description="Included Q47 assets are represented in the manifest.",
        expected=included_asset_names,
        observed=manifest_asset_names,
        passed=included_asset_names == manifest_asset_names,
        source_finding_id=None,
        evidence_refs=["q47-mapping-regression.md"],
    )
    rec.check(
        "q47.q48_not_distribution_truth",
        category="q47_mapping",
        description="Q48 release draft remains publication-review evidence, not distribution truth.",
        expected="q48_publication_draft_is_distribution_truth false",
        observed={"q48_exists": q48_draft_path.exists(), "source_flag": source.get("q48_publication_draft_is_distribution_truth")},
        passed=source.get("q48_publication_draft_is_distribution_truth") is False,
        source_finding_id=None,
        evidence_refs=["q47-mapping-regression.md"],
    )
    rec.check(
        "q47.local_source_path_suppressed",
        category="q47_mapping",
        description="Local source paths are suppressed from portable distribution truth.",
        expected="q47 source repo value suppressed",
        observed={"source_paths": source.get("source_paths"), "suppressed": source.get("q47_source_repo_value_suppressed")},
        passed=bool(source.get("q47_source_repo_value_suppressed")),
        source_finding_id=None,
        evidence_refs=["q47-mapping-regression.md"],
    )
    return {"included_asset_names": included_asset_names, "manifest_asset_names": manifest_asset_names, "provenance_keys": sorted(provenance.keys())}


def run_signature_sbom_checks(rec: Recorder, manifest: dict[str, Any], minimal: dict[str, Any]) -> dict[str, Any]:
    signatures = manifest["spec"].get("signature_records", [])
    sboms = manifest["spec"].get("sbom_refs", [])
    rec.check(
        "signature.unsigned_boundary_explicit",
        category="signature_sbom",
        description="Signature records do not claim verification.",
        expected="all signatures unverified/unsigned",
        observed=signatures,
        passed=all(isinstance(sig, dict) and sig.get("verified") is False and sig.get("status") != "verified" for sig in signatures),
        source_finding_id=None,
        evidence_refs=["no-overclaiming-review.md"],
    )
    rec.check(
        "sbom.unavailable_boundary_explicit",
        category="signature_sbom",
        description="SBOM records are unavailable or placeholder, not generated.",
        expected="status unavailable or placeholder",
        observed=sboms,
        passed=bool(sboms) and all(isinstance(sbom, dict) and sbom.get("status") in {"unavailable", "placeholder"} for sbom in sboms),
        source_finding_id=None,
        evidence_refs=["no-overclaiming-review.md"],
    )
    validate_probe(
        rec,
        "signature.false_verification_refuses",
        minimal,
        lambda m: m["spec"]["signature_records"][0].update({"status": "verified", "verified": True}),
        "distribution.signature_unverified",
        "schema.optional_extension_boundary_missing",
    )
    validate_probe(
        rec,
        "sbom.generated_claim_refuses",
        minimal,
        lambda m: m["spec"]["sbom_refs"][0].update({"status": "generated"}),
        "distribution.sbom_unavailable",
        "schema.optional_extension_boundary_missing",
    )
    return {"signature_records": signatures, "sbom_refs": sboms}


def run_no_overclaiming_checks(rec: Recorder, manifest: dict[str, Any]) -> dict[str, Any]:
    status = manifest.get("status", {})
    false_fields = [
        "install_apply_implemented",
        "update_apply_implemented",
        "repair_apply_implemented",
        "rollback_apply_implemented",
        "uninstall_apply_implemented",
        "release_publication_implemented",
        "target_repository_mutation_implemented",
        "network_calls_implemented",
        "provider_model_calls_implemented",
    ]
    observed = {field: status.get(field) for field in false_fields}
    rec.check(
        "non_capabilities.false_boundary_preserved",
        category="non_capability",
        description="DistributionManifest report does not claim apply, publication, network, provider/model, or target mutation behavior.",
        expected="all false-boundary fields false",
        observed=observed,
        passed=all(value is False for value in observed.values()),
        source_finding_id=None,
        evidence_refs=["no-overclaiming-review.md"],
    )
    return {"false_boundary": observed}


def changed_files_snapshot() -> list[str]:
    completed = run_cmd(["git", "status", "--short"])
    lines = [line for line in completed.get("stdout_excerpt", "").splitlines() if line.strip()]
    return lines


def status_contains_only_allowed_check_outputs(status_text: str) -> bool:
    allowed_prefixes = (
        "M .aide/queue/index.yaml",
        "?? .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01/",
        "?? .aide/reports/distribution-manifest-v1-repair-01-check/",
    )
    lines = [line.strip() for line in status_text.splitlines() if line.strip()]
    if lines == ["## main...origin/main"]:
        return True
    for line in lines:
        if line == "## main...origin/main":
            continue
        if not any(line.startswith(prefix) for prefix in allowed_prefixes):
            return False
    return True


def write_evidence_md(name: str, title: str, body: Any) -> None:
    text = [f"# {title}", ""]
    if isinstance(body, str):
        text.append(body)
    else:
        text.append("```json")
        text.append(stable_json(body).rstrip())
        text.append("```")
    write_text(EVIDENCE_ROOT / name, "\n".join(text) + "\n")


def write_report_md(assertions: list[dict[str, Any]], material_findings: list[dict[str, Any]], result: str, next_task: str) -> None:
    lines = [
        "# DistributionManifest v1 Repair 01 Check",
        "",
        f"- result: {result}",
        f"- material_finding_count: {len(material_findings)}",
        "- missing_evidence: 0",
        f"- recommended_next_task: {next_task}",
        "",
        "## Material Findings",
        "",
    ]
    if material_findings:
        for item in material_findings:
            lines.extend(
                [
                    f"### {item['id']}",
                    "",
                    f"- source_finding_id: {item.get('source_finding_id')}",
                    f"- expected: {item.get('expected')}",
                    f"- observed: `{json.dumps(item.get('observed'), sort_keys=True)[:900]}`",
                    "",
                ]
            )
    else:
        lines.append("None.")
        lines.append("")
    lines.extend(["## Assertion Counts", ""])
    pass_count = sum(1 for item in assertions if item["outcome"] == "PASS")
    fail_count = sum(1 for item in assertions if item["outcome"] == "FAIL")
    warning_count = sum(1 for item in assertions if item["outcome"] == "WARNING")
    lines.extend([f"- pass: {pass_count}", f"- fail: {fail_count}", f"- warning: {warning_count}", ""])
    write_text(REPORT_ROOT / "check-report.md", "\n".join(lines))


def write_status_files(result: str, next_task: str, material_count: int, missing_evidence: int) -> None:
    task_yaml = f"""schema_version: aide.queue-task.v0
id: {TASK_ID}
title: Check DistributionManifest v1 Repair 01
status: needs_review
planning_state: check_completed
result: {result}
task_type: check
created_at: 2026-06-26
updated_at: 2026-06-26
review_gate: needs_review
source_task: {SOURCE_TASK_ID}
source_commit: {SOURCE_COMMIT}
source_capability: {CAPABILITY}
source_result: PASS_WITH_WARNINGS
proposed_capability: {CAPABILITY}
accepted_capability: null
authorizes_implementation: false
material_finding_count: {material_count}
missing_evidence: {missing_evidence}
recommended_next_task: {next_task}
allowed_paths:
  - .aide/queue/{TASK_ID}/**
  - .aide/reports/distribution-manifest-v1-repair-01-check/**
  - .aide/queue/index.yaml
  - PLANS.md
  - IMPLEMENT.md
read_only_paths:
  - AGENTS.md
  - README.md
  - DOCUMENTATION.md
  - ROADMAP.md
  - PLANS.md
  - IMPLEMENT.md
  - .aide/profile.yaml
  - .aide/queue/README.md
  - .aide/queue/policy.yaml
  - .aide/queue/index.yaml
  - .aide/queue/{SOURCE_TASK_ID}/**
  - .aide/queue/{SOURCE_CHECK_TASK_ID}/**
  - .aide/protocol/aide-distribution-manifest-v1.schema.json
  - core/protocol/distribution_manifest.py
  - .aide/scripts/tests/test_aide_distribution_manifest_v1.py
  - .aide/fixtures/distribution-manifest-v1/**
  - .aide/reports/distribution-manifest-v1/**
  - .aide/release/**
  - .aide/export/aide-lite-pack-v0/**
forbidden_paths:
  - .aide/protocol/aide-distribution-manifest-v1.schema.json
  - core/protocol/distribution_manifest.py
  - .aide/scripts/aide_lite.py
  - .aide/scripts/tests/test_aide_distribution_manifest_v1.py
  - .aide/fixtures/distribution-manifest-v1/**
  - .aide/reports/distribution-manifest-v1/**
  - target repositories
non_capabilities:
  - no implementation repair
  - no DistributionManifest acceptance
  - no ProjectLock work
  - no install apply
  - no update apply
  - no repair apply
  - no rollback apply
  - no uninstall apply
  - no release publication
  - no Git tag creation
  - no GitHub Release creation
  - no upload
  - no network call
  - no provider/model call
  - no target repository mutation
  - no branch/worktree automation
  - no Workbench runtime
  - no MCP runtime
  - no source-change preview/apply/rollback
  - no promotion
evidence:
"""
    for name in REQUIRED_EVIDENCE:
        task_yaml += f"  - .aide/queue/{TASK_ID}/evidence/{name}\n"
    task_yaml += "reports:\n"
    for name in REQUIRED_REPORTS:
        task_yaml += f"  - .aide/reports/distribution-manifest-v1-repair-01-check/{name}\n"
    task_yaml += "warnings:\n"
    if result == "PASS_WITH_WARNINGS":
        task_yaml += "  - Existing Q47 local release artifacts remain preview/no-publish evidence.\n"
    if result == "REQUEST_CHANGES":
        task_yaml += "  - Material findings remain; downstream DistributionManifest acceptance and ProjectLock are blocked.\n"
    task_yaml += "blockers: []\n"
    write_text(TASK_ROOT / "task.yaml", task_yaml)
    status_yaml = f"""schema_version: aide.task-status.v0
id: {TASK_ID}
status: needs_review
planning_state: check_completed
result: {result}
review_gate: needs_review
updated_at: 2026-06-26
source_task: {SOURCE_TASK_ID}
source_commit: {SOURCE_COMMIT}
proposed_capability: {CAPABILITY}
accepted_capability: null
material_finding_count: {material_count}
missing_evidence: {missing_evidence}
recommended_next_task: {next_task}
implementation_repaired: false
distribution_manifest_accepted: false
project_lock_started: false
install_apply_executed: false
upgrade_apply_executed: false
repair_apply_executed: false
rollback_apply_executed: false
uninstall_apply_executed: false
release_publication_performed: false
target_repository_mutated: false
branch_worktree_automation_performed: false
network_calls_performed: false
provider_or_model_calls_performed: false
blockers: []
"""
    write_text(TASK_ROOT / "status.yaml", status_yaml)


REQUIRED_EVIDENCE = [
    "baseline.md",
    "source-repair-review.md",
    "nine-finding-check-matrix.md",
    "extension-boundary-review.md",
    "identity-boundary-review.md",
    "digest-recomputation.md",
    "component-graph-review.md",
    "artifact-integrity-review.md",
    "preaccess-path-safety.md",
    "checksum-value-review.md",
    "protocol-range-review.md",
    "contamination-review.md",
    "fixture-coverage-review.md",
    "q47-mapping-regression.md",
    "no-overclaiming-review.md",
    "changed-files.md",
    "validation-commands.md",
    "validation-results.md",
    "validation.md",
    "remaining-risks.md",
    "next-task-prompt.md",
]

REQUIRED_REPORTS = [
    "check-report.json",
    "check-report.md",
    "digest-review.json",
    "component-graph-review.json",
    "artifact-integrity-review.json",
    "checksum-review.json",
    "protocol-range-review.json",
    "contamination-review.json",
    "fixture-coverage-review.json",
    "material-findings.json",
    "status.md",
    "next-task-prompt.md",
]


def main() -> int:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    for path in list(EVIDENCE_ROOT.iterdir()):
        if path.name == Path(__file__).name:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    if REPORT_ROOT.exists():
        shutil.rmtree(REPORT_ROOT)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    rec = Recorder()
    schema = read_json(REPO_ROOT / ".aide/protocol/aide-distribution-manifest-v1.schema.json")
    manifest = read_json(SOURCE_REPORT_ROOT / "manifest.json")
    minimal = sut.minimal_fixture_manifest()
    source_summary = material_finding_source_summary()
    head = run_cmd(["git", "rev-parse", "HEAD"])["stdout_excerpt"].strip()
    origin = run_cmd(["git", "rev-parse", "origin/main"])["stdout_excerpt"].strip()
    status = run_cmd(["git", "status", "--short", "--branch"])["stdout_excerpt"].strip()
    log = run_cmd(["git", "log", "-15", "--oneline"])["stdout_excerpt"].strip()
    rec.check(
        "baseline.source_commit_at_head",
        category="baseline",
        description="Repair source commit is the current local HEAD.",
        expected=SOURCE_COMMIT,
        observed=head,
        passed=head == SOURCE_COMMIT,
        source_finding_id=None,
        evidence_refs=["baseline.md"],
    )
    rec.check(
        "baseline.clean_before_check_outputs",
        category="baseline",
        description="Worktree was clean before this phase; current dirt is limited to allowed check outputs.",
        expected="only this check task/report output and queue index may be dirty",
        observed=status,
        passed=status_contains_only_allowed_check_outputs(status),
        source_finding_id=None,
        evidence_refs=["baseline.md"],
    )
    rec.check(
        "source_repair.nine_closed_pending_findings",
        category="source_repair",
        description="Repair task self-hosted finding matrix contains exactly the nine source findings closed pending independent check.",
        expected=MATERIAL_FINDING_IDS,
        observed=source_summary,
        passed=source_summary["exists"]
        and source_summary["closed_pending_count"] == 9
        and sorted(source_summary["ids"]) == sorted(MATERIAL_FINDING_IDS),
        source_finding_id=None,
        evidence_refs=["source-repair-review.md", "nine-finding-check-matrix.md"],
    )
    extension_review = run_extension_checks(rec, minimal, schema)
    digest_review = run_identity_checks(rec, manifest)
    component_review = run_component_checks(rec, minimal, manifest)
    artifact_review = run_artifact_checks(rec, minimal, manifest)
    preaccess_review = run_preaccess_checks(rec)
    checksum_review = run_checksum_checks(rec, manifest)
    protocol_review = run_protocol_checks(rec, minimal)
    contamination_review = run_contamination_checks(rec, minimal)
    fixture_review = run_fixture_checks(rec)
    q47_review = run_q47_mapping_checks(rec, manifest)
    sig_sbom_review = run_signature_sbom_checks(rec, manifest, minimal)
    noncap_review = run_no_overclaiming_checks(rec, manifest)
    result = "PASS_WITH_WARNINGS" if not rec.material_findings else "REQUEST_CHANGES"
    next_task = PASS_NEXT if result == "PASS_WITH_WARNINGS" else FAIL_NEXT
    write_status_files(result, next_task, len(rec.material_findings), 0)
    for name in REQUIRED_EVIDENCE:
        path = EVIDENCE_ROOT / name
        if not path.exists():
            write_text(path, f"# {name}\n\nPreliminary placeholder created before validation command receipts.\n")
    validation_commands = [
        ["git", "diff", "--check"],
        ["git", "diff", "--cached", "--check"],
        ["py", "-3", "-m", "json.tool", ".aide/protocol/aide-distribution-manifest-v1.schema.json"],
        ["py", "-3", "-m", "compileall", "core/protocol", ".aide/scripts/tests"],
        ["py", "-3", "-m", "unittest", "discover", "-s", ".aide/scripts/tests", "-p", "test_aide_distribution_manifest_v1.py"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "distribution-manifest", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "distribution-manifest", "project"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "distribution-manifest", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "install", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "install", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "repair", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "repair", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "upgrade", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "upgrade", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "upgrade", "compatibility"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "rollback", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "rollback", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "uninstall", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "uninstall", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "release", "validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "release", "status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "release", "draft-validate"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "release", "draft-status"],
        ["py", "-3", ".aide/scripts/aide_lite.py", "task", "inspect", "--task-id", SOURCE_TASK_ID],
        ["py", "-3", ".aide/scripts/aide_lite.py", "task", "evidence", "--task-id", SOURCE_TASK_ID],
        ["py", "-3", ".aide/scripts/aide_lite.py", "task", "inspect", "--task-id", TASK_ID],
        ["py", "-3", ".aide/scripts/aide_lite.py", "task", "evidence", "--task-id", TASK_ID],
        ["py", "-3", ".aide/scripts/aide_lite.py", "validate"],
    ]
    validation_results = [run_cmd(command, timeout=240) for command in validation_commands]
    failing_validation = [item for item in validation_results if item["result"] != "PASS"]
    if failing_validation:
        rec.check(
            "validation.command_matrix_passes",
            category="validation",
            description="Required validation command matrix passes.",
            expected="all commands pass",
            observed=failing_validation,
            passed=False,
            source_finding_id=None,
            evidence_refs=["validation-results.md"],
        )
        result = "REQUEST_CHANGES"
        next_task = FAIL_NEXT
        write_status_files(result, next_task, len(rec.material_findings), 0)
    validation_summary = {"commands": validation_commands, "results": validation_results, "failing": failing_validation}
    changed_files = changed_files_snapshot()
    path_scan_patterns = ["C:/Users", "C:\\Users", "C:/Downloads", "C:\\Downloads"]
    secret_scan_patterns = ["api_key", "secret_key", "password =", "bearer "]
    scan_paths = [EVIDENCE_ROOT, REPORT_ROOT]
    scan_hits = []
    for root in scan_paths:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml"}:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
                for pattern in path_scan_patterns + secret_scan_patterns:
                    if pattern.lower() in text:
                        scan_hits.append({"path": rel(path), "pattern": pattern})
    if scan_hits:
        rec.check(
            "leak_scan.no_local_paths_or_secrets",
            category="validation",
            description="Committed reports/evidence contain no local absolute paths or obvious secret-like strings.",
            expected="no scan hits",
            observed=scan_hits,
            passed=False,
            source_finding_id=None,
            evidence_refs=["validation-results.md"],
        )
        result = "REQUEST_CHANGES"
        next_task = FAIL_NEXT
        write_status_files(result, next_task, len(rec.material_findings), 0)
    report = {
        "schema_version": "aide.distribution-manifest-v1-repair-01-check.v0",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "source_capability": CAPABILITY,
        "result": result,
        "material_finding_count": len(rec.material_findings),
        "missing_evidence": 0,
        "recommended_next_task": next_task,
        "assertions": rec.assertions,
        "warnings": rec.warnings,
        "non_capabilities": {
            "implementation_repaired": False,
            "distribution_manifest_accepted": False,
            "project_lock_started": False,
            "install_apply_executed": False,
            "update_apply_executed": False,
            "repair_apply_executed": False,
            "rollback_apply_executed": False,
            "uninstall_apply_executed": False,
            "release_publication_performed": False,
            "target_repository_mutated": False,
            "branch_worktree_automation_performed": False,
            "network_calls_performed": False,
            "provider_or_model_calls_performed": False,
        },
    }
    write_json(REPORT_ROOT / "check-report.json", report)
    write_json(REPORT_ROOT / "digest-review.json", digest_review)
    write_json(REPORT_ROOT / "component-graph-review.json", component_review)
    write_json(REPORT_ROOT / "artifact-integrity-review.json", artifact_review)
    write_json(REPORT_ROOT / "checksum-review.json", checksum_review)
    write_json(REPORT_ROOT / "protocol-range-review.json", protocol_review)
    write_json(REPORT_ROOT / "contamination-review.json", contamination_review)
    write_json(REPORT_ROOT / "fixture-coverage-review.json", fixture_review)
    write_json(REPORT_ROOT / "material-findings.json", {"material_findings": rec.material_findings})
    write_text(REPORT_ROOT / "status.md", f"# Status\n\n- result: {result}\n- material_finding_count: {len(rec.material_findings)}\n- missing_evidence: 0\n- recommended_next_task: {next_task}\n")
    write_text(REPORT_ROOT / "next-task-prompt.md", f"# Next Task\n\nCreate and process `{next_task}`.\n")
    write_report_md(rec.assertions, rec.material_findings, result, next_task)
    write_evidence_md("baseline.md", "Baseline", {"git_status_before_outputs": status, "head": head, "origin_main": origin, "log": log})
    write_evidence_md("source-repair-review.md", "Source Repair Review", source_summary)
    write_evidence_md("nine-finding-check-matrix.md", "Nine Finding Check Matrix", {"source_findings": MATERIAL_FINDING_IDS, "assertions": [a for a in rec.assertions if a.get("source_finding_id") in MATERIAL_FINDING_IDS]})
    write_evidence_md("extension-boundary-review.md", "Extension Boundary Review", extension_review)
    write_evidence_md("identity-boundary-review.md", "Identity Boundary Review", digest_review)
    write_evidence_md("digest-recomputation.md", "Digest Recalculation", digest_review)
    write_evidence_md("component-graph-review.md", "Component Graph Review", component_review)
    write_evidence_md("artifact-integrity-review.md", "Artifact Integrity Review", artifact_review)
    write_evidence_md("preaccess-path-safety.md", "Pre-Access Path Safety", preaccess_review)
    write_evidence_md("checksum-value-review.md", "Checksum Value Review", checksum_review)
    write_evidence_md("protocol-range-review.md", "Protocol Range Review", protocol_review)
    write_evidence_md("contamination-review.md", "Contamination Review", contamination_review)
    write_evidence_md("fixture-coverage-review.md", "Fixture Coverage Review", fixture_review)
    write_evidence_md("q47-mapping-regression.md", "Q47 Mapping Regression", q47_review)
    write_evidence_md("no-overclaiming-review.md", "No Overclaiming Review", {"signature_sbom": sig_sbom_review, "non_capabilities": noncap_review})
    write_evidence_md("changed-files.md", "Changed Files", {"changed_files": changed_files})
    write_evidence_md("validation-commands.md", "Validation Commands", {"commands": validation_commands})
    write_evidence_md("validation-results.md", "Validation Results", validation_summary)
    write_evidence_md("validation.md", "Validation Summary", {"result": result, "failing_validation": failing_validation, "scan_hits": scan_hits})
    write_evidence_md("remaining-risks.md", "Remaining Risks", {"material_findings": rec.material_findings, "warnings": rec.warnings})
    write_text(EVIDENCE_ROOT / "next-task-prompt.md", f"# Next Task\n\nCreate and process `{next_task}`.\n")
    # Rewrite status after all assertions and leak/validation checks have been recorded.
    write_status_files(result, next_task, len(rec.material_findings), 0)
    return 0 if result in {"PASS", "PASS_WITH_WARNINGS", "REQUEST_CHANGES"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
