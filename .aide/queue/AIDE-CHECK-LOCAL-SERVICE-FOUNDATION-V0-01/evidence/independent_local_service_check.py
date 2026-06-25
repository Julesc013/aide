from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01"
CAPABILITY = "local_service_foundation_v0"
NEXT_TASK = "AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01"
REPAIR_TASK = "AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-REPAIR-01"

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[4]
EVIDENCE_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID / "evidence"
REPORT_ROOT = REPO_ROOT / ".aide/reports/local-service-foundation-v0-check"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.service.artifact_store import ArtifactStore, ArtifactStoreError, sha256_bytes  # noqa: E402
from core.service.sqlite_store import LocalServiceError, SQLiteStore, digest_json  # noqa: E402


@dataclass(frozen=True)
class AssertionResult:
    id: str
    category: str
    description: str
    outcome: str
    severity: str
    expected: Any
    observed: Any
    evidence_refs: list[str]
    source_finding_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "description": self.description,
            "outcome": self.outcome,
            "severity": self.severity,
            "expected": self.expected,
            "observed": self.observed,
            "evidence_refs": self.evidence_refs,
            "source_finding_id": self.source_finding_id,
        }


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_status() -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return result.stdout


def assert_result(
    assertions: list[AssertionResult],
    *,
    assertion_id: str,
    category: str,
    description: str,
    condition: bool,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    severity: str = "material",
) -> None:
    assertions.append(
        AssertionResult(
            id=assertion_id,
            category=category,
            description=description,
            outcome="PASS" if condition else "FAIL",
            severity=severity,
            expected=expected,
            observed=observed,
            evidence_refs=evidence_refs,
        )
    )


def load_source_task() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_task = REPO_ROOT / ".aide/queue" / SOURCE_TASK_ID / "task.yaml"
    source_status = REPO_ROOT / ".aide/queue" / SOURCE_TASK_ID / "status.yaml"
    validation = REPO_ROOT / ".aide/reports/local-service-foundation-v0/validation.json"
    return (
        read_scalar_yaml(source_task),
        read_scalar_yaml(source_status),
        json.loads(validation.read_text(encoding="utf-8")),
    )


def read_scalar_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        value = raw_value.strip()
        if value in {"", ">", "|"}:
            continue
        if value == "null":
            data[key] = None
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            try:
                data[key] = int(value)
            except ValueError:
                data[key] = value.strip("\"'")
    return data


def run_cli_init_fixture() -> tuple[int, str, str, bool]:
    before = git_status()
    result = subprocess.run(
        [sys.executable, ".aide/scripts/aide_lite.py", "local-service", "init-fixture"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    after = git_status()
    return result.returncode, result.stdout, result.stderr, before == after


def exercise_store(assertions: list[AssertionResult]) -> None:
    with tempfile.TemporaryDirectory(prefix="aide-local-service-check-") as tmp:
        root = Path(tmp)
        db_path = root / "state.sqlite"
        store = SQLiteStore(db_path)
        try:
            first_version = store.initialize()
            second_version = store.initialize()
            raw_conn = sqlite3.connect(db_path)
            try:
                tables = {
                    row[0]
                    for row in raw_conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                }
            finally:
                raw_conn.close()
            expected_tables = {"migrations", "objects", "events", "artifact_metadata", "idempotency", "cursors"}
            assert_result(
                assertions,
                assertion_id="migrations.idempotent_schema",
                category="migrations",
                description="Migrations are deterministic and idempotent.",
                condition=first_version == 1 and second_version == 1 and expected_tables.issubset(tables),
                expected={"version": 1, "tables": sorted(expected_tables)},
                observed={"versions": [first_version, second_version], "tables": sorted(tables)},
                evidence_refs=[rel(SCRIPT_PATH)],
            )

            obj = store.put_object("aide://object/check", "CheckObject", {"value": 1})
            listed = store.list_objects(kind="CheckObject")
            read = store.get_object("aide://object/check")
            conflict_refused = False
            try:
                store.put_object("aide://object/check", "CheckObject", {"value": 2}, expected_version=99)
            except LocalServiceError as exc:
                conflict_refused = str(exc) == "resource_version_conflict"
            assert_result(
                assertions,
                assertion_id="objects.versioned_put_get_list",
                category="objects",
                description="Object put/get/list works and stale resource versions fail closed.",
                condition=obj.version == 1 and read.body == {"value": 1} and len(listed) == 1 and conflict_refused,
                expected=True,
                observed={"version": obj.version, "listed": len(listed), "conflict_refused": conflict_refused},
                evidence_refs=[rel(SCRIPT_PATH)],
            )

            _, seq_one = store.put_object_with_event(
                "aide://object/atomic",
                "CheckObject",
                {"value": "atomic"},
                event_ref="aide://event/atomic",
                event_type="object.updated",
            )
            rollback_refused = False
            rollback_absent = False
            try:
                store.put_object_with_event(
                    "aide://object/rollback",
                    "CheckObject",
                    {"value": "bad"},
                    event_ref="aide://event/rollback",
                    event_type="object.updated",
                    fail_after_object=True,
                )
            except LocalServiceError as exc:
                rollback_refused = str(exc) == "injected_atomic_failure"
            try:
                store.get_object("aide://object/rollback")
            except LocalServiceError as exc:
                rollback_absent = str(exc) == "object_missing"
            seq_two = store.append_event("aide://event/two", "event.two", "aide://object/atomic", {"n": 2})
            events = store.read_events_after(0)
            cursor = store.ack_cursor("aide://cursor/check", seq_two)
            assert_result(
                assertions,
                assertion_id="events.atomic_monotonic_cursor",
                category="events",
                description="Object/event commit is atomic, event sequences are monotonic, and cursors can resume.",
                condition=seq_one == 1 and [item["sequence"] for item in events] == [1, 2] and cursor["last_sequence"] == 2 and rollback_refused and rollback_absent,
                expected={"sequences": [1, 2], "cursor": 2},
                observed={"sequences": [item["sequence"] for item in events], "cursor": cursor, "rollback_refused": rollback_refused, "rollback_absent": rollback_absent},
                evidence_refs=[rel(SCRIPT_PATH)],
            )

            request_digest = digest_json({"request": "check"})
            first = store.record_idempotency("idem-check", request_digest, "aide://result/check")
            duplicate = store.record_idempotency("idem-check", request_digest, "aide://result/check")
            conflict = False
            try:
                store.record_idempotency("idem-check", digest_json({"request": "different"}), "aide://result/check")
            except LocalServiceError as exc:
                conflict = str(exc) == "idempotency_conflict"
            assert_result(
                assertions,
                assertion_id="idempotency.duplicate_conflict",
                category="idempotency",
                description="Idempotency duplicate reuses the result and conflicting requests fail closed.",
                condition=first["status"] == "recorded" and duplicate["status"] == "duplicate" and conflict,
                expected=True,
                observed={"first": first["status"], "duplicate": duplicate["status"], "conflict_refused": conflict},
                evidence_refs=[rel(SCRIPT_PATH)],
            )

            artifact_store = ArtifactStore(root)
            payload = b"local-service-check\n"
            write_one = artifact_store.write(payload)
            write_two = artifact_store.write(payload)
            store.record_artifact_metadata(write_one.digest, write_one.size, "text/plain", "check.txt")
            metadata = store.get_artifact_metadata(write_one.digest)
            digest_mismatch = False
            traversal = False
            try:
                artifact_store.write(payload, expected_digest="sha256:" + ("0" * 64))
            except ArtifactStoreError as exc:
                digest_mismatch = str(exc) == "artifact_digest_mismatch"
            try:
                artifact_store.read("sha256:../bad")
            except ArtifactStoreError as exc:
                traversal = str(exc) == "artifact_digest_invalid"
            assert_result(
                assertions,
                assertion_id="artifacts.cas_integrity",
                category="artifacts",
                description="Artifacts are content-addressed, deduplicated, digest-checked, and path-contained.",
                condition=write_one.digest == sha256_bytes(payload) and write_two.deduplicated and artifact_store.read(write_one.digest) == payload and metadata["digest"] == write_one.digest and digest_mismatch and traversal,
                expected=True,
                observed={"digest": write_one.digest, "deduplicated": write_two.deduplicated, "metadata": metadata, "digest_mismatch": digest_mismatch, "traversal": traversal},
                evidence_refs=[rel(SCRIPT_PATH)],
            )
        finally:
            store.close()

        reopened = SQLiteStore(db_path)
        try:
            persisted = reopened.get_object("aide://object/check").body == {"value": 1}
            persisted_events = [item["sequence"] for item in reopened.read_events_after(0)] == [1, 2]
        finally:
            reopened.close()
        assert_result(
            assertions,
            assertion_id="restart.persistence",
            category="restart",
            description="Objects and events persist across close/reopen.",
            condition=persisted and persisted_events,
            expected=True,
            observed={"object_persisted": persisted, "events_persisted": persisted_events},
            evidence_refs=[rel(SCRIPT_PATH)],
        )

        raw_conn = sqlite3.connect(db_path)
        try:
            raw_conn.execute("INSERT OR REPLACE INTO migrations(version, applied_at) VALUES (999, 'check')")
            raw_conn.commit()
        finally:
            raw_conn.close()
        future = SQLiteStore(db_path)
        try:
            future_refused = False
            try:
                future.initialize()
            except LocalServiceError as exc:
                future_refused = str(exc) == "future_migration"
        finally:
            future.close()
        assert_result(
            assertions,
            assertion_id="migrations.future_refusal",
            category="migrations",
            description="Future schema versions fail closed.",
            condition=future_refused,
            expected="future_migration",
            observed="future_migration" if future_refused else "not_refused",
            evidence_refs=[rel(SCRIPT_PATH)],
        )

        corrupt = root / "corrupt.sqlite"
        corrupt.write_text("not sqlite", encoding="utf-8")
        corrupted = SQLiteStore(corrupt)
        try:
            corruption_refused = False
            try:
                corrupted.health()
            except LocalServiceError:
                corruption_refused = True
        finally:
            corrupted.close()
        assert_result(
            assertions,
            assertion_id="health.corruption_refusal",
            category="health",
            description="Corrupted SQLite state is refused.",
            condition=corruption_refused,
            expected=True,
            observed=corruption_refused,
            evidence_refs=[rel(SCRIPT_PATH)],
        )


def run_check() -> dict[str, Any]:
    assertions: list[AssertionResult] = []
    source_task, source_status, validation = load_source_task()
    assert_result(
        assertions,
        assertion_id="source.task_chain",
        category="source-chain",
        description="Source build task reports the expected capability, result, evidence, and route.",
        condition=source_task.get("result") == "PASS_WITH_WARNINGS"
        and source_status.get("missing_evidence") == 0
        and validation.get("validated") is True
        and source_task.get("recommended_next_task") == TASK_ID,
        expected={"result": "PASS_WITH_WARNINGS", "missing_evidence": 0, "next": TASK_ID},
        observed={
            "result": source_task.get("result"),
            "missing_evidence": source_status.get("missing_evidence"),
            "validated": validation.get("validated"),
            "next": source_task.get("recommended_next_task"),
        },
        evidence_refs=[
            f".aide/queue/{SOURCE_TASK_ID}/task.yaml",
            f".aide/queue/{SOURCE_TASK_ID}/status.yaml",
            ".aide/reports/local-service-foundation-v0/validation.json",
        ],
    )

    returncode, stdout, stderr, status_unchanged = run_cli_init_fixture()
    cli_ok = returncode == 0 and "result: PASS_WITH_WARNINGS" in stdout and "state_root_is_temp: true" in stdout
    false_flags = all(f"{field}: false" in stdout for field in [
        "network_listener_opened",
        "scheduler_implemented",
        "worker_execution_implemented",
        "capability_execution_implemented",
        "trust_enforcement_implemented",
        "mcp_implemented",
        "workbench_implemented",
        "provider_model_calls_performed",
        "preview_apply_implemented",
        "repository_mutation_performed",
    ])
    assert_result(
        assertions,
        assertion_id="cli.init_fixture_boundary",
        category="cli",
        description="Public init-fixture CLI succeeds, uses temp state, preserves git status, and keeps false boundaries false.",
        condition=cli_ok and false_flags and status_unchanged and stderr == "",
        expected={"returncode": 0, "state_root_is_temp": True, "false_boundaries": True, "git_status_unchanged": True},
        observed={"returncode": returncode, "false_boundaries": false_flags, "git_status_unchanged": status_unchanged, "stderr": stderr},
        evidence_refs=[rel(SCRIPT_PATH)],
    )

    exercise_store(assertions)

    local_state_absent = not (REPO_ROOT / ".aide.local/service").exists()
    assert_result(
        assertions,
        assertion_id="local_state.absent",
        category="local-state",
        description="The check does not create committed or ignored live Service state under .aide.local/service.",
        condition=local_state_absent,
        expected="absent",
        observed="absent" if local_state_absent else "present",
        evidence_refs=[rel(SCRIPT_PATH)],
    )

    material_failures = [item for item in assertions if item.outcome != "PASS" and item.severity == "material"]
    status = "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES"
    report = {
        "task_id": TASK_ID,
        "checked_task": SOURCE_TASK_ID,
        "checked_capability": CAPABILITY,
        "status": status,
        "result": status,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "assertions": [item.to_dict() for item in assertions],
        "warnings": [
            "Service remains local, single-machine, no-network, and at-least-once only.",
            "Check uses production service modules as the system under test but does not repair them.",
        ],
        "explicit_non_capabilities": [
            "implementation_repair",
            "capability_acceptance",
            "network_api",
            "scheduler",
            "worker_execution",
            "capability_execution",
            "trust_enforcement",
            "mcp_runtime",
            "workbench_runtime",
            "exactly_once_delivery",
            "provider_model_calls",
            "preview_apply_rollback",
            "repository_mutation",
            "github_mutation",
            "release_or_promotion",
        ],
        "recommended_next_task": NEXT_TASK if not material_failures else REPAIR_TASK,
    }
    return report


def render_status_md(report: dict[str, Any]) -> str:
    lines = [
        "# Local Service Foundation v0 Check",
        "",
        f"- status: {report['status']}",
        f"- checked_task: {report['checked_task']}",
        f"- checked_capability: {report['checked_capability']}",
        f"- material_finding_count: {report['material_finding_count']}",
        f"- missing_evidence: {report['missing_evidence']}",
        f"- recommended_next_task: {report['recommended_next_task']}",
        "",
        "## Assertions",
        "",
    ]
    for assertion in report["assertions"]:
        lines.append(f"- {assertion['id']}: {assertion['outcome']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = run_check()
    write_json(EVIDENCE_ROOT / "check-report.json", report)
    write_json(EVIDENCE_ROOT / "assertions.json", report["assertions"])
    write_json(REPORT_ROOT / "check-report.json", report)
    write_json(REPORT_ROOT / "assertions.json", report["assertions"])
    (REPORT_ROOT / "status.md").parent.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "status.md").write_text(render_status_md(report), encoding="utf-8")
    (REPORT_ROOT / "explicit-non-capabilities.md").write_text(
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in report["explicit_non_capabilities"]) + "\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "next-task-prompt.md").write_text(
        "# Next Task Prompt\n\n```text\nCreate and process AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01.\n```\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "material_finding_count": report["material_finding_count"], "recommended_next_task": report["recommended_next_task"]}, sort_keys=True))
    return 0 if report["status"] == "PASS_WITH_WARNINGS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
