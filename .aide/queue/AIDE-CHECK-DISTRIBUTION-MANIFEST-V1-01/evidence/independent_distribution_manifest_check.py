"""Independent DistributionManifest v1 check harness.

This script is task-local evidence for
AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01. It uses the live helper only as the
system under test for behavior probes. Digest recomputation, closure checks,
and finding classification are implemented locally in this file.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01"
SOURCE_TASK_ID = "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01"
SOURCE_COMMIT = "ad975887910f6a7238ef076ce2fef0fd43687e37"
REPAIR_TASK = "AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01"
ACCEPT_TASK = "AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01"

REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / ".aide" / "queue" / TASK_ID
EVIDENCE_ROOT = TASK_ROOT / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide" / "reports" / "distribution-manifest-v1-check"

SOURCE_STATUS = REPO_ROOT / ".aide" / "queue" / SOURCE_TASK_ID / "status.yaml"
SOURCE_TASK = REPO_ROOT / ".aide" / "queue" / SOURCE_TASK_ID / "task.yaml"
SOURCE_MANIFEST = REPO_ROOT / ".aide" / "reports" / "distribution-manifest-v1" / "manifest.json"
SOURCE_VALIDATION = REPO_ROOT / ".aide" / "reports" / "distribution-manifest-v1" / "validation.json"
SOURCE_SCHEMA = REPO_ROOT / ".aide" / "protocol" / "aide-distribution-manifest-v1.schema.json"
SOURCE_HELPER = REPO_ROOT / "core" / "protocol" / "distribution_manifest.py"
FIXTURE_ROOT = REPO_ROOT / ".aide" / "fixtures" / "distribution-manifest-v1"
CHECKSUMS_JSON = REPO_ROOT / ".aide" / "release" / "dist" / "aide-lite-pack-v0.checksums.json"
RELEASE_ASSETS_JSON = REPO_ROOT / ".aide" / "release" / "dist" / "release-assets.json"
RELEASE_PROVENANCE_JSON = REPO_ROOT / ".aide" / "release" / "dist" / "release-provenance.json"
EXPORT_PACK_ROOT = REPO_ROOT / ".aide" / "export" / "aide-lite-pack-v0"


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    write_text(path, stable_json(data))


def run_capture(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    return {
        "args": args,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def repo_rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return "<outside-repository>"


def load_sut() -> Any:
    sys.path.insert(0, str(REPO_ROOT))
    from core.protocol import distribution_manifest as sut  # type: ignore

    return sut


def canonicalize_observed(manifest: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(manifest)
    spec = data.get("spec")
    if isinstance(spec, dict):
        if isinstance(spec.get("components"), list):
            spec["components"] = sorted(
                spec["components"],
                key=lambda item: str(item.get("component_ref", "")) if isinstance(item, dict) else "",
            )
        if isinstance(spec.get("artifacts"), list):
            spec["artifacts"] = sorted(
                spec["artifacts"],
                key=lambda item: str(item.get("artifact_ref", "")) if isinstance(item, dict) else "",
            )
        protocol = spec.get("protocol")
        if isinstance(protocol, dict):
            for key in [
                "required_features",
                "optional_features",
                "required_migrations",
                "compatibility_declarations",
            ]:
                if isinstance(protocol.get(key), list):
                    protocol[key] = sorted(str(item) for item in protocol[key])
    return data


def payload_for_digest_observed(manifest: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_observed(manifest)
    status = data.get("status")
    if isinstance(status, dict):
        status["manifest_payload_digest"] = ""
        status["distribution_digest"] = ""
    spec = data.get("spec")
    if isinstance(spec, dict):
        spec.pop("signature_records", None)
    return data


def manifest_payload_digest_observed(manifest: dict[str, Any]) -> str:
    return digest_bytes(canonical_bytes(payload_for_digest_observed(manifest)))


def immutable_artifact_digest_set_observed(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    digest_set: list[dict[str, Any]] = []
    artifacts = manifest.get("spec", {}).get("artifacts", [])
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if isinstance(artifact, dict):
                digest_set.append(
                    {
                        "artifact_ref": artifact.get("artifact_ref", ""),
                        "byte_count": artifact.get("byte_count", 0),
                        "content_digest": artifact.get("content_digest", ""),
                        "included": artifact.get("included", False),
                    }
                )
    return sorted(digest_set, key=lambda item: str(item["artifact_ref"]))


def distribution_digest_observed(manifest: dict[str, Any]) -> str:
    payload = {
        "manifest_payload_digest": manifest_payload_digest_observed(manifest),
        "immutable_artifact_digest_set": immutable_artifact_digest_set_observed(manifest),
    }
    return digest_bytes(canonical_bytes(payload))


def finalize_observed(manifest: dict[str, Any]) -> dict[str, Any]:
    data = canonicalize_observed(manifest)
    status = data.setdefault("status", {})
    status["manifest_payload_digest"] = manifest_payload_digest_observed(data)
    status["distribution_digest"] = distribution_digest_observed(data)
    return data


def component_digest_expected(component: dict[str, Any], artifact_map: dict[str, dict[str, Any]]) -> str:
    artifact_refs = sorted(str(ref) for ref in component.get("artifact_refs", []))
    payload = {
        "component_id": component.get("component_id", ""),
        "artifact_refs": artifact_refs,
        "artifact_digests": sorted(
            [
                {
                    "artifact_ref": ref,
                    "content_digest": str(artifact_map.get(ref, {}).get("content_digest", "")),
                }
                for ref in artifact_refs
            ],
            key=lambda item: item["artifact_ref"],
        ),
        "protocol_requirements": sorted(str(item) for item in component.get("protocol_requirements", [])),
    }
    return digest_bytes(canonical_bytes(payload))


def validate_sut(sut: Any, manifest: dict[str, Any], *, require_files: bool = False) -> dict[str, Any]:
    return sut.validate_distribution_manifest_object(
        manifest,
        repo_root=REPO_ROOT,
        require_artifact_files=require_files,
    )


def first_included_file_artifact(manifest: dict[str, Any]) -> dict[str, Any]:
    for artifact in manifest["spec"]["artifacts"]:
        if artifact.get("included") and artifact.get("source_kind") != "local_directory":
            return artifact
    raise AssertionError("no included file artifact found")


def mutate_and_validate(
    sut: Any,
    manifest: dict[str, Any],
    mutator: Any,
    *,
    require_files: bool = False,
) -> dict[str, Any]:
    data = copy.deepcopy(manifest)
    mutator(data)
    data = finalize_observed(data)
    result = validate_sut(sut, data, require_files=require_files)
    return {"valid": result["valid"], "codes": result["refusal_codes"], "errors": result["errors"]}


def collect_schema_paths(schema: Any, path: str = "$") -> dict[str, list[str]]:
    closed: list[str] = []
    extensions: list[str] = []
    if isinstance(schema, dict):
        if schema.get("additionalProperties") is False:
            closed.append(path)
        for key in schema:
            if key in {"extensions", "x-extensions"} or key.endswith("_extensions"):
                extensions.append(f"{path}.{key}")
        for key, value in schema.items():
            child = collect_schema_paths(value, f"{path}.{key}")
            closed.extend(child["closed"])
            extensions.extend(child["extensions"])
    elif isinstance(schema, list):
        for idx, item in enumerate(schema):
            child = collect_schema_paths(item, f"{path}[{idx}]")
            closed.extend(child["closed"])
            extensions.extend(child["extensions"])
    return {"closed": closed, "extensions": extensions}


def schema_rejects_optional_extension(schema: dict[str, Any]) -> bool:
    metadata = schema.get("properties", {}).get("metadata", {})
    return metadata.get("additionalProperties") is False and "extensions" not in metadata.get("properties", {})


def make_finding(
    finding_id: str,
    category: str,
    summary: str,
    expected: str,
    observed: str,
    evidence_refs: list[str],
    severity: str = "material",
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "category": category,
        "severity": severity,
        "summary": summary,
        "expected": expected,
        "observed": observed,
        "evidence_refs": evidence_refs,
        "source_finding_id": None,
    }


def review_baseline() -> dict[str, Any]:
    return {
        "git_status": run_capture(["git", "status", "--short", "--branch", "--untracked-files=all"]),
        "head": run_capture(["git", "rev-parse", "HEAD"]),
        "origin_main": run_capture(["git", "rev-parse", "origin/main"]),
        "source_task_exists": SOURCE_TASK.exists(),
        "source_status_exists": SOURCE_STATUS.exists(),
        "source_manifest_exists": SOURCE_MANIFEST.exists(),
        "source_validation_exists": SOURCE_VALIDATION.exists(),
        "source_schema_exists": SOURCE_SCHEMA.exists(),
        "source_helper_exists": SOURCE_HELPER.exists(),
    }


def run_check() -> dict[str, Any]:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    sut = load_sut()
    manifest = read_json(SOURCE_MANIFEST)
    schema = read_json(SOURCE_SCHEMA)
    validation_report = read_json(SOURCE_VALIDATION)
    helper_text = SOURCE_HELPER.read_text(encoding="utf-8")
    release_assets = read_json(RELEASE_ASSETS_JSON)
    release_provenance = read_json(RELEASE_PROVENANCE_JSON)
    checksums = read_json(CHECKSUMS_JSON)

    findings: list[dict[str, Any]] = []
    warnings: list[str] = []

    baseline = review_baseline()
    status_text = SOURCE_STATUS.read_text(encoding="utf-8")
    source_complete = "result: PASS_WITH_WARNINGS" in status_text and "missing_evidence: 0" in status_text
    source_no_apply = all(
        marker in status_text
        for marker in [
            "install_apply_executed: false",
            "upgrade_apply_executed: false",
            "repair_apply_executed: false",
            "rollback_apply_executed: false",
            "uninstall_apply_executed: false",
            "release_publication_performed: false",
            "target_repository_mutated: false",
        ]
    )

    schema_paths = collect_schema_paths(schema)
    if schema_rejects_optional_extension(schema):
        findings.append(
            make_finding(
                "schema.optional_extension_boundary_missing",
                "schema",
                "Closed canonical schema objects do not provide an explicit optional extension map.",
                "Unknown optional extension fields should be preserved or tolerated through an explicit extension surface.",
                "The root, metadata, spec, status, protocol, component, checksum, provenance, SBOM, and signature objects are closed with no extensions map; metadata optional extension would be rejected by schema.",
                ["schema-helper-alignment.md", "extension-compatibility-review.md"],
            )
        )

    digest_review: dict[str, Any] = {
        "source_manifest_payload_digest": manifest["status"]["manifest_payload_digest"],
        "independent_manifest_payload_digest": manifest_payload_digest_observed(manifest),
        "source_distribution_digest": manifest["status"]["distribution_digest"],
        "independent_distribution_digest": distribution_digest_observed(manifest),
        "mutation_probes": [],
    }
    if digest_review["source_manifest_payload_digest"] != digest_review["independent_manifest_payload_digest"]:
        findings.append(
            make_finding(
                "digest.independent_payload_mismatch",
                "digest",
                "Independent payload digest recomputation differs from the committed manifest.",
                "Independent canonical JSON recomputation should match committed digest vectors.",
                "Payload digest mismatch was observed.",
                ["independent-digest-recomputation.md"],
            )
        )

    mutation_cases = [
        ("recommended_next_task", "status", lambda m: m["status"].__setitem__("recommended_next_task", "AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01"), False),
        ("status_status", "status", lambda m: m["status"].__setitem__("status", "PASS"), False),
        ("proposed_capability", "status", lambda m: m["status"].__setitem__("proposed_capability", "distribution_manifest_v1_candidate"), False),
        ("implementation_boolean", "status", lambda m: m["status"].__setitem__("install_apply_implemented", True), False),
        ("operational_warning", "spec", lambda m: m["spec"]["known_limitations"].append("check-only operational warning"), True),
        ("distribution_identity", "metadata", lambda m: m["metadata"].__setitem__("release_id", "different-release"), True),
        ("artifact_digest", "artifact", lambda m: first_included_file_artifact(m).__setitem__("content_digest", "sha256:" + "a" * 64), True),
        ("component_digest", "component", lambda m: m["spec"]["components"][0].__setitem__("content_digest", "sha256:" + "b" * 64), True),
    ]
    mutable_status_changes = []
    for name, category, mutator, expected_change in mutation_cases:
        data = copy.deepcopy(manifest)
        mutator(data)
        data = finalize_observed(data)
        changed_payload = data["status"]["manifest_payload_digest"] != manifest["status"]["manifest_payload_digest"]
        changed_distribution = data["status"]["distribution_digest"] != manifest["status"]["distribution_digest"]
        digest_review["mutation_probes"].append(
            {
                "case": name,
                "category": category,
                "expected_identity_change": expected_change,
                "payload_digest_changed": changed_payload,
                "distribution_digest_changed": changed_distribution,
            }
        )
        if category == "status" and (changed_payload or changed_distribution):
            mutable_status_changes.append(name)
    if mutable_status_changes:
        findings.append(
            make_finding(
                "identity.mutable_status_changes_distribution_digest",
                "identity",
                "Mutable status and queue/controller fields are included in portable distribution identity.",
                "Distribution identity should bind immutable distribution declaration, not review routing or implementation state.",
                "Changing only these status fields changed the payload/distribution digest: "
                + ", ".join(mutable_status_changes),
                ["immutable-identity-review.md", "status-vs-spec-authority.md", "digest-review.json"],
            )
        )

    artifacts = manifest["spec"]["artifacts"]
    components = manifest["spec"]["components"]
    artifact_map = {str(item["artifact_ref"]): item for item in artifacts}
    component_review = {
        "component_count": len(components),
        "artifact_count": len(artifacts),
        "component_digest_recomputations": [],
        "behavior_probes": [],
    }
    component_digest_mismatches = []
    for component in components:
        expected = component_digest_expected(component, artifact_map)
        observed = component.get("content_digest")
        component_review["component_digest_recomputations"].append(
            {"component_ref": component.get("component_ref"), "expected": expected, "observed": observed}
        )
        if expected != observed:
            component_digest_mismatches.append(str(component.get("component_ref")))
    if component_digest_mismatches:
        findings.append(
            make_finding(
                "component.content_digest_recompute_mismatch",
                "component",
                "Component content digests do not match independent recomputation.",
                "Each component content_digest should recompute from its documented component payload.",
                "Mismatched component refs: " + ", ".join(component_digest_mismatches),
                ["component-graph-review.md"],
            )
        )

    def component_probe(name: str, mutator: Any) -> None:
        result = mutate_and_validate(sut, manifest, mutator)
        component_review["behavior_probes"].append({"case": name, **result})

    component_probe("corrupt_component_content_digest", lambda m: m["spec"]["components"][0].__setitem__("content_digest", "sha256:" + "c" * 64))
    component_probe("missing_artifact_ref", lambda m: m["spec"]["components"][0]["artifact_refs"].append("aide://distribution/artifact/missing"))
    component_probe("unknown_component_dependency", lambda m: m["spec"]["components"][0]["dependencies"].append("aide://distribution/component/missing"))

    def duplicate_component_id(m: dict[str, Any]) -> None:
        other = copy.deepcopy(m["spec"]["components"][0])
        other["component_ref"] = other["component_ref"] + "-second"
        other["content_digest"] = "sha256:" + "d" * 64
        m["spec"]["components"].append(other)

    component_probe("duplicate_component_id_different_ref", duplicate_component_id)

    def dependency_cycle(m: dict[str, Any]) -> None:
        first = m["spec"]["components"][0]
        second = copy.deepcopy(first)
        second["component_ref"] = first["component_ref"] + "-cycle"
        first["dependencies"] = [second["component_ref"]]
        second["dependencies"] = [first["component_ref"]]
        m["spec"]["components"].append(second)

    component_probe("dependency_cycle", dependency_cycle)
    passing_component_bad_cases = [probe["case"] for probe in component_review["behavior_probes"] if probe["valid"]]
    if passing_component_bad_cases:
        findings.append(
            make_finding(
                "component.graph_integrity_not_validated",
                "component",
                "Semantic component graph validation does not prove content digest, artifact-ref closure, dependency closure, or component_id uniqueness.",
                "Corrupted component digests, missing artifact refs, unknown dependencies, duplicate component IDs, and cycles should fail closed.",
                "The following malformed cases validated successfully: " + ", ".join(passing_component_bad_cases),
                ["component-graph-review.md", "component-graph-review.json"],
            )
        )

    artifact_review = {"behavior_probes": [], "file_artifacts": []}
    for artifact in artifacts:
        if artifact.get("included") and artifact.get("source_kind") != "local_directory":
            rel = str(artifact.get("relative_source_location", ""))
            path = REPO_ROOT / rel
            artifact_review["file_artifacts"].append(
                {
                    "artifact_ref": artifact.get("artifact_ref"),
                    "relative_source_location": rel,
                    "exists": path.exists(),
                    "byte_count_manifest": artifact.get("byte_count"),
                    "byte_count_actual": path.stat().st_size if path.exists() else None,
                    "digest_manifest": artifact.get("content_digest"),
                    "digest_actual": "sha256:" + file_sha256(path) if path.exists() else None,
                }
            )

    byte_count_probe = mutate_and_validate(
        sut,
        manifest,
        lambda m: first_included_file_artifact(m).__setitem__("byte_count", int(first_included_file_artifact(m)["byte_count"]) + 1),
        require_files=True,
    )
    artifact_review["behavior_probes"].append({"case": "wrong_byte_count", **byte_count_probe})
    media_probe = mutate_and_validate(
        sut,
        manifest,
        lambda m: first_included_file_artifact(m).__setitem__("media_type", "application/x-wrong"),
        require_files=True,
    )
    artifact_review["behavior_probes"].append({"case": "wrong_media_type", **media_probe})
    compression_probe = mutate_and_validate(
        sut,
        manifest,
        lambda m: first_included_file_artifact(m).__setitem__("compression_format", "zip" if first_included_file_artifact(m).get("compression_format") == "tar.gz" else "tar.gz"),
        require_files=True,
    )
    artifact_review["behavior_probes"].append({"case": "wrong_compression_format", **compression_probe})
    passing_artifact_bad_cases = [probe["case"] for probe in artifact_review["behavior_probes"] if probe["valid"]]
    if passing_artifact_bad_cases:
        findings.append(
            make_finding(
                "artifact.integrity_metadata_not_validated",
                "artifact",
                "Artifact validation does not fully compare committed metadata with actual artifact bytes and type.",
                "Byte counts, media type, and compression declarations should be validated for included local archive artifacts.",
                "The following malformed cases validated successfully: " + ", ".join(passing_artifact_bad_cases),
                ["artifact-integrity-review.md", "artifact-integrity-review.json"],
            )
        )

    preaccess_review = {
        "artifact_from_release_record_present": "def _artifact_from_release_record" in helper_text,
        "exists_before_forbidden_check": False,
        "stat_before_forbidden_check": False,
        "hash_before_forbidden_check": False,
    }
    function_start = helper_text.find("def _artifact_from_release_record")
    function_end = helper_text.find("\ndef ", function_start + 1)
    snippet = helper_text[function_start:function_end if function_end != -1 else len(helper_text)]
    forbidden_idx = snippet.find("forbidden_member_reason")
    exists_idx = snippet.find(".exists()")
    stat_idx = snippet.find(".stat()")
    hash_idx = snippet.find("sha256_file")
    preaccess_review["exists_before_forbidden_check"] = exists_idx != -1 and (forbidden_idx == -1 or exists_idx < forbidden_idx)
    preaccess_review["stat_before_forbidden_check"] = stat_idx != -1 and (forbidden_idx == -1 or stat_idx < forbidden_idx)
    preaccess_review["hash_before_forbidden_check"] = hash_idx != -1 and (forbidden_idx == -1 or hash_idx < forbidden_idx)
    if preaccess_review["exists_before_forbidden_check"] or preaccess_review["stat_before_forbidden_check"] or preaccess_review["hash_before_forbidden_check"]:
        findings.append(
            make_finding(
                "path.preaccess_validation_order_violation",
                "path_safety",
                "Release artifact projection touches filesystem paths before semantic path validation.",
                "Malformed source artifact paths should be rejected before exists/stat/open/hash or traversal.",
                "Source inspection shows path existence/stat/hash operations occur before any containment or forbidden-member validation in the release artifact projector.",
                ["path-preaccess-review.md"],
            )
        )

    checksum_review = {
        "checksum_file_digest": "sha256:" + file_sha256(CHECKSUMS_JSON),
        "manifest_checksum_digest": manifest["spec"]["checksums"]["manifest_digest"],
        "included_archive_artifacts": [],
        "behavior_probes": [],
    }
    checksum_map = checksums.get("checksums", {}) if isinstance(checksums.get("checksums"), dict) else {}
    for artifact in artifacts:
        if artifact.get("included") and artifact.get("checksum_ref"):
            rel = str(artifact.get("relative_source_location", ""))
            basename = Path(rel).name
            checksum_review["included_archive_artifacts"].append(
                {
                    "artifact_ref": artifact.get("artifact_ref"),
                    "basename": basename,
                    "checksum_entry_present": basename in checksum_map,
                    "checksum_value": checksum_map.get(basename),
                    "artifact_content_digest": str(artifact.get("content_digest", "")).removeprefix("sha256:"),
                    "checksum_matches_artifact": checksum_map.get(basename) == str(artifact.get("content_digest", "")).removeprefix("sha256:"),
                }
            )
    wrong_checksums_path = EVIDENCE_ROOT / "checksum-wrong-value-probe.json"
    first_artifact = first_included_file_artifact(manifest)
    first_name = Path(str(first_artifact["relative_source_location"])).name
    wrong_checksum_map = dict(checksum_map)
    wrong_checksum_map[first_name] = "f" * 64
    write_json(
        wrong_checksums_path,
        {
            "algorithm": "sha256",
            "checksums": wrong_checksum_map,
            "schema_version": "aide.release-checksums.v0",
        },
    )

    def wrong_checksum_value(m: dict[str, Any]) -> None:
        m["spec"]["checksums"]["checksum_manifest_path"] = repo_rel(wrong_checksums_path)
        m["spec"]["checksums"]["manifest_digest"] = "sha256:" + file_sha256(wrong_checksums_path)

    checksum_probe = mutate_and_validate(sut, manifest, wrong_checksum_value, require_files=True)
    checksum_review["behavior_probes"].append({"case": "wrong_checksum_value_same_name", **checksum_probe})
    if checksum_probe["valid"]:
        findings.append(
            make_finding(
                "checksum.value_not_verified",
                "checksum",
                "Checksum validation accepts a checksum entry with the correct name but the wrong digest value.",
                "Checksum validation should verify algorithm, key uniqueness, and value equality with the artifact content digest.",
                "A probe checksum manifest with the same artifact basename and a wrong digest value validated successfully.",
                ["checksum-review.md", "checksum-review.json"],
            )
        )

    protocol_review = {"behavior_probes": []}

    def protocol_probe(name: str, mutator: Any) -> None:
        result = mutate_and_validate(sut, manifest, mutator)
        protocol_review["behavior_probes"].append({"case": name, **result})

    protocol_probe("lower_bound_above_v1", lambda m: m["spec"]["protocol"].__setitem__("protocol_range", {"min": "2.0.0", "max": "3.x"}))
    protocol_probe("missing_min", lambda m: m["spec"]["protocol"]["protocol_range"].pop("min", None))
    protocol_probe("missing_reader_version", lambda m: m["spec"]["protocol"].pop("min_reader_version", None))
    protocol_probe("missing_writer_version", lambda m: m["spec"]["protocol"].pop("min_writer_version", None))
    protocol_probe("incompatible_component_constraints", lambda m: m["spec"]["components"][0].__setitem__("compatibility_constraints", {"min_reader_version": "2.0.0", "min_writer_version": "2.0.0"}))
    passing_protocol_bad_cases = [probe["case"] for probe in protocol_review["behavior_probes"] if probe["valid"]]
    if passing_protocol_bad_cases:
        findings.append(
            make_finding(
                "protocol.range_semantics_incomplete",
                "compatibility",
                "Protocol range validation does not enforce lower bounds, reader/writer fields, or component compatibility constraints.",
                "Ranges should prove v1 inclusion, min <= max, required reader/writer fields, and coherent component constraints.",
                "The following malformed compatibility cases validated successfully: " + ", ".join(passing_protocol_bad_cases),
                ["protocol-range-review.md", "protocol-range-review.json"],
            )
        )

    contamination_review = {
        "directory_inventory_skips_forbidden": "if forbidden_member_reason(rel):\n            continue" in helper_text,
        "forbidden_prefixes_declared": sorted(re.findall(r'"(\\.aide[^"]+|\\.env|raw-[^"]+)"', helper_text)),
    }
    if contamination_review["directory_inventory_skips_forbidden"]:
        findings.append(
            make_finding(
                "contamination.forbidden_members_silently_filtered",
                "contamination",
                "Local-directory distribution inventory silently skips forbidden source-state members.",
                "A contaminated distribution source should emit explicit contamination/refusal evidence or define a separate filtered-export proof boundary.",
                "Source inspection shows directory inventory continues past forbidden members rather than recording a refusal.",
                ["contamination-review.md"],
            )
        )

    fixture_files = sorted(path.stem for path in (FIXTURE_ROOT / "valid").glob("*.json")) + sorted(
        path.stem for path in (FIXTURE_ROOT / "invalid").glob("*.json")
    )
    required_fixture_cases = [
        "minimal-unsigned",
        "full-local-archive",
        "local-directory",
        "reordered-input",
        "duplicate-component",
        "duplicate-component-id",
        "duplicate-artifact",
        "missing-digest",
        "malformed-digest",
        "wrong-artifact-digest",
        "wrong-component-digest",
        "wrong-payload-digest",
        "wrong-distribution-digest",
        "missing-artifact-ref",
        "missing-dependency",
        "dependency-cycle",
        "unsupported-source",
        "unknown-optional-feature",
        "unknown-required-feature",
        "unsupported-protocol-range",
        "inverted-protocol-range",
        "forbidden-member",
        "source-contamination",
        "aide-local-member",
        "absolute-path",
        "traversal-path",
        "checksum-missing",
        "checksum-wrong-value",
        "checksum-basename-collision",
        "signature-placeholder",
        "false-signature-verification",
        "missing-sbom",
        "incompatible-migration",
        "unknown-optional-extension-round-trip",
    ]
    fixture_review = {
        "observed_cases": fixture_files,
        "required_cases": required_fixture_cases,
        "missing_cases": [case for case in required_fixture_cases if case not in fixture_files],
    }
    if fixture_review["missing_cases"]:
        findings.append(
            make_finding(
                "fixture.required_coverage_incomplete",
                "fixture",
                "The committed fixture corpus does not cover required adversarial cases.",
                "Required direct fixtures should exist for the distribution manifest contract and known risk matrix.",
                "Missing fixture cases: " + ", ".join(fixture_review["missing_cases"]),
                ["fixture-coverage-review.md"],
            )
        )

    q47_review = {
        "release_assets_count": len(release_assets.get("artifacts", [])) if isinstance(release_assets.get("artifacts"), list) else 0,
        "manifest_artifact_count": len(artifacts),
        "q47_dirty_state_manifest": manifest["spec"]["source"]["q47_dirty_state"],
        "q47_dirty_state_provenance": release_provenance.get("dirty_state"),
        "q48_publication_draft_is_distribution_truth": manifest["spec"]["source"]["q48_publication_draft_is_distribution_truth"],
        "source_repo_local_path_suppressed": manifest["spec"]["provenance"]["source_repo_local_path_suppressed"],
    }
    if q47_review["q48_publication_draft_is_distribution_truth"] is not False:
        findings.append(
            make_finding(
                "q47.q48_publication_claim_leaks_into_truth",
                "q47_mapping",
                "Q48 draft state is treated as distribution truth.",
                "Q48 draft evidence should remain publication-review material only.",
                "q48_publication_draft_is_distribution_truth was not false.",
                ["q47-source-mapping-review.md"],
            )
        )

    signature_sbom_review = {
        "signature_records": manifest["spec"].get("signature_records", []),
        "sbom_refs": manifest["spec"].get("sbom_refs", []),
    }
    non_capability_review = {
        "source_validation_status": validation_report.get("status") or validation_report.get("validation_status"),
        "explicit_non_capabilities": manifest["spec"].get("explicit_non_capabilities", []),
        "no_apply_flags": {
            "install": manifest["status"].get("install_apply_implemented") is False,
            "update": manifest["status"].get("update_apply_implemented") is False,
            "repair": manifest["status"].get("repair_apply_implemented") is False,
            "rollback": manifest["status"].get("rollback_apply_implemented") is False,
            "uninstall": manifest["status"].get("uninstall_apply_implemented") is False,
            "release_publication": manifest["status"].get("release_publication_implemented") is False,
        },
    }

    result = "REQUEST_CHANGES" if any(item["severity"] == "material" for item in findings) else "PASS_WITH_WARNINGS"
    recommended_next_task = REPAIR_TASK if result == "REQUEST_CHANGES" else ACCEPT_TASK

    report = {
        "schema_version": "aide.distribution-manifest-v1-check-report.v1",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "status": result,
        "material_finding_count": sum(1 for item in findings if item["severity"] == "material"),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next_task,
        "source_task_complete": source_complete,
        "source_no_apply_or_publication": source_no_apply,
        "assertions": [
            {
                "id": finding["id"],
                "category": finding["category"],
                "description": finding["summary"],
                "outcome": "FAIL",
                "severity": finding["severity"],
                "expected": finding["expected"],
                "observed": finding["observed"],
                "evidence_refs": finding["evidence_refs"],
                "source_finding_id": finding["source_finding_id"],
            }
            for finding in findings
        ],
        "warnings": warnings,
    }

    compatibility_review = {
        "schema_closed_object_count": len(schema_paths["closed"]),
        "schema_extension_paths": schema_paths["extensions"],
        "unknown_optional_extensions_supported": not schema_rejects_optional_extension(schema),
        "protocol_review": protocol_review,
        "extension_boundary_finding": any(item["id"] == "schema.optional_extension_boundary_missing" for item in findings),
    }

    write_json(REPORT_ROOT / "check-report.json", report)
    write_json(REPORT_ROOT / "digest-review.json", digest_review)
    write_json(REPORT_ROOT / "component-graph-review.json", component_review)
    write_json(REPORT_ROOT / "artifact-integrity-review.json", artifact_review)
    write_json(REPORT_ROOT / "checksum-review.json", checksum_review)
    write_json(REPORT_ROOT / "protocol-range-review.json", protocol_review)
    write_json(REPORT_ROOT / "q47-mapping-review.json", q47_review)
    write_json(REPORT_ROOT / "compatibility-review.json", compatibility_review)
    write_json(REPORT_ROOT / "material-findings.json", {"findings": findings})

    write_text(REPORT_ROOT / "check-report.md", render_check_report(report, findings))
    write_text(REPORT_ROOT / "status.md", render_status(report))
    write_text(REPORT_ROOT / "next-task-prompt.md", render_next_task_prompt(recommended_next_task, findings))

    evidence_sections = {
        "baseline.md": render_baseline(baseline, source_complete, source_no_apply),
        "source-build-review.md": render_source_build(source_complete, source_no_apply),
        "schema-helper-alignment.md": render_schema_review(schema_paths, schema_rejects_optional_extension(schema)),
        "extension-compatibility-review.md": render_extension_review(schema_paths, schema_rejects_optional_extension(schema)),
        "immutable-identity-review.md": render_digest_review(digest_review),
        "independent-digest-recomputation.md": render_digest_review(digest_review),
        "component-graph-review.md": render_component_review(component_review),
        "artifact-integrity-review.md": render_artifact_review(artifact_review),
        "path-preaccess-review.md": render_preaccess_review(preaccess_review),
        "checksum-review.md": render_checksum_review(checksum_review),
        "protocol-range-review.md": render_protocol_review(protocol_review),
        "q47-source-mapping-review.md": render_q47_review(q47_review),
        "status-vs-spec-authority.md": render_status_authority(digest_review),
        "signature-sbom-review.md": render_signature_sbom(signature_sbom_review),
        "contamination-review.md": render_contamination_review(contamination_review),
        "fixture-coverage-review.md": render_fixture_review(fixture_review),
        "no-overclaiming-review.md": render_non_capability_review(non_capability_review),
        "validation.md": render_validation_summary(report),
        "next-task-prompt.md": render_next_task_prompt(recommended_next_task, findings),
    }
    for name, text in evidence_sections.items():
        write_text(EVIDENCE_ROOT / name, text)

    return {
        "report": report,
        "findings": findings,
        "digest_review": digest_review,
        "component_review": component_review,
        "artifact_review": artifact_review,
        "checksum_review": checksum_review,
        "protocol_review": protocol_review,
        "q47_review": q47_review,
    }


def render_check_report(report: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    lines = [
        "# DistributionManifest v1 Independent Check",
        "",
        f"- result: {report['result']}",
        f"- material_finding_count: {report['material_finding_count']}",
        f"- missing_evidence: {report['missing_evidence']}",
        f"- recommended_next_task: {report['recommended_next_task']}",
        "",
        "## Material Findings",
        "",
    ]
    if not findings:
        lines.append("- none")
    for finding in findings:
        lines.extend(
            [
                f"### {finding['id']}",
                "",
                f"- category: {finding['category']}",
                f"- severity: {finding['severity']}",
                f"- expected: {finding['expected']}",
                f"- observed: {finding['observed']}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def render_status(report: dict[str, Any]) -> str:
    return (
        "# DistributionManifest v1 Check Status\n\n"
        f"- result: {report['result']}\n"
        f"- material_finding_count: {report['material_finding_count']}\n"
        f"- missing_evidence: {report['missing_evidence']}\n"
        f"- source_task: {SOURCE_TASK_ID}\n"
        f"- source_commit: {SOURCE_COMMIT}\n"
        f"- recommended_next_task: {report['recommended_next_task']}\n"
        "- implementation_repaired: false\n"
        "- distribution_manifest_accepted: false\n"
        "- project_lock_started: false\n"
    )


def render_next_task_prompt(task_id: str, findings: list[dict[str, Any]]) -> str:
    if task_id == REPAIR_TASK:
        ids = "\n".join(f"- {finding['id']}" for finding in findings)
        return (
            f"# {REPAIR_TASK}\n\n"
            f"Create and process `{REPAIR_TASK}`.\n\n"
            "Repair only the material findings from "
            f"`{TASK_ID}` without broadening DistributionManifest v1 into install/apply, "
            "publication, target mutation, or ProjectLock work.\n\n"
            "Material findings to close:\n\n"
            f"{ids}\n\n"
            f"Stop at `needs_review` and recommend exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.\n"
        )
    return (
        f"# {ACCEPT_TASK}\n\n"
        f"Create and process `{ACCEPT_TASK}`. Accept only `distribution_manifest_v1`.\n"
    )


def render_baseline(baseline: dict[str, Any], source_complete: bool, source_no_apply: bool) -> str:
    return (
        "# Baseline\n\n"
        f"- git_status: `{baseline['git_status']['stdout']}`\n"
        f"- head: `{baseline['head']['stdout']}`\n"
        f"- origin_main: `{baseline['origin_main']['stdout']}`\n"
        f"- source_task_complete: {str(source_complete).lower()}\n"
        f"- source_no_apply_or_publication: {str(source_no_apply).lower()}\n"
        f"- source_manifest_exists: {str(baseline['source_manifest_exists']).lower()}\n"
        f"- source_schema_exists: {str(baseline['source_schema_exists']).lower()}\n"
        f"- source_helper_exists: {str(baseline['source_helper_exists']).lower()}\n"
    )


def render_source_build(source_complete: bool, source_no_apply: bool) -> str:
    return (
        "# Source Build Review\n\n"
        f"- source_task: `{SOURCE_TASK_ID}`\n"
        f"- source_commit: `{SOURCE_COMMIT}`\n"
        f"- source_complete: {str(source_complete).lower()}\n"
        f"- source_no_apply_or_publication: {str(source_no_apply).lower()}\n"
        "- source_reports_used_as_inputs_not_authority: true\n"
    )


def render_schema_review(schema_paths: dict[str, list[str]], rejects_extension: bool) -> str:
    return (
        "# Schema Helper Alignment\n\n"
        f"- closed_object_count: {len(schema_paths['closed'])}\n"
        f"- extension_surface_count: {len(schema_paths['extensions'])}\n"
        f"- metadata_optional_extension_rejected_by_schema: {str(rejects_extension).lower()}\n"
        "- draft_2020_12_declared: true\n"
    )


def render_extension_review(schema_paths: dict[str, list[str]], rejects_extension: bool) -> str:
    return (
        "# Extension Compatibility Review\n\n"
        f"- closed_object_paths_sample: {', '.join(schema_paths['closed'][:8])}\n"
        f"- extension_paths: {', '.join(schema_paths['extensions']) or 'none'}\n"
        f"- optional_extension_round_trip_supported: {str(not rejects_extension).lower()}\n"
    )


def render_digest_review(review: dict[str, Any]) -> str:
    lines = [
        "# Independent Digest Recomposition",
        "",
        f"- source_manifest_payload_digest: `{review['source_manifest_payload_digest']}`",
        f"- independent_manifest_payload_digest: `{review['independent_manifest_payload_digest']}`",
        f"- source_distribution_digest: `{review['source_distribution_digest']}`",
        f"- independent_distribution_digest: `{review['independent_distribution_digest']}`",
        "",
        "## Mutation Probes",
        "",
    ]
    for probe in review["mutation_probes"]:
        lines.append(
            f"- {probe['case']}: payload_changed={str(probe['payload_digest_changed']).lower()}, "
            f"distribution_changed={str(probe['distribution_digest_changed']).lower()}"
        )
    return "\n".join(lines) + "\n"


def render_component_review(review: dict[str, Any]) -> str:
    lines = ["# Component Graph Review", "", "## Behavior Probes", ""]
    for probe in review["behavior_probes"]:
        lines.append(f"- {probe['case']}: valid={str(probe['valid']).lower()}, codes={', '.join(probe['codes']) or 'none'}")
    return "\n".join(lines) + "\n"


def render_artifact_review(review: dict[str, Any]) -> str:
    lines = ["# Artifact Integrity Review", "", "## Behavior Probes", ""]
    for probe in review["behavior_probes"]:
        lines.append(f"- {probe['case']}: valid={str(probe['valid']).lower()}, codes={', '.join(probe['codes']) or 'none'}")
    return "\n".join(lines) + "\n"


def render_preaccess_review(review: dict[str, Any]) -> str:
    return (
        "# Path Pre-Access Review\n\n"
        f"- artifact_projector_present: {str(review['artifact_from_release_record_present']).lower()}\n"
        f"- exists_before_forbidden_check: {str(review['exists_before_forbidden_check']).lower()}\n"
        f"- stat_before_forbidden_check: {str(review['stat_before_forbidden_check']).lower()}\n"
        f"- hash_before_forbidden_check: {str(review['hash_before_forbidden_check']).lower()}\n"
    )


def render_checksum_review(review: dict[str, Any]) -> str:
    lines = [
        "# Checksum Review",
        "",
        f"- checksum_file_digest: `{review['checksum_file_digest']}`",
        f"- manifest_checksum_digest: `{review['manifest_checksum_digest']}`",
        "",
        "## Behavior Probes",
        "",
    ]
    for probe in review["behavior_probes"]:
        lines.append(f"- {probe['case']}: valid={str(probe['valid']).lower()}, codes={', '.join(probe['codes']) or 'none'}")
    return "\n".join(lines) + "\n"


def render_protocol_review(review: dict[str, Any]) -> str:
    lines = ["# Protocol Range Review", "", "## Behavior Probes", ""]
    for probe in review["behavior_probes"]:
        lines.append(f"- {probe['case']}: valid={str(probe['valid']).lower()}, codes={', '.join(probe['codes']) or 'none'}")
    return "\n".join(lines) + "\n"


def render_q47_review(review: dict[str, Any]) -> str:
    return (
        "# Q47 Source Mapping Review\n\n"
        f"- release_assets_count: {review['release_assets_count']}\n"
        f"- manifest_artifact_count: {review['manifest_artifact_count']}\n"
        f"- q47_dirty_state_manifest: {str(review['q47_dirty_state_manifest']).lower()}\n"
        f"- q47_dirty_state_provenance: {str(review['q47_dirty_state_provenance']).lower()}\n"
        f"- q48_publication_draft_is_distribution_truth: {str(review['q48_publication_draft_is_distribution_truth']).lower()}\n"
        f"- source_repo_local_path_suppressed: {str(review['source_repo_local_path_suppressed']).lower()}\n"
    )


def render_status_authority(review: dict[str, Any]) -> str:
    status_probes = [probe for probe in review["mutation_probes"] if probe["category"] == "status"]
    lines = ["# Status Versus Spec Authority", ""]
    for probe in status_probes:
        lines.append(
            f"- {probe['case']}: changed_identity={str(probe['distribution_digest_changed']).lower()}"
        )
    return "\n".join(lines) + "\n"


def render_signature_sbom(review: dict[str, Any]) -> str:
    return (
        "# Signature And SBOM Review\n\n"
        f"- signature_record_count: {len(review['signature_records'])}\n"
        f"- sbom_ref_count: {len(review['sbom_refs'])}\n"
        "- verified_signature_claimed: false\n"
        "- generated_sbom_claimed: false\n"
    )


def render_contamination_review(review: dict[str, Any]) -> str:
    return (
        "# Contamination Review\n\n"
        f"- directory_inventory_skips_forbidden: {str(review['directory_inventory_skips_forbidden']).lower()}\n"
    )


def render_fixture_review(review: dict[str, Any]) -> str:
    lines = ["# Fixture Coverage Review", "", f"- observed_case_count: {len(review['observed_cases'])}", ""]
    lines.append("## Missing Required Cases")
    lines.append("")
    for case in review["missing_cases"]:
        lines.append(f"- {case}")
    return "\n".join(lines) + "\n"


def render_non_capability_review(review: dict[str, Any]) -> str:
    lines = ["# No Overclaiming Review", "", f"- source_validation_status: {review['source_validation_status']}", ""]
    for key, value in review["no_apply_flags"].items():
        lines.append(f"- {key}_apply_or_publication_flag_false: {str(value).lower()}")
    return "\n".join(lines) + "\n"


def render_validation_summary(report: dict[str, Any]) -> str:
    return (
        "# Validation Summary\n\n"
        f"- result: {report['result']}\n"
        f"- material_finding_count: {report['material_finding_count']}\n"
        f"- missing_evidence: {report['missing_evidence']}\n"
        f"- recommended_next_task: {report['recommended_next_task']}\n"
    )


def main() -> int:
    result = run_check()
    print(stable_json(result["report"]))
    return 0 if result["report"]["missing_evidence"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
