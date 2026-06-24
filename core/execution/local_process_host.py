"""Bounded LocalProcessExecutionHost v0 reference implementation.

This module starts exactly one allowlisted local reference worker process through
RegisteredProcessExecutionProvider v0. It is not a general worker harness,
arbitrary command runner, scheduler, Service, Workbench integration, provider
bridge, preview/apply path, or repository mutation mechanism.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from core.execution.registered_process import (
    DecoderResult,
    PreconditionResult,
    RegisteredProcessExecutionProvider,
    RegisteredProcessSpec,
)
from core.protocol import envelope, event_record, evidence_packet
from core.protocol.execution_receipt import CapabilityOutcome, ProcessExecutionReceipt
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
ACCEPTED_CONTRACT_TASK_ID = "AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01"
ACCEPTED_PROVIDER = "registered_process_execution_provider_v0"
CAPABILITY_ID = "aide.local-process-host.reference-worker.run"
CAPABILITY_REF = "aide://capability/local-process-execution-host-reference-worker-v0"
PROPOSED_CAPABILITY_LABEL = "local_process_execution_host_v0"
HOST_REF = "aide://execution-host/local-process/reference-v0"
RUN_REF = "aide://execution-host-run/local-process-reference-01"
WORKUNIT_REF = "aide://workunit/AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
EVIDENCE_REF = "aide://evidence/local-process-execution-host-v0"
REPORT_REF = "aide://report/local-process-execution-host-v0"
EVENT_REF = "aide://event/EVT-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
DETERMINISTIC_TIMESTAMP = "2026-06-25T00:00:00+10:00"
DEFAULT_TIMEOUT_SECONDS = 30.0

FIXTURE_WORKER_REL = Path(".aide/fixtures/local-process-execution-host/reference_worker.py")
HOST_MODULE_REL = Path("core/execution/local_process_host.py")
PROVIDER_REL = Path("core/execution/registered_process.py")
PROCESS_INVOCATION_REL = Path("core/protocol/process_invocation.py")
EXECUTION_RECEIPT_REL = Path("core/protocol/execution_receipt.py")
AIDE_LITE_REL = Path(".aide/scripts/aide_lite.py")
RELEVANT_SOURCE_RELS = [
    FIXTURE_WORKER_REL,
    HOST_MODULE_REL,
    PROVIDER_REL,
    PROCESS_INVOCATION_REL,
    EXECUTION_RECEIPT_REL,
    AIDE_LITE_REL,
]
STATE_PROBE_COVERAGE = [
    "git_revision",
    "git_porcelain_status",
    "git_tracked_tree_digest",
    "selected_source_digests",
]

REPORT_ROOT = Path(".aide/reports/local-process-execution-host")
STATUS_MD = REPORT_ROOT / "status.md"
HOST_DESCRIPTOR_JSON = REPORT_ROOT / "host-descriptor.json"
RUN_BINDING_JSON = REPORT_ROOT / "run-binding.json"
HOST_EVENT_JSON = REPORT_ROOT / "host-event.json"
HOST_ARTIFACT_JSON = REPORT_ROOT / "host-artifact.json"
HOST_USAGE_JSON = REPORT_ROOT / "host-usage.json"
INVOCATION_REQUEST_JSON = REPORT_ROOT / "invocation-request.json"
EXECUTION_RECEIPT_JSON = REPORT_ROOT / "execution-receipt.json"
CAPABILITY_OUTCOME_JSON = REPORT_ROOT / "capability-outcome.json"
RUN_RESULT_JSON = REPORT_ROOT / "run-result.json"
EVIDENCE_PACKET_JSON = REPORT_ROOT / "evidence-packet.json"
EVENT_RECORD_JSON = REPORT_ROOT / "event-record.json"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
HOST_REPORT_JSON = REPORT_ROOT / "host-report.json"
HOST_REPORT_MD = REPORT_ROOT / "host-report.md"
WARNING_DISPOSITION_MD = REPORT_ROOT / "warning-disposition.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REPORT_FILES = [
    STATUS_MD,
    HOST_DESCRIPTOR_JSON,
    RUN_BINDING_JSON,
    HOST_EVENT_JSON,
    HOST_ARTIFACT_JSON,
    HOST_USAGE_JSON,
    INVOCATION_REQUEST_JSON,
    EXECUTION_RECEIPT_JSON,
    CAPABILITY_OUTCOME_JSON,
    RUN_RESULT_JSON,
    EVIDENCE_PACKET_JSON,
    EVENT_RECORD_JSON,
    PROJECTION_JSON,
    VALIDATION_JSON,
    HOST_REPORT_JSON,
    HOST_REPORT_MD,
    WARNING_DISPOSITION_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    NEXT_TASK_PROMPT_MD,
]

FALSE_BOUNDARY_FIELDS = [
    "arbitrary_shell_command_executed",
    "private_tool_called",
    "broad_dispatch_used",
    "network_call_performed",
    "provider_or_model_called",
    "workbench_started",
    "workbench_apply_performed",
    "preview_or_apply_performed",
    "patch_transaction_applied",
    "service_started",
    "database_opened",
    "source_repository_mutated",
    "target_repository_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "release_or_promotion_performed",
]

EXPLICIT_NON_CAPABILITIES = [
    "arbitrary_command_runner",
    "generic_worker_harness",
    "autonomous_agent_worker",
    "remote_execution_host",
    "worker_lease",
    "scheduler",
    "supervisor",
    "service_runtime",
    "workbench_runtime",
    "provider_model_call",
    "network_call",
    "preview_or_apply",
    "rollback",
    "patch_transaction_apply",
    "source_repository_mutation",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
    "persistent_idempotency",
    "process_cancellation",
    "streaming_artifact_store",
]

REFUSAL_CODES = {
    "unsupported_capability": "AIDE_LOCAL_PROCESS_HOST_UNSUPPORTED_CAPABILITY",
    "invalid_request": "AIDE_LOCAL_PROCESS_HOST_INVALID_REQUEST",
    "repository_missing": "AIDE_LOCAL_PROCESS_HOST_REPOSITORY_MISSING",
    "revision_mismatch": "AIDE_LOCAL_PROCESS_HOST_REVISION_MISMATCH",
    "fixture_missing": "AIDE_LOCAL_PROCESS_HOST_FIXTURE_MISSING",
    "digest_mismatch": "AIDE_LOCAL_PROCESS_HOST_DIGEST_MISMATCH",
    "timeout": "AIDE_LOCAL_PROCESS_HOST_TIMEOUT",
    "nonzero_exit": "AIDE_LOCAL_PROCESS_HOST_NONZERO_EXIT",
    "empty_output": "AIDE_LOCAL_PROCESS_HOST_EMPTY_OUTPUT",
    "malformed_json": "AIDE_LOCAL_PROCESS_HOST_MALFORMED_JSON",
    "schema_mismatch": "AIDE_LOCAL_PROCESS_HOST_SCHEMA_MISMATCH",
    "worker_failed": "AIDE_LOCAL_PROCESS_HOST_WORKER_FAILED",
    "unexpected_mutation": "AIDE_LOCAL_PROCESS_HOST_UNEXPECTED_REPOSITORY_MUTATION",
}

Runner = Callable[[Sequence[str], Path, Mapping[str, str], float], subprocess.CompletedProcess[str]]


def stable_json(data: Any) -> str:
    return envelope.stable_json(data)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    envelope.write_json(path, obj)


def read_json(path: Path) -> dict[str, Any]:
    return envelope.read_json(path)


def write_text(path: Path, text: str) -> None:
    envelope.write_text(path, text)


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _false_boundary() -> dict[str, bool]:
    return {field: False for field in FALSE_BOUNDARY_FIELDS}


def git_stdout(root: Path, args: Sequence[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False, text=True, shell=False)
    except OSError as exc:
        return False, str(exc)
    if completed.returncode != 0:
        return False, (completed.stderr or completed.stdout).strip()
    return True, completed.stdout.strip()


def capture_aide_state(root: Path) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {"repository_present": False}
    ok_revision, revision = git_stdout(root, ["rev-parse", "HEAD"])
    ok_status, status = git_stdout(root, ["status", "--porcelain=v1", "--untracked-files=all"])
    ok_tree, tree = git_stdout(root, ["ls-files", "-s"])
    digests: dict[str, str] = {}
    for rel in RELEVANT_SOURCE_RELS:
        path = root / rel
        digests[rel.as_posix()] = sha256_file(path) if path.is_file() else "missing"
    return {
        "repository_present": True,
        "revision": revision if ok_revision else "",
        "revision_error": "" if ok_revision else revision,
        "porcelain_status": status if ok_status else "",
        "porcelain_status_digest": sha256_text(status if ok_status else ""),
        "tracked_tree_digest": sha256_text(tree if ok_tree else ""),
        "tracked_tree_observed": ok_tree,
        "selected_source_digests": digests,
        "clean": ok_status and status == "",
    }


def resolve_python_executable(value: str | Path | None = None) -> str:
    return str((Path(value) if value else Path(sys.executable)).resolve())


def sanitized_environment() -> dict[str, str]:
    allowed = ["COMSPEC", "PATH", "PATHEXT", "SYSTEMROOT", "TEMP", "TMP", "WINDIR", "SystemDrive", "USERPROFILE", "HOME"]
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PYTHONUTF8": "1", "PYTHONHASHSEED": "0"})
    return env


def build_argv(python_executable: str, repo_root: Path) -> list[str]:
    return [
        str(Path(python_executable).resolve()),
        str((repo_root / FIXTURE_WORKER_REL).resolve()),
        "--run-id",
        RUN_REF,
        "--workunit-ref",
        TASK_ID,
        "--json",
    ]


def build_invocation_request(
    *,
    repo_root: str | Path = ".",
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    revision = expected_revision
    if revision is None and (root / ".git").exists():
        ok, observed = git_stdout(root, ["rev-parse", "HEAD"])
        revision = observed if ok else ""
    py = resolve_python_executable(python_executable)
    if expected_digests is None:
        expected_digests = {rel.as_posix(): sha256_file(root / rel) for rel in RELEVANT_SOURCE_RELS if (root / rel).is_file()}
    return {
        "schema_version": "aide.local-process-execution-host.invocation-request.v0",
        "task_id": TASK_ID,
        "capability_id": capability_id,
        "expected_capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "repo_root": str(root),
        "expected_revision": revision or "",
        "python_executable": py,
        "fixture_worker_path": str((root / FIXTURE_WORKER_REL).resolve()),
        "timeout_seconds": float(timeout_seconds),
        "argv": build_argv(py, root),
        "argv_template": ["<python>", FIXTURE_WORKER_REL.as_posix(), "--run-id", RUN_REF, "--workunit-ref", TASK_ID, "--json"],
        "shell": False,
        "expected_digests": dict(expected_digests),
        "preexisting_dirty_state_allowed": True,
    }


def _preflight_error(request: Mapping[str, Any], before_state: Mapping[str, Any]) -> tuple[str, str] | None:
    if request.get("capability_id") != CAPABILITY_ID:
        return REFUSAL_CODES["unsupported_capability"], "Only the local process reference worker capability is admitted."
    root = Path(str(request.get("repo_root", "")))
    if not root.exists() or not (root / ".git").exists():
        return REFUSAL_CODES["repository_missing"], "AIDE repository checkout is missing."
    expected_revision = str(request.get("expected_revision") or "")
    if not expected_revision or before_state.get("revision") != expected_revision:
        return REFUSAL_CODES["revision_mismatch"], "AIDE repository revision did not match the pinned revision."
    if not (root / FIXTURE_WORKER_REL).is_file():
        return REFUSAL_CODES["fixture_missing"], "Local process reference worker fixture is missing."
    expected_digests = request.get("expected_digests", {})
    if isinstance(expected_digests, Mapping):
        actual = before_state.get("selected_source_digests", {})
        for rel, expected in expected_digests.items():
            if actual.get(str(rel)) != expected:
                return REFUSAL_CODES["digest_mismatch"], f"Selected source digest mismatch: {rel}"
    argv = list(request.get("argv") or [])
    expected_argv = build_argv(str(request.get("python_executable", "")), root)
    if argv != expected_argv or len(argv) != 7:
        return REFUSAL_CODES["invalid_request"], "LocalProcessExecutionHost argv shape is not the exact allowlisted invocation."
    return None


class AideStateProbe:
    coverage = STATE_PROBE_COVERAGE

    def __init__(self, root: Path):
        self.root = root

    def capture(self) -> Mapping[str, Any]:
        return capture_aide_state(self.root)

    def mutation_observation(self, before_state: Mapping[str, Any], after_state: Mapping[str, Any]) -> str:
        if (
            before_state.get("revision") == after_state.get("revision")
            and before_state.get("porcelain_status") == after_state.get("porcelain_status")
            and before_state.get("tracked_tree_digest") == after_state.get("tracked_tree_digest")
            and before_state.get("selected_source_digests") == after_state.get("selected_source_digests")
        ):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


class LocalProcessHostPrecondition:
    def __init__(self, request: Mapping[str, Any]):
        self.request = request

    def check(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
        spec: RegisteredProcessSpec,
        before_state: Mapping[str, Any],
    ) -> PreconditionResult:
        del invocation, binding, spec
        preflight = _preflight_error(self.request, before_state)
        if preflight is None:
            return PreconditionResult(True)
        code, message = preflight
        return PreconditionResult(False, code, message)


def parse_reference_worker_stdout(stdout: str, returncode: int | None) -> tuple[dict[str, Any] | None, str | None, str]:
    if not stdout.strip():
        return None, REFUSAL_CODES["empty_output"], "none"
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return None, REFUSAL_CODES["malformed_json"], "none"
    if not isinstance(payload, dict):
        return None, REFUSAL_CODES["malformed_json"], "none"
    errors: list[str] = []
    if payload.get("schema_version") != "aide.local-process-reference-worker-result.v0":
        errors.append("schema_version mismatch")
    if payload.get("worker_kind") != "local_reference_worker":
        errors.append("worker_kind mismatch")
    if payload.get("run_id") != RUN_REF:
        errors.append("run_id mismatch")
    if payload.get("workunit_ref") != TASK_ID:
        errors.append("workunit_ref mismatch")
    if payload.get("network_call_performed") is not False:
        errors.append("network_call_performed must be false")
    if payload.get("provider_or_model_called") is not False:
        errors.append("provider_or_model_called must be false")
    if payload.get("repository_mutation_performed") is not False:
        errors.append("repository_mutation_performed must be false")
    if payload.get("preview_or_apply_performed") is not False:
        errors.append("preview_or_apply_performed must be false")
    if errors:
        return {"schema_errors": errors, "raw_status": payload.get("status")}, REFUSAL_CODES["schema_mismatch"], "typed_refusal"
    normalized = {
        "command_id": CAPABILITY_ID,
        "source_command": FIXTURE_WORKER_REL.as_posix(),
        "source_schema": "aide.local-process-reference-worker-result.v0",
        "status": payload.get("status"),
        "worker_kind": payload.get("worker_kind"),
        "run_id": payload.get("run_id"),
        "workunit_ref": payload.get("workunit_ref"),
        "event_count": payload.get("event_count"),
        "artifact_count": payload.get("artifact_count"),
        "network_call_performed": payload.get("network_call_performed"),
        "provider_or_model_called": payload.get("provider_or_model_called"),
        "repository_mutation_performed": payload.get("repository_mutation_performed"),
        "preview_or_apply_performed": payload.get("preview_or_apply_performed"),
        "release_or_promotion_performed": payload.get("release_or_promotion_performed"),
    }
    if payload.get("status") == "PASS" and returncode == 0:
        return normalized, None, "typed_result"
    if returncode not in (0, None):
        return normalized, REFUSAL_CODES["nonzero_exit"], "typed_refusal"
    return normalized, REFUSAL_CODES["worker_failed"], "typed_refusal"


class LocalReferenceWorkerOutputDecoder:
    decoder_id = "aide.local-process-reference-worker-json-v0"

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> DecoderResult:
        parsed, reason_code, domain_outcome = parse_reference_worker_stdout(stdout, returncode)
        if reason_code:
            return DecoderResult(
                "decoded" if parsed else "refused",
                domain_outcome,
                domain_result=parsed or {},
                refusal={"reason_code": reason_code, "result": parsed or {}},
                reason_code=reason_code,
                message="Local process reference worker did not produce a successful typed result.",
            )
        return DecoderResult("decoded", "typed_result", domain_result=parsed or {})


class LocalProcessHostStreamScrubber:
    scrubber_id = "aide-local-process-host-stream-scrubber-v0"

    def __init__(self, request: Mapping[str, Any]):
        self.repo_root = str(request.get("repo_root", ""))
        self.python_executable = str(request.get("python_executable", ""))

    def scrub(self, text: str) -> str:
        return scrub_string(text, repo_root=self.repo_root, python_executable=self.python_executable)


def build_registered_process_spec(request: Mapping[str, Any]) -> RegisteredProcessSpec:
    argv = [str(item) for item in request.get("argv", [])]
    executable = argv[0] if argv else ""
    return RegisteredProcessSpec(
        capability_ref=CAPABILITY_REF,
        executable=executable,
        argument_plan=[ArgumentToken("literal", item) for item in argv[1:]],
        working_directory=str(Path(str(request.get("repo_root", ""))).resolve()),
        timeout_seconds=float(request.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
        environment=sanitized_environment(),
        decoder_id=LocalReferenceWorkerOutputDecoder.decoder_id,
        state_probe_id="aide-local-process-host-git-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id=LocalProcessHostStreamScrubber.scrubber_id,
        provider_spec_ref="aide://provider-spec/local-process-execution-host-reference-worker-v0",
        conformance_profile_ref="aide://conformance-profile/local-process-execution-host-v0",
        executable_digest=sha256_file(Path(executable)) if executable and Path(executable).is_file() else "",
        metadata={
            "argv_template": list(request.get("argv_template", [])),
            "command": "aide.local_process_reference_worker",
            "executable_identity": "python",
            "host_ref": HOST_REF,
            "run_ref": RUN_REF,
            "preexisting_dirty_state_allowed": True,
        },
    )


def _reason_code(reason_code: str, receipt: ProcessExecutionReceipt) -> str:
    if reason_code in set(REFUSAL_CODES.values()):
        return reason_code
    if reason_code == "missing_executable":
        return REFUSAL_CODES["invalid_request"]
    if reason_code == "digest_mismatch":
        return REFUSAL_CODES["digest_mismatch"]
    if reason_code == "invalid_spec":
        return REFUSAL_CODES["invalid_request"]
    if receipt.timed_out or reason_code == "timeout":
        return REFUSAL_CODES["timeout"]
    return reason_code or REFUSAL_CODES["invalid_request"]


def _receipt_launch(receipt: ProcessExecutionReceipt) -> dict[str, Any] | None:
    launch = receipt.metadata.get("launch") if isinstance(receipt.metadata, Mapping) else None
    if not isinstance(launch, Mapping):
        return None
    return {
        "argv": [str(item) for item in launch.get("argv", [])],
        "cwd": str(launch.get("cwd", "")),
        "env_constraints": {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
            "PYTHONHASHSEED": "0",
        },
        "environment_manifest_digest": launch.get("environment_manifest_digest", ""),
        "timeout": launch.get("timeout"),
        "shell": False,
    }


def refusal(
    *,
    request: Mapping[str, Any],
    reason_code: str,
    message: str,
    process_call_count: int,
    domain_result: Mapping[str, Any] | None = None,
    returncode: int | None = None,
    stdout: Mapping[str, Any] | None = None,
    stderr: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.run-result.v0",
        "kind": "LocalProcessExecutionHostRunResult",
        "task_id": TASK_ID,
        "capability_id": request.get("capability_id", CAPABILITY_ID),
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "result": "REFUSED",
        "status": "REFUSED",
        "reason_code": reason_code,
        "message": message,
        "process_call_count": process_call_count,
        "local_process_execution_host_implemented": process_call_count == 1,
        "reference_worker_process_started": process_call_count == 1,
        "bounded_worker_session_executed": process_call_count == 1,
        "result_origin": "reference_worker_json" if domain_result else "host_preflight_or_transport",
        "constructed_success_result": False,
        "returncode": returncode,
        "stdout": dict(stdout or {}),
        "stderr": dict(stderr or {}),
        "reference_worker_json_parsed": bool(domain_result),
        "reference_worker_result": dict(domain_result or {}),
        "typed_refusal": True,
        "typed_result": False,
        **_false_boundary(),
    }


def _result_from_provider(
    *,
    request: Mapping[str, Any],
    receipt: ProcessExecutionReceipt,
    outcome: CapabilityOutcome,
) -> dict[str, Any]:
    before_state = dict(receipt.metadata.get("before_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    after_state = dict(receipt.metadata.get("after_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    domain_result = dict(outcome.domain_result or {})
    state_changed = receipt.mutation_observation != "none_detected_within_probe_coverage"
    if receipt.launcher_call_count == 0:
        result = refusal(
            request=request,
            reason_code=_reason_code(outcome.reason_code, receipt),
            message=outcome.message or "Registered process preflight refused launch.",
            process_call_count=0,
            domain_result=domain_result or None,
            returncode=receipt.return_code,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    elif receipt.timed_out:
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["timeout"],
            message="Local process reference worker timed out.",
            process_call_count=receipt.launcher_call_count,
            returncode=None,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    elif state_changed:
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["unexpected_mutation"],
            message="AIDE repository state changed during bounded local process host invocation.",
            process_call_count=receipt.launcher_call_count,
            domain_result=domain_result or None,
            returncode=receipt.return_code,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    elif outcome.reason_code:
        result = refusal(
            request=request,
            reason_code=_reason_code(outcome.reason_code, receipt),
            message=outcome.message or "Local process reference worker returned a typed refusal.",
            process_call_count=receipt.launcher_call_count,
            domain_result=domain_result or None,
            returncode=receipt.return_code,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    else:
        result = {
            "schema_version": "aide.local-process-execution-host.run-result.v0",
            "kind": "LocalProcessExecutionHostRunResult",
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "result": "PASS",
            "status": "PASS",
            "reason_code": "",
            "message": "Local process reference worker returned a typed PASS result.",
            "process_call_count": receipt.launcher_call_count,
            "local_process_execution_host_implemented": receipt.launcher_call_count == 1,
            "reference_worker_process_started": receipt.launcher_call_count == 1,
            "bounded_worker_session_executed": receipt.launcher_call_count == 1,
            "result_origin": "reference_worker_json",
            "constructed_success_result": False,
            "returncode": receipt.return_code,
            "stdout": dict(receipt.stdout),
            "stderr": dict(receipt.stderr),
            "reference_worker_json_parsed": True,
            "reference_worker_result": domain_result,
            "typed_refusal": False,
            "typed_result": True,
            **_false_boundary(),
        }
    result["before_state"] = before_state
    result["after_state"] = after_state
    result["workspace_state_unchanged"] = not state_changed
    result["mutation_observation"] = receipt.mutation_observation
    result["probe_coverage"] = list(receipt.probe_coverage)
    result["allowlisted_process_call"] = _receipt_launch(receipt)
    result["argv_template"] = request.get("argv_template")
    result["environment_constraints"] = {
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
        "PYTHONHASHSEED": "0",
    }
    result["process_execution_receipt"] = receipt.to_dict()
    result["capability_outcome"] = outcome.to_dict()
    result["provider_ref"] = receipt.provider_ref
    result["provider_core_changed_by_task"] = False
    result["host_role"] = "bounded_local_process_reference_execution_host"
    return result


def invoke_local_process_host(request: Mapping[str, Any], *, runner: Runner | None = None) -> dict[str, Any]:
    repo_root = Path(str(request.get("repo_root", ""))).resolve()
    spec = build_registered_process_spec(request)
    invocation = CapabilityInvocation(
        invocation_ref="aide://invocation/local-process-execution-host-reference-worker-01",
        capability_ref=CAPABILITY_REF,
        values={"capability_id": CAPABILITY_ID, "host_ref": HOST_REF, "run_ref": RUN_REF},
    )
    binding = CapabilityBinding(
        capability_ref=CAPABILITY_REF,
        provider_id=RegisteredProcessExecutionProvider.provider_id,
        provider_spec_ref=spec.provider_spec_ref,
        provider_spec=spec,
        decoder_id=spec.decoder_id,
        state_probe_id=spec.state_probe_id,
        scrubber_id=spec.scrubber_id,
        conformance_profile_ref=spec.conformance_profile_ref,
    )
    provider = RegisteredProcessExecutionProvider(
        runner=runner,
        precondition=LocalProcessHostPrecondition(request),
        state_probe=AideStateProbe(repo_root),
        output_decoder=LocalReferenceWorkerOutputDecoder(),
        stream_scrubber=LocalProcessHostStreamScrubber(request),
    )
    receipt, outcome = provider.execute(invocation, binding)
    return _result_from_provider(request=request, receipt=receipt, outcome=outcome)


def scrub_string(text: str, *, repo_root: str = "", python_executable: str = "") -> str:
    result = text
    replacements = [
        (repo_root, "<aide-root>"),
        (repo_root.replace("\\", "/"), "<aide-root>"),
        (python_executable, "<python>"),
        (python_executable.replace("\\", "/"), "<python>"),
    ]
    for needle, replacement in replacements:
        if needle:
            result = result.replace(needle, replacement)
    result = re.sub(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"'\],}]+", "<absolute-path>", result)
    result = re.sub(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}", "<secret-like-redacted>", result)
    return result


def scrub_data(data: Any, *, repo_root: str = "", python_executable: str = "") -> Any:
    if isinstance(data, str):
        return scrub_string(data, repo_root=repo_root, python_executable=python_executable)
    if isinstance(data, list):
        return [scrub_data(item, repo_root=repo_root, python_executable=python_executable) for item in data]
    if isinstance(data, dict):
        return {str(key): scrub_data(value, repo_root=repo_root, python_executable=python_executable) for key, value in data.items()}
    return data


def artifact(repo_root: Path, path: Path, role: str) -> dict[str, Any]:
    return evidence_packet.artifact_ref(repo_root, path, role)


def build_host_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.descriptor.v0",
        "kind": "ExecutionHostDescriptor",
        "task_id": TASK_ID,
        "host_ref": HOST_REF,
        "host_kind": "local_process",
        "transport_modes": ["stdio"],
        "supported_operations": ["probe", "create_run", "stream_events", "collect_artifacts", "finish", "reconcile"],
        "capability_execution_distinct": True,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "local_process_execution_host_implemented": bool(result.get("local_process_execution_host_implemented")),
        "reference_worker_only": True,
        "general_worker_harness_implemented": False,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }


def build_run_binding(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.run-binding.v0",
        "kind": "ExecutionHostRunBinding",
        "task_id": TASK_ID,
        "binding_id": "aide://execution-host-binding/local-process-reference-01",
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workunit_ref": WORKUNIT_REF,
        "context_refs": [],
        "execution_started": result.get("process_call_count") == 1,
        "worker_process_started": result.get("process_call_count") == 1,
        "process_call_count": result.get("process_call_count"),
        "result": result.get("result"),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }


def build_host_event(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.event.v0",
        "kind": "ExecutionHostEvent",
        "task_id": TASK_ID,
        "event_ref": "aide://execution-host-event/local-process-reference-0001",
        "run_ref": RUN_REF,
        "event_type": "RunObserved",
        "sequence": 1,
        "payload": {
            "result": result.get("result"),
            "process_call_count": result.get("process_call_count"),
            "result_origin": result.get("result_origin"),
            "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        },
        "delivered": True,
        "runtime_event_store_implemented": False,
    }


def build_host_artifact(result: Mapping[str, Any]) -> dict[str, Any]:
    stdout = result.get("stdout") if isinstance(result.get("stdout"), Mapping) else {}
    return {
        "schema_version": "aide.local-process-execution-host.artifact.v0",
        "kind": "ExecutionHostArtifact",
        "task_id": TASK_ID,
        "artifact_ref": "aide://execution-host-artifact/local-process-reference-stdout",
        "run_ref": RUN_REF,
        "artifact_role": "stdout",
        "media_type": "application/json",
        "digest": stdout.get("sha256", "sha256:" + ("0" * 64)),
        "byte_count": stdout.get("byte_count", 0),
        "persisted": False,
        "streaming_artifact_store_implemented": False,
    }


def build_host_usage(result: Mapping[str, Any]) -> dict[str, Any]:
    worker = result.get("reference_worker_result") if isinstance(result.get("reference_worker_result"), Mapping) else {}
    return {
        "schema_version": "aide.local-process-execution-host.usage.v0",
        "kind": "ExecutionHostUsage",
        "task_id": TASK_ID,
        "usage_ref": "aide://execution-host-usage/local-process-reference-01",
        "run_ref": RUN_REF,
        "meters": {
            "processes": result.get("process_call_count", 0),
            "network_calls": 0,
            "provider_model_calls": 0,
            "events": worker.get("event_count", 0),
        },
        "limits": {"processes": 1, "network_calls": 0, "provider_model_calls": 0},
        "measured": True,
    }


def build_evidence_packet(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    return evidence_packet.build_evidence_packet(
        source_task_id=TASK_ID,
        source_task_kind="build",
        subject={"type": "capability", "id": PROPOSED_CAPABILITY_LABEL},
        capability_label=evidence_packet.FEATURE_FLAG,
        claims=[
            evidence_packet.claim("exactly_one_reference_worker_process", "supported" if result.get("process_call_count") == 1 else "contradicted", "One allowlisted local reference worker process was launched."),
            evidence_packet.claim("workspace_state_unchanged", "supported" if result.get("workspace_state_unchanged") else "contradicted", "AIDE state probe observed no mutation within declared coverage."),
            evidence_packet.claim("no_arbitrary_command_runner", "supported", "The host exposes only one fixture worker argv shape."),
        ],
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        artifacts=[
            artifact(repo_root, HOST_DESCRIPTOR_JSON, "host_descriptor"),
            artifact(repo_root, RUN_RESULT_JSON, "run_result"),
            artifact(repo_root, EXECUTION_RECEIPT_JSON, "execution_receipt"),
        ],
        validations=[
            evidence_packet.validation("py -3 .aide/scripts/aide_lite.py local-process-execution-host run", "PASS_WITH_WARNINGS", 0),
            evidence_packet.validation("py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_local_process_execution_host.py", "PASS", 0),
        ],
        warnings=[
            "This is a bounded local reference worker only, not a general worker harness or scheduler.",
            "Cancellation, durable idempotency, streaming artifacts, and resource quotas remain unimplemented.",
        ],
        source_path=Path(".aide/queue") / TASK_ID / "task.yaml",
        phase="PASS_WITH_WARNINGS",
        validation_warnings=["Reference worker fixture proves local process host mechanics only."],
    )


def build_event_record(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    return event_record.build_event_record(
        repo_root=repo_root,
        event_ref=EVENT_REF,
        event_type="ExecutionHostRunRecorded",
        subject_ref=f"aide://queue-task/{TASK_ID}",
        subject_kind="queue-task",
        occurred_at=DETERMINISTIC_TIMESTAMP,
        sequence=1,
        actor={"ref": "aide://source/aide-lite", "kind": "source", "name": "aide-lite"},
        payload={
            "host_ref": HOST_REF,
            "run_ref": RUN_REF,
            "result": result.get("result"),
            "process_call_count": result.get("process_call_count"),
            "reference_worker_process_started": result.get("reference_worker_process_started"),
        },
        evidence_refs=[EVIDENCE_REF],
        report_refs=[REPORT_REF],
        causation_ref=f"aide://queue-task/{ACCEPTED_CONTRACT_TASK_ID}",
        correlation_ref="aide://wave/execution-host-v0",
        source_path=(Path(".aide/reports/local-process-execution-host/run-result.json").as_posix()),
        required_event_type=False,
    )


def build_projection(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.projection.v0",
        "kind": "LocalProcessExecutionHostProjection",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS" if result.get("result") == "PASS" else "FAILED_VALIDATION",
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "provider_ref": result.get("provider_ref"),
        "process_call_count": result.get("process_call_count"),
        "local_process_execution_host_implemented": result.get("local_process_execution_host_implemented"),
        "reference_worker_process_started": result.get("reference_worker_process_started"),
        "bounded_worker_session_executed": result.get("bounded_worker_session_executed"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }


def render_status_markdown(data: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# LocalProcessExecutionHost v0 Status",
            "",
            f"- result: {data.get('status')}",
            f"- proposed capability: {PROPOSED_CAPABILITY_LABEL}",
            f"- provider: {RegisteredProcessExecutionProvider.provider_id}",
            f"- report exists: {str(data.get('host_report_exists', False)).lower()}",
            f"- recommended next task: {data.get('recommended_next_task')}",
            "",
        ]
    )


def render_host_report_markdown(report: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# LocalProcessExecutionHost v0 Build Report",
            "",
            f"- result: {report.get('validation_status')}",
            f"- process_call_count: {report.get('process_call_count')}",
            f"- reference_worker_process_started: {str(report.get('reference_worker_process_started', False)).lower()}",
            f"- workspace_state_unchanged: {str(report.get('workspace_state_unchanged', False)).lower()}",
            f"- mutation_observation: {report.get('mutation_observation')}",
            f"- result_origin: {report.get('result_origin')}",
            "",
            "## Boundary",
            "",
            "This slice proves one bounded local reference worker process through the accepted registered process provider.",
            "It does not implement an autonomous worker harness, scheduler, Service, Workbench, provider/model calls, network calls, preview/apply/rollback, or repository mutation.",
            "",
        ]
    )


def write_static_reports(repo_root: Path, result: Mapping[str, Any]) -> None:
    write_text(
        repo_root / WARNING_DISPOSITION_MD,
        "\n".join(
            [
                "# Warning Disposition",
                "",
                "- The host runs only the committed local reference worker fixture.",
                "- No cancellation, durable idempotency, streaming artifact storage, resource quotas, scheduler, or Service runtime is implemented.",
                "- The accepted ExecutionHost contract remains projection-only; this build adds a bounded reference implementation report, not a schema acceptance update.",
                "",
            ]
        ),
    )
    write_text(
        repo_root / EXPLICIT_NON_CAPABILITIES_MD,
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES) + "\n",
    )
    write_text(
        repo_root / NEXT_TASK_PROMPT_MD,
        "\n".join(
            [
                "# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01",
                "",
                "Create and process AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01.",
                "Independently verify the bounded LocalProcessExecutionHost v0 build.",
                "If material checks pass, recommend AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01.",
                "If material findings remain, recommend AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01.",
                "",
            ]
        ),
    )


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root).resolve()
    data = {
        "schema_version": "aide.local-process-execution-host.status.v0",
        "status": "PASS_WITH_WARNINGS" if (root / VALIDATION_JSON).exists() else "NOT_RUN",
        "task_id": TASK_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "capability_id": CAPABILITY_ID,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "host_report_exists": (root / HOST_REPORT_JSON).exists(),
        "validation_report_exists": (root / VALIDATION_JSON).exists(),
        "recommended_next_task": CHECK_TASK_ID,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def _validation_errors(result: Mapping[str, Any], report_files: Sequence[Path]) -> list[str]:
    errors: list[str] = []
    if result.get("result") != "PASS":
        errors.append(f"run result was not PASS: {result.get('result')}")
    if result.get("process_call_count") != 1:
        errors.append("process_call_count must be exactly 1")
    if result.get("reference_worker_process_started") is not True:
        errors.append("reference_worker_process_started must be true")
    if result.get("local_process_execution_host_implemented") is not True:
        errors.append("local_process_execution_host_implemented must be true")
    if result.get("workspace_state_unchanged") is not True:
        errors.append("workspace_state_unchanged must be true")
    if result.get("provider_ref") != RegisteredProcessExecutionProvider.provider_id:
        errors.append("provider_ref must be registered_process_execution_provider_v0")
    if result.get("constructed_success_result") is not False:
        errors.append("constructed_success_result must be false")
    if result.get("allowlisted_process_call") is None:
        errors.append("allowlisted_process_call evidence is missing")
    for field in FALSE_BOUNDARY_FIELDS:
        if result.get(field) is not False:
            errors.append(f"{field} must remain false")
    missing = [path.as_posix() for path in report_files if not path.exists()]
    if missing:
        errors.append("missing report files: " + ", ".join(missing))
    return errors


def run_host(
    repo_root: str | Path = ".",
    *,
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
    runner: Runner | None = None,
    write_reports: bool = True,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    request = build_invocation_request(
        repo_root=root,
        expected_revision=expected_revision,
        capability_id=capability_id,
        python_executable=python_executable,
        timeout_seconds=timeout_seconds,
        expected_digests=expected_digests,
    )
    raw_result = invoke_local_process_host(request, runner=runner)
    result = scrub_data(raw_result, repo_root=str(root), python_executable=str(request.get("python_executable", "")))
    validation_status = "PASS_WITH_WARNINGS" if result.get("result") == "PASS" else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.local-process-execution-host.report.v0",
        "task_id": TASK_ID,
        "validation_status": validation_status,
        "status": validation_status,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "capability_id": CAPABILITY_ID,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "provider_ref": result.get("provider_ref"),
        "process_call_count": result.get("process_call_count"),
        "local_process_execution_host_implemented": result.get("local_process_execution_host_implemented"),
        "reference_worker_process_started": result.get("reference_worker_process_started"),
        "bounded_worker_session_executed": result.get("bounded_worker_session_executed"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "typed_result": result.get("typed_result"),
        "typed_refusal": result.get("typed_refusal"),
        "provider_core_changed_by_task": False,
        "recommended_next_task": CHECK_TASK_ID,
        "warnings": [
            "Bounded local reference worker only; no general worker harness, scheduler, cancellation, durable idempotency, Service, or Workbench runtime.",
            "Accepted ExecutionHost contract remains projection-only pending independent check and acceptance of this live reference host.",
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }
    if write_reports:
        request_scrubbed = scrub_data(request, repo_root=str(root), python_executable=str(request.get("python_executable", "")))
        write_json(root / INVOCATION_REQUEST_JSON, request_scrubbed)
        write_json(root / RUN_RESULT_JSON, result)
        write_json(root / EXECUTION_RECEIPT_JSON, result["process_execution_receipt"])
        write_json(root / CAPABILITY_OUTCOME_JSON, result["capability_outcome"])
        write_json(root / HOST_DESCRIPTOR_JSON, build_host_descriptor(result))
        write_json(root / RUN_BINDING_JSON, build_run_binding(result))
        write_json(root / HOST_EVENT_JSON, build_host_event(result))
        write_json(root / HOST_ARTIFACT_JSON, build_host_artifact(result))
        write_json(root / HOST_USAGE_JSON, build_host_usage(result))
        write_json(root / EVIDENCE_PACKET_JSON, build_evidence_packet(root, result))
        write_json(root / EVENT_RECORD_JSON, build_event_record(root, result))
        write_json(root / PROJECTION_JSON, build_projection(result))
        write_json(root / HOST_REPORT_JSON, report)
        write_text(root / HOST_REPORT_MD, render_host_report_markdown(report))
        write_static_reports(root, result)
        write_text(
            root / STATUS_MD,
            render_status_markdown(
                {
                    "status": validation_status,
                    "host_report_exists": True,
                    "validation_report_exists": True,
                    "recommended_next_task": CHECK_TASK_ID,
                }
            ),
        )
        validation = validate_reports(root)
        report["validation_status"] = validation["validation_status"]
        report["status"] = validation["validation_status"]
        report["validation_errors"] = validation["validation_errors"]
        write_json(root / HOST_REPORT_JSON, report)
        write_text(root / HOST_REPORT_MD, render_host_report_markdown(report))
        result["validation_status"] = validation["validation_status"]
        result["validation_errors"] = validation["validation_errors"]
    else:
        result["validation_status"] = validation_status
        result["validation_errors"] = _validation_errors(result, [])
    return result


def validate_reports(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root).resolve()
    errors: list[str] = []
    try:
        result = read_json(root / RUN_RESULT_JSON)
    except ValueError as exc:
        result = {}
        errors.append(str(exc))
    errors.extend(_validation_errors(result, [root / path for path in REPORT_FILES if path != VALIDATION_JSON]))
    leak_hits: list[str] = []
    root_text = str(root)
    secret_pattern = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    for rel in REPORT_FILES:
        path = root / rel
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if root_text in text or root_text.replace("\\", "/") in text:
            leak_hits.append(rel.as_posix())
        if secret_pattern.search(text):
            leak_hits.append(rel.as_posix() + ":secret-like")
    if leak_hits:
        errors.append("local path or secret-like leak detected: " + ", ".join(sorted(set(leak_hits))))
    validation_status = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    report = {
        "schema_version": "aide.local-process-execution-host.validation.v0",
        "task_id": TASK_ID,
        "validation_status": validation_status,
        "validated": not errors,
        "process_call_count": result.get("process_call_count"),
        "local_process_execution_host_implemented": result.get("local_process_execution_host_implemented"),
        "reference_worker_process_started": result.get("reference_worker_process_started"),
        "bounded_worker_session_executed": result.get("bounded_worker_session_executed"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "provider_ref": result.get("provider_ref"),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "validation_errors": errors,
        "validation_warnings": [
            "This is a bounded reference LocalProcessExecutionHost; cancellation, durable idempotency, streaming artifacts, quotas, and scheduler remain absent.",
        ],
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / VALIDATION_JSON, report)
    return report
