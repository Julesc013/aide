"""Eureka public-alpha read-only process adapter.

This adapter proves a third reuse case for the proposed generic registered
process provider. It invokes exactly one existing Eureka command shape:
``<python> scripts/public_alpha_smoke.py --json``.

It is not a general Eureka command runner, worker host, runtime, provider/model
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
from core.protocol import envelope, event_record, evidence_packet, workunit
from core.protocol.execution_receipt import CapabilityOutcome, ProcessExecutionReceipt
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


TASK_ID = "AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01"
CHECK_TASK_ID = "AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01"
CAPABILITY_ID = "eureka.public-alpha-readonly.validate"
PROPOSED_CAPABILITY_LABEL = "eureka_public_alpha_readonly_validation_process_adapter_v0"
CAPABILITY_REF = "aide://capability/eureka-public-alpha-readonly-process-adapter-v0"
CONTEXT_DESCRIPTOR_REF = "aide://context/eureka-readonly-process-adapter"
CONTEXT_PACK_REF = "aide://context-pack/eureka-readonly-process-adapter-01"
WORKUNIT_REF = "aide://workunit/AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01"
EVIDENCE_REF = "aide://evidence/eureka-readonly-process-adapter"
REPORT_REF = "aide://report/eureka-readonly-process-adapter"
EVENT_REF = "aide://event/EVT-EUREKA-READONLY-PROCESS-ADAPTER-01"
DETERMINISTIC_TIMESTAMP = "2026-06-25T00:00:00+10:00"
DEFAULT_TIMEOUT_SECONDS = 120.0
EXPECTED_REMOTE_URL = "https://github.com/Julesc013/eureka.git"
REQUESTED_COMMAND_REL = Path("scripts/validate_public_alpha_readonly.py")
SELECTED_COMMAND_REL = Path("scripts/public_alpha_smoke.py")
SELECTED_COMMAND_IMPL_REL = Path("tools/release/public_alpha_smoke.py")
COMMAND_SOURCE_RELS = [SELECTED_COMMAND_REL, SELECTED_COMMAND_IMPL_REL]
STATE_PROBE_COVERAGE = [
    "git_revision",
    "git_porcelain_status",
    "git_tracked_tree_digest",
    "selected_command_digests",
]

REPORT_ROOT = Path(".aide/reports/eureka-readonly-process-adapter")
STATUS_MD = REPORT_ROOT / "status.md"
CONTEXT_DESCRIPTOR_JSON = REPORT_ROOT / "context-descriptor.json"
CONTEXT_PACK_JSON = REPORT_ROOT / "context-pack.json"
WORKUNIT_JSON = REPORT_ROOT / "workunit.json"
CAPABILITY_DESCRIPTOR_JSON = REPORT_ROOT / "capability-descriptor.json"
INVOCATION_REQUEST_JSON = REPORT_ROOT / "invocation-request.json"
EXECUTION_RECEIPT_JSON = REPORT_ROOT / "execution-receipt.json"
CAPABILITY_OUTCOME_JSON = REPORT_ROOT / "capability-outcome.json"
INVOCATION_RESULT_JSON = REPORT_ROOT / "invocation-result.json"
EVIDENCE_PACKET_JSON = REPORT_ROOT / "evidence-packet.json"
EVENT_RECORD_JSON = REPORT_ROOT / "event-record.json"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
ADAPTER_REPORT_JSON = REPORT_ROOT / "adapter-report.json"
ADAPTER_REPORT_MD = REPORT_ROOT / "adapter-report.md"
WARNING_DISPOSITION_MD = REPORT_ROOT / "warning-disposition.md"
EXPLICIT_NON_CAPABILITIES_MD = REPORT_ROOT / "explicit-non-capabilities.md"
NEXT_TASK_PROMPT_MD = REPORT_ROOT / "next-task-prompt.md"

REPORT_FILES = [
    STATUS_MD,
    CONTEXT_DESCRIPTOR_JSON,
    CONTEXT_PACK_JSON,
    WORKUNIT_JSON,
    CAPABILITY_DESCRIPTOR_JSON,
    INVOCATION_REQUEST_JSON,
    EXECUTION_RECEIPT_JSON,
    CAPABILITY_OUTCOME_JSON,
    INVOCATION_RESULT_JSON,
    EVIDENCE_PACKET_JSON,
    EVENT_RECORD_JSON,
    PROJECTION_JSON,
    VALIDATION_JSON,
    ADAPTER_REPORT_JSON,
    ADAPTER_REPORT_MD,
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
    "worker_executed",
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
    "registered_process_provider_acceptance",
    "arbitrary_command_runner",
    "generic_command_cli",
    "provider_core_mutation",
    "eureka_repository_mutation",
    "eureka_public_launch",
    "eureka_source_fanout",
    "downloads_uploads_install_execution",
    "provider_model_call",
    "network_call",
    "worker_execution",
    "service_runtime",
    "workbench_behavior",
    "preview_or_apply",
    "rollback",
    "patch_transaction_apply",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]

REFUSAL_CODES = {
    "unsupported_capability": "AIDE_EUREKA_READONLY_UNSUPPORTED_CAPABILITY",
    "invalid_request": "AIDE_EUREKA_READONLY_INVALID_REQUEST",
    "checkout_missing": "AIDE_EUREKA_READONLY_CHECKOUT_MISSING",
    "repository_identity_mismatch": "AIDE_EUREKA_READONLY_REPOSITORY_IDENTITY_MISMATCH",
    "revision_mismatch": "AIDE_EUREKA_READONLY_REVISION_MISMATCH",
    "dirty_checkout": "AIDE_EUREKA_READONLY_DIRTY_CHECKOUT",
    "script_missing": "AIDE_EUREKA_READONLY_SCRIPT_MISSING",
    "digest_mismatch": "AIDE_EUREKA_READONLY_DIGEST_MISMATCH",
    "timeout": "AIDE_EUREKA_READONLY_TIMEOUT",
    "nonzero_exit": "AIDE_EUREKA_READONLY_NONZERO_EXIT",
    "empty_output": "AIDE_EUREKA_READONLY_EMPTY_OUTPUT",
    "malformed_json": "AIDE_EUREKA_READONLY_MALFORMED_JSON",
    "schema_mismatch": "AIDE_EUREKA_READONLY_SCHEMA_MISMATCH",
    "validation_failed": "AIDE_EUREKA_READONLY_VALIDATION_FAILED",
    "inconsistent_returncode": "AIDE_EUREKA_READONLY_INCONSISTENT_RETURNCODE",
    "unexpected_mutation": "AIDE_EUREKA_READONLY_UNEXPECTED_REPOSITORY_MUTATION",
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


def resolve_python_executable(value: str | Path | None = None) -> str:
    return str((Path(value) if value else Path(sys.executable)).resolve())


def resolve_eureka_root(value: str | Path | None = None, *, aide_root: Path | None = None) -> Path:
    if value:
        return Path(value).resolve()
    for env_name in ("AIDE_EUREKA_ROOT", "EUREKA_ROOT"):
        if os.environ.get(env_name):
            return Path(os.environ[env_name]).resolve()
    root = (aide_root or Path.cwd()).resolve()
    candidates: list[Path] = []
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "Eureka" / "eureka")
    candidates.append(root.parent / "eureka")
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate.resolve()
    return (root.parent / "eureka").resolve()


def sanitized_environment() -> dict[str, str]:
    allowed = ["COMSPEC", "PATH", "PATHEXT", "SYSTEMROOT", "TEMP", "TMP", "WINDIR", "SystemDrive", "USERPROFILE", "HOME"]
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PYTHONUTF8": "1", "PYTHONHASHSEED": "0"})
    return env


def build_argv(python_executable: str, eureka_root: Path) -> list[str]:
    return [str(Path(python_executable).resolve()), str((eureka_root / SELECTED_COMMAND_REL).resolve()), "--json"]


def capture_eureka_state(root: Path) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {"repository_present": False}
    ok_revision, revision = git_stdout(root, ["rev-parse", "HEAD"])
    ok_status, status = git_stdout(root, ["status", "--porcelain=v1", "--untracked-files=all"])
    ok_tree, tree = git_stdout(root, ["ls-files", "-s"])
    ok_remote, remote = git_stdout(root, ["remote", "get-url", "origin"])
    digests: dict[str, str] = {}
    for rel in COMMAND_SOURCE_RELS:
        path = root / rel
        digests[rel.as_posix()] = sha256_file(path) if path.is_file() else "missing"
    return {
        "repository_present": True,
        "revision": revision if ok_revision else "",
        "revision_error": "" if ok_revision else revision,
        "remote_url": remote if ok_remote else "",
        "remote_error": "" if ok_remote else remote,
        "porcelain_status": status if ok_status else "",
        "porcelain_status_digest": sha256_text(status if ok_status else ""),
        "tracked_tree_digest": sha256_text(tree if ok_tree else ""),
        "tracked_tree_observed": ok_tree,
        "selected_command_digests": digests,
        "clean": ok_status and status == "",
    }


def build_invocation_request(
    *,
    repo_root: str | Path = ".",
    eureka_root: str | Path | None = None,
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    aide_root = Path(repo_root).resolve()
    root = resolve_eureka_root(eureka_root, aide_root=aide_root)
    revision = expected_revision
    if revision is None and (root / ".git").exists():
        ok, observed = git_stdout(root, ["rev-parse", "HEAD"])
        revision = observed if ok else ""
    py = resolve_python_executable(python_executable)
    if expected_digests is None:
        expected_digests = {rel.as_posix(): sha256_file(root / rel) for rel in COMMAND_SOURCE_RELS if (root / rel).is_file()}
    return {
        "schema_version": "aide.eureka-readonly-process.invocation-request.v1",
        "task_id": TASK_ID,
        "capability_id": capability_id,
        "expected_capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "repo_root": str(aide_root),
        "eureka_root": str(root),
        "expected_revision": revision or "",
        "expected_remote_url": EXPECTED_REMOTE_URL,
        "python_executable": py,
        "requested_command": REQUESTED_COMMAND_REL.as_posix(),
        "selected_command": SELECTED_COMMAND_REL.as_posix(),
        "selected_command_reason": "requested validator absent in pinned local checkout; selected existing public-alpha safe-mode JSON smoke command",
        "script_path": str((root / SELECTED_COMMAND_REL).resolve()),
        "timeout_seconds": float(timeout_seconds),
        "argv": build_argv(py, root),
        "argv_template": ["<python>", SELECTED_COMMAND_REL.as_posix(), "--json"],
        "shell": False,
        "expected_digests": dict(expected_digests),
    }


def _preflight_error(request: Mapping[str, Any], before_state: Mapping[str, Any]) -> tuple[str, str] | None:
    if request.get("capability_id") != CAPABILITY_ID:
        return REFUSAL_CODES["unsupported_capability"], "Only eureka.public-alpha-readonly.validate is admitted by this adapter."
    root = Path(str(request.get("eureka_root", "")))
    if not root.exists() or not (root / ".git").exists():
        return REFUSAL_CODES["checkout_missing"], "Eureka repository checkout is missing."
    remote = str(before_state.get("remote_url", ""))
    if remote.lower() != EXPECTED_REMOTE_URL.lower():
        return REFUSAL_CODES["repository_identity_mismatch"], "Eureka repository identity did not match the accepted origin URL."
    expected_revision = str(request.get("expected_revision") or "")
    if not expected_revision or before_state.get("revision") != expected_revision:
        return REFUSAL_CODES["revision_mismatch"], "Eureka repository revision did not match the pinned revision."
    if before_state.get("clean") is not True:
        return REFUSAL_CODES["dirty_checkout"], "Eureka checkout is not clean."
    if not (root / SELECTED_COMMAND_REL).is_file():
        return REFUSAL_CODES["script_missing"], "Selected Eureka command is missing."
    expected_digests = request.get("expected_digests", {})
    if isinstance(expected_digests, Mapping):
        actual = before_state.get("selected_command_digests", {})
        for rel, expected in expected_digests.items():
            if actual.get(str(rel)) != expected:
                return REFUSAL_CODES["digest_mismatch"], f"Selected Eureka command digest mismatch: {rel}"
    argv = list(request.get("argv") or [])
    expected_argv = build_argv(str(request.get("python_executable", "")), root)
    if argv != expected_argv or len(argv) != 3:
        return REFUSAL_CODES["invalid_request"], "Eureka adapter argv shape is not the exact allowlisted invocation."
    return None


class EurekaStateProbe:
    coverage = STATE_PROBE_COVERAGE

    def __init__(self, root: Path):
        self.root = root

    def capture(self) -> Mapping[str, Any]:
        return capture_eureka_state(self.root)

    def mutation_observation(self, before_state: Mapping[str, Any], after_state: Mapping[str, Any]) -> str:
        if (
            before_state.get("revision") == after_state.get("revision")
            and before_state.get("porcelain_status") == after_state.get("porcelain_status")
            and before_state.get("tracked_tree_digest") == after_state.get("tracked_tree_digest")
            and before_state.get("selected_command_digests") == after_state.get("selected_command_digests")
        ):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


class EurekaPrecondition:
    def __init__(self, request: Mapping[str, Any]):
        self.request = request

    def check(self, invocation: CapabilityInvocation, binding: CapabilityBinding, spec: RegisteredProcessSpec, before_state: Mapping[str, Any]) -> PreconditionResult:
        del invocation, binding, spec
        preflight = _preflight_error(self.request, before_state)
        if preflight is None:
            return PreconditionResult(True)
        code, message = preflight
        return PreconditionResult(False, code, message)


def parse_public_alpha_smoke(stdout: str, returncode: int | None) -> tuple[dict[str, Any] | None, str | None, str]:
    if not stdout.strip():
        return None, REFUSAL_CODES["empty_output"], "none"
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return None, REFUSAL_CODES["malformed_json"], "none"
    if not isinstance(payload, dict):
        return None, REFUSAL_CODES["malformed_json"], "none"
    errors: list[str] = []
    if payload.get("created_by_slice") != "public_alpha_deployment_readiness_review_v0":
        errors.append("created_by_slice mismatch")
    if payload.get("mode") != "public_alpha":
        errors.append("mode must be public_alpha")
    if payload.get("status") not in {"passed", "failed"}:
        errors.append("status must be passed or failed")
    if not isinstance(payload.get("checks"), list):
        errors.append("checks must be an array")
    if not isinstance(payload.get("total_checks"), int):
        errors.append("total_checks must be an integer")
    if not isinstance(payload.get("passed_checks"), int):
        errors.append("passed_checks must be an integer")
    if not isinstance(payload.get("failed_checks"), int):
        errors.append("failed_checks must be an integer")
    if errors:
        return {"schema_errors": errors, "raw_status": payload.get("status")}, REFUSAL_CODES["schema_mismatch"], "typed_refusal"
    status = str(payload["status"])
    normalized = {
        "command_id": CAPABILITY_ID,
        "source_command": SELECTED_COMMAND_REL.as_posix(),
        "requested_command_available": False,
        "source_schema": "public_alpha_smoke.implicit_v0",
        "status": "valid" if status == "passed" else "invalid",
        "raw_status": status,
        "mode": payload.get("mode"),
        "total_checks": payload.get("total_checks"),
        "passed_checks": payload.get("passed_checks"),
        "failed_checks": payload.get("failed_checks"),
        "checks": payload.get("checks"),
    }
    if status == "passed" and returncode == 0:
        return normalized, None, "typed_result"
    if status == "failed" and returncode == 1:
        return normalized, REFUSAL_CODES["validation_failed"], "typed_refusal"
    return normalized, REFUSAL_CODES["inconsistent_returncode"], "typed_refusal"


class EurekaPublicAlphaOutputDecoder:
    decoder_id = "eureka.public-alpha-smoke-json-v0"

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> DecoderResult:
        parsed, reason_code, domain_outcome = parse_public_alpha_smoke(stdout, returncode)
        if reason_code:
            return DecoderResult(
                "decoded" if parsed else "refused",
                domain_outcome,
                domain_result=parsed or {},
                refusal={"reason_code": reason_code, "result": parsed or {}},
                reason_code=reason_code,
                message="Eureka public-alpha smoke output did not produce a successful read-only validation result.",
            )
        return DecoderResult("decoded", "typed_result", domain_result=parsed or {})


class EurekaStreamScrubber:
    scrubber_id = "eureka-readonly-stream-scrubber-v0"

    def __init__(self, request: Mapping[str, Any]):
        self.eureka_root = str(request.get("eureka_root", ""))
        self.repo_root = str(request.get("repo_root", ""))
        self.python_executable = str(request.get("python_executable", ""))

    def scrub(self, text: str) -> str:
        return scrub_string(text, eureka_root=self.eureka_root, repo_root=self.repo_root, python_executable=self.python_executable)


def build_registered_process_spec(request: Mapping[str, Any]) -> RegisteredProcessSpec:
    argv = [str(item) for item in request.get("argv", [])]
    executable = argv[0] if argv else ""
    return RegisteredProcessSpec(
        capability_ref=CAPABILITY_REF,
        executable=executable,
        argument_plan=[ArgumentToken("literal", item) for item in argv[1:]],
        working_directory=str(Path(str(request.get("eureka_root", ""))).resolve()),
        timeout_seconds=float(request.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
        environment=sanitized_environment(),
        decoder_id=EurekaPublicAlphaOutputDecoder.decoder_id,
        state_probe_id="eureka-git-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id=EurekaStreamScrubber.scrubber_id,
        provider_spec_ref="aide://provider-spec/eureka-public-alpha-readonly-process-adapter-v0",
        conformance_profile_ref="aide://conformance-profile/eureka-public-alpha-readonly-process-adapter-v0",
        executable_digest=sha256_file(Path(executable)) if executable and Path(executable).is_file() else "",
        metadata={
            "argv_template": list(request.get("argv_template", [])),
            "command": "eureka.public_alpha_smoke",
            "executable_identity": "python",
            "requested_command": request.get("requested_command"),
            "selected_command": request.get("selected_command"),
        },
    )


def _eureka_reason_code(reason_code: str, receipt: ProcessExecutionReceipt) -> str:
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
        "schema_version": "aide.eureka-readonly-process.invocation-result.v1",
        "kind": "EurekaReadonlyProcessInvocationResult",
        "task_id": TASK_ID,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "result": "REFUSED",
        "status": "REFUSED",
        "reason_code": reason_code,
        "message": message,
        "process_call_count": process_call_count,
        "actual_eureka_process_spawned": process_call_count == 1,
        "result_origin": "eureka_public_alpha_smoke_json" if domain_result else "adapter_preflight_or_transport",
        "constructed_success_result": False,
        "returncode": returncode,
        "stdout": dict(stdout or {}),
        "stderr": dict(stderr or {}),
        "eureka_json_parsed": bool(domain_result),
        "eureka_result": dict(domain_result or {}),
        "typed_refusal": True,
        "typed_result": False,
        **_false_boundary(),
    }


def _result_from_provider(*, request: Mapping[str, Any], receipt: ProcessExecutionReceipt, outcome: CapabilityOutcome) -> dict[str, Any]:
    before_state = dict(receipt.metadata.get("before_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    after_state = dict(receipt.metadata.get("after_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    domain_result = dict(outcome.domain_result or {})
    state_changed = receipt.mutation_observation != "none_detected_within_probe_coverage"
    if receipt.launcher_call_count == 0:
        result = refusal(
            request=request,
            reason_code=_eureka_reason_code(outcome.reason_code, receipt),
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
            message="Eureka read-only validator timed out.",
            process_call_count=receipt.launcher_call_count,
            returncode=None,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    elif state_changed:
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["unexpected_mutation"],
            message="Eureka repository state changed during read-only invocation.",
            process_call_count=receipt.launcher_call_count,
            domain_result=domain_result or None,
            returncode=receipt.return_code,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
    elif outcome.reason_code:
        result = refusal(
            request=request,
            reason_code=_eureka_reason_code(outcome.reason_code, receipt),
            message=outcome.message or "Eureka command returned a typed failed validation result.",
            process_call_count=receipt.launcher_call_count,
            domain_result=domain_result or None,
            returncode=receipt.return_code,
            stdout=receipt.stdout,
            stderr=receipt.stderr,
        )
        if domain_result:
            result["status"] = "FAILED_VALIDATION"
            result["result"] = "FAILED_VALIDATION"
    else:
        result = {
            "schema_version": "aide.eureka-readonly-process.invocation-result.v1",
            "kind": "EurekaReadonlyProcessInvocationResult",
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "result": "PASS",
            "status": "PASS",
            "reason_code": "",
            "message": "Eureka public-alpha smoke command returned a valid read-only result.",
            "process_call_count": receipt.launcher_call_count,
            "actual_eureka_process_spawned": receipt.launcher_call_count == 1,
            "result_origin": "eureka_public_alpha_smoke_json",
            "constructed_success_result": False,
            "returncode": receipt.return_code,
            "stdout": dict(receipt.stdout),
            "stderr": dict(receipt.stderr),
            "eureka_json_parsed": True,
            "eureka_result": domain_result,
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
    result["requested_command"] = request.get("requested_command")
    result["selected_command"] = request.get("selected_command")
    result["selected_command_reason"] = request.get("selected_command_reason")
    result["process_execution_receipt"] = receipt.to_dict()
    result["capability_outcome"] = outcome.to_dict()
    result["provider_ref"] = receipt.provider_ref
    result["provider_core_changed_by_task"] = False
    result["adapter_role"] = "thin_eureka_public_alpha_readonly_process_adapter"
    return result


def invoke_eureka_readonly(request: Mapping[str, Any], *, runner: Runner | None = None) -> dict[str, Any]:
    eureka_root = Path(str(request.get("eureka_root", ""))).resolve()
    spec = build_registered_process_spec(request)
    invocation = CapabilityInvocation("aide://invocation/eureka-readonly-process-adapter-01", CAPABILITY_REF, values={"capability_id": CAPABILITY_ID})
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
        precondition=EurekaPrecondition(request),
        state_probe=EurekaStateProbe(eureka_root),
        output_decoder=EurekaPublicAlphaOutputDecoder(),
        stream_scrubber=EurekaStreamScrubber(request),
    )
    receipt, outcome = provider.execute(invocation, binding)
    return _result_from_provider(request=request, receipt=receipt, outcome=outcome)


def scrub_string(text: str, *, eureka_root: str = "", repo_root: str = "", python_executable: str = "") -> str:
    result = text
    replacements = [
        (eureka_root, "<eureka-root>"),
        (eureka_root.replace("\\", "/"), "<eureka-root>"),
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


def scrub_data(data: Any, *, eureka_root: str = "", repo_root: str = "", python_executable: str = "") -> Any:
    if isinstance(data, str):
        return scrub_string(data, eureka_root=eureka_root, repo_root=repo_root, python_executable=python_executable)
    if isinstance(data, list):
        return [scrub_data(item, eureka_root=eureka_root, repo_root=repo_root, python_executable=python_executable) for item in data]
    if isinstance(data, dict):
        return {str(key): scrub_data(value, eureka_root=eureka_root, repo_root=repo_root, python_executable=python_executable) for key, value in data.items()}
    return data


def artifact(repo_root: Path, path: Path, role: str) -> dict[str, Any]:
    return evidence_packet.artifact_ref(repo_root, path, role)


def build_context_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.eureka-readonly-process.context-descriptor.v1",
        "kind": "ContextDescriptor",
        "task_id": TASK_ID,
        "context_ref": CONTEXT_DESCRIPTOR_REF,
        "repository": {
            "kind": "external-eureka",
            "identity": "Julesc013/eureka",
            "revision": (result.get("before_state") or {}).get("revision") if isinstance(result.get("before_state"), dict) else "",
            "remote_url": EXPECTED_REMOTE_URL,
            "local_checkout_path_committed": False,
        },
        "source_digests": (result.get("before_state") or {}).get("selected_command_digests", {}) if isinstance(result.get("before_state"), dict) else {},
        "scope": {
            "capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "provider_ref": RegisteredProcessExecutionProvider.provider_id,
            "requested_command": REQUESTED_COMMAND_REL.as_posix(),
            "selected_command": SELECTED_COMMAND_REL.as_posix(),
        },
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
    }


def build_context_pack(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.eureka-readonly-process.context-pack.v1",
        "kind": "ContextPack",
        "task_id": TASK_ID,
        "context_pack_ref": CONTEXT_PACK_REF,
        "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
        "workunit_ref": WORKUNIT_REF,
        "artifacts": [
            artifact(repo_root, CONTEXT_DESCRIPTOR_JSON, "context_descriptor"),
            artifact(repo_root, CAPABILITY_DESCRIPTOR_JSON, "capability_descriptor"),
            artifact(repo_root, INVOCATION_RESULT_JSON, "invocation_result"),
        ],
        "provider_reuse_claim": {
            "provider_core": RegisteredProcessExecutionProvider.provider_id,
            "provider_core_changed_by_task": False,
            "shared_receipt_model": True,
            "shared_outcome_model": True,
        },
        "status": {
            "validation_performed": True,
            "validation_status": "PASS_WITH_WARNINGS" if result.get("actual_eureka_process_spawned") else "FAILED_VALIDATION",
            "process_call_count": result.get("process_call_count"),
            "workspace_state_unchanged": result.get("workspace_state_unchanged"),
            "mutation_observation": result.get("mutation_observation"),
            "trusted": False,
            **_false_boundary(),
        },
    }


def build_workunit_record(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    return workunit.build_workunit(
        task_id=TASK_ID,
        title="Build Eureka Read-Only Process Adapter",
        work_type="build",
        authorizes_implementation=True,
        check_only=False,
        acceptance_review=False,
        implementation_scope="thin-eureka-readonly-adapter-over-registered-process-provider-v0",
        stop_state="needs_review",
        predecessors=["AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01"],
        dependencies=[],
        scope={
            "allowed_paths": [
                "core/interop/eureka/**",
                ".aide/scripts/aide_lite.py",
                ".aide/scripts/tests/test_aide_eureka_readonly_process_adapter.py",
                ".aide/reports/eureka-readonly-process-adapter/**",
                ".aide/queue/AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01/**",
                ".aide/queue/index.yaml",
                "PLANS.md",
                "IMPLEMENT.md",
            ],
            "forbidden_paths": [
                "core/execution/registered_process.py",
                "core/protocol/process_invocation.py",
                "core/protocol/execution_receipt.py",
                "core/interop/aide/**",
                "core/interop/dominium/**",
                "<local-eureka-checkout>/**",
            ],
            "forbidden_operations": list(EXPLICIT_NON_CAPABILITIES),
            "registered_capability_id": CAPABILITY_ID,
            "invocation_limit": 1,
        },
        validation_spec={
            "commands": [
                workunit.validation(
                    "py -3 .aide/scripts/aide_lite.py aide-eureka-readonly-process-adapter run",
                    "PASS_WITH_WARNINGS",
                    0,
                    "Invokes exactly one allowlisted Eureka public-alpha smoke process.",
                ),
                workunit.validation(
                    "py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_eureka_readonly_process_adapter.py",
                    "PASS",
                    0,
                    "Focused fake-runner Eureka adapter tests.",
                ),
            ]
        },
        evidence_requirements=[
            INVOCATION_RESULT_JSON.as_posix(),
            EXECUTION_RECEIPT_JSON.as_posix(),
            CAPABILITY_OUTCOME_JSON.as_posix(),
            EVIDENCE_PACKET_JSON.as_posix(),
            EVENT_RECORD_JSON.as_posix(),
        ],
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        capability_label=workunit.FEATURE_FLAG,
        artifacts=[
            artifact(repo_root, CONTEXT_DESCRIPTOR_JSON, "context_descriptor"),
            artifact(repo_root, CONTEXT_PACK_JSON, "context_pack"),
            artifact(repo_root, INVOCATION_RESULT_JSON, "invocation_result"),
        ],
        source_path=Path(".aide/queue/AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01/task.yaml"),
        phase="needs_review",
        result="PASS_WITH_WARNINGS" if result.get("actual_eureka_process_spawned") else "FAILED_VALIDATION",
    )


def build_capability_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.eureka-readonly-process.capability-descriptor.v1",
        "kind": "CapabilityDescriptor",
        "task_id": TASK_ID,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "provider_status": "proposed_unaccepted",
        "accepted": False,
        "provider_acceptance_claimed": False,
        "requested_command": REQUESTED_COMMAND_REL.as_posix(),
        "selected_command": SELECTED_COMMAND_REL.as_posix(),
        "selected_command_warning": "requested validator absent in pinned local checkout",
        "result_origin": result.get("result_origin"),
        "process_call_count": result.get("process_call_count"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        **_false_boundary(),
    }


def build_projection(result: Mapping[str, Any], validation_status: str) -> dict[str, Any]:
    projection = {
        "schema_version": "aide.eureka-readonly-process.projection.v1",
        "kind": "EurekaReadonlyProcessProjection",
        "task_id": TASK_ID,
        "status": validation_status,
        "flow": [
            "clean pinned Eureka checkout",
            "ContextDescriptor",
            "ContextPack",
            "WorkUnit",
            "registered capability lookup",
            "exactly one Eureka public-alpha smoke process invocation",
            "typed Eureka result or refusal",
            "ProcessExecutionReceipt",
            "CapabilityOutcome",
            "EvidencePacket",
            "EventRecord",
            "deterministic read-only projection",
        ],
        "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
        "context_pack_ref": CONTEXT_PACK_REF,
        "workunit_ref": WORKUNIT_REF,
        "capability_ref": CAPABILITY_REF,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "evidence_ref": EVIDENCE_REF,
        "event_ref": EVENT_REF,
        "requested_command": REQUESTED_COMMAND_REL.as_posix(),
        "selected_command": SELECTED_COMMAND_REL.as_posix(),
        "process_call_count": result.get("process_call_count"),
        "launcher_call_count": (result.get("process_execution_receipt") or {}).get("launcher_call_count") if isinstance(result.get("process_execution_receipt"), dict) else None,
        "domain_outcome": (result.get("capability_outcome") or {}).get("domain_outcome") if isinstance(result.get("capability_outcome"), dict) else "",
        "result_origin": result.get("result_origin"),
        "eureka_status": (result.get("eureka_result") or {}).get("status") if isinstance(result.get("eureka_result"), dict) else "",
        "mutation_observation": result.get("mutation_observation"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "provider_core_changed_by_task": False,
        "reports": [rel.as_posix() for rel in REPORT_FILES],
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    projection["projection_digest"] = sha256_text(stable_json(projection))
    return projection


def build_evidence_packet(repo_root: Path, result: Mapping[str, Any], validation_status: str) -> dict[str, Any]:
    claims = [
        evidence_packet.claim("registered_provider_reused", "supported", "The adapter invokes the unchanged RegisteredProcessExecutionProvider v0."),
        evidence_packet.claim("exactly_one_process_invocation", "supported" if result.get("process_call_count") == 1 else "contradicted", "The allowlisted Eureka read-only process was spawned exactly once."),
        evidence_packet.claim("stdout_json_result_origin", "supported" if result.get("eureka_json_parsed") else "contradicted", "The AIDE result was derived from Eureka command JSON stdout."),
        evidence_packet.claim("shared_receipt_model", "supported" if isinstance(result.get("process_execution_receipt"), dict) else "contradicted", "The adapter emits the shared ProcessExecutionReceipt model."),
        evidence_packet.claim("workspace_state_unchanged", "supported" if result.get("workspace_state_unchanged") else "contradicted", "Before and after Eureka state evidence match within declared probe coverage."),
    ]
    return evidence_packet.build_evidence_packet(
        source_task_id=TASK_ID,
        source_task_kind="build",
        subject={"type": "capability", "id": CAPABILITY_ID, "ref": CAPABILITY_REF},
        capability_label=evidence_packet.FEATURE_FLAG,
        claims=claims,
        explicit_non_capabilities=list(EXPLICIT_NON_CAPABILITIES),
        artifacts=[
            artifact(repo_root, CONTEXT_DESCRIPTOR_JSON, "context_descriptor"),
            artifact(repo_root, CONTEXT_PACK_JSON, "context_pack"),
            artifact(repo_root, WORKUNIT_JSON, "workunit"),
            artifact(repo_root, CAPABILITY_DESCRIPTOR_JSON, "capability_descriptor"),
            artifact(repo_root, INVOCATION_RESULT_JSON, "invocation_result"),
            artifact(repo_root, EXECUTION_RECEIPT_JSON, "execution_receipt"),
            artifact(repo_root, CAPABILITY_OUTCOME_JSON, "capability_outcome"),
        ],
        validations=[
            evidence_packet.validation("Eureka read-only process adapter", validation_status, 0 if validation_status in {"PASS", "PASS_WITH_WARNINGS"} else 1),
        ],
        warnings=[
            "RegisteredProcessExecutionProvider v0 remains proposed and unaccepted.",
            "Requested scripts/validate_public_alpha_readonly.py is absent in this local Eureka checkout.",
            "Selected command is scripts/public_alpha_smoke.py --json.",
            "Mutation observation is limited to declared Git probe coverage.",
        ],
        risks=[],
        source_path=EVIDENCE_PACKET_JSON,
        name="Eureka read-only process adapter evidence",
        phase=validation_status,
        validation_warnings=["Independent Eureka adapter check remains required before provider acceptance."],
    )


def build_event_record(repo_root: Path) -> dict[str, Any]:
    return event_record.build_event_record(
        repo_root=repo_root,
        event_ref=EVENT_REF,
        event_type="EvidencePacketRecorded",
        subject_ref=EVIDENCE_REF,
        subject_kind="evidence",
        occurred_at=DETERMINISTIC_TIMESTAMP,
        sequence=1,
        actor={"ref": "aide://source/aide-lite", "kind": "source", "name": "aide-lite"},
        payload={
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "provider_ref": RegisteredProcessExecutionProvider.provider_id,
            "invocation_count": 1,
            "projection_only": True,
            "event_log_appended": False,
        },
        evidence_refs=[EVIDENCE_REF],
        report_refs=[REPORT_REF],
        causation_ref=WORKUNIT_REF,
        correlation_ref=CONTEXT_PACK_REF,
        source_path=EVENT_RECORD_JSON.as_posix(),
    )


def write_outputs(repo_root: Path, request: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    validation_status = "PASS_WITH_WARNINGS" if (
        result.get("process_call_count") == 1
        and result.get("actual_eureka_process_spawned") is True
        and result.get("eureka_json_parsed") is True
        and result.get("workspace_state_unchanged") is True
        and result.get("status") == "PASS"
    ) else "FAILED_VALIDATION"
    scrub_context = {
        "eureka_root": str(request.get("eureka_root", "")),
        "repo_root": str(request.get("repo_root", "")),
        "python_executable": str(request.get("python_executable", "")),
    }
    for path, payload in [
        (CONTEXT_DESCRIPTOR_JSON, build_context_descriptor(result)),
        (CONTEXT_PACK_JSON, build_context_pack(repo_root, result)),
        (WORKUNIT_JSON, build_workunit_record(repo_root, result)),
        (CAPABILITY_DESCRIPTOR_JSON, build_capability_descriptor(result)),
        (INVOCATION_REQUEST_JSON, dict(request)),
        (EXECUTION_RECEIPT_JSON, dict(result.get("process_execution_receipt") or {})),
        (CAPABILITY_OUTCOME_JSON, dict(result.get("capability_outcome") or {})),
        (INVOCATION_RESULT_JSON, dict(result)),
        (PROJECTION_JSON, build_projection(result, validation_status)),
        (ADAPTER_REPORT_JSON, {"schema_version": "aide.eureka-readonly-process.adapter-report.v1", "kind": "EurekaReadonlyProcessAdapterReport", "task_id": TASK_ID, "status": validation_status, "result": result, "recommended_next_task": CHECK_TASK_ID, **_false_boundary()}),
    ]:
        write_json(repo_root / path, scrub_data(payload, **scrub_context))
    write_json(repo_root / EVIDENCE_PACKET_JSON, scrub_data(build_evidence_packet(repo_root, result, validation_status), **scrub_context))
    write_json(repo_root / EVENT_RECORD_JSON, scrub_data(build_event_record(repo_root), **scrub_context))
    validation = validate_reports(repo_root)
    validation = validate_reports(repo_root)
    return validation


def scan_for_leaks(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    absolute_pattern = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"']+")
    secret_pattern = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    if not root.exists():
        return findings
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        text = path.read_text(encoding="utf-8", errors="replace")
        if absolute_pattern.search(text):
            findings.append({"path": path.relative_to(root).as_posix(), "kind": "absolute_path"})
        if secret_pattern.search(text):
            findings.append({"path": path.relative_to(root).as_posix(), "kind": "secret_like"})
    return findings


def validation_errors(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REPORT_FILES:
        if not (repo_root / rel).exists():
            errors.append(f"missing required output: {rel.as_posix()}")
    if errors:
        return errors
    result = read_json(repo_root / INVOCATION_RESULT_JSON)
    receipt = read_json(repo_root / EXECUTION_RECEIPT_JSON)
    outcome = read_json(repo_root / CAPABILITY_OUTCOME_JSON)
    workunit_record = read_json(repo_root / WORKUNIT_JSON)
    evidence = read_json(repo_root / EVIDENCE_PACKET_JSON)
    event = read_json(repo_root / EVENT_RECORD_JSON)
    projection = read_json(repo_root / PROJECTION_JSON)
    errors.extend(workunit.validate_workunit(workunit_record))
    errors.extend(evidence_packet.validate_evidence_packet(evidence))
    errors.extend(event_record.validate_event_record(event))
    if result.get("proposed_capability_label") != PROPOSED_CAPABILITY_LABEL:
        errors.append("proposed capability label mismatch")
    if result.get("process_call_count") != 1:
        errors.append("process_call_count must be exactly 1")
    if result.get("actual_eureka_process_spawned") is not True:
        errors.append("actual_eureka_process_spawned must be true")
    if result.get("result_origin") != "eureka_public_alpha_smoke_json":
        errors.append("result must originate from Eureka public-alpha smoke JSON")
    if result.get("constructed_success_result") is not False:
        errors.append("constructed success results are forbidden")
    if result.get("workspace_state_unchanged") is not True:
        errors.append("Eureka workspace state changed across invocation")
    if result.get("mutation_observation") != "none_detected_within_probe_coverage":
        errors.append("mutation observation must be none within declared probe coverage")
    if receipt.get("provider_ref") != RegisteredProcessExecutionProvider.provider_id:
        errors.append("receipt provider_ref mismatch")
    if receipt.get("launcher_call_count") != result.get("process_call_count"):
        errors.append("launcher_call_count must match process_call_count")
    if outcome.get("domain_outcome") != "typed_result":
        errors.append("capability outcome must be typed_result for this build proof")
    if (result.get("eureka_result") or {}).get("status") != "valid":
        errors.append("Eureka public-alpha result status must be valid")
    allowlisted = result.get("allowlisted_process_call") if isinstance(result.get("allowlisted_process_call"), dict) else {}
    if allowlisted.get("shell") is not False:
        errors.append("process runner shell flag must be false")
    if result.get("provider_core_changed_by_task") is not False:
        errors.append("provider core must not be changed by this adapter task")
    expected_projection_digest = sha256_text(stable_json({key: value for key, value in projection.items() if key != "projection_digest"}))
    if projection.get("projection_digest") != expected_projection_digest:
        errors.append("projection digest mismatch")
    leaks = scan_for_leaks(repo_root / REPORT_ROOT)
    if leaks:
        errors.append(f"report leak scan found {len(leaks)} finding(s)")
    return errors


def validate_reports(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    errors = validation_errors(root)
    status_value = "PASS_WITH_WARNINGS" if not errors else "FAILED_VALIDATION"
    result = read_json(root / INVOCATION_RESULT_JSON) if (root / INVOCATION_RESULT_JSON).exists() else {}
    report = {
        "schema_version": "aide.eureka-readonly-process.validation.v1",
        "kind": "EurekaReadonlyProcessValidation",
        "task_id": TASK_ID,
        "status": status_value,
        "validation_status": status_value,
        "validated": not errors,
        "validation_errors": errors,
        "warnings": [
            "RegisteredProcessExecutionProvider v0 remains proposed and unaccepted.",
            "Requested scripts/validate_public_alpha_readonly.py is absent in the local pinned Eureka checkout.",
            "Selected scripts/public_alpha_smoke.py --json as the narrowest existing read-only JSON command.",
            "Mutation observation is limited to declared Git probe coverage.",
        ],
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "process_call_count": result.get("process_call_count"),
        "workspace_state_unchanged": result.get("workspace_state_unchanged"),
        "mutation_observation": result.get("mutation_observation"),
        "result_origin": result.get("result_origin"),
        "requested_command_available": False,
        "selected_command": SELECTED_COMMAND_REL.as_posix(),
        "eureka_status": (result.get("eureka_result") or {}).get("status") if isinstance(result.get("eureka_result"), dict) else "",
        "missing_evidence": 0 if not errors else len(errors),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / STATUS_MD, render_status_markdown(report))
    if (root / ADAPTER_REPORT_JSON).exists():
        write_text(root / ADAPTER_REPORT_MD, render_adapter_report_markdown(read_json(root / ADAPTER_REPORT_JSON), report))
    write_text(root / WARNING_DISPOSITION_MD, render_warning_disposition_markdown())
    write_text(root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    return report


def run_adapter(
    repo_root: str | Path = ".",
    *,
    eureka_root: str | Path | None = None,
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
    runner: Runner | None = None,
    write_reports: bool = True,
) -> dict[str, Any]:
    root = Path(repo_root)
    request = build_invocation_request(
        repo_root=root,
        eureka_root=eureka_root,
        expected_revision=expected_revision,
        capability_id=capability_id,
        python_executable=python_executable,
        timeout_seconds=timeout_seconds,
        expected_digests=expected_digests,
    )
    result = invoke_eureka_readonly(request, runner=runner)
    if write_reports:
        validation = write_outputs(root, request, result)
        result = {**result, "validation_status": validation["validation_status"], "validation_errors": validation["validation_errors"]}
    return result


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    validation_exists = (root / VALIDATION_JSON).exists()
    validation = read_json(root / VALIDATION_JSON) if validation_exists else {}
    data = {
        "schema_version": "aide.eureka-readonly-process.status.v1",
        "kind": "EurekaReadonlyProcessStatus",
        "task_id": TASK_ID,
        "status": validation.get("validation_status", "NOT_RUN") if validation_exists else "NOT_RUN",
        "validation_report_exists": validation_exists,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "provider_ref": RegisteredProcessExecutionProvider.provider_id,
        "process_call_count": validation.get("process_call_count"),
        "workspace_state_unchanged": validation.get("workspace_state_unchanged"),
        "mutation_observation": validation.get("mutation_observation"),
        "result_origin": validation.get("result_origin"),
        "requested_command_available": False,
        "selected_command": SELECTED_COMMAND_REL.as_posix(),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def render_status_markdown(data: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Eureka Read-Only Process Adapter Status",
            "",
            f"- task_id: `{TASK_ID}`",
            f"- status: `{data.get('status') or data.get('validation_status')}`",
            f"- capability_id: `{CAPABILITY_ID}`",
            f"- proposed_capability_label: `{PROPOSED_CAPABILITY_LABEL}`",
            f"- provider_ref: `{RegisteredProcessExecutionProvider.provider_id}`",
            f"- process_call_count: `{data.get('process_call_count', '')}`",
            f"- workspace_state_unchanged: `{str(data.get('workspace_state_unchanged', False)).lower()}`",
            f"- mutation_observation: `{data.get('mutation_observation', '')}`",
            f"- result_origin: `{data.get('result_origin', '')}`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            "",
        ]
    )


def render_adapter_report_markdown(report: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
    result = report.get("result", {}) if isinstance(report.get("result"), dict) else {}
    eureka_result = result.get("eureka_result") if isinstance(result.get("eureka_result"), dict) else {}
    return "\n".join(
        [
            "# Eureka Read-Only Process Adapter",
            "",
            f"- status: `{validation.get('validation_status')}`",
            f"- capability_id: `{CAPABILITY_ID}`",
            f"- proposed_capability_label: `{PROPOSED_CAPABILITY_LABEL}`",
            f"- provider_ref: `{RegisteredProcessExecutionProvider.provider_id}`",
            f"- selected_command: `{SELECTED_COMMAND_REL.as_posix()} --json`",
            f"- requested_command_available: `false`",
            f"- process_call_count: `{result.get('process_call_count')}`",
            f"- result_origin: `{result.get('result_origin')}`",
            f"- eureka_status: `{eureka_result.get('status', '')}`",
            f"- workspace_state_unchanged: `{str(result.get('workspace_state_unchanged', False)).lower()}`",
            f"- mutation_observation: `{result.get('mutation_observation')}`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            "",
        ]
    )


def render_warning_disposition_markdown() -> str:
    return "\n".join(
        [
            "# Warning Disposition",
            "",
            "- RegisteredProcessExecutionProvider v0 remains proposed and unaccepted.",
            "- Requested `scripts/validate_public_alpha_readonly.py --json` is absent in the local pinned Eureka checkout.",
            "- The selected command is `scripts/public_alpha_smoke.py --json`.",
            "- The selected command emits an implicit public-alpha smoke JSON shape, not `public_alpha_readonly_validation.v0`.",
            "- Mutation observation is limited to declared Git probe coverage.",
            "",
        ]
    )


def render_explicit_non_capabilities_markdown() -> str:
    lines = ["# Explicit Non-Capabilities", ""]
    lines.extend(f"- `{item}`" for item in EXPLICIT_NON_CAPABILITIES)
    lines.append("")
    return "\n".join(lines)


def render_next_task_prompt() -> str:
    return "\n".join(
        [
            f"# {CHECK_TASK_ID}",
            "",
            f"Create and process `{CHECK_TASK_ID}`.",
            "",
            "Independently check `AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01`.",
            "",
            "Verify the selected Eureka command is an existing Eureka-owned read-only JSON command,",
            "the result originates from Eureka output, exactly one allowlisted process launches with",
            "`shell=False`, invalid preconditions launch zero processes, the Eureka checkout remains",
            "unchanged within declared probe coverage, committed evidence is scrubbed, provider core",
            "remains unchanged, and the provider remains proposed and unaccepted.",
            "",
            "If material findings remain, recommend exactly:",
            "",
            "AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-REPAIR-01",
            "",
            "If the check passes, recommend exactly:",
            "",
            "AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01",
            "",
        ]
    )
