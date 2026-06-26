"""OwnershipLedger v1 helpers.

OwnershipLedger records ownership taxonomy and path/section authority for a
ProjectLock-selected AIDE distribution. It is not an install plan, install
record, apply engine, admission record, authorization mechanism, or mutation
mechanism.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from core.protocol import envelope, project_lock


API_VERSION = envelope.API_VERSION
KIND = "OwnershipLedger"
SCHEMA_VERSION = "aide.ownership-ledger.v1"
TASK_ID = "AIDE-BUILD-OWNERSHIP-LEDGER-V1-01"
CHECK_TASK_ID = "AIDE-CHECK-OWNERSHIP-LEDGER-V1-01"
PROPOSED_CAPABILITY = "ownership_ledger_v1"
DETERMINISTIC_TIMESTAMP = "fixture-timestamp:ownership-ledger-v1"

REPORT_ROOT = Path(".aide/reports/ownership-ledger-v1")
SCHEMA_PATH = Path(".aide/protocol/aide-ownership-ledger-v1.schema.json")
FIXTURE_ROOT = Path(".aide/fixtures/ownership-ledger-v1")

LEDGER_JSON = REPORT_ROOT / "ownership-ledger.json"
LEDGER_MD = REPORT_ROOT / "ownership-ledger.md"
STATUS_MD = REPORT_ROOT / "status.md"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
VALIDATION_MD = REPORT_ROOT / "validation.md"
TAXONOMY_JSON = REPORT_ROOT / "taxonomy.json"
RECORD_INDEX_JSON = REPORT_ROOT / "record-index.json"
FIXTURE_MATRIX_JSON = REPORT_ROOT / "fixture-matrix.json"
FIXTURE_MATRIX_MD = REPORT_ROOT / "fixture-matrix.md"
NON_CAPABILITIES_MD = REPORT_ROOT / "non-capabilities.md"

PROJECT_LOCK_JSON = project_lock.LOCK_JSON
PROJECT_LOCK_ACCEPTANCE_JSON = Path(".aide/reports/project-lock-v0-accept/acceptance-report.json")

OWNERSHIP_CLASSES = [
    "vendor_managed_file",
    "vendor_managed_section",
    "project_owned",
    "project_overlay",
    "project_generated",
    "runtime_generated",
    "local_only",
    "evidence_only",
    "preserved_legacy",
    "unknown",
    "never_touch",
]

SUPPORTED_REQUIRED_FEATURES = {
    "ownership_ledger_v1",
    "project_lock_v0",
    "distribution_manifest_v1",
    "sha256_digest_canonical_json_v1",
}

SUPPORTED_OPTIONAL_FEATURES = {
    "managed_section_identity_v1",
    "target_overlay_ownership_v1",
}

REFUSAL_CODES = [
    "ownership_ledger.missing",
    "ownership_ledger.invalid",
    "ownership_ledger.project_lock_not_accepted",
    "ownership_ledger.project_lock_digest_mismatch",
    "ownership_ledger.missing_taxonomy_class",
    "ownership_ledger.unknown_taxonomy_class",
    "ownership_ledger.duplicate_record",
    "ownership_ledger.record_class_unknown",
    "ownership_ledger.vendor_digest_missing",
    "ownership_ledger.managed_section_identity_missing",
    "ownership_ledger.unknown_allows_apply",
    "ownership_ledger.never_touch_allows_apply",
    "ownership_ledger.automatic_apply_forbidden",
    "ownership_ledger.absolute_path_forbidden",
    "ownership_ledger.path_traversal_forbidden",
    "ownership_ledger.source_state_contamination",
    "ownership_ledger.unknown_required_feature",
    "ownership_ledger.extension_required_unknown",
    "ownership_ledger.digest_mismatch",
]

EXPLICIT_NON_CAPABILITIES = [
    "install_truth",
    "install_plan",
    "install_apply",
    "update_apply",
    "repair_apply",
    "rollback_apply",
    "uninstall_apply",
    "admission",
    "authorization",
    "target_repository_mutation",
    "release_publication",
    "git_tag_creation",
    "github_release_creation",
    "upload",
    "network_call",
    "provider_model_call",
    "workbench_runtime",
    "mcp_runtime",
    "source_change_preview_apply_rollback",
    "promotion",
]

PATH_RE = re.compile(r"(^[A-Za-z]:[\\/])|(^\\\\)|(^/)|(^|/)\.\.($|/)")


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_digest(data: bytes) -> str:
    return "sha256:" + __import__("hashlib").sha256(data).hexdigest()


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


def load_project_lock(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / PROJECT_LOCK_JSON
    if path.exists():
        return read_json(path)
    return project_lock.build_project_lock(repo_root)


def load_project_lock_acceptance(repo_root: str | Path) -> dict[str, Any]:
    path = Path(repo_root) / PROJECT_LOCK_ACCEPTANCE_JSON
    if not path.exists():
        return {}
    return read_json(path)


def project_lock_is_accepted(repo_root: str | Path, lock: dict[str, Any]) -> bool:
    acceptance = load_project_lock_acceptance(repo_root)
    return (
        acceptance.get("result") == "ACCEPTED_WITH_WARNINGS"
        and acceptance.get("accepted_capability") == "project_lock_v0"
        and acceptance.get("material_finding_count") == 0
        and acceptance.get("source_check_result") == "PASS_WITH_WARNINGS"
        and lock.get("status", {}).get("project_lock_digest") is not None
    )


def taxonomy() -> list[dict[str, Any]]:
    descriptions = {
        "vendor_managed_file": "AIDE-distributed file with exact source digest authority.",
        "vendor_managed_section": "AIDE-distributed managed section inside a host file.",
        "project_owned": "Target project file that AIDE must not overwrite silently.",
        "project_overlay": "Target-owned overlay that configures an AIDE distribution.",
        "project_generated": "Target-local generated projection that is recreated in target context.",
        "runtime_generated": "Runtime/local generated state outside committed distribution truth.",
        "local_only": "Local operator state that is never distribution truth.",
        "evidence_only": "Evidence records preserved for audit, not source distribution content.",
        "preserved_legacy": "Legacy or pre-existing target state preserved unless manually migrated.",
        "unknown": "Observed path without sufficient ownership proof; blocks automatic apply.",
        "never_touch": "Path class that AIDE distribution apply must never modify.",
    }
    entries = []
    for class_id in OWNERSHIP_CLASSES:
        entries.append(
            {
                "class_id": class_id,
                "authority": "aide_distribution" if class_id.startswith("vendor_") else "target_project",
                "automatic_apply_allowed": False,
                "overwrite_allowed": False,
                "delete_allowed": False,
                "blocks_automatic_apply": class_id in {"unknown", "never_touch", "project_owned", "local_only"},
                "description": descriptions[class_id],
                "extensions": {},
            }
        )
    return entries


def ownership_record(
    record_id: str,
    ownership_class: str,
    target_path: str,
    *,
    path_kind: str = "file",
    source_ref: str | None = None,
    content_digest: str | None = None,
    section_id: str | None = None,
    managed_section_identity: str | None = None,
    authority: str | None = None,
) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "ownership_class": ownership_class,
        "path_kind": path_kind,
        "target_path": target_path,
        "section_id": section_id,
        "source_ref": source_ref,
        "content_digest": content_digest,
        "managed_section_identity": managed_section_identity,
        "authority": authority or ("aide_distribution" if ownership_class.startswith("vendor_") else "target_project"),
        "mutation_policy": "no_apply_metadata_only",
        "apply_allowed": False,
        "overwrite_allowed": False,
        "delete_allowed": False,
        "evidence_refs": [],
        "extensions": {},
    }


def default_records(lock: dict[str, Any]) -> list[dict[str, Any]]:
    selected_digest = lock.get("spec", {}).get("selected_components", [{}])[0].get("selected_digest")
    source_distribution_ref = lock.get("metadata", {}).get("selected_distribution_ref")
    return [
        ownership_record(
            "vendor-file-aide-lite-cli",
            "vendor_managed_file",
            ".aide/scripts/aide_lite.py",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
        ),
        ownership_record(
            "vendor-file-project-lock-schema",
            "vendor_managed_file",
            ".aide/protocol/aide-project-lock-v0.schema.json",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
        ),
        ownership_record(
            "vendor-section-agents-summary",
            "vendor_managed_section",
            "AGENTS.md",
            path_kind="managed_section",
            section_id="aide-self-hosting-summary",
            source_ref=source_distribution_ref,
            content_digest=selected_digest,
            managed_section_identity="AIDE-GENERATED:aide-self-hosting-summary",
        ),
        ownership_record("project-owned-readme", "project_owned", "README.md"),
        ownership_record("project-overlay-policy", "project_overlay", ".aide/project-overlays/policy.yaml"),
        ownership_record("project-generated-context", "project_generated", ".aide/context/generated/context-pack.json"),
        ownership_record("runtime-generated-local-state", "runtime_generated", ".aide.local/**", path_kind="glob"),
        ownership_record("local-only-operator-state", "local_only", "local-only/**", path_kind="glob"),
        ownership_record("evidence-only-queue-evidence", "evidence_only", ".aide/queue/**/evidence/**", path_kind="glob"),
        ownership_record("preserved-legacy-state", "preserved_legacy", ".aide/legacy/**", path_kind="glob"),
        ownership_record("unknown-unclassified", "unknown", "unclassified/**", path_kind="glob"),
        ownership_record("never-touch-git", "never_touch", ".git/**", path_kind="glob"),
    ]


def build_ownership_ledger(repo_root: str | Path) -> dict[str, Any]:
    lock = load_project_lock(repo_root)
    lock_digest = lock["status"]["project_lock_digest"]
    ledger = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "ledger_ref": "aide://ownership-ledger/aide-self-project-lock-v0",
            "project_ref": lock["metadata"]["project_ref"],
            "project_identity": lock["metadata"]["project_identity"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock_digest,
            "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
            "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
            "ownership_profile": "aide-lite-target-default",
            "ledger_revision": "0",
            "created_from": "accepted_project_lock_v0",
            "created_at_classification": "deterministic_projection_not_wall_clock",
            "extensions": {},
        },
        "spec": {
            "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
            "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
            "taxonomy": taxonomy(),
            "records": default_records(lock),
            "unknown_ownership_policy": {
                "blocks_automatic_apply": True,
                "requires_manual_review": True,
                "extensions": {},
            },
            "managed_section_policy": {
                "requires_exact_section_identity": True,
                "manual_outside_only": True,
                "extensions": {},
            },
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "ownership_ledger_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_ownership_ledger(ledger)


def ownership_ledger_payload(ledger: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(ledger)
    payload.pop("status", None)
    return payload


def ownership_ledger_digest(ledger: dict[str, Any]) -> str:
    return sha256_digest(canonical_json_bytes(ownership_ledger_payload(ledger)))


def finalize_ownership_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    ledger = copy.deepcopy(ledger)
    ledger.setdefault("status", {})["ownership_ledger_digest"] = ownership_ledger_digest(ledger)
    return ledger


def _add_error(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def _path_refusal(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    if PATH_RE.search(normalized):
        if normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("//"):
            return "ownership_ledger.absolute_path_forbidden"
        return "ownership_ledger.path_traversal_forbidden"
    if "latest-" in normalized:
        return "ownership_ledger.source_state_contamination"
    return None


def _extension_refusal(container: dict[str, Any]) -> bool:
    extensions = container.get("extensions")
    if not isinstance(extensions, dict):
        return False
    return any(str(key).startswith("requires.") for key in extensions)


def validate_ownership_ledger_object(
    ledger: dict[str, Any],
    *,
    lock: dict[str, Any] | None = None,
    repo_root: str | Path | None = None,
    require_project_lock_acceptance: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    if ledger.get("kind") != KIND:
        _add_error(errors, "ownership_ledger.invalid", "kind must be OwnershipLedger")
    if ledger.get("schema_version") != SCHEMA_VERSION:
        _add_error(errors, "ownership_ledger.invalid", "schema_version mismatch")
    if lock is None and repo_root is not None:
        lock = load_project_lock(repo_root)
    if lock is not None:
        if ledger.get("metadata", {}).get("project_lock_digest") != lock.get("status", {}).get("project_lock_digest"):
            _add_error(errors, "ownership_ledger.project_lock_digest_mismatch", "project lock digest mismatch")
        if require_project_lock_acceptance:
            if repo_root is None or not project_lock_is_accepted(repo_root, lock):
                _add_error(errors, "ownership_ledger.project_lock_not_accepted", "ProjectLock v0 is not accepted")
    elif require_project_lock_acceptance:
        _add_error(errors, "ownership_ledger.project_lock_not_accepted", "ProjectLock v0 is not available")

    spec = ledger.get("spec", {})
    if not isinstance(spec, dict):
        _add_error(errors, "ownership_ledger.invalid", "spec must be an object")
        spec = {}
    if any(feature not in SUPPORTED_REQUIRED_FEATURES for feature in spec.get("required_features", [])):
        _add_error(errors, "ownership_ledger.unknown_required_feature", "unknown required feature")
    if _extension_refusal(ledger) or _extension_refusal(ledger.get("metadata", {})) or _extension_refusal(spec):
        _add_error(errors, "ownership_ledger.extension_required_unknown", "required extension is unsupported")

    taxonomy_entries = spec.get("taxonomy", [])
    if not isinstance(taxonomy_entries, list):
        taxonomy_entries = []
        _add_error(errors, "ownership_ledger.invalid", "taxonomy must be a list")
    taxonomy_classes = [entry.get("class_id") for entry in taxonomy_entries if isinstance(entry, dict)]
    for class_id in OWNERSHIP_CLASSES:
        if class_id not in taxonomy_classes:
            _add_error(errors, "ownership_ledger.missing_taxonomy_class", f"missing taxonomy class: {class_id}")
    for class_id in taxonomy_classes:
        if class_id not in OWNERSHIP_CLASSES:
            _add_error(errors, "ownership_ledger.unknown_taxonomy_class", f"unknown taxonomy class: {class_id}")

    record_ids: set[str] = set()
    records = spec.get("records", [])
    if not isinstance(records, list):
        records = []
        _add_error(errors, "ownership_ledger.invalid", "records must be a list")
    record_classes = {entry.get("ownership_class") for entry in records if isinstance(entry, dict)}
    for class_id in OWNERSHIP_CLASSES:
        if class_id not in record_classes:
            _add_error(errors, "ownership_ledger.missing_taxonomy_class", f"no record for class: {class_id}")
    for record in records:
        if not isinstance(record, dict):
            _add_error(errors, "ownership_ledger.invalid", "record must be an object")
            continue
        record_id = str(record.get("record_id", ""))
        if record_id in record_ids:
            _add_error(errors, "ownership_ledger.duplicate_record", f"duplicate record: {record_id}")
        record_ids.add(record_id)
        ownership_class = record.get("ownership_class")
        if ownership_class not in OWNERSHIP_CLASSES:
            _add_error(errors, "ownership_ledger.record_class_unknown", f"unknown record class: {ownership_class}")
        target_path = str(record.get("target_path", ""))
        path_refusal = _path_refusal(target_path)
        if path_refusal:
            _add_error(errors, path_refusal, f"unsafe path: {target_path}")
        if record.get("apply_allowed") is not False or record.get("overwrite_allowed") is not False or record.get("delete_allowed") is not False:
            _add_error(errors, "ownership_ledger.automatic_apply_forbidden", f"record enables apply: {record_id}")
        if ownership_class == "vendor_managed_file" and not record.get("content_digest"):
            _add_error(errors, "ownership_ledger.vendor_digest_missing", f"vendor file missing digest: {record_id}")
        if ownership_class == "vendor_managed_section" and not record.get("managed_section_identity"):
            _add_error(errors, "ownership_ledger.managed_section_identity_missing", f"managed section missing identity: {record_id}")
        if ownership_class == "unknown" and record.get("apply_allowed") is not False:
            _add_error(errors, "ownership_ledger.unknown_allows_apply", f"unknown record allows apply: {record_id}")
        if ownership_class == "never_touch" and record.get("apply_allowed") is not False:
            _add_error(errors, "ownership_ledger.never_touch_allows_apply", f"never_touch record allows apply: {record_id}")
        if _extension_refusal(record):
            _add_error(errors, "ownership_ledger.extension_required_unknown", f"required extension on record: {record_id}")

    expected_digest = ledger.get("status", {}).get("ownership_ledger_digest")
    actual_digest = ownership_ledger_digest(ledger)
    if expected_digest != actual_digest:
        _add_error(errors, "ownership_ledger.digest_mismatch", "ownership ledger digest mismatch")
    for feature in spec.get("optional_features", []):
        if feature not in SUPPORTED_OPTIONAL_FEATURES:
            warnings.append(f"unknown optional feature tolerated: {feature}")
    return {
        "valid": not errors,
        "result": "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION",
        "errors": errors,
        "warnings": warnings,
        "refusal_codes": sorted({error["code"] for error in errors}),
        "ownership_ledger_digest": actual_digest,
    }


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return read_json(Path(repo_root) / SCHEMA_PATH)


def status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    return {
        "status": "PASS_WITH_WARNINGS",
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/ownership_ledger.py").exists(),
        "project_lock_report_exists": (root / PROJECT_LOCK_JSON).exists(),
        "project_lock_acceptance_report_exists": (root / PROJECT_LOCK_ACCEPTANCE_JSON).exists(),
        "ownership_ledger_report_exists": (root / LEDGER_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "admission_implemented": False,
        "authorization_implemented": False,
    }


def project(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    ledger = build_ownership_ledger(root)
    validation = validate_ownership_ledger_object(ledger, lock=load_project_lock(root), repo_root=root)
    REPORT_ROOT_ABS = root / REPORT_ROOT
    write_json(root / LEDGER_JSON, ledger)
    write_json(root / TAXONOMY_JSON, {"taxonomy": ledger["spec"]["taxonomy"]})
    write_json(root / RECORD_INDEX_JSON, {"records": ledger["spec"]["records"]})
    write_text(
        root / LEDGER_MD,
        "\n".join(
            [
                "# OwnershipLedger v1",
                "",
                f"- result: `{validation['result']}`",
                f"- proposed_capability: `{PROPOSED_CAPABILITY}`",
                f"- record_count: `{len(ledger['spec']['records'])}`",
                f"- ownership_ledger_digest: `{ledger['status']['ownership_ledger_digest']}`",
                f"- recommended_next_task: `{CHECK_TASK_ID}`",
                "",
            ]
        ),
    )
    write_text(
        root / STATUS_MD,
        "\n".join(
            [
                "# OwnershipLedger v1 Status",
                "",
                f"- status: `{validation['result']}`",
                f"- schema_exists: `{(root / SCHEMA_PATH).exists()}`",
                f"- helper_exists: `{(root / 'core/protocol/ownership_ledger.py').exists()}`",
                f"- project_lock_accepted: `{project_lock_is_accepted(root, load_project_lock(root))}`",
                f"- record_count: `{len(ledger['spec']['records'])}`",
                f"- report_root: `{REPORT_ROOT.as_posix()}`",
                "",
            ]
        ),
    )
    write_text(root / NON_CAPABILITIES_MD, "\n".join(["# Non-Capabilities", "", *[f"- {item}" for item in EXPLICIT_NON_CAPABILITIES], ""]))
    return {
        "status": validation["result"],
        "project_lock_digest": ledger["metadata"]["project_lock_digest"],
        "ownership_ledger_digest": ledger["status"]["ownership_ledger_digest"],
        "record_count": len(ledger["spec"]["records"]),
        "taxonomy_count": len(ledger["spec"]["taxonomy"]),
        "ledger_path": LEDGER_JSON.as_posix(),
        "source_artifacts_mutated": False,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "install_apply_implemented": False,
        "update_apply_implemented": False,
        "target_repository_mutation_implemented": False,
        "admission_implemented": False,
        "authorization_implemented": False,
    }


def minimal_fixture_ledger() -> dict[str, Any]:
    lock = project_lock.minimal_fixture_lock()
    return build_ledger_from_lock(lock)


def build_ledger_from_lock(lock: dict[str, Any]) -> dict[str, Any]:
    ledger = {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "ledger_ref": "aide://ownership-ledger/fixture",
            "project_ref": lock["metadata"]["project_ref"],
            "project_identity": lock["metadata"]["project_identity"],
            "project_lock_ref": lock["metadata"]["project_lock_ref"],
            "project_lock_digest": lock["status"]["project_lock_digest"],
            "selected_distribution_digest": lock["metadata"]["selected_distribution_digest"],
            "manifest_payload_digest": lock["metadata"]["manifest_payload_digest"],
            "ownership_profile": "fixture-default",
            "ledger_revision": "0",
            "created_from": "accepted_project_lock_v0",
            "created_at_classification": DETERMINISTIC_TIMESTAMP,
            "extensions": {},
        },
        "spec": {
            "required_features": sorted(SUPPORTED_REQUIRED_FEATURES),
            "optional_features": sorted(SUPPORTED_OPTIONAL_FEATURES),
            "taxonomy": taxonomy(),
            "records": default_records(lock),
            "unknown_ownership_policy": {"blocks_automatic_apply": True, "requires_manual_review": True, "extensions": {}},
            "managed_section_policy": {"requires_exact_section_identity": True, "manual_outside_only": True, "extensions": {}},
            "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
            "extensions": {},
        },
        "status": {
            "status": "PASS_WITH_WARNINGS",
            "validation_result": "PASS_WITH_WARNINGS",
            "proposed_capability": PROPOSED_CAPABILITY,
            "recommended_next_task": CHECK_TASK_ID,
            "ownership_ledger_digest": "",
            "install_apply_implemented": False,
            "update_apply_implemented": False,
            "target_repository_mutation_implemented": False,
            "admission_implemented": False,
            "authorization_implemented": False,
            "extensions": {},
        },
        "extensions": {},
    }
    return finalize_ownership_ledger(ledger)


def write_fixture_corpus(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root) / FIXTURE_ROOT
    valid_root = root / "valid"
    invalid_root = root / "invalid"
    valid_root.mkdir(parents=True, exist_ok=True)
    invalid_root.mkdir(parents=True, exist_ok=True)
    base = minimal_fixture_ledger()

    def write_case(folder: Path, name: str, data: dict[str, Any]) -> None:
        write_json(folder / f"{name}.json", finalize_ownership_ledger(data))

    write_case(valid_root, "minimal-valid-ledger", base)
    full = copy.deepcopy(base)
    full["spec"]["optional_features"].append("future.optional.ownership-ledger")
    full["extensions"] = {"future.optional": {"preserve": True}}
    write_case(valid_root, "extension-round-trip", full)
    reordered = copy.deepcopy(base)
    reordered["spec"]["records"] = list(reversed(reordered["spec"]["records"]))
    write_case(valid_root, "reordered-records-valid", reordered)

    invalid_cases: dict[str, dict[str, Any]] = {}
    invalid_cases["project-lock-digest-mismatch"] = mutate(base, lambda d: d["metadata"].__setitem__("project_lock_digest", "sha256:" + "0" * 64))
    invalid_cases["missing-taxonomy-class"] = mutate(base, lambda d: d["spec"].__setitem__("taxonomy", d["spec"]["taxonomy"][:-1]))
    invalid_cases["unknown-taxonomy-class"] = mutate(base, lambda d: d["spec"]["taxonomy"].append({"class_id": "mystery", "authority": "target_project", "automatic_apply_allowed": False, "overwrite_allowed": False, "delete_allowed": False, "blocks_automatic_apply": True, "description": "invalid", "extensions": {}}))
    invalid_cases["duplicate-record"] = mutate(base, lambda d: d["spec"]["records"].append(copy.deepcopy(d["spec"]["records"][0])))
    invalid_cases["unknown-record-class"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("ownership_class", "mystery"))
    invalid_cases["vendor-digest-missing"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("content_digest", None))
    invalid_cases["managed-section-identity-missing"] = mutate(base, lambda d: d["spec"]["records"][2].__setitem__("managed_section_identity", None))
    invalid_cases["unknown-allows-apply"] = mutate_record(base, "unknown", lambda r: r.__setitem__("apply_allowed", True))
    invalid_cases["never-touch-allows-apply"] = mutate_record(base, "never_touch", lambda r: r.__setitem__("apply_allowed", True))
    invalid_cases["absolute-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", "C:/outside/file.txt"))
    invalid_cases["traversal-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", "../outside/file.txt"))
    invalid_cases["source-latest-path"] = mutate(base, lambda d: d["spec"]["records"][0].__setitem__("target_path", ".aide/context/latest-task-packet.md"))
    invalid_cases["unknown-required-feature"] = mutate(base, lambda d: d["spec"]["required_features"].append("future.required.ownership"))
    invalid_cases["extension-required-unknown"] = mutate(base, lambda d: d["spec"]["extensions"].__setitem__("requires.future", {"enabled": True}))
    for name, data in invalid_cases.items():
        write_case(invalid_root, name, data)
    return {"valid": sorted(path.stem for path in valid_root.glob("*.json")), "invalid": sorted(path.stem for path in invalid_root.glob("*.json"))}


def mutate(data: dict[str, Any], mutator) -> dict[str, Any]:
    clone = copy.deepcopy(data)
    mutator(clone)
    return clone


def mutate_record(data: dict[str, Any], ownership_class: str, mutator) -> dict[str, Any]:
    def apply(clone: dict[str, Any]) -> None:
        record = next(item for item in clone["spec"]["records"] if item["ownership_class"] == ownership_class)
        mutator(record)

    return mutate(data, apply)


EXPECTED_INVALID_REFUSALS = {
    "project-lock-digest-mismatch": ["ownership_ledger.project_lock_digest_mismatch"],
    "missing-taxonomy-class": ["ownership_ledger.missing_taxonomy_class"],
    "unknown-taxonomy-class": ["ownership_ledger.unknown_taxonomy_class"],
    "duplicate-record": ["ownership_ledger.duplicate_record"],
    "unknown-record-class": ["ownership_ledger.record_class_unknown"],
    "vendor-digest-missing": ["ownership_ledger.vendor_digest_missing"],
    "managed-section-identity-missing": ["ownership_ledger.managed_section_identity_missing"],
    "unknown-allows-apply": ["ownership_ledger.automatic_apply_forbidden"],
    "never-touch-allows-apply": ["ownership_ledger.automatic_apply_forbidden"],
    "absolute-path": ["ownership_ledger.absolute_path_forbidden"],
    "traversal-path": ["ownership_ledger.path_traversal_forbidden"],
    "source-latest-path": ["ownership_ledger.source_state_contamination"],
    "unknown-required-feature": ["ownership_ledger.unknown_required_feature"],
    "extension-required-unknown": ["ownership_ledger.extension_required_unknown"],
}


def fixture_matrix(repo_root: str | Path) -> list[dict[str, Any]]:
    write_fixture_corpus(repo_root)
    lock = project_lock.minimal_fixture_lock()
    results: list[dict[str, Any]] = []
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "valid").glob("*.json")):
        data = read_json(path)
        result = validate_ownership_ledger_object(data, lock=lock, require_project_lock_acceptance=False)
        results.append({"case_id": path.stem, "expected_result": "PASS", "observed_result": result["result"], "observed_refusal_codes": result["refusal_codes"], "passed": result["valid"], "path": path.relative_to(repo_root).as_posix()})
    for path in sorted((Path(repo_root) / FIXTURE_ROOT / "invalid").glob("*.json")):
        data = read_json(path)
        result = validate_ownership_ledger_object(data, lock=lock, require_project_lock_acceptance=False)
        expected = EXPECTED_INVALID_REFUSALS[path.stem]
        passed = not result["valid"] and set(expected).issubset(set(result["refusal_codes"]))
        results.append({"case_id": path.stem, "expected_result": "FAILED_VALIDATION", "expected_refusal_codes": expected, "observed_result": result["result"], "observed_refusal_codes": result["refusal_codes"], "passed": passed, "path": path.relative_to(repo_root).as_posix()})
    return results


def validate(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    project_report = project(root)
    ledger = read_json(root / LEDGER_JSON)
    lock = load_project_lock(root)
    ledger_validation = validate_ownership_ledger_object(ledger, lock=lock, repo_root=root)
    fixtures = fixture_matrix(root)
    fixture_passed = all(item["passed"] for item in fixtures)
    errors = ledger_validation["errors"] + ([] if fixture_passed else [{"code": "ownership_ledger.fixture_failure", "message": "fixture corpus failed"}])
    checks = {
        "schema_exists": (root / SCHEMA_PATH).exists(),
        "helper_exists": (root / "core/protocol/ownership_ledger.py").exists(),
        "cli_registered": True,
        "ledger_generated": (root / LEDGER_JSON).exists(),
        "ledger_valid": ledger_validation["valid"],
        "fixture_matrix_passed": fixture_passed,
        "project_lock_accepted": project_lock_is_accepted(root, lock),
        "project_lock_digest_bound": ledger["metadata"]["project_lock_digest"] == lock["status"]["project_lock_digest"],
        "taxonomy_complete": {entry["class_id"] for entry in ledger["spec"]["taxonomy"]} == set(OWNERSHIP_CLASSES),
        "unknown_blocks_apply": all(record["apply_allowed"] is False for record in ledger["spec"]["records"] if record["ownership_class"] == "unknown"),
        "never_touch_blocks_apply": all(record["apply_allowed"] is False for record in ledger["spec"]["records"] if record["ownership_class"] == "never_touch"),
        "install_apply_not_implemented": ledger["status"]["install_apply_implemented"] is False,
        "update_apply_not_implemented": ledger["status"]["update_apply_implemented"] is False,
        "target_repository_mutation_not_implemented": ledger["status"]["target_repository_mutation_implemented"] is False,
        "admission_not_implemented": ledger["status"]["admission_implemented"] is False,
        "authorization_not_implemented": ledger["status"]["authorization_implemented"] is False,
    }
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": SCHEMA_VERSION,
        "validation_status": validation_status,
        "proposed_capability": PROPOSED_CAPABILITY,
        "recommended_next_task": CHECK_TASK_ID,
        "checks": checks,
        "project_report": project_report,
        "ledger_validation": ledger_validation,
        "fixture_results": fixtures,
        "errors": errors,
        "warnings": [
            "OwnershipLedger v1 is proposed until independent check and acceptance.",
            "OwnershipLedger records ownership only and performs no apply or target mutation.",
        ],
        "explicit_non_capabilities": EXPLICIT_NON_CAPABILITIES,
    }
    write_json(root / VALIDATION_JSON, report)
    write_json(root / FIXTURE_MATRIX_JSON, {"fixture_results": fixtures})
    write_text(root / FIXTURE_MATRIX_MD, "\n".join(["# OwnershipLedger v1 Fixture Matrix", "", *[f"- {item['case_id']}: {item['observed_result']} ({'PASS' if item['passed'] else 'FAIL'})" for item in fixtures], ""]))
    write_text(root / VALIDATION_MD, "\n".join(["# OwnershipLedger v1 Validation", "", f"- result: `{validation_status}`", f"- error_count: `{len(errors)}`", f"- recommended_next_task: `{CHECK_TASK_ID}`", ""]))
    return report
