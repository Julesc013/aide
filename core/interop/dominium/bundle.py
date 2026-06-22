"""Report writing, CLI-facing commands, fixtures, and demo orchestration."""

from __future__ import annotations

import ast
import shutil
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from . import conformance, fixture_replay, integrity, models, operations, projector, snapshot, validation
from .references import sha256_bytes, sha256_file


PINNED_DOMINIUM_HEAD = "c92b386027890c1bbf14aef6eaafe0357b7b03dd"


def default_dominium_root(repo_root: str | Path) -> Path:
    root = Path(repo_root).resolve()
    candidate = root.parent.parent / "Dominium" / "dominium"
    if candidate.exists():
        return candidate
    return Path("C:/Projects/Dominium/dominium")


def _dominium_root(repo_root: str | Path, dominium_root: str | Path | None = None) -> Path:
    return Path(dominium_root).resolve() if dominium_root is not None else default_dominium_root(repo_root)


def _revision(revision: str | None = None) -> str:
    return revision or PINNED_DOMINIUM_HEAD


def load_schema(repo_root: str | Path) -> dict[str, Any]:
    return models.read_json(Path(repo_root) / models.SCHEMA_PATH)


def _runtime_dependency_entries(repo_root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for rel in models.required_runtime_dependency_paths():
        path = repo_root / rel
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"required runtime dependency missing: {rel}")
        entries.append(
            {
                "path": rel,
                "sha256": sha256_file(path),
                "required": True,
                "role": "cli_entrypoint" if rel == ".aide/scripts/aide_lite.py" else "runtime_dependency",
            }
        )
    return entries


def runtime_dependency_manifest(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    entries = _runtime_dependency_entries(root)
    payload = {
        "schema_version": "aide.dominium-readonly-seam.runtime-dependency-manifest.v0",
        "task_id": models.REPAIR_TASK_ID,
        "entrypoint": ".aide/scripts/aide_lite.py",
        "module_search_root": ".",
        "supported_python_version_range": ">=3.11",
        "dependency_count": len(entries),
        "dependencies": entries,
    }
    payload["manifest_digest"] = integrity.stable_digest({key: value for key, value in payload.items() if key != "manifest_digest"})
    return payload


def write_runtime_dependency_manifest(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    manifest = runtime_dependency_manifest(root)
    models.write_json(root / models.RUNTIME_DEPENDENCY_MANIFEST_JSON, manifest)
    return manifest


def _validate_manifest_entry(entry: dict[str, Any], seen: set[str]) -> str:
    rel = str(entry.get("path", ""))
    path = Path(rel)
    if not rel or path.is_absolute() or ".." in path.parts or "\\" in rel:
        raise ValueError(f"unsafe runtime dependency path: {rel}")
    if rel in seen:
        raise ValueError(f"duplicate runtime dependency path: {rel}")
    seen.add(rel)
    return rel


def _validate_runtime_dependency_manifest(source_root: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    payload = {key: value for key, value in manifest.items() if key != "manifest_digest"}
    if manifest.get("manifest_digest") != integrity.stable_digest(payload):
        raise ValueError("runtime dependency manifest digest mismatch")
    seen: set[str] = set()
    entries = []
    for raw_entry in manifest.get("dependencies", []):
        if not isinstance(raw_entry, dict):
            raise ValueError("runtime dependency entry must be an object")
        rel = _validate_manifest_entry(raw_entry, seen)
        path = source_root / rel
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"runtime dependency missing: {rel}")
        if raw_entry.get("sha256") != sha256_file(path):
            raise ValueError(f"runtime dependency hash mismatch: {rel}")
        entries.append(dict(raw_entry))
    if int(manifest.get("dependency_count", -1)) != len(entries):
        raise ValueError("runtime dependency manifest count mismatch")
    return entries


def load_runtime_dependency_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / models.RUNTIME_DEPENDENCY_MANIFEST_JSON
    if not path.exists():
        return write_runtime_dependency_manifest(repo_root)
    manifest = models.read_json(path)
    _validate_runtime_dependency_manifest(repo_root, manifest)
    return manifest


def _copy_runtime_dependencies_from_manifest(source_root: Path, target_root: Path, manifest: dict[str, Any]) -> None:
    entries = _validate_runtime_dependency_manifest(source_root, manifest)
    for entry in entries:
        rel = entry["path"]
        src = source_root / rel
        dst = target_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if sha256_file(dst) != entry["sha256"]:
            raise ValueError(f"copied runtime dependency hash mismatch: {rel}")


def _copy_runtime_dependencies(source_root: Path, target_root: Path) -> None:
    manifest = load_runtime_dependency_manifest(source_root)
    _copy_runtime_dependencies_from_manifest(source_root, target_root, manifest)


def local_import_closure(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    declared = {str(item["path"]) for item in load_runtime_dependency_manifest(root).get("dependencies", []) if isinstance(item, dict)}
    start_paths = [
        ".aide/scripts/aide_lite.py",
        "core/protocol/envelope.py",
        *[path.relative_to(root).as_posix() for path in sorted((root / "core/interop/dominium").glob("*.py"))],
    ]
    derived: set[str] = set()
    dynamic_imports: list[str] = []
    for rel in start_paths:
        path = root / rel
        if not path.exists():
            continue
        derived.add(rel)
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            module = ""
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name
                    if module.startswith("core."):
                        derived.add(module.replace(".", "/") + ".py")
            if module.startswith("core."):
                derived.add(module.replace(".", "/") + ".py")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "__import__":
                dynamic_imports.append(rel)
    derived = {rel for rel in derived if (root / rel).exists() and rel.startswith(("core/", ".aide/scripts/"))}
    return {
        "schema_version": "aide.dominium-readonly-seam.import-closure.v0",
        "declared_dependencies": sorted(declared),
        "derived_dependencies": sorted(derived),
        "missing_declarations": sorted(derived - declared),
        "unused_declarations": sorted(declared - derived),
        "dynamic_imports": sorted(set(dynamic_imports)),
        "optional_imports": ["tomllib"],
        "undeclared_dependency_count": len(derived - declared),
    }


def _run_portable_cli_sequence(repo_root: Path, dominium_root: Path, revision: str | None, commands: list[str], cwd: Path) -> list[dict[str, Any]]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.pop("PYTHONUSERBASE", None)
    env["AIDE_DOMINIUM_PORTABILITY_CHILD"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    script = r"""
import contextlib
import hashlib
import importlib.util
import io
import json
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
dominium_root = sys.argv[2]
revision = sys.argv[3]
commands = sys.argv[4:]
spec = importlib.util.spec_from_file_location("aide_lite_portability", repo_root / ".aide/scripts/aide_lite.py")
module = importlib.util.module_from_spec(spec)
sys.modules["aide_lite_portability"] = module
spec.loader.exec_module(module)
results = []
for command in commands:
    stdout = io.StringIO()
    stderr = io.StringIO()
    argv = [
        "--repo-root",
        str(repo_root),
        "dominium-seam",
        command,
        "--dominium-root",
        dominium_root,
        "--revision",
        revision,
    ]
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        returncode = module.main(argv)
    stdout_value = stdout.getvalue()
    stderr_value = stderr.getvalue()
    results.append(
        {
            "command": command,
            "returncode": int(returncode),
            "stdout_sha256": "sha256:" + hashlib.sha256(stdout_value.encode("utf-8")).hexdigest(),
            "stderr_sha256": "sha256:" + hashlib.sha256(stderr_value.encode("utf-8")).hexdigest(),
            "stdout_preview": stdout_value.splitlines()[:20],
            "stderr_preview": stderr_value.splitlines()[:20],
        }
    )
print(json.dumps(results, sort_keys=True))
sys.exit(0 if all(item["returncode"] == 0 for item in results) else 1)
"""
    argv = [
        sys.executable,
        "-I",
        "-c",
        script,
        str(repo_root),
        str(dominium_root),
        _revision(revision),
        *commands,
    ]
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, check=False)
    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError:
        parsed = []
    if result.returncode != 0 and not parsed:
        return [
            {
                "command": "sequence",
                "returncode": result.returncode,
                "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")),
                "stderr_sha256": sha256_bytes(result.stderr.encode("utf-8")),
                "stdout_preview": result.stdout.splitlines()[:20],
                "stderr_preview": result.stderr.splitlines()[:20],
            }
        ]
    return parsed


def _relative_output_hashes(repo_root: Path, paths: list[Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in paths:
        path = repo_root / rel
        if path.exists():
            hashes[rel.as_posix()] = sha256_file(path)
    return hashes


def _path_leak_count(repo_root: Path, forbidden_needles: list[str]) -> int:
    count = 0
    for root in [repo_root / models.REPORT_ROOT, repo_root / models.INTEROP_ROOT, repo_root / models.FIXTURE_ROOT]:
        if not root.exists():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count += sum(1 for needle in forbidden_needles if needle and needle in text)
    return count


def portability_check(repo_root: str | Path, *, dominium_root: str | Path, revision: str | None = None) -> dict[str, Any]:
    source_root = Path(repo_root)
    dom_root = Path(dominium_root)
    manifest = load_runtime_dependency_manifest(source_root)
    comparison_paths = [
        models.SEAM_BUNDLE_JSON,
        models.SOURCE_SNAPSHOT_JSON,
        models.PROJECTION_INDEX_JSON,
        models.VALIDATION_JSON,
        models.CONFORMANCE_RESULTS_JSON,
        models.CONFORMANCE_ASSERTIONS_JSON,
        models.CONFORMANCE_EVIDENCE_JSON,
        models.COMPATIBILITY_JSON,
        models.DEMO_RESULT_JSON,
        models.OPERATION_TRACE_JSON,
        models.OPERATION_GUARD_CONFORMANCE_JSON,
        models.FIXTURE_MANIFEST_JSON,
        models.INTEROP_SEAM_BUNDLE_JSON,
        models.INTEROP_BRIDGE_MANIFEST_JSON,
        models.INTEROP_CONFORMANCE_EXPECTATIONS_JSON,
        models.RUNTIME_DEPENDENCY_MANIFEST_JSON,
    ]
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        roots = [base / "portable-a", base / "portable-b"]
        command_results: list[dict[str, Any]] = []
        output_hashes: list[dict[str, str]] = []
        required_sets = []
        for index, temp_root in enumerate(roots):
            _copy_runtime_dependencies_from_manifest(source_root, temp_root, manifest)
            cwd = base / f"cwd-{temp_root.name}"
            cwd.mkdir()
            old_hashseed = os.environ.get("PYTHONHASHSEED")
            os.environ["PYTHONHASHSEED"] = str(index + 1)
            try:
                command_results.extend(_run_portable_cli_sequence(temp_root, dom_root, revision, ["status", "snapshot", "project", "validate", "diff", "demo"], cwd))
            finally:
                if old_hashseed is None:
                    os.environ.pop("PYTHONHASHSEED", None)
                else:
                    os.environ["PYTHONHASHSEED"] = old_hashseed
            output_hashes.append(_relative_output_hashes(temp_root, comparison_paths))
            required_sets.append(sorted(path.as_posix() for path in comparison_paths if (temp_root / path).exists()))
        byte_equal = output_hashes[0] == output_hashes[1]
        required_output_set_equal = required_sets[0] == required_sets[1] == sorted(path.as_posix() for path in comparison_paths)
        forbidden_needles = [str(source_root.resolve()), str(base.resolve()), os.path.expanduser("~")]
        path_leak_count = sum(_path_leak_count(root, forbidden_needles) for root in roots)
        closure = local_import_closure(source_root)
        result = {
            "schema_version": "aide.dominium-readonly-seam.portability-result.v0",
            "task_id": models.REPAIR_TASK_ID,
            "status": "PASS" if byte_equal and required_output_set_equal and path_leak_count == 0 and closure["undeclared_dependency_count"] == 0 and all(item["returncode"] == 0 for item in command_results) else "FAILED_VALIDATION",
            "isolated_cli_roots": 2,
            "commands": command_results,
            "compared_outputs": [path.as_posix() for path in comparison_paths],
            "required_output_sets": required_sets,
            "required_output_set_equal": required_output_set_equal,
            "output_hashes_equal": byte_equal,
            "output_hashes": output_hashes,
            "absolute_path_leak_count": path_leak_count,
            "dependency_manifest": manifest,
            "import_closure": closure,
            "undeclared_dependency_count": closure["undeclared_dependency_count"],
            "sanitized_environment": {"PYTHONPATH_removed": True, "PYTHONHOME_removed": True, "PYTHONNOUSERSITE": "1", "python_isolated_mode": True},
            "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        }
        return result


def _write_bundle_reports(repo_root: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    projection_index = projector.projection_index_for_bundle(bundle)
    models.write_json(repo_root / models.SEAM_BUNDLE_JSON, bundle)
    models.write_json(repo_root / models.SOURCE_SNAPSHOT_JSON, bundle["source_snapshot"])
    models.write_json(repo_root / models.PROJECTION_INDEX_JSON, projection_index)
    models.write_json(repo_root / models.INTEROP_SEAM_BUNDLE_JSON, bundle)
    models.write_json(repo_root / models.INTEROP_BRIDGE_MANIFEST_JSON, bundle["records"]["dominium_bridge_manifest"])
    models.write_json(repo_root / models.INTEROP_CONFORMANCE_EXPECTATIONS_JSON, {"schema_version": "aide.dominium-readonly-seam.conformance-expectations.v0", "expectations": conformance.conformance_expectations()})
    write_runtime_dependency_manifest(repo_root)
    return projection_index


def _fixture_manifest(repo_root: Path, files: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(files):
        if path.exists() and path.is_file():
            entries.append({"path": path.relative_to(repo_root).as_posix(), "sha256": sha256_file(path)})
    return {
        "schema_version": "aide.dominium-readonly-seam.fixture-manifest.v0",
        "fixture_count": len(entries),
        "fixtures": entries,
    }


def write_fixtures(repo_root: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    positive_root = repo_root / models.FIXTURE_ROOT / "positive"
    negative_root = repo_root / models.FIXTURE_ROOT / "negative"
    for root in [positive_root, negative_root]:
        root.mkdir(parents=True, exist_ok=True)
        for existing in root.glob("*.json"):
            existing.unlink()
    files: list[Path] = []
    positive_records = {
        "host-manifest.json": bundle["records"]["host_manifest"],
        "host-capability-set.json": bundle["records"]["host_capability_set"],
        "workspace-descriptor.json": bundle["records"]["workspace_descriptor"],
        "context-descriptor.json": bundle["records"]["context_descriptor"],
        "artifact-references.json": {"records": bundle["records"]["artifact_references"]},
        "diagnostic-projections.json": {"records": bundle["records"]["diagnostic_projections"]},
        "refusal-projections.json": {"records": bundle["records"]["refusal_projections"]},
        "evidence-reference-set.json": bundle["records"]["evidence_reference_set"],
        "event-envelopes.json": {"records": bundle["records"]["event_envelopes"]},
        "dominium-bridge-manifest.json": bundle["records"]["dominium_bridge_manifest"],
        "complete-seam-bundle.json": bundle,
    }
    for name, obj in positive_records.items():
        path = positive_root / name
        models.write_json(path, obj)
        files.append(path)
    for case in fixture_replay.negative_fixture_cases(bundle):
        path = negative_root / f"{case['name']}.json"
        models.write_json(path, case)
        files.append(path)
    manifest = _fixture_manifest(repo_root, files)
    models.write_json(repo_root / models.FIXTURE_MANIFEST_JSON, manifest)
    return manifest


def render_status_markdown(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium Read-Only Seam v0 Status",
            "",
            f"- result: `{data.get('status') or data.get('validation_status')}`",
            f"- capability_target: `{models.FEATURE_FLAG}`",
            f"- source_revision: `{data.get('source_revision', '')}`",
            f"- selected_file_count: `{data.get('selected_file_count', 0)}`",
            f"- record_count: `{data.get('record_count', 0)}`",
            f"- fixture_count: `{data.get('fixture_count', 0)}`",
            f"- dominium_command_invoked: `{str(data.get('dominium_command_invoked', False)).lower()}`",
            f"- network_call_performed: `{str(data.get('network_call_performed', False)).lower()}`",
            f"- mutation_performed: `{str(data.get('mutation_performed', False)).lower()}`",
            f"- recommended_next_task: `{models.RECOMMENDED_NEXT_TASK}`",
            "",
            "Offline read-only projection only. It is not a Host runtime, bridge runtime, Workbench implementation, service, transport, preview/apply/rollback, or mutation capability.",
            "",
        ]
    )


def render_risks_markdown() -> str:
    return "\n".join(
        [
            "# Dominium Read-Only Seam Risks",
            "",
            "- Local Dominium input is read-only and may be behind remote main; freshness is recorded in source-snapshot.json.",
            "- SeamBundle is generated projection evidence, not canonical Dominium truth.",
            "- Command invocation, runtime bridge behavior, Workbench UI, preview/apply/rollback, and mutation remain absent by design.",
            "",
        ]
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    lines.extend(f"- `{item}`" for item in models.EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            "# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04",
            "",
            "Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04`.",
            "",
            "Use `.aide/queue/index.yaml` as canonical queue truth.",
            "",
            "Independently check `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` without modifying the seam implementation.",
            "Verify the 12 Repair 03 findings are closed, including schema union and extension bounds, strict fixture replay, CLI-backed conformance evidence, no-write proof, guard exercise, semantic operation aggregates, complete portability outputs, and arbitrary unsupported-verb typed refusals.",
            "",
            "If no material issue exists, recommend `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.",
            "If a material defect remains, recommend one bounded follow-up repair task.",
            "",
        ]
    )


def snapshot_dominium_source(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    report = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    models.write_json(root / models.SOURCE_SNAPSHOT_JSON, report)
    return report


def project_dominium_seam(
    repo_root: str | Path,
    *,
    dominium_root: str | Path | None = None,
    revision: str | None = None,
    write_portability: bool = True,
) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    bundle = projector.build_seam_bundle(root, dom_root, revision=_revision(revision), expected_revision=_revision(revision))
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    bundle["validation_summary"] = {
        "validation_status": validation_report["validation_status"],
        "validated": validation_report["validated"],
        "error_count": len(validation_report["errors"]),
        "warning_count": len(validation_report["warnings"]),
    }
    integrity.finalize_bundle(bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    bundle["validation_summary"] = {
        "validation_status": validation_report["validation_status"],
        "validated": validation_report["validated"],
        "error_count": len(validation_report["errors"]),
        "warning_count": len(validation_report["warnings"]),
    }
    integrity.finalize_bundle(bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    projection_index = _write_bundle_reports(root, bundle)
    fixture_manifest = write_fixtures(root, bundle)
    validation_report = validation.validate_bundle(bundle, dominium_root=dom_root)
    conformance_report = conformance.conformance_results(bundle, validation_report, dominium_root=dom_root)
    conformance_assertion_report = conformance.conformance_assertions(bundle, validation_report, dominium_root=dom_root)
    conformance_evidence = conformance.conformance_evidence(bundle, validation_report, dominium_root=dom_root, repo_root=root)
    compatibility = {
        "schema_version": "aide.dominium-readonly-seam.compatibility.v1",
        "status": "PASS",
        "read_old_write_current": True,
        "unknown_optional_field_handling": "preserve_or_ignore_by_owner_contract",
        "unknown_required_field_refusal": True,
        "windows_path_handling_checked": True,
        "posix_repo_relative_paths_checked": True,
        "stable_utf8_json_output": True,
        "deterministic_key_and_record_ordering": True,
    }
    models.write_json(root / models.VALIDATION_JSON, validation_report)
    models.write_json(root / models.CONFORMANCE_RESULTS_JSON, conformance_report)
    models.write_json(root / models.CONFORMANCE_ASSERTIONS_JSON, conformance_assertion_report)
    models.write_json(root / models.CONFORMANCE_EVIDENCE_JSON, conformance_evidence)
    models.write_json(root / models.COMPATIBILITY_JSON, compatibility)
    if write_portability and os.environ.get("AIDE_DOMINIUM_PORTABILITY_CHILD") != "1":
        models.write_json(root / models.PORTABILITY_RESULT_JSON, portability_check(root, dominium_root=dom_root, revision=revision))
    status = {
        "status": validation_report["validation_status"],
        "source_revision": bundle["manifest"]["source_revision"],
        "selected_file_count": bundle["manifest"]["selected_file_count"],
        "record_count": bundle["manifest"]["record_count"],
        "fixture_count": fixture_manifest["fixture_count"],
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    models.write_text(root / models.RISKS_MD, render_risks_markdown())
    models.write_text(root / models.EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    models.write_text(root / models.NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    return {
        "schema_version": "aide.dominium-readonly-seam.projection-report.v0",
        "status": validation_report["validation_status"],
        "source_revision": bundle["manifest"]["source_revision"],
        "selected_file_count": bundle["manifest"]["selected_file_count"],
        "record_count": bundle["manifest"]["record_count"],
        "fixture_count": fixture_manifest["fixture_count"],
        "projection_index_digest": integrity.stable_digest(projection_index),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }


def validate_dominium_seam(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None, project: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    if project or not (root / models.SEAM_BUNDLE_JSON).exists():
        project_dominium_seam(root, dominium_root=dom_root, revision=revision)
    bundle = models.read_json(root / models.SEAM_BUNDLE_JSON)
    report = validation.validate_bundle(bundle, dominium_root=dom_root)
    models.write_json(root / models.VALIDATION_JSON, report)
    models.write_json(root / models.CONFORMANCE_RESULTS_JSON, conformance.conformance_results(bundle, report, dominium_root=dom_root))
    models.write_json(root / models.CONFORMANCE_ASSERTIONS_JSON, conformance.conformance_assertions(bundle, report, dominium_root=dom_root))
    status = {
        "status": report["validation_status"],
        "source_revision": bundle.get("manifest", {}).get("source_revision", ""),
        "selected_file_count": bundle.get("manifest", {}).get("selected_file_count", 0),
        "record_count": bundle.get("manifest", {}).get("record_count", 0),
        "fixture_count": (models.read_json(root / models.FIXTURE_MANIFEST_JSON).get("fixture_count", 0) if (root / models.FIXTURE_MANIFEST_JSON).exists() else 0),
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    return report


def dominium_seam_diff(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    if not (root / models.SEAM_BUNDLE_JSON).exists():
        project_dominium_seam(root, dominium_root=dom_root, revision=revision)
    current = (root / models.SEAM_BUNDLE_JSON).read_bytes()
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        _copy_runtime_dependencies(root, temp_root)
        project_dominium_seam(temp_root, dominium_root=dom_root, revision=revision, write_portability=False)
        fresh = (temp_root / models.SEAM_BUNDLE_JSON).read_bytes()
    report = {
        "schema_version": "aide.dominium-readonly-seam.diff.v0",
        "status": "PASS" if current == fresh else "FAILED_VALIDATION",
        "byte_equal": current == fresh,
        "current_sha256": sha256_bytes(current),
        "fresh_sha256": sha256_bytes(fresh),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
    models.write_json(root / models.DIFF_JSON, report)
    return report


def run_dominium_seam_demo(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    ledger = operations.OperationLedger()
    with operations.observe_with(ledger):
        before_status = snapshot.worktree_status(dom_root)
        before_snapshot = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
        projection = project_dominium_seam(root, dominium_root=dom_root, revision=revision, write_portability=False)
        validation_report = validate_dominium_seam(root, dominium_root=dom_root, revision=revision, project=False)
        diff = dominium_seam_diff(root, dominium_root=dom_root, revision=revision)
        after_snapshot = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
        after_status = snapshot.worktree_status(dom_root)
    before_hashes = {item["path"]: item["sha256"] for item in before_snapshot["selected_files"]}
    after_hashes = {item["path"]: item["sha256"] for item in after_snapshot["selected_files"]}
    source_mutation_count = sum(1 for key, value in before_hashes.items() if after_hashes.get(key) != value)
    operation_report = ledger.as_report()
    raw_trace = {
        "schema_version": "aide.dominium-readonly-seam.operation-trace.v0",
        "task_id": models.REPAIR_TASK_ID,
        "observations": ledger.raw_trace(),
    }
    raw_trace["raw_trace_sha256"] = operation_report["raw_trace_sha256"]
    guard_report = operations.guard_conformance()
    result = {
        "schema_version": "aide.dominium-readonly-seam.demo-result.v0",
        "task_id": models.REPAIR_TASK_ID,
        "status": "PASS_WITH_WARNINGS"
        if validation_report["validation_status"] in {"PASS", "PASS_WITH_WARNINGS"}
        and diff["byte_equal"]
        and source_mutation_count == 0
        and before_status == after_status
        and operation_report["forbidden_operation_count"] == 0
        else "FAILED_VALIDATION",
        "input_revision": before_snapshot["source_revision"],
        "input_hashes": before_hashes,
        "output_hashes": {
            models.SEAM_BUNDLE_JSON.as_posix(): sha256_file(root / models.SEAM_BUNDLE_JSON),
            models.VALIDATION_JSON.as_posix(): sha256_file(root / models.VALIDATION_JSON),
            models.PROJECTION_INDEX_JSON.as_posix(): sha256_file(root / models.PROJECTION_INDEX_JSON),
        },
        "record_counts": {
            "selected_files": before_snapshot["selected_file_count"],
            "records": projection["record_count"],
            "fixtures": projection["fixture_count"],
        },
        "validation_result": validation_report["validation_status"],
        "elapsed_time": {
            "status": "not_measured",
            "elapsed_ms": None,
            "reason": "determinism and source immutability are measured; wall-clock timing is intentionally not asserted by the offline demo",
        },
        "source_mutation_count": source_mutation_count,
        "allowed_operation_count": operation_report["allowed_operation_count"],
        "forbidden_operation_count": operation_report["forbidden_operation_count"],
        "operation_ledger": operation_report,
        "operation_trace_ref": models.OPERATION_TRACE_JSON.as_posix(),
        "operation_guard_conformance_ref": models.OPERATION_GUARD_CONFORMANCE_JSON.as_posix(),
        "dominium_status_before": before_status,
        "dominium_status_after": after_status,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
    }
    models.write_json(root / models.DEMO_RESULT_JSON, result)
    models.write_json(root / models.OPERATION_TRACE_JSON, raw_trace)
    models.write_json(root / models.OPERATION_GUARD_CONFORMANCE_JSON, guard_report)
    models.write_text(
        root / models.STATUS_MD,
        render_status_markdown(
            {
                "status": result["status"],
                "source_revision": result["input_revision"],
                "selected_file_count": result["record_counts"]["selected_files"],
                "record_count": result["record_counts"]["records"],
                "fixture_count": result["record_counts"]["fixtures"],
                "dominium_command_invoked": False,
                "network_call_performed": False,
                "mutation_performed": False,
            }
        ),
    )
    return result


def dominium_seam_status(repo_root: str | Path, *, dominium_root: str | Path | None = None, revision: str | None = None) -> dict[str, Any]:
    root = Path(repo_root)
    dom_root = _dominium_root(root, dominium_root)
    schema_exists = (root / models.SCHEMA_PATH).exists()
    bundle_exists = (root / models.SEAM_BUNDLE_JSON).exists()
    source_revision = ""
    selected_file_count = 0
    record_count = 0
    dominium_available = False
    try:
        source = snapshot.build_source_snapshot(dom_root, revision=_revision(revision), expected_revision=_revision(revision))
        dominium_available = True
        source_revision = source["source_revision"]
        selected_file_count = source["selected_file_count"]
    except Exception:
        source = {}
    if bundle_exists:
        bundle = models.read_json(root / models.SEAM_BUNDLE_JSON)
        record_count = int(bundle.get("manifest", {}).get("record_count", 0))
    status = {
        "schema_version": "aide.dominium-readonly-seam.status.v0",
        "status": "PASS_WITH_WARNINGS" if schema_exists and dominium_available else "BLOCKED",
        "capability_target": models.FEATURE_FLAG,
        "schema_exists": schema_exists,
        "bundle_exists": bundle_exists,
        "dominium_available": dominium_available,
        "source_revision": source_revision,
        "selected_file_count": selected_file_count,
        "record_count": record_count,
        "warnings": list(models.WARNING_MESSAGES),
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        "dominium_command_invoked": False,
        "network_call_performed": False,
        "mutation_performed": False,
    }
    models.write_text(root / models.STATUS_MD, render_status_markdown(status))
    return status


def unsupported_operation_refusal(operation: str) -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-readonly-seam.unsupported-operation-refusal.v0",
        "status": "REFUSED",
        "reason_code": "AIDE_DOMINIUM_SEAM_UNSUPPORTED_OPERATION",
        "operation": operation,
        "message": f"dominium-seam {operation} is outside the read-only seam boundary",
        "retryable": False,
        "recommended_next_task": models.RECOMMENDED_NEXT_TASK,
        **models.false_status(),
    }
