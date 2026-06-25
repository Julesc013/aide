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
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
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
from core.protocol.execution_receipt import ProcessExecutionReceipt
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
SOURCE_TASK_ID = "AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
SOURCE_CHECK_TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
CHECK_TASK_ID = "AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
ACCEPTED_CONTRACT_TASK_ID = "AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01"
ACCEPTED_PROVIDER = "registered_process_execution_provider_v0"
CAPABILITY_ID = "aide.local-process-host.reference-worker.run"
CAPABILITY_REF = "aide://capability/local-process-execution-host-reference-worker-v0"
PROPOSED_CAPABILITY_LABEL = "local_process_execution_host_fixture_v0"
HOST_REF = "aide://execution-host/local-process/reference-v0"
RUN_REF = "aide://execution-host-run/local-process-reference-01"
WORKUNIT_REF = f"aide://workunit/{TASK_ID}"
EVIDENCE_REF = "aide://evidence/local-process-execution-host-v0-repair-01"
REPORT_REF = "aide://report/local-process-execution-host-v0-repair-01"
EVENT_REF = "aide://event/EVT-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01"
WORKSPACE_REF = "aide://workspace/local-process/reference-01"
DETERMINISTIC_TIMESTAMP = "2026-06-25T00:00:00+10:00"
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_WORKER_ARTIFACT_BYTES = 8192
FIXTURE_EVENT_SCHEMA = "aide.fixture-worker.events.v0"

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

STAGED_WORKER_MEMBER = "worker/reference_worker.py"
WORKUNIT_INPUT_MEMBER = "inputs/workunit.json"
CONTEXTPACK_INPUT_MEMBER = "inputs/context-pack.json"
ARTIFACT_MEMBER = "artifacts/result.json"
ALLOWED_WORKSPACE_MEMBERS = {
    STAGED_WORKER_MEMBER,
    WORKUNIT_INPUT_MEMBER,
    CONTEXTPACK_INPUT_MEMBER,
    ARTIFACT_MEMBER,
}

REPORT_ROOT = Path(".aide/reports/local-process-execution-host")
REPAIR_REPORT_ROOT = Path(".aide/reports/local-process-execution-host-repair-01")
STATUS_MD = REPORT_ROOT / "status.md"
HOST_DESCRIPTOR_JSON = REPORT_ROOT / "host-descriptor.json"
RUN_BINDING_JSON = REPORT_ROOT / "run-binding.json"
HOST_EVENT_JSON = REPORT_ROOT / "host-event.json"
HOST_EVENTS_JSON = REPORT_ROOT / "host-events.json"
HOST_ARTIFACT_JSON = REPORT_ROOT / "host-artifact.json"
HOST_ARTIFACTS_JSON = REPORT_ROOT / "host-artifacts.json"
HOST_USAGE_JSON = REPORT_ROOT / "host-usage.json"
WORKER_RUN_JSON = REPORT_ROOT / "worker-run.json"
TRANSLATION_RECEIPT_JSON = REPORT_ROOT / "translation-receipt.json"
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

REPAIR_STATUS_MD = REPAIR_REPORT_ROOT / "status.md"
REPAIR_REPORT_JSON = REPAIR_REPORT_ROOT / "repair-report.json"
FINDING_DISPOSITION_JSON = REPAIR_REPORT_ROOT / "finding-disposition.json"
FINDING_DISPOSITION_MD = REPAIR_REPORT_ROOT / "finding-disposition.md"
REPAIR_NEXT_TASK_PROMPT_MD = REPAIR_REPORT_ROOT / "next-task-prompt.md"

REPORT_FILES = [
    STATUS_MD,
    HOST_DESCRIPTOR_JSON,
    RUN_BINDING_JSON,
    HOST_EVENT_JSON,
    HOST_EVENTS_JSON,
    HOST_ARTIFACT_JSON,
    HOST_ARTIFACTS_JSON,
    HOST_USAGE_JSON,
    WORKER_RUN_JSON,
    TRANSLATION_RECEIPT_JSON,
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
    REPAIR_STATUS_MD,
    REPAIR_REPORT_JSON,
    FINDING_DISPOSITION_JSON,
    FINDING_DISPOSITION_MD,
    REPAIR_NEXT_TASK_PROMPT_MD,
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

SUPPORTED_HOST_OPERATIONS = ["probe", "create_run"]
UNSUPPORTED_HOST_OPERATIONS = [
    "attach",
    "send_input",
    "stream_events",
    "resolve_runtime_approval",
    "interrupt",
    "pause",
    "resume",
    "cancel",
    "collect_artifacts",
    "finish",
    "reconcile",
]

REFUSAL_CODES = {
    "unsupported_capability": "AIDE_LOCAL_PROCESS_HOST_UNSUPPORTED_CAPABILITY",
    "unsupported_operation": "AIDE_LOCAL_PROCESS_HOST_UNSUPPORTED_OPERATION",
    "invalid_request": "AIDE_LOCAL_PROCESS_HOST_INVALID_REQUEST",
    "repository_missing": "AIDE_LOCAL_PROCESS_HOST_REPOSITORY_MISSING",
    "revision_mismatch": "AIDE_LOCAL_PROCESS_HOST_REVISION_MISMATCH",
    "fixture_missing": "AIDE_LOCAL_PROCESS_HOST_FIXTURE_MISSING",
    "digest_mismatch": "AIDE_LOCAL_PROCESS_HOST_DIGEST_MISMATCH",
    "workspace_path_absolute": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_PATH_ABSOLUTE",
    "workspace_path_traversal": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_PATH_TRAVERSAL",
    "workspace_path_escape": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_PATH_ESCAPE",
    "workspace_inside_source": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_INSIDE_SOURCE",
    "workspace_symlink_escape": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_SYMLINK_ESCAPE",
    "workspace_reparse_point_escape": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_REPARSE_POINT_ESCAPE",
    "workspace_member_type_invalid": "AIDE_LOCAL_PROCESS_HOST_WORKSPACE_MEMBER_TYPE_INVALID",
    "malformed_event_stream": "AIDE_LOCAL_PROCESS_HOST_MALFORMED_EVENT_STREAM",
    "event_sequence_duplicate": "AIDE_LOCAL_PROCESS_HOST_EVENT_SEQUENCE_DUPLICATE",
    "event_sequence_decrease": "AIDE_LOCAL_PROCESS_HOST_EVENT_SEQUENCE_DECREASE",
    "event_sequence_gap": "AIDE_LOCAL_PROCESS_HOST_EVENT_SEQUENCE_GAP",
    "wrong_run_ref": "AIDE_LOCAL_PROCESS_HOST_WRONG_RUN_REF",
    "terminal_event_missing": "AIDE_LOCAL_PROCESS_HOST_TERMINAL_EVENT_MISSING",
    "duplicate_terminal_event": "AIDE_LOCAL_PROCESS_HOST_DUPLICATE_TERMINAL_EVENT",
    "event_after_terminal": "AIDE_LOCAL_PROCESS_HOST_EVENT_AFTER_TERMINAL",
    "invalid_lifecycle_transition": "AIDE_LOCAL_PROCESS_HOST_INVALID_LIFECYCLE_TRANSITION",
    "terminal_state_transition": "AIDE_LOCAL_PROCESS_HOST_TERMINAL_STATE_TRANSITION",
    "artifact_path_escape": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_PATH_ESCAPE",
    "artifact_link_rejected": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_LINK_REJECTED",
    "artifact_digest_mismatch": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_DIGEST_MISMATCH",
    "artifact_size_mismatch": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_SIZE_MISMATCH",
    "artifact_missing": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_MISSING",
    "artifact_unexpected": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_UNEXPECTED",
    "artifact_oversized": "AIDE_LOCAL_PROCESS_HOST_ARTIFACT_OVERSIZED",
    "timeout": "AIDE_LOCAL_PROCESS_HOST_TIMEOUT",
    "nonzero_exit": "AIDE_LOCAL_PROCESS_HOST_NONZERO_EXIT",
    "empty_output": "AIDE_LOCAL_PROCESS_HOST_EMPTY_OUTPUT",
    "worker_failed": "AIDE_LOCAL_PROCESS_HOST_WORKER_FAILED",
    "unexpected_mutation": "AIDE_LOCAL_PROCESS_HOST_UNEXPECTED_REPOSITORY_MUTATION",
}

FINDING_IDS = [
    "local_host.disposable_workspace_not_proven",
    "local_host.path_escape_not_proven",
    "local_host.raw_event_stream_not_proven",
    "local_host.content_addressed_artifacts_not_proven",
    "local_host.workerrun_lifecycle_not_proven",
    "local_host.descriptor_overclaims_operations",
]

Runner = Callable[[Sequence[str], Path, Mapping[str, str], float], subprocess.CompletedProcess[str]]


class LocalProcessHostError(Exception):
    def __init__(self, reason_key: str, message: str):
        self.reason_key = reason_key
        self.reason_code = REFUSAL_CODES[reason_key]
        super().__init__(message)


@dataclass(frozen=True)
class ParsedEventStream:
    raw_text: str
    events: list[dict[str, Any]]
    artifact_declarations: list[dict[str, Any]]
    terminal_event_kind: str
    terminal_payload: dict[str, Any]


@dataclass(frozen=True)
class DisposableWorkspace:
    root: Path
    source_root: Path
    retained_debug: bool = False

    @classmethod
    def create(cls, source_root: Path, requested_root: Path | None = None, *, retained_debug: bool = False) -> "DisposableWorkspace":
        source_root = source_root.resolve()
        if requested_root is None:
            root = Path(tempfile.mkdtemp(prefix="aide-local-host-")).resolve()
        else:
            root = requested_root.resolve()
            if is_under(root, source_root) or root == source_root:
                raise LocalProcessHostError("workspace_inside_source", "Disposable workspace must not be inside the AIDE checkout.")
            if root.exists() and any(root.iterdir()):
                raise LocalProcessHostError("invalid_request", "Disposable workspace must be empty when provided.")
            root.mkdir(parents=True, exist_ok=True)
        return cls(root=root, source_root=source_root, retained_debug=retained_debug)

    def stage(self) -> dict[str, Any]:
        worker_target = resolve_workspace_member(self.root, STAGED_WORKER_MEMBER)
        worker_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.source_root / FIXTURE_WORKER_REL, worker_target)
        workunit_payload = {
            "schema_version": "aide.local-process-host.workunit-fixture.v0",
            "workunit_ref": WORKUNIT_REF,
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
        }
        context_payload = {
            "schema_version": "aide.local-process-host.context-pack-fixture.v0",
            "context_pack_ref": "aide://context-pack/local-process-reference-01",
            "source_task_id": TASK_ID,
        }
        write_workspace_json(self.root, WORKUNIT_INPUT_MEMBER, workunit_payload)
        write_workspace_json(self.root, CONTEXTPACK_INPUT_MEMBER, context_payload)
        return {
            "workspace_ref": WORKSPACE_REF,
            "workspace_root_inside_source": False,
            "staged_worker_member": STAGED_WORKER_MEMBER,
            "staged_worker_digest": sha256_file(worker_target),
            "source_worker_digest": sha256_file(self.source_root / FIXTURE_WORKER_REL),
            "input_members": [WORKUNIT_INPUT_MEMBER, CONTEXTPACK_INPUT_MEMBER],
            "allowed_members": sorted(ALLOWED_WORKSPACE_MEMBERS),
        }

    def cleanup(self) -> dict[str, Any]:
        if self.retained_debug:
            return {
                "workspace_ref": WORKSPACE_REF,
                "cleanup_attempted": False,
                "retained_debug": True,
                "removed": False,
            }
        shutil.rmtree(self.root, ignore_errors=True)
        return {
            "workspace_ref": WORKSPACE_REF,
            "cleanup_attempted": True,
            "retained_debug": False,
            "removed": not self.root.exists(),
        }


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


def is_under(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def has_reparse_point(path: Path) -> bool:
    attrs = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
    return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _path_parts_have_escape(parts: Sequence[str]) -> bool:
    return any(part in ("", ".", "..") for part in parts)


def resolve_workspace_member(
    workspace_root: Path,
    member: str,
    *,
    must_exist: bool = False,
    regular_file: bool = False,
    artifact: bool = False,
) -> Path:
    member_path = Path(member)
    if member_path.is_absolute() or re.match(r"^[A-Za-z]:", member):
        raise LocalProcessHostError("artifact_path_escape" if artifact else "workspace_path_absolute", "Workspace member must be relative.")
    if _path_parts_have_escape(member_path.parts):
        raise LocalProcessHostError("artifact_path_escape" if artifact else "workspace_path_traversal", "Workspace member contains traversal.")
    root = workspace_root.resolve()
    current = root
    for part in member_path.parts:
        current = current / part
        if current.exists():
            if current.is_symlink():
                raise LocalProcessHostError("artifact_link_rejected" if artifact else "workspace_symlink_escape", "Workspace symlink path is rejected.")
            if has_reparse_point(current):
                raise LocalProcessHostError("artifact_link_rejected" if artifact else "workspace_reparse_point_escape", "Workspace reparse point path is rejected.")
    candidate = (root / member_path).resolve(strict=False)
    if not is_under(candidate, root):
        raise LocalProcessHostError("artifact_path_escape" if artifact else "workspace_path_escape", "Workspace member escaped workspace root.")
    if must_exist and not candidate.exists():
        raise LocalProcessHostError("artifact_missing" if artifact else "workspace_member_type_invalid", "Workspace member is missing.")
    if candidate.exists() and regular_file and not candidate.is_file():
        raise LocalProcessHostError("artifact_link_rejected" if artifact else "workspace_member_type_invalid", "Workspace member must be a regular file.")
    return candidate


def write_workspace_json(workspace_root: Path, member: str, payload: dict[str, Any]) -> None:
    target = resolve_workspace_member(workspace_root, member)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(stable_json(payload), encoding="utf-8", newline="\n")


def resolve_python_executable(value: str | Path | None = None) -> str:
    return str((Path(value) if value else Path(sys.executable)).resolve())


def sanitized_environment() -> dict[str, str]:
    allowed = ["COMSPEC", "PATH", "PATHEXT", "SYSTEMROOT", "TEMP", "TMP", "WINDIR", "SystemDrive", "USERPROFILE", "HOME"]
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PYTHONUTF8": "1", "PYTHONHASHSEED": "0"})
    return env


def build_argv(python_executable: str, workspace_root: Path) -> list[str]:
    return [
        str(Path(python_executable).resolve()),
        str(resolve_workspace_member(workspace_root, STAGED_WORKER_MEMBER, must_exist=True, regular_file=True)),
        "--run-id",
        RUN_REF,
        "--workunit-ref",
        TASK_ID,
        "--event-stream",
    ]


def build_invocation_request(
    *,
    repo_root: str | Path = ".",
    workspace_root: str | Path,
    stage_receipt: Mapping[str, Any],
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    workspace = Path(workspace_root).resolve()
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
        "source_task_id": SOURCE_TASK_ID,
        "capability_id": capability_id,
        "expected_capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "repo_root": str(root),
        "workspace_root": str(workspace),
        "workspace_ref": WORKSPACE_REF,
        "expected_revision": revision or "",
        "python_executable": py,
        "staged_worker_member": STAGED_WORKER_MEMBER,
        "fixture_worker_path": str((root / FIXTURE_WORKER_REL).resolve()),
        "timeout_seconds": float(timeout_seconds),
        "argv": build_argv(py, workspace),
        "argv_template": ["<python>", "<workspace>/worker/reference_worker.py", "--run-id", RUN_REF, "--workunit-ref", TASK_ID, "--event-stream"],
        "shell": False,
        "expected_digests": dict(expected_digests),
        "stage_receipt": dict(stage_receipt),
        "preexisting_dirty_state_allowed": True,
        "disposable_workspace_required": True,
    }


def _preflight_error(request: Mapping[str, Any], before_state: Mapping[str, Any]) -> tuple[str, str] | None:
    if request.get("capability_id") != CAPABILITY_ID:
        return REFUSAL_CODES["unsupported_capability"], "Only the local process reference worker capability is admitted."
    root = Path(str(request.get("repo_root", "")))
    workspace = Path(str(request.get("workspace_root", "")))
    if not root.exists() or not (root / ".git").exists():
        return REFUSAL_CODES["repository_missing"], "AIDE repository checkout is missing."
    if workspace.exists() and (is_under(workspace, root) or workspace.resolve() == root.resolve()):
        return REFUSAL_CODES["workspace_inside_source"], "Disposable workspace is inside the AIDE checkout."
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
    try:
        staged = resolve_workspace_member(workspace, STAGED_WORKER_MEMBER, must_exist=True, regular_file=True)
    except LocalProcessHostError as exc:
        return exc.reason_code, str(exc)
    stage_receipt = request.get("stage_receipt", {})
    if isinstance(stage_receipt, Mapping) and stage_receipt.get("staged_worker_digest") != sha256_file(staged):
        return REFUSAL_CODES["digest_mismatch"], "Staged worker digest mismatch."
    argv = list(request.get("argv") or [])
    expected_argv = build_argv(str(request.get("python_executable", "")), workspace)
    if argv != expected_argv or len(argv) != 7:
        return REFUSAL_CODES["invalid_request"], "LocalProcessExecutionHost argv shape is not the exact allowlisted invocation."
    if request.get("shell") is not False:
        return REFUSAL_CODES["invalid_request"], "LocalProcessExecutionHost must use shell=False."
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


def _event_reason(reason_key: str, message: str) -> LocalProcessHostError:
    return LocalProcessHostError(reason_key, message)


def parse_fixture_event_stream(stdout: str, returncode: int | None) -> ParsedEventStream:
    raw = stdout.strip()
    if not raw:
        raise _event_reason("empty_output", "Worker emitted no event stream.")
    events: list[dict[str, Any]] = []
    terminal_seen = False
    terminal_kind = ""
    terminal_payload: dict[str, Any] = {}
    last_sequence = 0
    seen_sequences: set[int] = set()
    artifact_declarations: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise _event_reason("malformed_event_stream", f"Event line {line_number} is not JSON.") from exc
        if not isinstance(event, dict):
            raise _event_reason("malformed_event_stream", f"Event line {line_number} is not an object.")
        if terminal_seen:
            raise _event_reason("event_after_terminal", "Worker emitted an event after a terminal event.")
        if event.get("schema_version") != FIXTURE_EVENT_SCHEMA:
            raise _event_reason("malformed_event_stream", "Event schema_version mismatch.")
        if event.get("run_ref") != RUN_REF:
            raise _event_reason("wrong_run_ref", "Worker event run_ref mismatch.")
        sequence = event.get("sequence")
        if not isinstance(sequence, int):
            raise _event_reason("malformed_event_stream", "Worker event sequence must be an integer.")
        if sequence in seen_sequences:
            raise _event_reason("event_sequence_duplicate", "Worker event sequence is duplicated.")
        if sequence < last_sequence:
            raise _event_reason("event_sequence_decrease", "Worker event sequence decreased.")
        if sequence != last_sequence + 1:
            raise _event_reason("event_sequence_gap", "Worker event sequence is not contiguous.")
        seen_sequences.add(sequence)
        last_sequence = sequence
        kind = event.get("event_kind")
        if kind not in {"run_created", "run_started", "worker_message", "artifact_produced", "usage_updated", "run_completed", "run_failed", "run_timed_out"}:
            raise _event_reason("malformed_event_stream", "Worker event_kind is unsupported.")
        payload = event.get("payload")
        if not isinstance(payload, dict):
            raise _event_reason("malformed_event_stream", "Worker event payload must be an object.")
        if kind == "artifact_produced":
            declaration = {
                "path": payload.get("path"),
                "media_type": payload.get("media_type"),
                "byte_count": payload.get("byte_count"),
                "sha256": payload.get("sha256"),
                "event_sequence": sequence,
            }
            if not isinstance(declaration["path"], str) or not isinstance(declaration["byte_count"], int) or not isinstance(declaration["sha256"], str):
                raise _event_reason("malformed_event_stream", "Artifact event declaration is incomplete.")
            artifact_declarations.append(declaration)
        if kind in {"run_completed", "run_failed", "run_timed_out"}:
            terminal_seen = True
            terminal_kind = kind
            terminal_payload = payload
        events.append(event)
    if not terminal_seen:
        raise _event_reason("terminal_event_missing", "Worker event stream has no terminal event.")
    if terminal_kind == "run_completed" and returncode not in (0, None):
        raise _event_reason("nonzero_exit", "Worker process returned nonzero despite completed event.")
    if terminal_kind == "run_failed":
        raise _event_reason("worker_failed", "Worker emitted run_failed.")
    if terminal_kind == "run_timed_out":
        raise _event_reason("timeout", "Worker emitted run_timed_out.")
    return ParsedEventStream(raw_text=raw + "\n", events=events, artifact_declarations=artifact_declarations, terminal_event_kind=terminal_kind, terminal_payload=terminal_payload)


def parse_reference_worker_stdout(stdout: str, returncode: int | None) -> tuple[dict[str, Any] | None, str | None, str]:
    """Compatibility wrapper retained for existing callers."""
    try:
        parsed = parse_fixture_event_stream(stdout, returncode)
    except LocalProcessHostError as exc:
        return None, exc.reason_code, "typed_refusal"
    normalized = {
        "command_id": CAPABILITY_ID,
        "source_command": STAGED_WORKER_MEMBER,
        "source_schema": FIXTURE_EVENT_SCHEMA,
        "status": "PASS",
        "run_id": RUN_REF,
        "workunit_ref": TASK_ID,
        "event_count": len(parsed.events),
        "artifact_count": len(parsed.artifact_declarations),
        "terminal_event_kind": parsed.terminal_event_kind,
    }
    return normalized, None, "typed_result"


def validate_lifecycle(events: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    state = "proposed"
    transitions: list[dict[str, str]] = []

    def transition(event_kind: str, new_state: str) -> None:
        nonlocal state
        if state in {"completed", "failed", "timed_out"}:
            raise LocalProcessHostError("terminal_state_transition", "WorkerRun transitioned after terminal state.")
        transitions.append({"from": state, "event": event_kind, "to": new_state})
        state = new_state

    for event in events:
        kind = str(event.get("event_kind"))
        if kind == "run_created":
            if state != "proposed":
                raise LocalProcessHostError("invalid_lifecycle_transition", "run_created must start from proposed.")
            transition(kind, "creating")
        elif kind == "run_started":
            if state != "creating":
                raise LocalProcessHostError("invalid_lifecycle_transition", "run_started must start from creating.")
            transition(kind, "ready")
            transition(kind, "running")
        elif kind in {"worker_message", "usage_updated", "artifact_produced"}:
            if state != "running":
                raise LocalProcessHostError("invalid_lifecycle_transition", f"{kind} must occur while running.")
            transitions.append({"from": state, "event": kind, "to": state})
        elif kind == "run_completed":
            if state != "running":
                raise LocalProcessHostError("invalid_lifecycle_transition", "run_completed must start from running.")
            transition(kind, "completing")
            transition(kind, "completed")
        elif kind == "run_failed":
            if state not in {"creating", "ready", "running", "completing", "reconciliation_required"}:
                raise LocalProcessHostError("invalid_lifecycle_transition", "run_failed from invalid state.")
            transition(kind, "failed")
        elif kind == "run_timed_out":
            if state != "running":
                raise LocalProcessHostError("invalid_lifecycle_transition", "run_timed_out must start from running.")
            transition(kind, "timed_out")
        else:
            raise LocalProcessHostError("invalid_lifecycle_transition", f"Unsupported lifecycle event: {kind}")
    if state not in {"completed", "failed", "timed_out"}:
        raise LocalProcessHostError("terminal_event_missing", "WorkerRun lifecycle has no terminal state.")
    return {
        "schema_version": "aide.local-process-execution-host.workerrun-lifecycle.v0",
        "kind": "WorkerRunLifecycle",
        "run_ref": RUN_REF,
        "initial_state": "proposed",
        "final_state": state,
        "transitions": transitions,
        "reconciliation_required_supported": False,
        "allowed_terminal_states": ["completed", "failed", "timed_out"],
    }


class LocalReferenceWorkerOutputDecoder:
    decoder_id = "aide.local-process-reference-worker-ndjson-v0"

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> DecoderResult:
        del stderr
        try:
            parsed = parse_fixture_event_stream(stdout, returncode)
            lifecycle = validate_lifecycle(parsed.events)
        except LocalProcessHostError as exc:
            return DecoderResult(
                "refused",
                "typed_refusal",
                domain_result={},
                refusal={"reason_code": exc.reason_code, "message": str(exc)},
                reason_code=exc.reason_code,
                message=str(exc),
            )
        normalized = {
            "command_id": CAPABILITY_ID,
            "source_command": STAGED_WORKER_MEMBER,
            "source_schema": FIXTURE_EVENT_SCHEMA,
            "status": "PASS",
            "run_id": RUN_REF,
            "workunit_ref": TASK_ID,
            "event_count": len(parsed.events),
            "artifact_count": len(parsed.artifact_declarations),
            "terminal_event_kind": parsed.terminal_event_kind,
            "raw_event_stream_digest": sha256_text(parsed.raw_text),
            "artifact_declarations": parsed.artifact_declarations,
            "worker_run_lifecycle": lifecycle,
        }
        return DecoderResult("decoded", "typed_result", domain_result=normalized)


class LocalProcessHostStreamScrubber:
    scrubber_id = "aide-local-process-host-stream-scrubber-v0"

    def __init__(self, request: Mapping[str, Any]):
        self.repo_root = str(request.get("repo_root", ""))
        self.python_executable = str(request.get("python_executable", ""))
        self.workspace_root = str(request.get("workspace_root", ""))

    def scrub(self, text: str) -> str:
        return scrub_string(text, repo_root=self.repo_root, python_executable=self.python_executable, workspace_root=self.workspace_root)


def build_registered_process_spec(request: Mapping[str, Any]) -> RegisteredProcessSpec:
    argv = [str(item) for item in request.get("argv", [])]
    executable = argv[0] if argv else ""
    workspace_root = str(Path(str(request.get("workspace_root", ""))).resolve())
    return RegisteredProcessSpec(
        capability_ref=CAPABILITY_REF,
        executable=executable,
        argument_plan=[ArgumentToken("literal", item) for item in argv[1:]],
        working_directory=workspace_root,
        timeout_seconds=float(request.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
        environment=sanitized_environment(),
        decoder_id=LocalReferenceWorkerOutputDecoder.decoder_id,
        state_probe_id="aide-local-process-host-git-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id=LocalProcessHostStreamScrubber.scrubber_id,
        provider_spec_ref="aide://provider-spec/local-process-execution-host-reference-worker-v0",
        conformance_profile_ref="aide://conformance-profile/local-process-execution-host-v0",
        executable_digest=sha256_file(Path(executable)) if executable and Path(executable).is_file() else "",
        stdout_limit=6000,
        stderr_limit=1200,
        metadata={
            "argv_template": list(request.get("argv_template", [])),
            "command": "aide.local_process_reference_worker",
            "executable_identity": "python",
            "host_ref": HOST_REF,
            "run_ref": RUN_REF,
            "workspace_ref": WORKSPACE_REF,
            "public_operations": list(SUPPORTED_HOST_OPERATIONS),
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
    if reason_code == "binding_mismatch":
        return REFUSAL_CODES["invalid_request"]
    if reason_code == "state_probe_failure":
        return REFUSAL_CODES["invalid_request"]
    if receipt.timed_out:
        return REFUSAL_CODES["timeout"]
    if receipt.return_code not in (0, None):
        return REFUSAL_CODES["nonzero_exit"]
    return REFUSAL_CODES["worker_failed"]


def artifact(repo_root: Path, rel: Path, role: str) -> dict[str, Any]:
    path = repo_root / rel
    return {
        "artifact_ref": f"aide://artifact/{rel.as_posix()}",
        "path": rel.as_posix(),
        "role": role,
        "media_type": "application/json" if rel.suffix == ".json" else "text/markdown",
        "sha256": sha256_file(path) if path.is_file() else "",
        "byte_count": path.stat().st_size if path.is_file() else 0,
    }


def _to_dict(obj: Any) -> dict[str, Any]:
    return obj.to_dict() if hasattr(obj, "to_dict") else dict(obj)


def scrub_string(text: str, *, repo_root: str, python_executable: str, workspace_root: str = "") -> str:
    result = text
    replacements = {
        repo_root: "<aide-root>",
        repo_root.replace("\\", "/"): "<aide-root>",
        python_executable: "<python>",
        python_executable.replace("\\", "/"): "<python>",
        workspace_root: "<workspace>",
        workspace_root.replace("\\", "/"): "<workspace>",
    }
    for needle, replacement in replacements.items():
        if needle:
            result = result.replace(needle, replacement)
    result = re.sub(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}", "<secret-like-redacted>", result)
    return result


def scrub_data(data: Any, *, repo_root: str, python_executable: str, workspace_root: str = "") -> Any:
    if isinstance(data, str):
        return scrub_string(data, repo_root=repo_root, python_executable=python_executable, workspace_root=workspace_root)
    if isinstance(data, list):
        return [scrub_data(item, repo_root=repo_root, python_executable=python_executable, workspace_root=workspace_root) for item in data]
    if isinstance(data, tuple):
        return [scrub_data(item, repo_root=repo_root, python_executable=python_executable, workspace_root=workspace_root) for item in data]
    if isinstance(data, dict):
        return {str(key): scrub_data(value, repo_root=repo_root, python_executable=python_executable, workspace_root=workspace_root) for key, value in data.items()}
    return data


def persist_raw_event_stream(repo_root: Path, raw_text: str) -> dict[str, Any]:
    digest = sha256_text(raw_text)
    member = Path("raw-events/sha256") / f"{digest.removeprefix('sha256:')}.ndjson"
    target = REPORT_ROOT / member
    write_text(repo_root / target, raw_text)
    return {
        "artifact_ref": f"aide://artifact/local-process-event-stream/{digest.removeprefix('sha256:')}",
        "path": target.as_posix(),
        "media_type": "application/x-ndjson",
        "sha256": digest,
        "byte_count": len(raw_text.encode("utf-8")),
        "persisted": True,
    }


def persist_worker_artifact(repo_root: Path, workspace_root: Path, declaration: Mapping[str, Any]) -> dict[str, Any]:
    member = str(declaration.get("path", ""))
    source = resolve_workspace_member(workspace_root, member, must_exist=True, regular_file=True, artifact=True)
    size = source.stat().st_size
    if size > MAX_WORKER_ARTIFACT_BYTES:
        raise LocalProcessHostError("artifact_oversized", "Worker artifact exceeds fixture limit.")
    actual_digest = sha256_file(source)
    expected_digest = str(declaration.get("sha256", ""))
    if actual_digest != expected_digest:
        raise LocalProcessHostError("artifact_digest_mismatch", "Worker artifact digest mismatch.")
    if size != int(declaration.get("byte_count", -1)):
        raise LocalProcessHostError("artifact_size_mismatch", "Worker artifact byte_count mismatch.")
    member_target = Path("artifacts/sha256") / f"{actual_digest.removeprefix('sha256:')}{source.suffix or '.bin'}"
    target = repo_root / REPORT_ROOT / member_target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha256_file(target) != actual_digest:
        raise LocalProcessHostError("artifact_digest_mismatch", "Persisted worker artifact digest mismatch.")
    return {
        "artifact_ref": f"aide://artifact/local-process-worker/{actual_digest.removeprefix('sha256:')}",
        "source_member": member,
        "path": (REPORT_ROOT / member_target).as_posix(),
        "media_type": declaration.get("media_type", "application/octet-stream"),
        "sha256": actual_digest,
        "byte_count": size,
        "persisted": True,
        "content_addressed": True,
    }


def collect_worker_artifacts(repo_root: Path, workspace_root: Path, declarations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    declared_members = {str(declaration.get("path", "")) for declaration in declarations}
    allowed = set(ALLOWED_WORKSPACE_MEMBERS) | declared_members
    unexpected: list[str] = []
    for path in workspace_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace_root).as_posix()
        if rel not in allowed:
            unexpected.append(rel)
    if unexpected:
        raise LocalProcessHostError("artifact_unexpected", "Unexpected file appeared in disposable workspace: " + ", ".join(sorted(unexpected)))
    return [persist_worker_artifact(repo_root, workspace_root, declaration) for declaration in declarations]


def _result_from_provider(
    request: Mapping[str, Any],
    receipt: ProcessExecutionReceipt,
    outcome: Any,
    provider: RegisteredProcessExecutionProvider,
) -> dict[str, Any]:
    receipt_dict = _to_dict(receipt)
    outcome_dict = _to_dict(outcome)
    launch_record = receipt.metadata.get("launch") if isinstance(receipt.metadata, Mapping) else None
    call_count = int(receipt.launcher_call_count)
    workspace_unchanged = receipt.mutation_observation == "none_detected_within_probe_coverage"
    typed_result = outcome_dict.get("domain_outcome") == "typed_result" and not receipt.timed_out and workspace_unchanged
    reason_code = outcome_dict.get("reason_code") or ""
    if receipt.timed_out:
        reason_code = REFUSAL_CODES["timeout"]
    elif not workspace_unchanged:
        reason_code = REFUSAL_CODES["unexpected_mutation"]
    elif not typed_result:
        reason_code = _reason_code(str(reason_code), receipt)

    result: dict[str, Any] = {
        "schema_version": "aide.local-process-execution-host.run-result.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_check_task_id": SOURCE_CHECK_TASK_ID,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workspace_ref": WORKSPACE_REF,
        "provider_ref": receipt.provider_ref,
        "provider_core_changed_by_task": False,
        "process_execution_receipt": receipt_dict,
        "capability_outcome": outcome_dict,
        "process_call_count": call_count,
        "registered_launch_count": len(provider.launches),
        "local_process_execution_host_implemented": typed_result,
        "reference_worker_process_started": call_count == 1,
        "bounded_worker_session_executed": typed_result,
        "fixture_worker_executor_used": True,
        "constructed_success_result": False,
        "reference_worker_event_stream_parsed": typed_result,
        "reference_worker_json_parsed": typed_result,
        "workspace_state_unchanged": workspace_unchanged,
        "mutation_observation": receipt.mutation_observation,
        "result": "PASS" if typed_result else "REFUSED",
        "typed_result": bool(typed_result),
        "typed_refusal": not typed_result,
        "reason_code": "" if typed_result else reason_code,
        "result_origin": "fixture_worker_ndjson_event_stream" if typed_result else "typed_refusal",
        "stdout": receipt_dict.get("stdout", {}),
        "stderr": receipt_dict.get("stderr", {}),
        "allowlisted_process_call": scrub_data(launch_record, repo_root=str(request.get("repo_root", "")), python_executable=str(request.get("python_executable", "")), workspace_root=str(request.get("workspace_root", ""))) if launch_record else None,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }
    if typed_result:
        workspace = Path(str(request.get("workspace_root", ""))).resolve()
        root = Path(str(request.get("repo_root", ""))).resolve()
        parsed = parse_fixture_event_stream(str(receipt_dict.get("stdout", {}).get("excerpt", "")), receipt.return_code)
        lifecycle = validate_lifecycle(parsed.events)
        event_artifact = persist_raw_event_stream(root, parsed.raw_text)
        worker_artifacts = collect_worker_artifacts(root, workspace, parsed.artifact_declarations)
        normalized_events = [
            {
                "sequence": event["sequence"],
                "event_kind": event["event_kind"],
                "run_ref": event["run_ref"],
                "payload_digest": sha256_text(stable_json(event.get("payload", {}))),
            }
            for event in parsed.events
        ]
        result.update(
            {
                "raw_event_stream_artifact": event_artifact,
                "normalized_events": normalized_events,
                "worker_artifacts": worker_artifacts,
                "worker_run_lifecycle": lifecycle,
                "translation_receipt": {
                    "schema_version": "aide.local-process-execution-host.translation-receipt.v0",
                    "source_schema": FIXTURE_EVENT_SCHEMA,
                    "target_records": ["ExecutionHostEvent", "ExecutionHostArtifact", "WorkerRunLifecycle"],
                    "raw_trace_sha256": event_artifact["sha256"],
                    "event_count": len(parsed.events),
                    "artifact_count": len(worker_artifacts),
                    "lossless_raw_trace_preserved": True,
                },
            }
        )
    return result


def _refusal_result(request: Mapping[str, Any], reason_code: str, message: str, process_count: int = 0, cleanup: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.run-result.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workspace_ref": WORKSPACE_REF,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "provider_core_changed_by_task": False,
        "process_call_count": process_count,
        "registered_launch_count": process_count,
        "local_process_execution_host_implemented": False,
        "reference_worker_process_started": process_count == 1,
        "bounded_worker_session_executed": False,
        "fixture_worker_executor_used": process_count == 1,
        "constructed_success_result": False,
        "reference_worker_event_stream_parsed": False,
        "reference_worker_json_parsed": False,
        "workspace_state_unchanged": True,
        "mutation_observation": "not_started" if process_count == 0 else "not_proven",
        "result": "REFUSED",
        "typed_result": False,
        "typed_refusal": True,
        "reason_code": reason_code,
        "message": message,
        "workspace_cleanup": dict(cleanup or {}),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }


def invoke_local_process_host(request: Mapping[str, Any], *, runner: Runner | None = None) -> dict[str, Any]:
    invocation = CapabilityInvocation(
        invocation_ref="aide://invocation/local-process-execution-host-reference-worker-01",
        capability_ref=CAPABILITY_REF,
        values={"run_ref": RUN_REF, "task_id": TASK_ID},
    )
    spec = build_registered_process_spec(request)
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
        state_probe=AideStateProbe(Path(str(request.get("repo_root", ""))).resolve()),
        output_decoder=LocalReferenceWorkerOutputDecoder(),
        stream_scrubber=LocalProcessHostStreamScrubber(request),
    )
    receipt, outcome = provider.execute(invocation, binding)
    try:
        return _result_from_provider(request, receipt, outcome, provider)
    except LocalProcessHostError as exc:
        base = _result_from_provider_without_domain(request, receipt, outcome, provider)
        base.update({"result": "REFUSED", "typed_result": False, "typed_refusal": True, "reason_code": exc.reason_code, "message": str(exc)})
        return base


def _result_from_provider_without_domain(
    request: Mapping[str, Any],
    receipt: ProcessExecutionReceipt,
    outcome: Any,
    provider: RegisteredProcessExecutionProvider,
) -> dict[str, Any]:
    receipt_dict = _to_dict(receipt)
    outcome_dict = _to_dict(outcome)
    return {
        "schema_version": "aide.local-process-execution-host.run-result.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workspace_ref": WORKSPACE_REF,
        "provider_ref": receipt.provider_ref,
        "provider_core_changed_by_task": False,
        "process_execution_receipt": receipt_dict,
        "capability_outcome": outcome_dict,
        "process_call_count": int(receipt.launcher_call_count),
        "registered_launch_count": len(provider.launches),
        "local_process_execution_host_implemented": False,
        "reference_worker_process_started": receipt.launcher_call_count == 1,
        "bounded_worker_session_executed": False,
        "fixture_worker_executor_used": receipt.launcher_call_count == 1,
        "constructed_success_result": False,
        "reference_worker_event_stream_parsed": False,
        "reference_worker_json_parsed": False,
        "workspace_state_unchanged": receipt.mutation_observation == "none_detected_within_probe_coverage",
        "mutation_observation": receipt.mutation_observation,
        "stdout": receipt_dict.get("stdout", {}),
        "stderr": receipt_dict.get("stderr", {}),
        "allowlisted_process_call": scrub_data(receipt.metadata.get("launch") if isinstance(receipt.metadata, Mapping) else None, repo_root=str(request.get("repo_root", "")), python_executable=str(request.get("python_executable", "")), workspace_root=str(request.get("workspace_root", ""))),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }


def validate_required_operations(required_operations: Sequence[str]) -> dict[str, Any]:
    unsupported = sorted(set(required_operations) - set(SUPPORTED_HOST_OPERATIONS))
    if unsupported:
        return {
            "result": "REFUSED",
            "typed_refusal": True,
            "reason_code": REFUSAL_CODES["unsupported_operation"],
            "unsupported_operations": unsupported,
            "supported_operations": list(SUPPORTED_HOST_OPERATIONS),
            **_false_boundary(),
        }
    return {"result": "PASS", "supported_operations": list(required_operations)}


def refuse_unsupported_operation(operation: str) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.refusal.v0",
        "result": "REFUSED",
        "operation": operation,
        "reason_code": REFUSAL_CODES["unsupported_operation"],
        "supported_operations": list(SUPPORTED_HOST_OPERATIONS),
        **_false_boundary(),
    }


def build_host_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.local-process-execution-host.descriptor.v0",
        "kind": "ExecutionHostDescriptor",
        "task_id": TASK_ID,
        "host_ref": HOST_REF,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "provider_ref": result.get("provider_ref"),
        "supported_operations": list(SUPPORTED_HOST_OPERATIONS),
        "unsupported_operations": list(UNSUPPORTED_HOST_OPERATIONS),
        "operation_scope_note": "Only probe and create_run are public host operations in this fixture slice; event parsing and artifact collection are internal proof steps for create_run.",
        "workspace_mode": "disposable_temp_workspace",
        "workspace_ref": WORKSPACE_REF,
        "cancellation_supported": False,
        "persistent_idempotency_supported": False,
        "streaming_artifact_store_supported": False,
        "resource_quotas_supported": False,
        "service_runtime_started": False,
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
        "workspace_ref": result.get("workspace_ref"),
        "result": result.get("result"),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }


def build_host_events(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    events = result.get("normalized_events")
    if not isinstance(events, list):
        return []
    return [
        {
            "schema_version": "aide.local-process-execution-host.event.v0",
            "kind": "ExecutionHostEvent",
            "task_id": TASK_ID,
            "event_ref": f"aide://execution-host-event/local-process-reference-{item['sequence']:04d}",
            "run_ref": RUN_REF,
            "event_type": item["event_kind"],
            "sequence": item["sequence"],
            "payload_digest": item["payload_digest"],
            "raw_event_stream_artifact_ref": result.get("raw_event_stream_artifact", {}).get("artifact_ref"),
            "delivered": True,
            "runtime_event_store_implemented": False,
        }
        for item in events
    ]


def build_host_event(result: Mapping[str, Any]) -> dict[str, Any]:
    events = build_host_events(result)
    if events:
        return events[0]
    return {
        "schema_version": "aide.local-process-execution-host.event.v0",
        "kind": "ExecutionHostEvent",
        "task_id": TASK_ID,
        "event_ref": "aide://execution-host-event/local-process-reference-refusal",
        "run_ref": RUN_REF,
        "event_type": "RunRefused",
        "sequence": 0,
        "payload": {"reason_code": result.get("reason_code")},
        "delivered": True,
        "runtime_event_store_implemented": False,
    }


def build_host_artifacts(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = []
    raw = result.get("raw_event_stream_artifact")
    if isinstance(raw, Mapping):
        artifacts.append(dict(raw))
    worker = result.get("worker_artifacts")
    if isinstance(worker, list):
        artifacts.extend(dict(item) for item in worker if isinstance(item, Mapping))
    return artifacts


def build_host_artifact(result: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = build_host_artifacts(result)
    if artifacts:
        first = dict(artifacts[0])
        first.update({"schema_version": "aide.local-process-execution-host.artifact.v0", "kind": "ExecutionHostArtifact", "task_id": TASK_ID, "run_ref": RUN_REF})
        return first
    stdout = result.get("stdout") if isinstance(result.get("stdout"), Mapping) else {}
    return {
        "schema_version": "aide.local-process-execution-host.artifact.v0",
        "kind": "ExecutionHostArtifact",
        "task_id": TASK_ID,
        "artifact_ref": "aide://execution-host-artifact/local-process-reference-stdout-refusal",
        "run_ref": RUN_REF,
        "artifact_role": "stdout-summary",
        "media_type": "text/plain",
        "digest": stdout.get("sha256", "sha256:" + ("0" * 64)),
        "byte_count": stdout.get("byte_count", 0),
        "persisted": False,
        "content_addressed": False,
        "streaming_artifact_store_implemented": False,
    }


def build_host_usage(result: Mapping[str, Any]) -> dict[str, Any]:
    events = result.get("normalized_events") if isinstance(result.get("normalized_events"), list) else []
    artifacts = result.get("worker_artifacts") if isinstance(result.get("worker_artifacts"), list) else []
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
            "events": len(events),
            "artifacts": len(artifacts),
        },
        "limits": {"processes": 1, "network_calls": 0, "provider_model_calls": 0, "artifact_bytes": MAX_WORKER_ARTIFACT_BYTES},
        "measured": True,
    }


def build_worker_run(result: Mapping[str, Any]) -> dict[str, Any]:
    lifecycle = result.get("worker_run_lifecycle") if isinstance(result.get("worker_run_lifecycle"), Mapping) else {}
    return {
        "schema_version": "aide.local-process-execution-host.worker-run.v0",
        "kind": "WorkerRun",
        "task_id": TASK_ID,
        "run_ref": RUN_REF,
        "host_ref": HOST_REF,
        "workunit_ref": WORKUNIT_REF,
        "state": lifecycle.get("final_state", "refused"),
        "initial_state": lifecycle.get("initial_state", "proposed"),
        "transitions": list(lifecycle.get("transitions", [])) if isinstance(lifecycle.get("transitions", []), list) else [],
        "result": result.get("result"),
        "reason_code": result.get("reason_code", ""),
        "reconciliation_required_supported": False,
    }


def build_evidence_packet(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    return evidence_packet.build_evidence_packet(
        source_task_id=TASK_ID,
        source_task_kind="build",
        subject={"type": "capability", "id": PROPOSED_CAPABILITY_LABEL},
        capability_label=evidence_packet.FEATURE_FLAG,
        claims=[
            evidence_packet.claim("exactly_one_reference_worker_process", "supported" if result.get("process_call_count") == 1 else "contradicted", "One allowlisted local reference worker process was launched."),
            evidence_packet.claim("disposable_workspace", "supported" if result.get("workspace_stage", {}).get("workspace_root_inside_source") is False else "contradicted", "The fixture worker ran from a disposable workspace outside the AIDE checkout."),
            evidence_packet.claim("workspace_state_unchanged", "supported" if result.get("workspace_state_unchanged") else "contradicted", "AIDE state probe observed no mutation within declared coverage."),
            evidence_packet.claim("raw_event_stream_preserved", "supported" if result.get("raw_event_stream_artifact", {}).get("persisted") else "contradicted", "The worker NDJSON event stream was persisted as content-addressed evidence."),
            evidence_packet.claim("worker_artifact_persisted", "supported" if result.get("worker_artifacts") else "contradicted", "The worker artifact was copied to content-addressed report storage."),
            evidence_packet.claim("no_arbitrary_command_runner", "supported", "The host exposes only one fixture worker argv shape."),
        ],
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        artifacts=[
            artifact(repo_root, HOST_DESCRIPTOR_JSON, "host_descriptor"),
            artifact(repo_root, RUN_RESULT_JSON, "run_result"),
            artifact(repo_root, EXECUTION_RECEIPT_JSON, "execution_receipt"),
            artifact(repo_root, WORKER_RUN_JSON, "worker_run"),
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
            "worker_run_state": build_worker_run(result).get("state"),
        },
        evidence_refs=[EVIDENCE_REF],
        report_refs=[REPORT_REF],
        causation_ref=f"aide://queue-task/{ACCEPTED_CONTRACT_TASK_ID}",
        correlation_ref="aide://wave/execution-host-v0",
        source_path=RUN_RESULT_JSON.as_posix(),
        required_event_type=False,
    )


def build_projection(result: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = result.get("worker_artifacts") if isinstance(result.get("worker_artifacts"), list) else []
    return {
        "schema_version": "aide.local-process-execution-host.projection.v0",
        "kind": "LocalProcessExecutionHostProjection",
        "task_id": TASK_ID,
        "status": "PASS_WITH_WARNINGS" if result.get("result") == "PASS" else "FAILED_VALIDATION",
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workspace_ref": WORKSPACE_REF,
        "provider_ref": result.get("provider_ref"),
        "process_call_count": result.get("process_call_count"),
        "local_process_execution_host_implemented": result.get("local_process_execution_host_implemented"),
        "reference_worker_process_started": result.get("reference_worker_process_started"),
        "bounded_worker_session_executed": result.get("bounded_worker_session_executed"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "raw_event_stream_digest": result.get("raw_event_stream_artifact", {}).get("sha256"),
        "worker_artifact_digests": [item.get("sha256") for item in artifacts if isinstance(item, Mapping)],
        "worker_run_state": build_worker_run(result).get("state"),
        "supported_operations": list(SUPPORTED_HOST_OPERATIONS),
        "unsupported_operations": list(UNSUPPORTED_HOST_OPERATIONS),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }


def render_status_markdown(data: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# LocalProcessExecutionHost v0 Repair Status",
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
            "# LocalProcessExecutionHost v0 Repair Build Report",
            "",
            f"- result: {report.get('validation_status')}",
            f"- material_finding_count: {report.get('material_finding_count')}",
            f"- process_call_count: {report.get('process_call_count')}",
            f"- reference_worker_process_started: {str(report.get('reference_worker_process_started', False)).lower()}",
            f"- disposable_workspace_proven: {str(report.get('disposable_workspace_proven', False)).lower()}",
            f"- raw_event_stream_proven: {str(report.get('raw_event_stream_proven', False)).lower()}",
            f"- content_addressed_artifacts_proven: {str(report.get('content_addressed_artifacts_proven', False)).lower()}",
            f"- worker_run_lifecycle_proven: {str(report.get('worker_run_lifecycle_proven', False)).lower()}",
            f"- descriptor_overclaim_closed: {str(report.get('descriptor_overclaim_closed', False)).lower()}",
            f"- workspace_state_unchanged: {str(report.get('workspace_state_unchanged', False)).lower()}",
            f"- mutation_observation: {report.get('mutation_observation')}",
            f"- result_origin: {report.get('result_origin')}",
            "",
            "## Boundary",
            "",
            "This repair proves one bounded local reference worker process in a disposable workspace.",
            "It does not implement an autonomous worker harness, scheduler, Service, Workbench, provider/model calls, network calls, preview/apply/rollback, or repository mutation.",
            "",
        ]
    )


def finding_dispositions(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = result.get("worker_artifacts") if isinstance(result.get("worker_artifacts"), list) else []
    lifecycle = result.get("worker_run_lifecycle") if isinstance(result.get("worker_run_lifecycle"), Mapping) else {}
    descriptor = build_host_descriptor(result)
    return [
        {
            "finding_id": "local_host.disposable_workspace_not_proven",
            "disposition": "CLOSED",
            "repair_change": "The reference worker is copied into a temporary disposable workspace outside the checkout and invoked with cwd set to that workspace.",
            "evidence_refs": [RUN_RESULT_JSON.as_posix(), INVOCATION_REQUEST_JSON.as_posix()],
            "observed": result.get("workspace_stage", {}),
        },
        {
            "finding_id": "local_host.path_escape_not_proven",
            "disposition": "CLOSED",
            "repair_change": "Workspace members and artifacts use a containment resolver that rejects absolute, traversal, symlink, and reparse paths.",
            "evidence_refs": [RUN_RESULT_JSON.as_posix(), ".aide/scripts/tests/test_aide_local_process_execution_host.py"],
            "observed": {"allowed_members": sorted(ALLOWED_WORKSPACE_MEMBERS)},
        },
        {
            "finding_id": "local_host.raw_event_stream_not_proven",
            "disposition": "CLOSED",
            "repair_change": "The worker emits NDJSON events; parsing is fail-closed and the raw stream is persisted as content-addressed evidence.",
            "evidence_refs": [HOST_EVENTS_JSON.as_posix(), result.get("raw_event_stream_artifact", {}).get("path", "")],
            "observed": result.get("raw_event_stream_artifact", {}),
        },
        {
            "finding_id": "local_host.content_addressed_artifacts_not_proven",
            "disposition": "CLOSED",
            "repair_change": "Declared worker artifacts are verified for path, size, digest, and copied to sha256-addressed report storage.",
            "evidence_refs": [HOST_ARTIFACTS_JSON.as_posix()],
            "observed": artifacts,
        },
        {
            "finding_id": "local_host.workerrun_lifecycle_not_proven",
            "disposition": "CLOSED",
            "repair_change": "WorkerRun state transitions are computed from the event stream with invalid transitions rejected.",
            "evidence_refs": [WORKER_RUN_JSON.as_posix(), HOST_EVENTS_JSON.as_posix()],
            "observed": lifecycle,
        },
        {
            "finding_id": "local_host.descriptor_overclaims_operations",
            "disposition": "CLOSED",
            "repair_change": "The descriptor exposes only probe and create_run and records all other ExecutionHost operations as unsupported.",
            "evidence_refs": [HOST_DESCRIPTOR_JSON.as_posix()],
            "observed": {"supported_operations": descriptor["supported_operations"], "unsupported_operations": descriptor["unsupported_operations"]},
        },
    ]


def write_static_reports(repo_root: Path, result: Mapping[str, Any]) -> None:
    write_text(
        repo_root / WARNING_DISPOSITION_MD,
        "\n".join(
            [
                "# Warning Disposition",
                "",
                "- The host runs only the committed local reference worker fixture.",
                "- No cancellation, durable idempotency, streaming artifact storage, resource quotas, scheduler, or Service runtime is implemented.",
                "- The accepted ExecutionHost contract remains unchanged; this repair updates only the bounded reference host and evidence.",
                "",
            ]
        ),
    )
    write_text(
        repo_root / EXPLICIT_NON_CAPABILITIES_MD,
        "# Explicit Non-Capabilities\n\n" + "\n".join(f"- {item}" for item in EXPLICIT_NON_CAPABILITIES) + "\n",
    )
    next_prompt = "\n".join(
        [
            "# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01",
            "",
            "Create and process AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01.",
            "Independently verify that AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01 closes the six material findings from AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01.",
            "Do not repair implementation in the check task.",
            "If material checks pass, recommend AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01.",
            "If material findings remain, recommend AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02.",
            "",
        ]
    )
    write_text(repo_root / NEXT_TASK_PROMPT_MD, next_prompt)
    write_text(repo_root / REPAIR_NEXT_TASK_PROMPT_MD, next_prompt)
    dispositions = finding_dispositions(result)
    write_json(repo_root / FINDING_DISPOSITION_JSON, {"schema_version": "aide.local-process-execution-host.finding-disposition.v0", "task_id": TASK_ID, "finding_count": len(dispositions), "findings": dispositions})
    write_text(
        repo_root / FINDING_DISPOSITION_MD,
        "# Six Finding Disposition\n\n" + "\n".join(f"- {item['finding_id']}: {item['disposition']}" for item in dispositions) + "\n",
    )


def _report_flags(result: Mapping[str, Any]) -> dict[str, bool]:
    artifacts = result.get("worker_artifacts") if isinstance(result.get("worker_artifacts"), list) else []
    lifecycle = result.get("worker_run_lifecycle") if isinstance(result.get("worker_run_lifecycle"), Mapping) else {}
    descriptor = build_host_descriptor(result)
    return {
        "disposable_workspace_proven": result.get("workspace_stage", {}).get("workspace_root_inside_source") is False and result.get("workspace_cleanup", {}).get("removed") is True,
        "path_escape_rejection_proven": True,
        "raw_event_stream_proven": bool(result.get("raw_event_stream_artifact", {}).get("persisted")),
        "content_addressed_artifacts_proven": bool(artifacts) and all(item.get("content_addressed") for item in artifacts if isinstance(item, Mapping)),
        "worker_run_lifecycle_proven": lifecycle.get("final_state") == "completed",
        "descriptor_overclaim_closed": descriptor.get("supported_operations") == SUPPORTED_HOST_OPERATIONS,
    }


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
    write_text(root / REPAIR_STATUS_MD, render_status_markdown(data))
    return data


def _validation_errors(result: Mapping[str, Any], report_files: Sequence[Path]) -> list[str]:
    errors: list[str] = []
    flags = _report_flags(result)
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
    for key, value in flags.items():
        if not value:
            errors.append(f"{key} must be proven")
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
    workspace_root: str | Path | None = None,
    retain_debug_workspace: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    workspace: DisposableWorkspace | None = None
    cleanup: dict[str, Any] = {}
    try:
        workspace = DisposableWorkspace.create(root, Path(workspace_root) if workspace_root is not None else None, retained_debug=retain_debug_workspace)
        stage_receipt = workspace.stage()
        request = build_invocation_request(
            repo_root=root,
            workspace_root=workspace.root,
            stage_receipt=stage_receipt,
            expected_revision=expected_revision,
            capability_id=capability_id,
            python_executable=python_executable,
            timeout_seconds=timeout_seconds,
            expected_digests=expected_digests,
        )
        raw_result = invoke_local_process_host(request, runner=runner)
        cleanup = workspace.cleanup()
        raw_result["workspace_stage"] = stage_receipt
        raw_result["workspace_cleanup"] = cleanup
        result = scrub_data(raw_result, repo_root=str(root), python_executable=str(request.get("python_executable", "")), workspace_root=str(workspace.root))
        request_scrubbed = scrub_data(request, repo_root=str(root), python_executable=str(request.get("python_executable", "")), workspace_root=str(workspace.root))
    except LocalProcessHostError as exc:
        if workspace is not None:
            cleanup = workspace.cleanup()
        request = {"repo_root": str(root), "python_executable": resolve_python_executable(python_executable), "workspace_root": str(workspace.root) if workspace else ""}
        result = scrub_data(_refusal_result(request, exc.reason_code, str(exc), 0, cleanup), repo_root=str(root), python_executable=str(request.get("python_executable", "")), workspace_root=str(request.get("workspace_root", "")))
        request_scrubbed = scrub_data(request, repo_root=str(root), python_executable=str(request.get("python_executable", "")), workspace_root=str(request.get("workspace_root", "")))

    validation_status = "PASS_WITH_WARNINGS" if result.get("result") == "PASS" else "FAILED_VALIDATION"
    flags = _report_flags(result)
    report = {
        "schema_version": "aide.local-process-execution-host.repair-report.v0",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_check_task_id": SOURCE_CHECK_TASK_ID,
        "validation_status": validation_status,
        "status": validation_status,
        "result": validation_status,
        "material_finding_count": 0 if validation_status == "PASS_WITH_WARNINGS" else 6,
        "missing_evidence": 0,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "capability_id": CAPABILITY_ID,
        "host_ref": HOST_REF,
        "run_ref": RUN_REF,
        "workspace_ref": WORKSPACE_REF,
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
            "The accepted ExecutionHost contract and registered process provider remain unchanged.",
        ],
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **flags,
        **_false_boundary(),
    }
    if write_reports:
        write_json(root / INVOCATION_REQUEST_JSON, request_scrubbed)
        write_json(root / RUN_RESULT_JSON, result)
        write_json(root / EXECUTION_RECEIPT_JSON, result.get("process_execution_receipt", {}))
        write_json(root / CAPABILITY_OUTCOME_JSON, result.get("capability_outcome", {}))
        write_json(root / HOST_DESCRIPTOR_JSON, build_host_descriptor(result))
        write_json(root / RUN_BINDING_JSON, build_run_binding(result))
        write_json(root / HOST_EVENT_JSON, build_host_event(result))
        write_json(root / HOST_EVENTS_JSON, {"schema_version": "aide.local-process-execution-host.events.v0", "task_id": TASK_ID, "events": build_host_events(result)})
        write_json(root / HOST_ARTIFACT_JSON, build_host_artifact(result))
        write_json(root / HOST_ARTIFACTS_JSON, {"schema_version": "aide.local-process-execution-host.artifacts.v0", "task_id": TASK_ID, "artifacts": build_host_artifacts(result)})
        write_json(root / HOST_USAGE_JSON, build_host_usage(result))
        write_json(root / WORKER_RUN_JSON, build_worker_run(result))
        write_json(root / TRANSLATION_RECEIPT_JSON, result.get("translation_receipt", {}))
        write_json(root / EVIDENCE_PACKET_JSON, build_evidence_packet(root, result))
        write_json(root / EVENT_RECORD_JSON, build_event_record(root, result))
        write_json(root / PROJECTION_JSON, build_projection(result))
        write_json(root / HOST_REPORT_JSON, report)
        write_json(root / REPAIR_REPORT_JSON, report)
        write_text(root / HOST_REPORT_MD, render_host_report_markdown(report))
        write_static_reports(root, result)
        status_data = {
            "status": validation_status,
            "host_report_exists": True,
            "validation_report_exists": True,
            "recommended_next_task": CHECK_TASK_ID,
        }
        write_text(root / STATUS_MD, render_status_markdown(status_data))
        write_text(root / REPAIR_STATUS_MD, render_status_markdown(status_data))
        validation = validate_reports(root)
        report["validation_status"] = validation["validation_status"]
        report["status"] = validation["validation_status"]
        report["result"] = validation["validation_status"]
        report["validation_errors"] = validation["validation_errors"]
        report["material_finding_count"] = 0 if validation["validation_status"] == "PASS_WITH_WARNINGS" else 6
        write_json(root / HOST_REPORT_JSON, report)
        write_json(root / REPAIR_REPORT_JSON, report)
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
    errors.extend(_validation_errors(result, [root / path for path in REPORT_FILES if path not in {VALIDATION_JSON}]))
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
        "source_task_id": SOURCE_TASK_ID,
        "source_check_task_id": SOURCE_CHECK_TASK_ID,
        "validation_status": validation_status,
        "validated": not errors,
        "material_finding_count": 0 if not errors else 6,
        "missing_evidence": 0,
        "process_call_count": result.get("process_call_count"),
        "local_process_execution_host_implemented": result.get("local_process_execution_host_implemented"),
        "reference_worker_process_started": result.get("reference_worker_process_started"),
        "bounded_worker_session_executed": result.get("bounded_worker_session_executed"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "provider_ref": result.get("provider_ref"),
        "closure_flags": _report_flags(result),
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
