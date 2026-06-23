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


TASK_ID = "AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
BUILD_TASK_ID = "AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
ACCEPT_TASK_ID = "AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
REPAIR_TASK_ID = "AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-REPAIR-01"
CAPABILITY_ID = "dominium.validation.run"
REPORT_ROOT = Path(".aide/reports/dominium-workunit-validation-slice")
CHECK_REPORT_ROOT = Path(".aide/reports/dominium-workunit-validation-slice-check")
CHECK_EVIDENCE_ROOT = Path(".aide/queue/AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/evidence")
SOURCE_PATH = Path("core/interop/dominium/workunit_validation.py")


def stable_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def workspace_digest(root: Path, rel: Path) -> str:
    workspace = root / rel
    entries: list[dict[str, str]] = []
    for path in sorted(item for item in workspace.rglob("*") if item.is_file()):
        entries.append({"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)})
    return sha256_bytes(stable_json(entries).encode("utf-8"))


def check(condition: bool, assertion_id: str, description: str, expected: Any, observed: Any, refs: list[str]) -> dict[str, Any]:
    return {
        "id": assertion_id,
        "description": description,
        "outcome": "PASS" if condition else "FAIL",
        "expected": expected,
        "observed": observed,
        "evidence_refs": refs,
    }


def copy_slice_runtime(repo_root: Path, target: Path, module: Any) -> None:
    rels = {
        ".aide/scripts/aide_lite.py",
        "core/__init__.py",
        "core/interop/__init__.py",
        "core/interop/dominium/__init__.py",
        "core/interop/dominium/workunit_validation.py",
        "core/protocol/__init__.py",
        "core/protocol/envelope.py",
        "core/protocol/reference_id.py",
        "core/protocol/workunit.py",
        "core/protocol/evidence_packet.py",
        "core/protocol/event_record.py",
        ".aide/protocol/aide-workunit.schema.json",
        ".aide/protocol/aide-context-pack-v2.schema.json",
        ".aide/protocol/aide-evidence-packet.schema.json",
        ".aide/protocol/aide-event-record.schema.json",
        ".aide/queue/AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01/status.yaml",
        ".aide/reports/dominium-readonly-seam-v0-accept/acceptance-report.json",
    }
    rels.update(rel.as_posix() for rel in module.source_paths())
    rels.update(path.relative_to(repo_root).as_posix() for path in (repo_root / "core/interop/dominium").glob("*.py"))
    for rel in sorted(rels):
        source = repo_root / rel
        if source.exists() and source.is_file():
            destination = target / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def run_clean_cli(repo_root: Path, module: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        copy_slice_runtime(repo_root, root, module)
        command = [sys.executable, str(root / ".aide/scripts/aide_lite.py"), "--repo-root", str(root), "dominium-workunit-validation", "run"]
        result = subprocess.run(command, check=False, capture_output=True, text=True, cwd=str(root))
        if result.returncode != 0:
            raise RuntimeError(f"clean CLI run failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
        projection = read_json(root / module.PROJECTION_JSON)
        reports = {
            "stdout_sha256": sha256_bytes(result.stdout.encode("utf-8")),
            "stderr_sha256": sha256_bytes(result.stderr.encode("utf-8")),
            "projection_sha256": sha256_file(root / module.PROJECTION_JSON),
            "context_pack_sha256": sha256_file(root / module.CONTEXT_PACK_JSON),
            "workunit_sha256": sha256_file(root / module.WORKUNIT_JSON),
            "evidence_packet_sha256": sha256_file(root / module.EVIDENCE_PACKET_JSON),
            "event_record_sha256": sha256_file(root / module.EVENT_RECORD_JSON),
            "invocation_result_sha256": sha256_file(root / module.INVOCATION_RESULT_JSON),
        }
        streams = {"stdout": result.stdout, "stderr": result.stderr}
        return projection, reports, streams


def scan_for_local_leaks(paths: list[Path], repo_root: Path) -> list[dict[str, str]]:
    leaks: list[dict[str, str]] = []
    patterns = [
        re.escape(str(repo_root).replace("\\", "\\\\")),
        re.escape(str(repo_root)),
        r"[A-Za-z]:\\",
        r"BEGIN (RSA|OPENSSH|PRIVATE) KEY",
        r"\bsk-[A-Za-z0-9]{20,}",
        r"api[_-]?key\s*[:=]",
        r"password\s*[:=]",
        r"bearer\s+[A-Za-z0-9]",
    ]
    for base in paths:
        for path in sorted(item for item in base.rglob("*") if item.is_file()):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in patterns:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    leaks.append({"path": path.as_posix(), "pattern": pattern})
    return leaks


def load_module(repo_root: Path) -> Any:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from core.interop.dominium import workunit_validation

    return workunit_validation


def main() -> int:
    repo_root = Path.cwd()
    module = load_module(repo_root)
    assertions: list[dict[str, Any]] = []
    warnings: list[str] = []

    source_text = (repo_root / SOURCE_PATH).read_text(encoding="utf-8")
    fixture_backed = "local_fixture_callable" in source_text and "def expected_success_result" in source_text
    live_dominium_call = any(token in source_text for token in ["subprocess.run", "dominium.validation.run(", "import dominium"])

    assertions.append(check(fixture_backed, "authority.fixture_backed_adapter_declared", "Source declares the underlying executor as a fixture-backed local callable.", True, fixture_backed, [SOURCE_PATH.as_posix()]))
    assertions.append(check(not live_dominium_call, "authority.no_live_dominium_executor", "Source does not invoke a Dominium-owned executable or command implementation.", False, live_dominium_call, [SOURCE_PATH.as_posix()]))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        module.write_fixture_workspace(root)
        clean_before = workspace_digest(root, module.WORKSPACE_ROOT)
        observed_calls = {"count": 0}
        original_success = module.expected_success_result

        def observed_success() -> dict[str, Any]:
            observed_calls["count"] += 1
            return original_success()

        module.expected_success_result = observed_success
        try:
            success = module.invoke_capability(root, CAPABILITY_ID)
            clean_after = workspace_digest(root, module.WORKSPACE_ROOT)
            unsupported = module.invoke_capability(root, "dominium.future.unsupported")
            missing_count_after_unsupported = observed_calls["count"]

            request_path = root / module.VALIDATION_REQUEST_JSON
            request = read_json(request_path)
            request["target"] = "mutated-invalid-target"
            write_json(request_path, request)
            malformed = module.invoke_capability(root, CAPABILITY_ID)
            malformed_count_after = observed_calls["count"]
        finally:
            module.expected_success_result = original_success

    assertions.append(check(observed_calls["count"] == 1, "executor.clean_success_entered_once", "The success executor function was independently instrumented and entered once for a clean supported request.", 1, observed_calls["count"], [SOURCE_PATH.as_posix()]))
    assertions.append(check(success.get("result") == "PASS" and success.get("underlying_executor") == "local_fixture_callable", "result.typed_fixture_success", "Supported request returns a typed fixture-backed success result.", "PASS/local_fixture_callable", {"result": success.get("result"), "underlying_executor": success.get("underlying_executor")}, [".aide/fixtures/dominium-workunit-validation-slice/workspace/validation-request.json"]))
    assertions.append(check(clean_before == clean_after, "state.fixture_workspace_unchanged", "Before/after workspace digests are independently recomputed and unchanged.", clean_before, clean_after, [".aide/fixtures/dominium-workunit-validation-slice/workspace"]))
    assertions.append(check(unsupported.get("result") == "REFUSED" and missing_count_after_unsupported == 1, "refusal.unsupported_no_executor", "Unsupported capabilities return typed refusal and do not enter the success executor.", {"result": "REFUSED", "executor_count": 1}, {"result": unsupported.get("result"), "executor_count": missing_count_after_unsupported}, [SOURCE_PATH.as_posix()]))
    assertions.append(check(malformed.get("result") == "REFUSED" and malformed.get("reason_code") == "AIDE_DOMINIUM_WORKUNIT_VALIDATION_INVALID_REQUEST" and malformed_count_after == 1, "refusal.malformed_request_no_executor", "Malformed registered requests return typed refusal and do not enter the success executor.", {"result": "REFUSED", "executor_count": 1}, {"result": malformed.get("result"), "reason_code": malformed.get("reason_code"), "executor_count": malformed_count_after}, [SOURCE_PATH.as_posix()]))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        module.write_fixture_workspace(root)
        original = module.invoke_capability(root, CAPABILITY_ID)
        request_path = root / module.VALIDATION_REQUEST_JSON
        request = read_json(request_path)
        request["benign_metadata"] = "digest-probe"
        write_json(request_path, request)
        changed = module.invoke_capability(root, CAPABILITY_ID)
    assertions.append(check(original.get("validation_request_sha256") != changed.get("validation_request_sha256"), "result.hash_derived_from_fixture_input", "Success result includes hashes derived from fixture input bytes.", "changed hash after benign metadata", {"original": original.get("validation_request_sha256"), "changed": changed.get("validation_request_sha256")}, [".aide/fixtures/dominium-workunit-validation-slice/workspace/validation-request.json"]))

    first_projection, first_hashes, first_streams = run_clean_cli(repo_root, module)
    second_projection, second_hashes, second_streams = run_clean_cli(repo_root, module)
    assertions.append(check(first_projection == second_projection, "determinism.semantic_projection_equal", "Two clean runs produce identical semantic projection JSON.", True, first_projection == second_projection, [".aide/reports/dominium-workunit-validation-slice/projection.json"]))
    assertions.append(check(first_hashes == second_hashes, "determinism.output_hashes_equal", "Two clean runs produce identical deterministic output hashes and CLI streams.", True, first_hashes == second_hashes, [".aide/reports/dominium-workunit-validation-slice"]))

    build_reports = [repo_root / REPORT_ROOT, repo_root / ".aide/fixtures/dominium-workunit-validation-slice"]
    leaks = scan_for_local_leaks(build_reports, repo_root)
    assertions.append(check(not leaks, "leak_scan.no_absolute_paths_or_secrets", "Generated build reports and fixtures do not leak local absolute paths or secret-like values.", [], leaks, [REPORT_ROOT.as_posix(), ".aide/fixtures/dominium-workunit-validation-slice"]))

    context = read_json(repo_root / REPORT_ROOT / "context-descriptor.json")
    context_pack = read_json(repo_root / REPORT_ROOT / "context-pack.json")
    workunit = read_json(repo_root / REPORT_ROOT / "workunit.json")
    evidence = read_json(repo_root / REPORT_ROOT / "evidence-packet.json")
    event = read_json(repo_root / REPORT_ROOT / "event-record.json")
    invocation = read_json(repo_root / REPORT_ROOT / "invocation-result.json")

    assertions.append(check(context.get("kind") == "ContextDescriptor" and context.get("spec", {}).get("registered_capability_id") == CAPABILITY_ID, "record.context_descriptor_valid", "ContextDescriptor identifies the registered capability.", CAPABILITY_ID, context.get("spec", {}).get("registered_capability_id"), [str(REPORT_ROOT / "context-descriptor.json")]))
    assertions.append(check(context_pack.get("kind") == "ContextPack" and context_pack.get("spec", {}).get("registered_capability_id") == CAPABILITY_ID, "record.context_pack_valid", "ContextPack identifies the registered capability.", CAPABILITY_ID, context_pack.get("spec", {}).get("registered_capability_id"), [str(REPORT_ROOT / "context-pack.json")]))
    assertions.append(check(workunit.get("kind") == "WorkUnit" and workunit.get("spec", {}).get("authorized_invocation_count") == 1, "record.workunit_valid", "WorkUnit records a single authorized invocation.", 1, workunit.get("spec", {}).get("authorized_invocation_count"), [str(REPORT_ROOT / "workunit.json")]))
    claims = {claim.get("id"): claim.get("status") for claim in evidence.get("spec", {}).get("claims", [])}
    assertions.append(check(claims.get("exactly_one_invocation") == "supported" and invocation.get("invocation_count") == 1, "evidence.claims_match_behavior", "EvidencePacket claims match independently observed invocation behavior.", "supported/1", {"claim": claims.get("exactly_one_invocation"), "invocation_count": invocation.get("invocation_count")}, [str(REPORT_ROOT / "evidence-packet.json"), str(REPORT_ROOT / "invocation-result.json")]))

    event_spec = event.get("spec", {})
    refs_resolve = (
        event_spec.get("causation", {}).get("ref") == workunit.get("spec", {}).get("task_id", "").join(["aide://workunit/", ""]) and
        event_spec.get("correlation", {}).get("ref") == context_pack.get("spec", {}).get("context_pack_ref") and
        event_spec.get("subject", {}).get("ref") == evidence.get("spec", {}).get("evidence_ref") and
        evidence.get("spec", {}).get("evidence_ref") in event_spec.get("evidence_refs", [])
    )
    assertions.append(check(refs_resolve, "event.refs_resolve", "EventRecord causation, correlation, subject, and evidence refs resolve to generated records.", True, refs_resolve, [str(REPORT_ROOT / "event-record.json")]))

    false_fields = [
        "arbitrary_shell_command_executed",
        "private_tool_called",
        "broad_dispatch_used",
        "network_call_performed",
        "provider_or_model_called",
        "worker_executed",
        "workbench_apply_performed",
        "preview_or_apply_performed",
        "patch_transaction_applied",
        "source_repository_mutated",
        "target_repository_mutated",
        "branch_or_worktree_created",
        "github_mutation_performed",
        "release_or_promotion_performed",
    ]
    false_boundary_ok = all(invocation.get(field) is False for field in false_fields)
    assertions.append(check(false_boundary_ok, "boundary.false_fields_complete", "Forbidden boundary fields remain boolean false in the invocation result.", "all false", {field: invocation.get(field) for field in false_fields}, [str(REPORT_ROOT / "invocation-result.json")]))

    status_text = (repo_root / ".aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/status.yaml").read_text(encoding="utf-8")
    warning_precise = "fixture" in status_text and "not a general Dominium command runner" in status_text
    assertions.append(check(warning_precise, "authority.warning_is_precise", "Build status distinguishes fixture-backed adapter execution from live Dominium command execution.", True, warning_precise, [".aide/queue/AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01/status.yaml"]))

    failed = [item for item in assertions if item["outcome"] != "PASS"]
    if failed:
        result = "FAILED_VALIDATION"
        next_task = REPAIR_TASK_ID
    elif fixture_backed and not live_dominium_call:
        result = "PASS_WITH_WARNINGS"
        next_task = ACCEPT_TASK_ID
        warnings.append("The checked capability is fixture_backed_dominium_validation_adapter, not live Dominium command execution.")
    else:
        result = "PASS"
        next_task = ACCEPT_TASK_ID

    report = {
        "schema_version": "aide.dominium-workunit-validation-slice-check.v1",
        "task_id": TASK_ID,
        "source_task_id": BUILD_TASK_ID,
        "source_commit": "8d8f511c77388b96118eb530f5361090b66911c1",
        "result": result,
        "material_finding_count": len(failed),
        "assertions": assertions,
        "warnings": warnings,
        "accepted_capability_label": "fixture_backed_dominium_validation_adapter" if result == "PASS_WITH_WARNINGS" else "dominium_validation_run",
        "live_dominium_command_execution_proven": bool(live_dominium_call),
        "fixture_backed_adapter_execution_proven": fixture_backed,
        "first_run_hashes": first_hashes,
        "second_run_hashes": second_hashes,
        "first_cli_stdout_sha256": first_hashes["stdout_sha256"],
        "next_task": next_task,
    }
    write_json(repo_root / CHECK_EVIDENCE_ROOT / "independent-check-result.json", report)
    write_json(repo_root / CHECK_REPORT_ROOT / "check-report.json", report)
    write_text(repo_root / CHECK_REPORT_ROOT / "status.md", render_status(report))
    write_text(repo_root / CHECK_REPORT_ROOT / "authority-review.md", render_authority(report))
    write_text(repo_root / CHECK_REPORT_ROOT / "evidence-review.md", render_evidence(report))
    write_text(repo_root / CHECK_REPORT_ROOT / "next-task-prompt.md", render_next_task(report))
    return 0 if result in {"PASS", "PASS_WITH_WARNINGS"} else 1


def render_status(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium WorkUnit Validation Slice Check",
            "",
            f"- task_id: `{report['task_id']}`",
            f"- source_task_id: `{report['source_task_id']}`",
            f"- result: `{report['result']}`",
            f"- material_finding_count: `{report['material_finding_count']}`",
            f"- accepted_capability_label: `{report['accepted_capability_label']}`",
            f"- live_dominium_command_execution_proven: `{str(report['live_dominium_command_execution_proven']).lower()}`",
            f"- fixture_backed_adapter_execution_proven: `{str(report['fixture_backed_adapter_execution_proven']).lower()}`",
            f"- next_task: `{report['next_task']}`",
            "",
        ]
    )


def render_authority(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Authority Review",
            "",
            "The check proves the fixture-backed AIDE adapter contract.",
            "",
            f"- fixture_backed_adapter_execution_proven: `{str(report['fixture_backed_adapter_execution_proven']).lower()}`",
            f"- live_dominium_command_execution_proven: `{str(report['live_dominium_command_execution_proven']).lower()}`",
            f"- accepted_capability_label: `{report['accepted_capability_label']}`",
            "",
            "The build must not be described as live Dominium command execution until a future task invokes a Dominium-owned implementation.",
            "",
        ]
    )


def render_evidence(report: dict[str, Any]) -> str:
    lines = ["# Evidence Review", ""]
    for assertion in report["assertions"]:
        lines.append(f"- {assertion['outcome']}: `{assertion['id']}` - {assertion['description']}")
    lines.append("")
    return "\n".join(lines)


def render_next_task(report: dict[str, Any]) -> str:
    if report["result"] in {"PASS", "PASS_WITH_WARNINGS"}:
        return "\n".join(
            [
                "# AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01",
                "",
                "Create and process `AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.",
                "",
                "Accept the capability precisely as `fixture_backed_dominium_validation_adapter` unless later evidence proves live Dominium-owned command execution.",
                "",
            ]
        )
    return "\n".join(
        [
            "# AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-REPAIR-01",
            "",
            "Repair the material findings from `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01` without widening the authority boundary.",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
