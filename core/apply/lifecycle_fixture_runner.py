"""Lifecycle fixture temp-workspace runner.

This module implements one protocol-shaped vertical slice for the
install-managed-section fixture. It copies canonical fixture input to a
generated temp workspace, mutates only that workspace, verifies the expected
postimage, and writes evidence reports. It is not a general lifecycle apply
engine.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from core.apply import managed_sections
except ModuleNotFoundError:
    import importlib.util

    _managed_sections_path = Path(__file__).with_name("managed_sections.py")
    _managed_sections_spec = importlib.util.spec_from_file_location(
        "aide_core_managed_sections_fallback",
        _managed_sections_path,
    )
    if _managed_sections_spec is None or _managed_sections_spec.loader is None:
        raise
    managed_sections = importlib.util.module_from_spec(_managed_sections_spec)
    _managed_sections_spec.loader.exec_module(managed_sections)


STATUS_SCHEMA_VERSION = "aide.lifecycle-fixture-runner-status.v0"
RUN_SCHEMA_VERSION = "aide.lifecycle-fixture-run.v0"
VERIFY_SCHEMA_VERSION = "aide.lifecycle-fixture-verify.v0"
TRANSACTION_SCHEMA_VERSION = "aide.lifecycle-fixture-temp-transaction.v0"
ROLLBACK_SCHEMA_VERSION = "aide.lifecycle-fixture-temp-rollback-record.v0"

SUPPORTED_SCENARIO = "install-managed-section"
SUPPORTED_MODE = "apply-temp"
FIXTURE_ROOT = Path(".aide/examples/apply/lifecycle-fixtures")
REPORT_ROOT = Path(".aide/reports/lifecycle-fixture-runner")
WORKSPACE_ROOT = REPORT_ROOT / "workspaces"
LATEST_WORKSPACE_NAME = "latest"
LATEST_RUN_JSON = REPORT_ROOT / "latest-run.json"
LATEST_RUN_MD = REPORT_ROOT / "latest-run.md"
LATEST_VERIFY_JSON = REPORT_ROOT / "latest-verify.json"
LATEST_VERIFY_MD = REPORT_ROOT / "latest-verify.md"
LATEST_STATUS_JSON = REPORT_ROOT / "status.json"
LATEST_STATUS_MD = REPORT_ROOT / "status.md"
LATEST_TRANSACTION_JSON = REPORT_ROOT / "latest-transaction-plan.json"
LATEST_ROLLBACK_JSON = REPORT_ROOT / "latest-rollback-record.json"

CAPABILITY_LABEL = "fixture_temp_apply_only"
NOT_CAPABILITIES = [
    "active_repo_apply",
    "target_repo_apply",
    "general_lifecycle_apply",
    "rollback_execution",
    "uninstall_execution",
    "release_ready",
    "production_ready",
]


class LifecycleFixtureError(ValueError):
    """Raised when a lifecycle fixture run must fail closed."""


class PathJailError(LifecycleFixtureError):
    """Raised when a planned mutation path escapes the temp workspace."""


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    mode: str
    plan: dict[str, Any]
    scenario_record: dict[str, Any]
    target_fixture_root: Path
    expected_state_root: Path
    target_path: str
    expected_preimage_hash: str
    expected_postimage_hash: str
    section_name: str
    replacement_block: str
    canonical_target_file: Path
    expected_target_file: Path
    rollback_record_file: Path


@dataclass(frozen=True)
class FixtureRun:
    scenario: Scenario
    workspace_root: Path
    run_id: str
    report_path: Path
    rollback_record_path: Path
    transaction_plan_path: Path


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleFixtureError(f"could not load JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LifecycleFixtureError(f"JSON root must be an object: {path}")
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text_hash(path: Path) -> str:
    return managed_sections.compute_text_hash(path.read_text(encoding="utf-8"))


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_relative_path(path_value: str | Path) -> str:
    raw = str(path_value).replace("\\", "/")
    if not raw or "\0" in raw:
        raise PathJailError("path must be non-empty and must not contain NUL")
    if raw.startswith("/") or raw.startswith("~") or re.match(r"^[A-Za-z]:", raw):
        raise PathJailError("absolute paths are not allowed")
    if any(ch in raw for ch in "*?[]"):
        raise PathJailError("wildcard paths are not allowed")
    path = PurePosixPath(raw)
    if any(part == ".." for part in path.parts):
        raise PathJailError("parent traversal is not allowed")
    if str(path) in {"", "."}:
        raise PathJailError("workspace root is not a valid mutation path")
    return path.as_posix()


def resolve_under_jail(workspace_root: Path, relative_path: str | Path) -> Path:
    """Resolve a mutating path under a workspace root and reject escapes."""

    rel = normalize_relative_path(relative_path)
    root = workspace_root.resolve()
    target = (root / rel).resolve(strict=False)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PathJailError("resolved path escaped temp workspace") from exc
    return target


def section_block(text: str, section_name: str, path: str) -> tuple[int, int, dict[str, Any]]:
    section = managed_sections.parse_managed_section(text, section_name=section_name, path=path)
    if not section.get("allowed"):
        raise LifecycleFixtureError(f"managed section is not valid in {path}: {section.get('blocked_reason')}")
    start_marker = str(section["start_marker"])
    end_marker = str(section["end_marker"])
    start = text.find(start_marker)
    end_start = text.find(end_marker, int(section["content_end"]))
    if start < 0 or end_start < 0:
        raise LifecycleFixtureError(f"managed section markers could not be located in {path}")
    return start, end_start + len(end_marker), section


def replace_managed_section_block(before_text: str, expected_text: str, section_name: str, path: str) -> tuple[str, bool]:
    """Replace the marker-bounded generated block while preserving manual text."""

    before_start, before_end, _before_section = section_block(before_text, section_name, path)
    expected_start, expected_end, _expected_section = section_block(expected_text, section_name, path)
    prefix = before_text[:before_start]
    suffix = before_text[before_end:]
    after_text = prefix + expected_text[expected_start:expected_end] + suffix
    manual_preserved = prefix == expected_text[:expected_start] and suffix == expected_text[expected_end:]
    return after_text, manual_preserved


class ScenarioLoader:
    """Load the single authorized lifecycle fixture scenario."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def load(self, scenario_id: str) -> Scenario:
        if scenario_id != SUPPORTED_SCENARIO:
            raise LifecycleFixtureError(f"unsupported lifecycle fixture scenario: {scenario_id}")

        scenarios_path = self.repo_root / FIXTURE_ROOT / "scenarios.json"
        plan_path = self.repo_root / FIXTURE_ROOT / "generated-plans/install-managed-section.plan.json"
        scenarios = load_json(scenarios_path)
        plan = load_json(plan_path)
        scenario_records = scenarios.get("scenarios", [])
        if not isinstance(scenario_records, list):
            raise LifecycleFixtureError("scenario metadata must contain a scenarios list")
        scenario_record = next(
            (record for record in scenario_records if isinstance(record, dict) and record.get("scenario_id") == scenario_id),
            None,
        )
        if scenario_record is None:
            raise LifecycleFixtureError(f"scenario metadata missing: {scenario_id}")
        if plan.get("scenario_id") != scenario_id:
            raise LifecycleFixtureError("generated plan scenario does not match requested scenario")

        operations = plan.get("explicit_operations", [])
        if not isinstance(operations, list) or len(operations) != 1:
            raise LifecycleFixtureError("install-managed-section requires exactly one explicit operation")
        operation = operations[0]
        if not isinstance(operation, dict) or operation.get("operation_type") != "update_managed_section":
            raise LifecycleFixtureError("install-managed-section requires one update_managed_section operation")
        target_path = normalize_relative_path(str(operation.get("path", "")))

        target_fixture_root = Path(str(plan.get("target_fixture_root", "")))
        expected_state_root = Path(str(plan.get("expected_state_ref", "")))
        if not str(target_fixture_root) or not str(expected_state_root):
            raise LifecycleFixtureError("generated plan missing target or expected state roots")

        canonical_target_file = self.repo_root / target_fixture_root / target_path
        expected_target_file = self.repo_root / expected_state_root / target_path
        rollback_record_file = self.repo_root / FIXTURE_ROOT / "rollback-records/install-managed-section.rollback.json"
        expected_report_ref = plan.get("expected_report_ref")
        if expected_report_ref and not (self.repo_root / str(expected_report_ref)).exists():
            raise LifecycleFixtureError("expected report ref is missing")
        if not canonical_target_file.exists():
            raise LifecycleFixtureError(f"canonical target fixture missing: {canonical_target_file}")
        if not expected_target_file.exists():
            raise LifecycleFixtureError(f"expected target fixture missing: {expected_target_file}")
        if not rollback_record_file.exists():
            raise LifecycleFixtureError(f"rollback record missing: {rollback_record_file}")

        preimage_hash = _required_hash(plan, "preimage_hash_requirements", target_path)
        postimage_hash = _required_hash(plan, "postimage_hash_requirements", target_path)
        if text_hash(canonical_target_file) != preimage_hash:
            raise LifecycleFixtureError("canonical target preimage hash does not match generated plan")
        if text_hash(expected_target_file) != postimage_hash:
            raise LifecycleFixtureError("expected target postimage hash does not match generated plan")

        before_text = canonical_target_file.read_text(encoding="utf-8")
        expected_text = expected_target_file.read_text(encoding="utf-8")
        sections = managed_sections.find_managed_sections(before_text)
        if len(sections) != 1:
            raise LifecycleFixtureError("selected fixture must contain exactly one managed section")
        section_name = str(sections[0]["section_name"])
        replacement_start, replacement_end, _expected_section = section_block(expected_text, section_name, target_path)
        replacement_block = expected_text[replacement_start:replacement_end]

        return Scenario(
            scenario_id=scenario_id,
            mode=SUPPORTED_MODE,
            plan=plan,
            scenario_record=scenario_record,
            target_fixture_root=target_fixture_root,
            expected_state_root=expected_state_root,
            target_path=target_path,
            expected_preimage_hash=preimage_hash,
            expected_postimage_hash=postimage_hash,
            section_name=section_name,
            replacement_block=replacement_block,
            canonical_target_file=canonical_target_file,
            expected_target_file=expected_target_file,
            rollback_record_file=rollback_record_file,
        )


class TransactionCompiler:
    """Compile the lifecycle scenario to a temp-workspace transaction plan."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def compile(self, scenario: Scenario, workspace_root: Path, run_id: str) -> dict[str, Any]:
        target = resolve_under_jail(workspace_root, scenario.target_path)
        expected_text = scenario.expected_target_file.read_text(encoding="utf-8")
        return {
            "schema_version": TRANSACTION_SCHEMA_VERSION,
            "transaction_id": f"lifecycle-fixture-{scenario.scenario_id}-{SUPPORTED_MODE}",
            "run_id": run_id,
            "scenario_id": scenario.scenario_id,
            "mode": SUPPORTED_MODE,
            "workspace_root": repo_rel(self.repo_root, workspace_root),
            "operation_allowlist": ["update_managed_section"],
            "operations": [
                {
                    "operation_id": "op-install-managed-section",
                    "operation_type": "update_managed_section",
                    "path": scenario.target_path,
                    "resolved_path": repo_rel(self.repo_root, target),
                    "section_name": scenario.section_name,
                    "expected_preimage_hash": scenario.expected_preimage_hash,
                    "expected_postimage_hash": scenario.expected_postimage_hash,
                    "expected_postimage": expected_text,
                    "path_jail_checked": True,
                }
            ],
            "capability_label": CAPABILITY_LABEL,
            "not_capabilities": list(NOT_CAPABILITIES),
            "canonical_fixture_mutation": False,
            "target_repo_mutation": False,
            "rollback_execution": False,
        }


class ScopedExecutor:
    """Apply the compiled transaction only inside the temp workspace."""

    def apply(self, plan: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
        operations = plan.get("operations", [])
        if not isinstance(operations, list) or len(operations) != 1:
            raise LifecycleFixtureError("temp runner supports exactly one operation")
        operation = operations[0]
        if not isinstance(operation, dict):
            raise LifecycleFixtureError("operation must be an object")
        if operation.get("operation_type") != "update_managed_section":
            raise LifecycleFixtureError("only update_managed_section is supported")
        target = resolve_under_jail(workspace_root, str(operation.get("path", "")))
        before_text = managed_sections.load_text_file_safely(target)
        preimage_hash = managed_sections.compute_text_hash(before_text)
        if preimage_hash != operation.get("expected_preimage_hash"):
            raise LifecycleFixtureError("temp workspace preimage hash does not match plan")
        expected_text = str(operation.get("expected_postimage", ""))
        section_name = str(operation.get("section_name", ""))
        after_text, manual_preserved = replace_managed_section_block(
            before_text,
            expected_text,
            section_name,
            str(operation.get("path", "")),
        )
        postimage_hash = managed_sections.compute_text_hash(after_text)
        if postimage_hash != operation.get("expected_postimage_hash"):
            raise LifecycleFixtureError("planned postimage hash does not match expected postimage hash")
        target.write_text(after_text, encoding="utf-8", newline="")
        actual_text = managed_sections.load_text_file_safely(target)
        actual_hash = managed_sections.compute_text_hash(actual_text)
        if actual_hash != postimage_hash:
            raise LifecycleFixtureError("actual temp postimage hash does not match planned postimage hash")
        return {
            "schema_version": "aide.lifecycle-fixture-temp-apply-report.v0",
            "operation_id": operation.get("operation_id"),
            "operation_type": "update_managed_section",
            "path": operation.get("path"),
            "resolved_path": operation.get("resolved_path"),
            "preimage_hash": preimage_hash,
            "postimage_hash": postimage_hash,
            "actual_postimage_hash": actual_hash,
            "manual_content_preserved": manual_preserved,
            "target_files_mutated": True,
            "mutation_scope": "temp_workspace_only",
            "path_jail_checked": True,
        }


class FixtureVerifier:
    """Verify latest lifecycle fixture run evidence and workspace state."""

    def verify(self, repo_root: Path, run_report: dict[str, Any] | None = None) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        report = run_report if run_report is not None else self._load_latest_run(repo_root, checks)
        if report is None:
            return self._verification_report(repo_root, "FAIL", checks)

        workspace = _repo_path(repo_root, report.get("workspace_root"))
        rollback = _repo_path(repo_root, report.get("rollback_record_path"))
        temp_target = _repo_path(repo_root, report.get("temp_target_path"))
        expected_file = _repo_path(repo_root, report.get("expected_postimage_ref"))
        canonical_file = _repo_path(repo_root, report.get("canonical_preimage_ref"))

        _check(checks, workspace.exists() and workspace.is_dir(), "referenced temp workspace exists", workspace.as_posix())
        _check(checks, rollback.exists() and rollback.is_file(), "referenced rollback record exists", rollback.as_posix())
        _check(checks, temp_target.exists() and temp_target.is_file(), "referenced temp target exists", temp_target.as_posix())
        _check(checks, expected_file.exists() and expected_file.is_file(), "referenced expected postimage exists", expected_file.as_posix())
        _check(checks, canonical_file.exists() and canonical_file.is_file(), "referenced canonical preimage exists", canonical_file.as_posix())

        if temp_target.exists() and expected_file.exists():
            actual_hash = text_hash(temp_target)
            expected_hash = text_hash(expected_file)
            _check(checks, actual_hash == report.get("postimage_hash"), "report postimage hash matches temp file", actual_hash)
            _check(checks, expected_hash == report.get("postimage_hash"), "expected postimage hash matches report", expected_hash)
            _check(
                checks,
                temp_target.read_text(encoding="utf-8") == expected_file.read_text(encoding="utf-8"),
                "temp target content matches expected postimage",
                repo_rel(repo_root, temp_target),
            )
        if canonical_file.exists():
            _check(
                checks,
                text_hash(canonical_file) == report.get("canonical_preimage_hash_after"),
                "canonical fixture hash after run matches report",
                repo_rel(repo_root, canonical_file),
            )
            _check(
                checks,
                report.get("canonical_preimage_hash_before") == report.get("canonical_preimage_hash_after"),
                "canonical fixture hash unchanged",
                str(report.get("canonical_preimage_hash_after", "")),
            )
        _check(checks, report.get("target_files_mutated") is True, "run report records temp target mutation", "temp only")
        _check(checks, report.get("canonical_fixture_mutated") is False, "run report records canonical fixture not mutated", "canonical read-only")
        _check(checks, report.get("capability_label") == CAPABILITY_LABEL, "capability label is bounded", str(report.get("capability_label", "")))
        _check(checks, report.get("not_capabilities") == NOT_CAPABILITIES, "negative capability labels are explicit", ",".join(NOT_CAPABILITIES))

        status = "PASS" if all(check["result"] == "PASS" for check in checks) else "FAIL"
        return self._verification_report(repo_root, status, checks, report)

    def _load_latest_run(self, repo_root: Path, checks: list[dict[str, Any]]) -> dict[str, Any] | None:
        path = repo_root / LATEST_RUN_JSON
        if not path.exists():
            _check(checks, False, "latest-run.json exists", LATEST_RUN_JSON.as_posix())
            return None
        try:
            data = load_json(path)
        except LifecycleFixtureError as exc:
            _check(checks, False, "latest-run.json parses", str(exc))
            return None
        _check(checks, True, "latest-run.json parses", LATEST_RUN_JSON.as_posix())
        return data

    def _verification_report(
        self,
        repo_root: Path,
        status: str,
        checks: list[dict[str, Any]],
        run_report: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        report = {
            "schema_version": VERIFY_SCHEMA_VERSION,
            "generated_at": timestamp(),
            "status": status,
            "result": status,
            "run_report_path": LATEST_RUN_JSON.as_posix(),
            "checks": checks,
            "capability_label": CAPABILITY_LABEL,
            "not_capabilities": list(NOT_CAPABILITIES),
            "canonical_fixture_mutation": False,
            "target_repo_mutation": False,
            "provider_model_calls": False,
            "gateway_calls": False,
            "network_calls": False,
        }
        if run_report is not None:
            report["run_id"] = run_report.get("run_id")
            report["scenario_id"] = run_report.get("scenario_id")
            report["workspace_root"] = run_report.get("workspace_root")
        write_json(repo_root / LATEST_VERIFY_JSON, report)
        write_text(repo_root / LATEST_VERIFY_MD, render_verify_markdown(report))
        return report


class EvidenceReporter:
    """Write lifecycle fixture runner reports."""

    def write_status(self, repo_root: Path) -> dict[str, Any]:
        latest_run_exists = (repo_root / LATEST_RUN_JSON).exists()
        data = {
            "schema_version": STATUS_SCHEMA_VERSION,
            "generated_at": timestamp(),
            "result": "PASS",
            "supported_scenarios": [SUPPORTED_SCENARIO],
            "supported_modes": [SUPPORTED_MODE],
            "report_root": REPORT_ROOT.as_posix(),
            "latest_run_exists": latest_run_exists,
            "latest_run": LATEST_RUN_JSON.as_posix() if latest_run_exists else "",
            "capability_label": CAPABILITY_LABEL,
            "not_capabilities": list(NOT_CAPABILITIES),
            "canonical_fixture_mutation": False,
            "target_repo_mutation": False,
            "provider_model_calls": False,
            "gateway_calls": False,
            "network_calls": False,
        }
        write_json(repo_root / LATEST_STATUS_JSON, data)
        write_text(repo_root / LATEST_STATUS_MD, render_status_markdown(data))
        return data

    def write_run(
        self,
        repo_root: Path,
        fixture_run: FixtureRun,
        transaction_plan: dict[str, Any],
        execution_report: dict[str, Any],
        canonical_hash_before: str,
        canonical_hash_after: str,
    ) -> dict[str, Any]:
        scenario = fixture_run.scenario
        temp_target = fixture_run.workspace_root / scenario.target_path
        rollback_record = {
            "schema_version": ROLLBACK_SCHEMA_VERSION,
            "rollback_id": f"rollback-{fixture_run.run_id}",
            "run_id": fixture_run.run_id,
            "scenario_id": scenario.scenario_id,
            "mode": SUPPORTED_MODE,
            "path": scenario.target_path,
            "operation_type": "update_managed_section",
            "preimage_hash": scenario.expected_preimage_hash,
            "postimage_hash": scenario.expected_postimage_hash,
            "restore_text_hash": scenario.expected_preimage_hash,
            "apply_allowed": False,
            "rollback_execution": False,
            "review_required": True,
            "capability_label": CAPABILITY_LABEL,
            "not_capabilities": list(NOT_CAPABILITIES),
        }
        write_json(fixture_run.transaction_plan_path, transaction_plan)
        write_json(fixture_run.rollback_record_path, rollback_record)
        report = {
            "schema_version": RUN_SCHEMA_VERSION,
            "generated_at": timestamp(),
            "run_id": fixture_run.run_id,
            "scenario_id": scenario.scenario_id,
            "mode": SUPPORTED_MODE,
            "status": "PASS",
            "result": "PASS",
            "workspace_root": repo_rel(repo_root, fixture_run.workspace_root),
            "temp_target_path": repo_rel(repo_root, temp_target),
            "canonical_preimage_ref": repo_rel(repo_root, scenario.canonical_target_file),
            "expected_postimage_ref": repo_rel(repo_root, scenario.expected_target_file),
            "source_plan_ref": repo_rel(repo_root, repo_root / FIXTURE_ROOT / "generated-plans/install-managed-section.plan.json"),
            "source_rollback_record_ref": repo_rel(repo_root, scenario.rollback_record_file),
            "transaction_plan_path": repo_rel(repo_root, fixture_run.transaction_plan_path),
            "rollback_record_path": repo_rel(repo_root, fixture_run.rollback_record_path),
            "operation_report": execution_report,
            "preimage_hash": scenario.expected_preimage_hash,
            "postimage_hash": scenario.expected_postimage_hash,
            "canonical_preimage_hash_before": canonical_hash_before,
            "canonical_preimage_hash_after": canonical_hash_after,
            "manual_content_preserved": bool(execution_report.get("manual_content_preserved")),
            "target_files_mutated": True,
            "canonical_fixture_mutated": canonical_hash_before != canonical_hash_after,
            "mutation_scope": "temp_workspace_only",
            "path_jail_checked": True,
            "capability_label": CAPABILITY_LABEL,
            "not_capabilities": list(NOT_CAPABILITIES),
            "active_repo_apply": False,
            "target_repo_apply": False,
            "general_lifecycle_apply": False,
            "rollback_execution": False,
            "uninstall_execution": False,
            "release_ready": False,
            "production_ready": False,
            "provider_model_calls": False,
            "gateway_calls": False,
            "network_calls": False,
            "review_gate": "needs_review",
        }
        write_json(fixture_run.report_path, report)
        write_json(repo_root / LATEST_RUN_JSON, report)
        write_text(repo_root / LATEST_RUN_MD, render_run_markdown(report))
        return report


def lifecycle_fixture_status(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    return EvidenceReporter().write_status(root)


def run_lifecycle_fixture(
    repo_root: str | Path,
    scenario_id: str = SUPPORTED_SCENARIO,
    mode: str = SUPPORTED_MODE,
    *,
    workspace_name: str = LATEST_WORKSPACE_NAME,
) -> dict[str, Any]:
    root = Path(repo_root)
    if mode != SUPPORTED_MODE:
        raise LifecycleFixtureError(f"unsupported lifecycle fixture mode: {mode}")
    scenario = ScenarioLoader(root).load(scenario_id)
    run_id = f"{scenario_id}-{mode}-{workspace_name}"
    workspace_root = root / WORKSPACE_ROOT / workspace_name
    reset_workspace(root, workspace_root)
    shutil.copytree(root / scenario.target_fixture_root, workspace_root)

    temp_target = resolve_under_jail(workspace_root, scenario.target_path)
    if text_hash(temp_target) != scenario.expected_preimage_hash:
        raise LifecycleFixtureError("copied temp fixture preimage hash does not match scenario")
    canonical_hash_before = text_hash(scenario.canonical_target_file)
    compiler = TransactionCompiler(root)
    transaction_plan = compiler.compile(scenario, workspace_root, run_id)
    execution_report = ScopedExecutor().apply(transaction_plan, workspace_root)
    canonical_hash_after = text_hash(scenario.canonical_target_file)

    fixture_run = FixtureRun(
        scenario=scenario,
        workspace_root=workspace_root,
        run_id=run_id,
        report_path=root / REPORT_ROOT / "run-report.json",
        rollback_record_path=root / LATEST_ROLLBACK_JSON,
        transaction_plan_path=root / LATEST_TRANSACTION_JSON,
    )
    report = EvidenceReporter().write_run(
        root,
        fixture_run,
        transaction_plan,
        execution_report,
        canonical_hash_before,
        canonical_hash_after,
    )
    verify_report = FixtureVerifier().verify(root, report)
    if verify_report.get("status") != "PASS":
        raise LifecycleFixtureError("lifecycle fixture run failed verification")
    return report


def verify_lifecycle_fixture(repo_root: str | Path) -> dict[str, Any]:
    return FixtureVerifier().verify(Path(repo_root))


def reset_workspace(repo_root: Path, workspace_root: Path) -> None:
    report_root = (repo_root / REPORT_ROOT).resolve()
    workspace_parent = workspace_root.parent.resolve()
    try:
        workspace_parent.relative_to(report_root)
    except ValueError as exc:
        raise LifecycleFixtureError("workspace parent must stay under lifecycle fixture report root") from exc
    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    workspace_root.parent.mkdir(parents=True, exist_ok=True)


def render_status_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Lifecycle Fixture Runner Status",
        "",
        f"- result: {data.get('result')}",
        f"- capability_label: {data.get('capability_label')}",
        f"- latest_run_exists: {str(data.get('latest_run_exists', False)).lower()}",
        "- target_repo_mutation: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        "",
        "## Supported",
        "",
    ]
    for scenario in data.get("supported_scenarios", []):
        lines.append(f"- scenario: {scenario}")
    for mode in data.get("supported_modes", []):
        lines.append(f"- mode: {mode}")
    return "\n".join(lines) + "\n"


def render_run_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Lifecycle Fixture Run",
            "",
            f"- result: {report.get('result')}",
            f"- run_id: {report.get('run_id')}",
            f"- scenario_id: {report.get('scenario_id')}",
            f"- mode: {report.get('mode')}",
            f"- workspace_root: {report.get('workspace_root')}",
            f"- temp_target_path: {report.get('temp_target_path')}",
            f"- capability_label: {report.get('capability_label')}",
            "- mutation_scope: temp_workspace_only",
            f"- manual_content_preserved: {str(report.get('manual_content_preserved', False)).lower()}",
            f"- canonical_fixture_mutated: {str(report.get('canonical_fixture_mutated', True)).lower()}",
            "- target_repo_mutation: false",
            "- provider_or_model_calls: none",
            "- network_calls: none",
            "",
        ]
    )


def render_verify_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Lifecycle Fixture Verify",
        "",
        f"- result: {report.get('result')}",
        f"- run_id: {report.get('run_id', '')}",
        f"- capability_label: {report.get('capability_label')}",
        "- target_repo_mutation: false",
        "- provider_or_model_calls: none",
        "- network_calls: none",
        "",
        "## Checks",
        "",
    ]
    for check in report.get("checks", []):
        if isinstance(check, dict):
            lines.append(f"- {check.get('result')}: {check.get('message')} ({check.get('detail', '')})")
    return "\n".join(lines) + "\n"


def _required_hash(plan: dict[str, Any], key: str, target_path: str) -> str:
    records = plan.get(key, [])
    if not isinstance(records, list):
        raise LifecycleFixtureError(f"{key} must be a list")
    for record in records:
        if isinstance(record, dict) and record.get("path") == target_path and record.get("required") is True:
            value = record.get("sha256")
            if isinstance(value, str) and value.startswith("sha256:"):
                return value
    raise LifecycleFixtureError(f"missing required hash in {key} for {target_path}")


def _repo_path(repo_root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value:
        return repo_root / "__missing__"
    return repo_root / value


def _check(checks: list[dict[str, Any]], passed: bool, message: str, detail: str) -> None:
    checks.append({"result": "PASS" if passed else "FAIL", "message": message, "detail": detail})
