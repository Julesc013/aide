"""Registered Dominium validation backend.

This module proves one bounded process invocation of Dominium's
``dominium.validation.run`` CLI boundary. It intentionally does not implement a
general command runner, shell dispatch, Workbench behavior, Service/runtime,
worker execution, provider/model calls, preview/apply, rollback, or mutation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
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
from core.protocol import envelope, event_record, evidence_packet, reference_id, workunit
from core.protocol.execution_receipt import CapabilityOutcome, ProcessExecutionReceipt
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


TASK_ID = "AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
CHECK_TASK_ID = "AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01"
ACCEPT_TASK_ID = "AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
SOURCE_ACCEPT_TASK_ID = "AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01"
CAPABILITY_ID = "dominium.validation.run"
SUPERSEDED_CAPABILITY_LABEL = "live_dominium_validation_command_readonly_v0"
PROPOSED_CAPABILITY_LABEL = "dominium_registered_validation_command_boundary_invocation_v0"
CAPABILITY_REF = "aide://capability/dominium-registered-validation-command-boundary-invocation"
CONTEXT_DESCRIPTOR_REF = "aide://context/dominium-registered-validation-context"
CONTEXT_PACK_REF = "aide://context-pack/dominium-registered-validation-backend-01"
WORKUNIT_REF = "aide://workunit/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
EVIDENCE_REF = "aide://evidence/dominium-registered-validation-backend"
REPORT_REF = "aide://report/dominium-registered-validation-backend"
EVENT_REF = "aide://event/EVT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
DETERMINISTIC_TIMESTAMP = "2026-06-23T00:00:00+10:00"
DEFAULT_TIMEOUT_SECONDS = 30.0
EXPECTED_REMOTE_URL = "https://github.com/Julesc013/dominium.git"
STATE_PROBE_COVERAGE = [
    "git_revision",
    "git_porcelain_status",
    "git_tracked_tree_digest",
    "command_implementation_digests",
]

REPORT_ROOT = Path(".aide/reports/dominium-registered-validation-backend")
STATUS_MD = REPORT_ROOT / "status.md"
CONTEXT_DESCRIPTOR_JSON = REPORT_ROOT / "context-descriptor.json"
CONTEXT_PACK_JSON = REPORT_ROOT / "context-pack.json"
WORKUNIT_JSON = REPORT_ROOT / "workunit.json"
CAPABILITY_DESCRIPTOR_JSON = REPORT_ROOT / "capability-descriptor.json"
INVOCATION_REQUEST_JSON = REPORT_ROOT / "invocation-request.json"
INVOCATION_RESULT_JSON = REPORT_ROOT / "invocation-result.json"
EVIDENCE_PACKET_JSON = REPORT_ROOT / "evidence-packet.json"
EVENT_RECORD_JSON = REPORT_ROOT / "event-record.json"
PROJECTION_JSON = REPORT_ROOT / "projection.json"
VALIDATION_JSON = REPORT_ROOT / "validation.json"
BACKEND_REPORT_JSON = REPORT_ROOT / "backend-report.json"
BACKEND_REPORT_MD = REPORT_ROOT / "backend-report.md"
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
    INVOCATION_RESULT_JSON,
    EVIDENCE_PACKET_JSON,
    EVENT_RECORD_JSON,
    PROJECTION_JSON,
    VALIDATION_JSON,
    BACKEND_REPORT_JSON,
    BACKEND_REPORT_MD,
    WARNING_DISPOSITION_MD,
    EXPLICIT_NON_CAPABILITIES_MD,
    NEXT_TASK_PROMPT_MD,
]

CLI_REL = Path("apps/workbench/module/validation/cli.py")
COMMAND_REL = Path("apps/workbench/module/validation/command.py")
SERVICE_ADAPTER_REL = Path("apps/workbench/module/validation/service_adapter.py")
COMMAND_SOURCE_RELS = [CLI_REL, COMMAND_REL, SERVICE_ADAPTER_REL]
RELEVANT_DOMINIUM_RELS = [
    *COMMAND_SOURCE_RELS,
    Path("contracts/command/validation_run_input.schema.json"),
    Path("contracts/command/validation_run_result.schema.json"),
    Path("contracts/schema/validation_result.schema.json"),
    Path("contracts/command/command_surface.contract.toml"),
    Path("contracts/refusal/refusal_code.registry.json"),
    Path("contracts/diagnostic/diagnostic_code.registry.json"),
    Path("contracts/action/validation_actions.registry.json"),
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
    "arbitrary_shell_command",
    "private_tool_call",
    "broad_dominium_command_dispatch",
    "general_dominium_command_runner",
    "provider_model_call",
    "network_call",
    "worker_execution",
    "workbench_apply",
    "service_runtime",
    "durable_database_state",
    "preview_or_apply",
    "rollback",
    "patch_transaction_apply",
    "source_repository_mutation",
    "target_repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
]

REFUSAL_CODES = {
    "unsupported_capability": "AIDE_DOMINIUM_REGISTERED_VALIDATION_UNSUPPORTED_CAPABILITY",
    "invalid_request": "AIDE_DOMINIUM_REGISTERED_VALIDATION_INVALID_REQUEST",
    "checkout_missing": "AIDE_DOMINIUM_REGISTERED_VALIDATION_CHECKOUT_MISSING",
    "repository_identity_mismatch": "AIDE_DOMINIUM_REGISTERED_VALIDATION_REPOSITORY_IDENTITY_MISMATCH",
    "revision_mismatch": "AIDE_DOMINIUM_REGISTERED_VALIDATION_REVISION_MISMATCH",
    "dirty_checkout": "AIDE_DOMINIUM_REGISTERED_VALIDATION_DIRTY_CHECKOUT",
    "cli_missing": "AIDE_DOMINIUM_REGISTERED_VALIDATION_CLI_MISSING",
    "digest_mismatch": "AIDE_DOMINIUM_REGISTERED_VALIDATION_DIGEST_MISMATCH",
    "timeout": "AIDE_DOMINIUM_REGISTERED_VALIDATION_TIMEOUT",
    "nonzero_exit": "AIDE_DOMINIUM_REGISTERED_VALIDATION_NONZERO_EXIT",
    "empty_output": "AIDE_DOMINIUM_REGISTERED_VALIDATION_EMPTY_OUTPUT",
    "malformed_json": "AIDE_DOMINIUM_REGISTERED_VALIDATION_MALFORMED_JSON",
    "unexpected_command_id": "AIDE_DOMINIUM_REGISTERED_VALIDATION_UNEXPECTED_COMMAND_ID",
    "unexpected_mutation": "AIDE_DOMINIUM_REGISTERED_VALIDATION_UNEXPECTED_REPOSITORY_MUTATION",
}

Runner = Callable[[Sequence[str], Path, Mapping[str, str], float], subprocess.CompletedProcess[str]]


class CountingRunner:
    """Process-runner wrapper used for independent call accounting."""

    def __init__(self, runner: Runner | None = None):
        self.runner = runner or default_process_runner
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        argv: Sequence[str],
        cwd: Path,
        env: Mapping[str, str],
        timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        self.calls.append(
            {
                "argv": list(argv),
                "cwd": str(cwd),
                "env": dict(env),
                "timeout": timeout,
                "shell": False,
            }
        )
        return self.runner(argv, cwd, env, timeout)


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


def _boundary_classification(result: dict[str, Any]) -> dict[str, Any]:
    command_result = result.get("dominium_command_result")
    if not isinstance(command_result, dict):
        command_result = {}
    payload = command_result.get("payload")
    if not isinstance(payload, dict):
        payload = {}
    validation_report = payload.get("validation_report")
    process_started = result.get("actual_dominium_cli_process_spawned") is True
    structured_output = result.get("dominium_stdout_json_parsed") is True
    registered_command = structured_output and command_result.get("command_id") == CAPABILITY_ID
    domain_status = str(command_result.get("status") or "").lower()
    if domain_status == "refused" or result.get("typed_refusal") is True:
        domain_outcome = "typed_refusal"
    elif command_result:
        domain_outcome = "typed_result"
    else:
        domain_outcome = "none"
    if validation_report is None:
        aggregate_executed = False
        aggregate_succeeded = False
    elif isinstance(validation_report, dict):
        aggregate_executed = True
        aggregate_succeeded = str(validation_report.get("status") or validation_report.get("result") or "").lower() in {"pass", "passed", "ok", "success"}
    else:
        aggregate_executed = True
        aggregate_succeeded = False
    result.update(
        {
            "process_started": process_started,
            "launcher_call_count": result.get("process_call_count", 0),
            "structured_output_parsed": structured_output,
            "transport_boundary_reached": "proven" if process_started and structured_output else "unproven",
            "registered_command_boundary_reached": "proven" if registered_command else "unproven",
            "run_validation_command_boundary_reached": "proven" if registered_command else "unproven",
            "service_adapter_boundary_reached": "unproven",
            "service_adapter_boundary_basis": "not_emitted_by_dominium_result",
            "domain_outcome": domain_outcome,
            "aggregate_validation_executed": aggregate_executed,
            "aggregate_validation_succeeded": aggregate_succeeded,
            "mutation_observation": "none_detected_within_probe_coverage"
            if result.get("checkout_state_unchanged") is True
            else "mutation_detected_within_probe_coverage",
            "probe_coverage": list(STATE_PROBE_COVERAGE),
        }
    )
    return result


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def default_dominium_root(repo_root: str | Path = ".") -> Path:
    root = Path(repo_root).resolve()
    candidates = [
        root.parent.parent / "Dominium" / "dominium",
        Path("C:/Projects/Dominium/dominium"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def normalize_remote_url(value: str) -> str:
    token = value.strip().replace("\\", "/")
    if token.startswith("git@github.com:"):
        owner_repo = token.split(":", 1)[1]
        if owner_repo.endswith(".git"):
            owner_repo = owner_repo[:-4]
        return f"https://github.com/{owner_repo}.git"
    if token.startswith("https://github.com/"):
        if not token.endswith(".git"):
            token = token + ".git"
        return token
    return token


def run_git(root: Path, args: Sequence[str], *, text: bool = True) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=text,
    )


def git_stdout(root: Path, args: Sequence[str]) -> tuple[bool, str]:
    result = run_git(root, args, text=True)
    stdout = str(result.stdout).strip()
    stderr = str(result.stderr).strip()
    if result.returncode != 0:
        return False, stderr or stdout
    return True, stdout


def tracked_tree_digest(root: Path) -> str:
    result = run_git(root, ["ls-files", "-s", "-z"], text=False)
    if result.returncode != 0:
        return "unavailable"
    data = bytes(result.stdout)
    return sha256_bytes(data)


def command_implementation_digests(root: Path) -> dict[str, str]:
    digests: dict[str, str] = {}
    for rel in RELEVANT_DOMINIUM_RELS:
        path = root / rel
        if path.exists() and path.is_file():
            digests[rel.as_posix()] = sha256_file(path)
        else:
            digests[rel.as_posix()] = "missing"
    return digests


def capture_dominium_state(root: Path) -> dict[str, Any]:
    head_ok, head = git_stdout(root, ["rev-parse", "HEAD"])
    remote_ok, remote = git_stdout(root, ["remote", "get-url", "origin"])
    status_ok, status_text = git_stdout(root, ["status", "--porcelain=v1", "--untracked-files=all"])
    branch_ok, branch_text = git_stdout(root, ["status", "--short", "--branch"])
    return {
        "repository_present": root.exists() and root.is_dir(),
        "git_head_available": head_ok,
        "revision": head if head_ok else "",
        "remote_url": remote if remote_ok else "",
        "normalized_remote_url": normalize_remote_url(remote) if remote_ok else "",
        "status_available": status_ok,
        "porcelain_status": status_text if status_ok else "",
        "short_branch_status": branch_text if branch_ok else "",
        "clean": status_ok and status_text == "",
        "tracked_tree_digest": tracked_tree_digest(root) if root.exists() else "missing",
        "command_implementation_digests": command_implementation_digests(root) if root.exists() else {},
    }


def sanitized_environment(base: Mapping[str, str] | None = None) -> dict[str, str]:
    source = dict(base or os.environ)
    keep = [
        "PATH",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "PATHEXT",
        "TEMP",
        "TMP",
        "SystemDrive",
        "HOME",
        "USERPROFILE",
    ]
    env = {key: source[key] for key in keep if key in source}
    env.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
            "PYTHONHASHSEED": "0",
        }
    )
    return env


def default_process_runner(
    argv: Sequence[str],
    cwd: Path,
    env: Mapping[str, str],
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=str(cwd),
        env=dict(env),
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
        check=False,
    )


def resolve_python_executable(value: str | Path | None = None) -> str:
    if value:
        return str(Path(value).resolve())
    executable = Path(sys.executable)
    if executable.exists():
        return str(executable.resolve())
    found = shutil.which("python")
    return str(Path(found).resolve()) if found else sys.executable


def build_argv(python_executable: str, dominium_root: Path) -> list[str]:
    return [
        python_executable,
        str((dominium_root / CLI_REL).resolve()),
        "--repo-root",
        str(dominium_root.resolve()),
        "--target",
        "all",
        "--profile",
        "FAST",
        "--surface",
        "aide",
        "--mode",
        "dry_run",
    ]


def build_invocation_request(
    *,
    repo_root: str | Path = ".",
    dominium_root: str | Path | None = None,
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    root = Path(dominium_root).resolve() if dominium_root else default_dominium_root(repo_root).resolve()
    revision = expected_revision
    if revision is None and root.exists():
        ok, observed = git_stdout(root, ["rev-parse", "HEAD"])
        revision = observed if ok else ""
    py = resolve_python_executable(python_executable)
    return {
        "schema_version": "aide.dominium-registered-validation.invocation-request.v1",
        "task_id": TASK_ID,
        "capability_id": capability_id,
        "expected_capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "dominium_root": str(root),
        "expected_revision": revision or "",
        "expected_remote_url": EXPECTED_REMOTE_URL,
        "python_executable": py,
        "script_path": str((root / CLI_REL).resolve()),
        "timeout_seconds": float(timeout_seconds),
        "argv": build_argv(py, root),
        "argv_template": [
            "<python>",
            CLI_REL.as_posix(),
            "--repo-root",
            "<pinned-dominium-root>",
            "--target",
            "all",
            "--profile",
            "FAST",
            "--surface",
            "aide",
            "--mode",
            "dry_run",
        ],
        "target": "all",
        "profile": "FAST",
        "surface": "aide",
        "mode": "dry_run",
        "write_reports_arg_present": False,
        "json_out_arg_present": False,
        "shell": False,
        "expected_digests": dict(expected_digests or {}),
    }


def refusal(
    *,
    request: Mapping[str, Any],
    reason_code: str,
    message: str,
    process_call_count: int,
    dominium_result: Mapping[str, Any] | None = None,
    returncode: int | None = None,
    stdout: str = "",
    stderr: str = "",
) -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-registered-validation.invocation-result.v1",
        "kind": "DominiumRegisteredValidationInvocationResult",
        "task_id": TASK_ID,
        "capability_id": request.get("capability_id", CAPABILITY_ID),
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "result": "REFUSED",
        "status": "REFUSED",
        "reason_code": reason_code,
        "message": message,
        "process_call_count": process_call_count,
        "actual_dominium_cli_process_spawned": process_call_count == 1,
        "fixture_callable_used_as_executor": False,
        "result_origin": "dominium_stdout_json" if dominium_result else "aide_preflight_or_process_boundary",
        "constructed_success_result": False,
        "returncode": returncode,
        "stdout": stream_summary(stdout),
        "stderr": stream_summary(stderr),
        "dominium_stdout_json_parsed": bool(dominium_result),
        "dominium_command_result": dict(dominium_result or {}),
        "typed_refusal": True,
        "typed_result": False,
        "service_adapter_boundary_reached": "unproven",
        "run_validation_command_boundary_reached": "proven" if dominium_result and dominium_result.get("command_id") == CAPABILITY_ID else "unproven",
        **_false_boundary(),
    }


def stream_summary(text: str) -> dict[str, Any]:
    return {
        "byte_count": len(text.encode("utf-8")),
        "sha256": sha256_text(text),
        "excerpt": text[:800],
    }


def _preflight_error(request: Mapping[str, Any], before_state: Mapping[str, Any]) -> tuple[str, str] | None:
    if request.get("capability_id") != CAPABILITY_ID:
        return REFUSAL_CODES["unsupported_capability"], "Only dominium.validation.run is admitted by this backend."
    dominium_root = Path(str(request.get("dominium_root", "")))
    if not dominium_root.exists() or not dominium_root.is_dir():
        return REFUSAL_CODES["checkout_missing"], "Pinned Dominium checkout is missing."
    if before_state.get("normalized_remote_url") != normalize_remote_url(EXPECTED_REMOTE_URL):
        return REFUSAL_CODES["repository_identity_mismatch"], "Dominium repository identity did not match the expected origin."
    expected_revision = str(request.get("expected_revision") or "")
    if not expected_revision or before_state.get("revision") != expected_revision:
        return REFUSAL_CODES["revision_mismatch"], "Dominium checkout revision did not match the pinned revision."
    if not before_state.get("clean"):
        return REFUSAL_CODES["dirty_checkout"], "Dominium checkout is dirty or has untracked files."
    for rel in COMMAND_SOURCE_RELS:
        if not (dominium_root / rel).is_file():
            return REFUSAL_CODES["cli_missing"], f"Required Dominium command implementation is missing: {rel.as_posix()}"
    command_text = (dominium_root / COMMAND_REL).read_text(encoding="utf-8", errors="replace")
    service_text = (dominium_root / SERVICE_ADAPTER_REL).read_text(encoding="utf-8", errors="replace")
    if 'COMMAND_ID = "dominium.validation.run"' not in command_text and "COMMAND_ID = 'dominium.validation.run'" not in command_text:
        return REFUSAL_CODES["unexpected_command_id"], "Dominium command.py does not declare command_id dominium.validation.run."
    if "def run_validation_command" not in command_text or "ValidationServiceAdapter" not in command_text:
        return REFUSAL_CODES["unexpected_command_id"], "Dominium command boundary does not reference run_validation_command and ValidationServiceAdapter."
    if "class ValidationServiceAdapter" not in service_text:
        return REFUSAL_CODES["unexpected_command_id"], "Dominium service adapter class was not found."
    expected_digests = request.get("expected_digests", {})
    if isinstance(expected_digests, Mapping):
        actual = before_state.get("command_implementation_digests", {})
        for rel, expected in expected_digests.items():
            if actual.get(str(rel)) != expected:
                return REFUSAL_CODES["digest_mismatch"], f"Command implementation digest mismatch: {rel}"
    argv = list(request.get("argv") or [])
    if "--write-reports" in argv or "--json-out" in argv:
        return REFUSAL_CODES["invalid_request"], "Write-output CLI flags are forbidden for this read-only backend."
    if len(argv) != 12:
        return REFUSAL_CODES["invalid_request"], "Dominium CLI argv shape is not the exact allowlisted invocation."
    return None


def parse_dominium_stdout(stdout: str) -> tuple[dict[str, Any] | None, str | None]:
    if not stdout.strip():
        return None, REFUSAL_CODES["empty_output"]
    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError:
        return None, REFUSAL_CODES["malformed_json"]
    if not isinstance(parsed, dict):
        return None, REFUSAL_CODES["malformed_json"]
    if parsed.get("command_id") != CAPABILITY_ID:
        return parsed, REFUSAL_CODES["unexpected_command_id"]
    return parsed, None


class DominiumStateProbe:
    coverage = STATE_PROBE_COVERAGE

    def __init__(self, root: Path):
        self.root = root

    def capture(self) -> Mapping[str, Any]:
        if self.root.exists():
            return capture_dominium_state(self.root)
        return {"repository_present": False}

    def mutation_observation(
        self,
        before_state: Mapping[str, Any],
        after_state: Mapping[str, Any],
    ) -> str:
        if (
            before_state.get("revision") == after_state.get("revision")
            and before_state.get("porcelain_status") == after_state.get("porcelain_status")
            and before_state.get("tracked_tree_digest") == after_state.get("tracked_tree_digest")
            and before_state.get("command_implementation_digests") == after_state.get("command_implementation_digests")
        ):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


class DominiumPrecondition:
    def __init__(self, request: Mapping[str, Any]):
        self.request = request

    def check(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
        spec: RegisteredProcessSpec,
        before_state: Mapping[str, Any],
    ) -> PreconditionResult:
        preflight = _preflight_error(self.request, before_state)
        if preflight is None:
            return PreconditionResult(True)
        code, message = preflight
        return PreconditionResult(False, code, message)


class DominiumOutputDecoder:
    decoder_id = "dominium.validation.run-json-v0"

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> DecoderResult:
        parsed, parse_error = parse_dominium_stdout(stdout)
        if parse_error:
            return DecoderResult(
                "refused",
                "none",
                domain_result=parsed,
                reason_code=parse_error,
                message="Dominium validation command stdout did not contain expected command JSON.",
            )
        if parsed and parsed.get("status") == "refused":
            return DecoderResult("decoded", "typed_refusal", domain_result=parsed, refusal=parsed)
        return DecoderResult("decoded", "typed_result", domain_result=parsed or {})


class DominiumStreamScrubber:
    scrubber_id = "dominium-report-stream-scrubber-v0"

    def __init__(self, request: Mapping[str, Any]):
        self.dominium_root = str(request.get("dominium_root", ""))
        self.python_executable = str(request.get("python_executable", ""))

    def scrub(self, text: str) -> str:
        return scrub_string(text, dominium_root=self.dominium_root, python_executable=self.python_executable)


def build_registered_process_spec(request: Mapping[str, Any]) -> RegisteredProcessSpec:
    argv = [str(item) for item in request.get("argv", [])]
    executable = argv[0] if argv else ""
    return RegisteredProcessSpec(
        capability_ref=CAPABILITY_REF,
        executable=executable,
        argument_plan=[ArgumentToken("literal", item) for item in argv[1:]],
        working_directory=str(Path(str(request.get("dominium_root", ""))).resolve()),
        timeout_seconds=float(request.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
        environment=sanitized_environment(),
        decoder_id=DominiumOutputDecoder.decoder_id,
        state_probe_id="dominium-git-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id=DominiumStreamScrubber.scrubber_id,
        provider_spec_ref="aide://provider-spec/dominium-registered-validation-command-boundary-v0",
        conformance_profile_ref="aide://conformance-profile/dominium-registered-validation-command-boundary-v0",
        metadata={
            "argv_template": list(request.get("argv_template", [])),
            "target": request.get("target"),
            "profile": request.get("profile"),
            "surface": request.get("surface"),
            "mode": request.get("mode"),
        },
    )


def _dominium_reason_code(reason_code: str, receipt: ProcessExecutionReceipt, outcome: CapabilityOutcome) -> str:
    if reason_code in set(REFUSAL_CODES.values()):
        return reason_code
    if reason_code == "missing_executable":
        return REFUSAL_CODES["cli_missing"]
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
    environment_constraints = {
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
        "PYTHONHASHSEED": "0",
    }
    return {
        "argv": [str(item) for item in launch.get("argv", [])],
        "cwd": str(launch.get("cwd", "")),
        "env": environment_constraints,
        "environment_manifest_digest": launch.get("environment_manifest_digest", ""),
        "timeout": launch.get("timeout"),
        "shell": False,
    }


def _result_from_provider(
    *,
    request: Mapping[str, Any],
    receipt: ProcessExecutionReceipt,
    outcome: CapabilityOutcome,
) -> dict[str, Any]:
    before_state = dict(receipt.metadata.get("before_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    after_state = dict(receipt.metadata.get("after_state", {})) if isinstance(receipt.metadata, Mapping) else {}
    dominium_result = dict(outcome.domain_result or {})
    stdout_excerpt = str(receipt.stdout.get("excerpt", "")) if isinstance(receipt.stdout, Mapping) else ""
    stderr_excerpt = str(receipt.stderr.get("excerpt", "")) if isinstance(receipt.stderr, Mapping) else ""
    state_changed = receipt.mutation_observation != "none_detected_within_probe_coverage"
    if receipt.launcher_call_count == 0:
        result = refusal(
            request=request,
            reason_code=_dominium_reason_code(outcome.reason_code, receipt, outcome),
            message=outcome.message or "Registered process preflight refused launch.",
            process_call_count=0,
            dominium_result=dominium_result or None,
            returncode=receipt.return_code,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    elif receipt.timed_out:
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["timeout"],
            message="Dominium validation command timed out.",
            process_call_count=receipt.launcher_call_count,
            returncode=None,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    elif state_changed:
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["unexpected_mutation"],
            message="Dominium checkout state changed during read-only validation command invocation.",
            process_call_count=receipt.launcher_call_count,
            dominium_result=dominium_result or None,
            returncode=receipt.return_code,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    elif outcome.reason_code:
        result = refusal(
            request=request,
            reason_code=_dominium_reason_code(outcome.reason_code, receipt, outcome),
            message=outcome.message or "Dominium validation command stdout did not contain the expected command JSON.",
            process_call_count=receipt.launcher_call_count,
            dominium_result=dominium_result or None,
            returncode=receipt.return_code,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    elif receipt.return_code not in (0, None) and dominium_result.get("status") != "refused":
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["nonzero_exit"],
            message="Dominium validation command exited nonzero without a typed Dominium refusal status.",
            process_call_count=receipt.launcher_call_count,
            dominium_result=dominium_result,
            returncode=receipt.return_code,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    elif receipt.return_code not in (0, None):
        result = refusal(
            request=request,
            reason_code=REFUSAL_CODES["nonzero_exit"],
            message="Dominium validation command returned a typed refusal.",
            process_call_count=receipt.launcher_call_count,
            dominium_result=dominium_result,
            returncode=receipt.return_code,
            stdout=stdout_excerpt,
            stderr=stderr_excerpt,
        )
    else:
        result = {
            "schema_version": "aide.dominium-registered-validation.invocation-result.v1",
            "kind": "DominiumRegisteredValidationInvocationResult",
            "task_id": TASK_ID,
            "capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "result": "PASS",
            "status": "PASS",
            "reason_code": "",
            "message": "Dominium validation command returned typed JSON output.",
            "process_call_count": receipt.launcher_call_count,
            "actual_dominium_cli_process_spawned": receipt.launcher_call_count == 1,
            "fixture_callable_used_as_executor": False,
            "result_origin": "dominium_stdout_json",
            "constructed_success_result": False,
            "returncode": receipt.return_code,
            "stdout": dict(receipt.stdout),
            "stderr": dict(receipt.stderr),
            "dominium_stdout_json_parsed": True,
            "dominium_command_result": dominium_result,
            "typed_refusal": False,
            "typed_result": True,
            "service_adapter_boundary_reached": "unproven",
            "run_validation_command_boundary_reached": "proven",
            **_false_boundary(),
        }
    result["stdout"] = dict(receipt.stdout)
    result["stderr"] = dict(receipt.stderr)
    result["before_state"] = before_state
    result["after_state"] = after_state
    result["checkout_state_unchanged"] = not state_changed
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
    return _boundary_classification(result)


def invoke_registered_validation(
    request: Mapping[str, Any],
    *,
    runner: Runner | CountingRunner | None = None,
) -> dict[str, Any]:
    dominium_root = Path(str(request.get("dominium_root", ""))).resolve()
    spec = build_registered_process_spec(request)
    invocation = CapabilityInvocation(
        invocation_ref="aide://invocation/dominium-registered-validation-command-boundary-01",
        capability_ref=CAPABILITY_REF,
        values={"capability_id": CAPABILITY_ID},
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
        precondition=DominiumPrecondition(request),
        state_probe=DominiumStateProbe(dominium_root),
        output_decoder=DominiumOutputDecoder(),
        stream_scrubber=DominiumStreamScrubber(request),
    )
    receipt, outcome = provider.execute(invocation, binding)
    return _result_from_provider(request=request, receipt=receipt, outcome=outcome)


def scrub_string(value: str, *, dominium_root: str = "", python_executable: str = "") -> str:
    result = value
    replacements: list[tuple[str, str]] = []
    if dominium_root:
        root = str(Path(dominium_root))
        replacements.extend([(root, "<dominium-root>"), (root.replace("\\", "/"), "<dominium-root>")])
    if python_executable:
        py = str(Path(python_executable))
        replacements.extend([(py, "<python>"), (py.replace("\\", "/"), "<python>")])
    try:
        aide_root = str(Path.cwd().resolve())
        replacements.extend([(aide_root, "<aide-root>"), (aide_root.replace("\\", "/"), "<aide-root>")])
    except OSError:
        pass
    for token, replacement in sorted(set(replacements), key=lambda item: len(item[0]), reverse=True):
        if token:
            result = result.replace(token, replacement)
    result = re.sub(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}", "<secret-redacted>", result)
    result = re.sub(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"']+", "<absolute-path-redacted>", result)
    return result


def scrub_data(data: Any, *, dominium_root: str = "", python_executable: str = "") -> Any:
    if isinstance(data, dict):
        return {key: scrub_data(value, dominium_root=dominium_root, python_executable=python_executable) for key, value in data.items()}
    if isinstance(data, list):
        return [scrub_data(item, dominium_root=dominium_root, python_executable=python_executable) for item in data]
    if isinstance(data, str):
        return scrub_string(data, dominium_root=dominium_root, python_executable=python_executable)
    return data


def artifact(repo_root: Path, path: Path, role: str) -> dict[str, Any]:
    actual = repo_root / path
    item: dict[str, Any] = {"path": path.as_posix(), "role": role}
    if actual.exists() and actual.is_file():
        item["sha256"] = sha256_file(actual)
    return item


def build_context_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    before_state = result.get("before_state", {}) if isinstance(result.get("before_state"), dict) else {}
    return {
        "apiVersion": envelope.API_VERSION,
        "kind": "ContextDescriptor",
        "metadata": {
            "id": "dominium-registered-validation-context",
            "created_at": DETERMINISTIC_TIMESTAMP,
            "producer": {"name": envelope.PRODUCER_NAME, "version": envelope.PRODUCER_VERSION},
            "semantic_owner": "AIDE",
            "identity_owner": "AIDE",
            "authority_role": "pinned_dominium_checkout_observation",
            "source_revision": before_state.get("revision", ""),
        },
        "spec": {
            "context_ref": CONTEXT_DESCRIPTOR_REF,
            "repository_identity": "github.com/Julesc013/dominium",
            "pinned_revision": before_state.get("revision", ""),
            "command_id": CAPABILITY_ID,
            "command_boundary": [
                CLI_REL.as_posix(),
                "run_validation_command",
                "ValidationServiceAdapter",
            ],
            "mutation_observation": result.get("mutation_observation"),
            "probe_coverage": list(STATE_PROBE_COVERAGE),
            "read_only_guarantee": False,
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "status": {
            "context_projected": True,
            "dominium_cli_process_invoked": bool(result.get("actual_dominium_cli_process_spawned")),
            "dominium_checkout_unchanged": bool(result.get("checkout_state_unchanged")),
            "process_started": result.get("process_started"),
            "launcher_call_count": result.get("launcher_call_count"),
            "structured_output_parsed": result.get("structured_output_parsed"),
            "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
            "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
            "aggregate_validation_executed": result.get("aggregate_validation_executed"),
            "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
            "mutation_observation": result.get("mutation_observation"),
            **_false_boundary(),
        },
    }


def build_context_pack(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    before_state = result.get("before_state", {}) if isinstance(result.get("before_state"), dict) else {}
    source_refs = [
        {
            "ref": reference_id.format_reference_id("source", rel.stem.replace("_", "-")),
            "role": "dominium_command_boundary",
            "kind": "source",
            "path": rel.as_posix(),
            "exists_at_pinned_revision": before_state.get("command_implementation_digests", {}).get(rel.as_posix()) not in {None, "missing"},
            "sha256": before_state.get("command_implementation_digests", {}).get(rel.as_posix()),
        }
        for rel in RELEVANT_DOMINIUM_RELS
    ]
    return {
        "apiVersion": envelope.API_VERSION,
        "kind": "ContextPack",
        "schema_version": "aide.context-pack.v2",
        "protocol_version": "0.1.0",
        "metadata": {
            "id": "dominium-registered-validation-backend-01",
            "name": "Dominium Registered Validation Backend ContextPack",
            "createdAt": DETERMINISTIC_TIMESTAMP,
            "sourcePath": CONTEXT_PACK_JSON.as_posix(),
            "producer": {"name": envelope.PRODUCER_NAME, "version": envelope.PRODUCER_VERSION},
            "compatibility": {
                "schemaVersion": "0.1.0",
                "protocolVersion": "0.1.0",
                "minReaderVersion": "0.1.0",
                "minWriterVersion": "0.1.0",
                "featureFlags": ["context_pack_v2", PROPOSED_CAPABILITY_LABEL],
                "requiredCapabilities": ["context_pack_v2"],
            },
        },
        "spec": {
            "context_pack_ref": CONTEXT_PACK_REF,
            "purpose": "bounded_live_dominium_validation_command_invocation",
            "work_unit_ref": WORKUNIT_REF,
            "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
            "registered_capability_ref": CAPABILITY_REF,
            "registered_capability_id": CAPABILITY_ID,
            "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
            "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
            "source_refs": source_refs,
            "sections": [
                {"id": "dominium_context", "source_refs": [CONTEXT_DESCRIPTOR_REF], "item_count": 1},
                {"id": "work_unit", "source_refs": [WORKUNIT_REF], "item_count": 1},
                {"id": "capability", "source_refs": [CAPABILITY_REF], "item_count": 1},
                {"id": "evidence", "source_refs": [EVIDENCE_REF], "item_count": 1},
            ],
            "allowed_paths": [
                "core/interop/dominium/registered_validation_backend.py",
                ".aide/reports/dominium-registered-validation-backend/**",
            ],
            "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        },
        "status": {
            "validation_performed": True,
            "validation_status": "PASS_WITH_WARNINGS" if result.get("actual_dominium_cli_process_spawned") else "FAILED_VALIDATION",
            "model_call_performed": False,
            "network_call_performed": False,
            "embedding_performed": False,
            "agent_started": False,
            "worker_started": False,
            "command_executed": True,
            "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
            "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
            "aggregate_validation_executed": result.get("aggregate_validation_executed"),
            "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
            "mutation_observation": result.get("mutation_observation"),
            "patch_applied": False,
            "repository_mutated": False,
            "trusted": False,
        },
    }


def build_workunit_record(repo_root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    record = workunit.build_workunit(
        task_id=TASK_ID,
        title="Build Dominium Registered Validation Backend",
        work_type="build",
        authorizes_implementation=True,
        check_only=False,
        acceptance_review=False,
        implementation_scope="exactly-one-readonly-dominium-validation-cli-process",
        stop_state="needs_review",
        predecessors=[SOURCE_ACCEPT_TASK_ID],
        dependencies=[],
        scope={
            "allowed_paths": [
                "core/interop/dominium/registered_validation_backend.py",
                ".aide/scripts/aide_lite.py",
                ".aide/scripts/tests/test_aide_dominium_registered_validation_backend.py",
                ".aide/reports/dominium-registered-validation-backend/**",
                ".aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/**",
            ],
            "forbidden_paths": [],
            "forbidden_operations": list(EXPLICIT_NON_CAPABILITIES),
            "registered_capability_id": CAPABILITY_ID,
            "invocation_limit": 1,
        },
        validation_spec={
            "commands": [
                workunit.validation(
                    "py -3 .aide/scripts/aide_lite.py dominium-registered-validation run",
                    "PASS_WITH_WARNINGS",
                    0,
                    "Invokes exactly one allowlisted Dominium validation CLI process.",
                )
            ]
        },
        evidence_requirements=[
            INVOCATION_RESULT_JSON.as_posix(),
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
        source_path=Path(".aide/queue/AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01/task.yaml"),
        phase="needs_review",
        result="PASS_WITH_WARNINGS" if result.get("actual_dominium_cli_process_spawned") else "FAILED_VALIDATION",
    )
    record["spec"]["registered_capability_id"] = CAPABILITY_ID
    record["spec"]["registered_capability_ref"] = CAPABILITY_REF
    record["spec"]["proposed_capability_label"] = PROPOSED_CAPABILITY_LABEL
    record["spec"]["supersedes_capability_label"] = SUPERSEDED_CAPABILITY_LABEL
    record["spec"]["mutation_observation"] = result.get("mutation_observation")
    record["spec"]["probe_coverage"] = list(STATE_PROBE_COVERAGE)
    record["spec"]["authorized_invocation_count"] = 1
    return record


def build_capability_descriptor(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "aide.dominium-registered-validation.capability-descriptor.v1",
        "kind": "CapabilityDescriptor",
        "task_id": TASK_ID,
        "id": CAPABILITY_ID,
        "capability_ref": CAPABILITY_REF,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "accepted": False,
        "mode": "bounded_invocation",
        "side_effect_class": "none_detected_within_declared_probe_coverage",
        "executor": "dominium_cli_process",
        "fixture_callable_used_as_executor": False,
        "invocation_limit": 1,
        "allowed_targets": ["all"],
        "allowed_argv_template": result.get("argv_template"),
        "shell_allowed": False,
        "private_tool_allowed": False,
        "broad_dispatch_allowed": False,
        "network_allowed": False,
        "provider_or_model_allowed": False,
        "worker_allowed": False,
        "mutation_allowed": False,
        "workbench_apply_allowed": False,
        "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
        "accepted_meaning": "registered Dominium validation command boundary invocation with typed result/refusal preservation and no mutation observed within declared probe coverage",
        "read_only_guarantee": False,
        "probe_coverage": list(STATE_PROBE_COVERAGE),
        "aggregate_validation_success_accepted": False,
        "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
        "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
        "aggregate_validation_executed": result.get("aggregate_validation_executed"),
        "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
        "mutation_observation": result.get("mutation_observation"),
    }


def build_evidence_packet(repo_root: Path, result: Mapping[str, Any], validation_status: str) -> dict[str, Any]:
    command_result = result.get("dominium_command_result", {}) if isinstance(result.get("dominium_command_result"), dict) else {}
    claims = [
        evidence_packet.claim("registered_capability_lookup", "supported", "The WorkUnit references the single admitted dominium.validation.run capability."),
        evidence_packet.claim("exactly_one_process_invocation", "supported" if result.get("process_call_count") == 1 else "contradicted", "The allowlisted Dominium CLI process was spawned exactly once."),
        evidence_packet.claim("dominium_stdout_json_origin", "supported" if result.get("dominium_stdout_json_parsed") else "contradicted", "The AIDE result was derived from Dominium stdout JSON."),
        evidence_packet.claim("fixture_callable_not_executor", "supported" if result.get("fixture_callable_used_as_executor") is False else "contradicted", "The accepted fixture callable was not used as this backend executor."),
        evidence_packet.claim("dominium_checkout_unchanged", "supported" if result.get("checkout_state_unchanged") else "contradicted", "Before and after Dominium state digests match."),
    ]
    if command_result.get("status") == "refused":
        claims.append(evidence_packet.claim("typed_dominium_refusal", "supported", "Dominium returned a typed refusal through the command boundary."))
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
        ],
        validations=[
            evidence_packet.validation("registered Dominium validation backend", validation_status, 0 if validation_status in {"PASS", "PASS_WITH_WARNINGS"} else 1),
        ],
        warnings=[
            "The capability label remains proposed until independent check and acceptance.",
            "A typed Dominium refusal is proof of the registered command result path, not proof of aggregate validation success.",
        ],
        risks=[],
        source_path=EVIDENCE_PACKET_JSON,
        name="Dominium registered validation backend evidence",
        phase=validation_status,
        validation_warnings=["Local Dominium checkout is pinned and clean but behind origin/main."],
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
            "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
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


def build_projection(result: Mapping[str, Any], validation_status: str) -> dict[str, Any]:
    projection = {
        "schema_version": "aide.dominium-registered-validation.projection.v1",
        "kind": "DominiumRegisteredValidationProjection",
        "task_id": TASK_ID,
        "status": validation_status,
        "flow": [
            "pinned clean Dominium checkout",
            "ContextDescriptor",
            "ContextPack",
            "WorkUnit",
            "registered capability lookup",
            "exactly one Dominium CLI process invocation",
            "typed Dominium result or refusal",
            "normalized AIDE result or refusal",
            "EvidencePacket",
            "EventRecord",
            "deterministic invocation-boundary projection",
        ],
        "context_descriptor_ref": CONTEXT_DESCRIPTOR_REF,
        "context_pack_ref": CONTEXT_PACK_REF,
        "workunit_ref": WORKUNIT_REF,
        "capability_ref": CAPABILITY_REF,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
        "evidence_ref": EVIDENCE_REF,
        "event_ref": EVENT_REF,
        "process_call_count": result.get("process_call_count"),
        "launcher_call_count": result.get("launcher_call_count"),
        "process_started": result.get("process_started"),
        "structured_output_parsed": result.get("structured_output_parsed"),
        "transport_boundary_reached": result.get("transport_boundary_reached"),
        "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
        "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
        "domain_outcome": result.get("domain_outcome"),
        "aggregate_validation_executed": result.get("aggregate_validation_executed"),
        "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
        "mutation_observation": result.get("mutation_observation"),
        "probe_coverage": result.get("probe_coverage"),
        "dominium_command_status": (result.get("dominium_command_result") or {}).get("status") if isinstance(result.get("dominium_command_result"), dict) else "",
        "checkout_state_unchanged": result.get("checkout_state_unchanged"),
        "result_origin": result.get("result_origin"),
        "reports": [rel.as_posix() for rel in REPORT_FILES],
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    projection["projection_digest"] = sha256_text(stable_json(projection))
    return projection


def scan_for_leaks(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    absolute_pattern = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"']+")
    secret_pattern = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    if not root.exists():
        return findings
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        text = path.read_text(encoding="utf-8", errors="replace")
        if absolute_pattern.search(text):
            findings.append({"path": _repo_relative(path, Path(".")), "kind": "absolute_path"})
        if secret_pattern.search(text):
            findings.append({"path": _repo_relative(path, Path(".")), "kind": "secret_like"})
    return findings


def validation_errors(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REPORT_FILES:
        if not (repo_root / rel).exists():
            errors.append(f"missing required output: {rel.as_posix()}")
    if errors:
        return errors
    result = read_json(repo_root / INVOCATION_RESULT_JSON)
    context_pack = read_json(repo_root / CONTEXT_PACK_JSON)
    workunit_record = read_json(repo_root / WORKUNIT_JSON)
    evidence = read_json(repo_root / EVIDENCE_PACKET_JSON)
    event = read_json(repo_root / EVENT_RECORD_JSON)
    projection = read_json(repo_root / PROJECTION_JSON)
    errors.extend(workunit.validate_workunit(workunit_record))
    errors.extend(evidence_packet.validate_evidence_packet(evidence))
    errors.extend(event_record.validate_event_record(event))
    if context_pack.get("kind") != "ContextPack":
        errors.append("context pack kind mismatch")
    if result.get("process_call_count") != 1:
        errors.append("process_call_count must be exactly 1")
    if result.get("actual_dominium_cli_process_spawned") is not True:
        errors.append("actual_dominium_cli_process_spawned must be true")
    if result.get("fixture_callable_used_as_executor") is not False:
        errors.append("fixture callable must not be executor")
    if result.get("dominium_stdout_json_parsed") is not True:
        errors.append("Dominium stdout JSON was not parsed")
    if result.get("proposed_capability_label") != PROPOSED_CAPABILITY_LABEL:
        errors.append("proposed capability label is not the relabelled invocation-boundary capability")
    if result.get("launcher_call_count") != result.get("process_call_count"):
        errors.append("launcher_call_count must match process_call_count for this provider")
    if result.get("structured_output_parsed") is not True:
        errors.append("structured_output_parsed must be true")
    if result.get("registered_command_boundary_reached") != "proven":
        errors.append("registered command boundary must be proven")
    if result.get("service_adapter_boundary_reached") != "unproven":
        errors.append("service adapter boundary must remain unproven without Dominium-emitted evidence")
    if result.get("aggregate_validation_executed") is not False:
        errors.append("aggregate validation execution must not be claimed")
    if result.get("aggregate_validation_succeeded") is not False:
        errors.append("aggregate validation success must not be claimed")
    if result.get("mutation_observation") != "none_detected_within_probe_coverage":
        errors.append("mutation observation must be scoped to declared probe coverage")
    command_result = result.get("dominium_command_result") if isinstance(result.get("dominium_command_result"), dict) else {}
    if command_result.get("command_id") != CAPABILITY_ID:
        errors.append("Dominium command_id mismatch")
    if result.get("checkout_state_unchanged") is not True:
        errors.append("Dominium checkout state changed")
    allowlisted = result.get("allowlisted_process_call") if isinstance(result.get("allowlisted_process_call"), dict) else {}
    argv = allowlisted.get("argv") if isinstance(allowlisted.get("argv"), list) else []
    if "--write-reports" in argv or "--json-out" in argv:
        errors.append("write-output CLI flags appeared in argv")
    if allowlisted.get("shell") is not False:
        errors.append("process runner shell flag must be false")
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
        "schema_version": "aide.dominium-registered-validation.validation.v1",
        "kind": "DominiumRegisteredValidationValidation",
        "task_id": TASK_ID,
        "status": status_value,
        "validation_status": status_value,
        "validated": not errors,
        "validation_errors": errors,
        "warnings": [
            "Capability label is proposed, not accepted.",
            "Local Dominium checkout is pinned and clean but may be behind origin/main.",
        ],
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
        "process_call_count": result.get("process_call_count"),
        "launcher_call_count": result.get("launcher_call_count"),
        "process_started": result.get("process_started"),
        "structured_output_parsed": result.get("structured_output_parsed"),
        "transport_boundary_reached": result.get("transport_boundary_reached"),
        "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
        "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
        "domain_outcome": result.get("domain_outcome"),
        "aggregate_validation_executed": result.get("aggregate_validation_executed"),
        "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
        "mutation_observation": result.get("mutation_observation"),
        "probe_coverage": result.get("probe_coverage"),
        "dominium_command_status": (result.get("dominium_command_result") or {}).get("status") if isinstance(result.get("dominium_command_result"), dict) else "",
        "result_origin": result.get("result_origin"),
        "checkout_state_unchanged": result.get("checkout_state_unchanged"),
        "missing_evidence": 0 if not errors else len(errors),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_json(root / VALIDATION_JSON, report)
    write_text(root / STATUS_MD, render_status_markdown(report))
    return report


def write_outputs(repo_root: Path, request: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    request = {**dict(request), "proposed_capability_label": PROPOSED_CAPABILITY_LABEL, "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL}
    result = _boundary_classification({**dict(result), "proposed_capability_label": PROPOSED_CAPABILITY_LABEL})
    validation_status = "PASS_WITH_WARNINGS" if (
        result.get("process_call_count") == 1
        and result.get("actual_dominium_cli_process_spawned") is True
        and result.get("dominium_stdout_json_parsed") is True
        and result.get("checkout_state_unchanged") is True
    ) else "FAILED_VALIDATION"
    scrub_context = {
        "dominium_root": str(request.get("dominium_root", "")),
        "python_executable": str(request.get("python_executable", "")),
    }
    context_descriptor = build_context_descriptor(result)
    context_pack = build_context_pack(repo_root, result)
    workunit_record = build_workunit_record(repo_root, result)
    capability = build_capability_descriptor(result)
    projection = build_projection(result, validation_status)
    backend_report = {
        "schema_version": "aide.dominium-registered-validation.backend-report.v1",
        "kind": "DominiumRegisteredValidationBackendReport",
        "task_id": TASK_ID,
        "status": validation_status,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
        "result": result,
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    for path, payload in [
        (CONTEXT_DESCRIPTOR_JSON, context_descriptor),
        (CONTEXT_PACK_JSON, context_pack),
        (WORKUNIT_JSON, workunit_record),
        (CAPABILITY_DESCRIPTOR_JSON, capability),
        (INVOCATION_REQUEST_JSON, dict(request)),
        (INVOCATION_RESULT_JSON, dict(result)),
        (PROJECTION_JSON, projection),
        (BACKEND_REPORT_JSON, backend_report),
    ]:
        write_json(repo_root / path, scrub_data(payload, **scrub_context))
    validation = validate_reports(repo_root)
    evidence = build_evidence_packet(repo_root, result, validation["validation_status"])
    event = build_event_record(repo_root)
    write_json(repo_root / EVIDENCE_PACKET_JSON, scrub_data(evidence, **scrub_context))
    write_json(repo_root / EVENT_RECORD_JSON, scrub_data(event, **scrub_context))
    validation = validate_reports(repo_root)
    write_text(repo_root / BACKEND_REPORT_MD, render_backend_report_markdown(read_json(repo_root / BACKEND_REPORT_JSON), validation))
    write_text(repo_root / WARNING_DISPOSITION_MD, render_warning_disposition_markdown(result))
    write_text(repo_root / EXPLICIT_NON_CAPABILITIES_MD, render_explicit_non_capabilities_markdown())
    write_text(repo_root / NEXT_TASK_PROMPT_MD, render_next_task_prompt())
    return validation


def run_backend(
    repo_root: str | Path = ".",
    *,
    dominium_root: str | Path | None = None,
    expected_revision: str | None = None,
    capability_id: str = CAPABILITY_ID,
    python_executable: str | Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    expected_digests: Mapping[str, str] | None = None,
    runner: Runner | CountingRunner | None = None,
    write_reports: bool = True,
) -> dict[str, Any]:
    root = Path(repo_root)
    request = build_invocation_request(
        repo_root=root,
        dominium_root=dominium_root,
        expected_revision=expected_revision,
        capability_id=capability_id,
        python_executable=python_executable,
        timeout_seconds=timeout_seconds,
        expected_digests=expected_digests,
    )
    result = invoke_registered_validation(request, runner=runner)
    if write_reports:
        validation = write_outputs(root, request, result)
        result = {**result, "validation_status": validation["validation_status"], "validation_errors": validation["validation_errors"]}
    return result


def status(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    validation_exists = (root / VALIDATION_JSON).exists()
    validation = read_json(root / VALIDATION_JSON) if validation_exists else {}
    data = {
        "schema_version": "aide.dominium-registered-validation.status.v1",
        "kind": "DominiumRegisteredValidationStatus",
        "task_id": TASK_ID,
        "status": validation.get("validation_status", "NOT_RUN") if validation_exists else "NOT_RUN",
        "validation_report_exists": validation_exists,
        "capability_id": CAPABILITY_ID,
        "proposed_capability_label": PROPOSED_CAPABILITY_LABEL,
        "supersedes_capability_label": SUPERSEDED_CAPABILITY_LABEL,
        "process_call_count": validation.get("process_call_count"),
        "launcher_call_count": validation.get("launcher_call_count"),
        "registered_command_boundary_reached": validation.get("registered_command_boundary_reached"),
        "service_adapter_boundary_reached": validation.get("service_adapter_boundary_reached"),
        "aggregate_validation_executed": validation.get("aggregate_validation_executed"),
        "aggregate_validation_succeeded": validation.get("aggregate_validation_succeeded"),
        "mutation_observation": validation.get("mutation_observation"),
        "recommended_next_task": CHECK_TASK_ID,
        **_false_boundary(),
    }
    write_text(root / STATUS_MD, render_status_markdown(data))
    return data


def render_status_markdown(data: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Dominium Registered Validation Backend Status",
            "",
            f"- task_id: `{TASK_ID}`",
            f"- status: `{data.get('status') or data.get('validation_status')}`",
            f"- capability_id: `{CAPABILITY_ID}`",
            f"- proposed_capability_label: `{PROPOSED_CAPABILITY_LABEL}`",
            f"- supersedes_capability_label: `{SUPERSEDED_CAPABILITY_LABEL}`",
            f"- process_call_count: `{data.get('process_call_count', '')}`",
            f"- launcher_call_count: `{data.get('launcher_call_count', '')}`",
            f"- registered_command_boundary_reached: `{data.get('registered_command_boundary_reached', '')}`",
            f"- service_adapter_boundary_reached: `{data.get('service_adapter_boundary_reached', '')}`",
            f"- aggregate_validation_executed: `{str(data.get('aggregate_validation_executed', False)).lower()}`",
            f"- aggregate_validation_succeeded: `{str(data.get('aggregate_validation_succeeded', False)).lower()}`",
            f"- mutation_observation: `{data.get('mutation_observation', '')}`",
            f"- checkout_state_unchanged: `{str(data.get('checkout_state_unchanged', False)).lower()}`",
            f"- result_origin: `{data.get('result_origin', '')}`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            "",
        ]
    )


def render_backend_report_markdown(report: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
    result = report.get("result", {}) if isinstance(report.get("result"), dict) else {}
    command_result = result.get("dominium_command_result", {}) if isinstance(result.get("dominium_command_result"), dict) else {}
    return "\n".join(
        [
            "# Dominium Registered Validation Backend",
            "",
            f"- status: `{validation.get('validation_status')}`",
            f"- capability_id: `{CAPABILITY_ID}`",
            f"- proposed_capability_label: `{PROPOSED_CAPABILITY_LABEL}`",
            f"- supersedes_capability_label: `{SUPERSEDED_CAPABILITY_LABEL}`",
            f"- process_call_count: `{result.get('process_call_count')}`",
            f"- launcher_call_count: `{result.get('launcher_call_count')}`",
            f"- registered_command_boundary_reached: `{result.get('registered_command_boundary_reached')}`",
            f"- service_adapter_boundary_reached: `{result.get('service_adapter_boundary_reached')}`",
            f"- aggregate_validation_executed: `{str(result.get('aggregate_validation_executed', False)).lower()}`",
            f"- aggregate_validation_succeeded: `{str(result.get('aggregate_validation_succeeded', False)).lower()}`",
            f"- mutation_observation: `{result.get('mutation_observation')}`",
            f"- dominium_command_status: `{command_result.get('status', '')}`",
            f"- result_origin: `{result.get('result_origin', '')}`",
            f"- checkout_state_unchanged: `{str(result.get('checkout_state_unchanged', False)).lower()}`",
            f"- recommended_next_task: `{CHECK_TASK_ID}`",
            "",
        ]
    )


def render_warning_disposition_markdown(result: Mapping[str, Any]) -> str:
    command_result = result.get("dominium_command_result", {}) if isinstance(result.get("dominium_command_result"), dict) else {}
    lines = [
        "# Warning Disposition",
        "",
        f"- The prior label `{SUPERSEDED_CAPABILITY_LABEL}` is superseded by `{PROPOSED_CAPABILITY_LABEL}`.",
        "- The local Dominium checkout was not refreshed; its observed HEAD is the pinned input.",
        "- The build proves the Dominium CLI command boundary was entered, not broad Dominium command dispatch.",
    ]
    if command_result.get("status") == "refused":
        lines.append("- Dominium returned a typed refusal from the real command path; this is recorded as a registered command-boundary result, not as validation success or service-adapter proof.")
    lines.append("")
    return "\n".join(lines)


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
            f"Independently check `{TASK_ID}`. Verify the active capability label is `{PROPOSED_CAPABILITY_LABEL}`, the real Dominium CLI was entered exactly once, the fixture callable was not used, the result originated from Dominium stdout JSON, registered command boundary evidence is separated from service-adapter and aggregate-validation claims, unsupported requests spawned no process, the checkout remained clean and unchanged within declared probe coverage, reports are scrubbed, and evidence is complete.",
            "",
            f"If the build passes, recommend `{ACCEPT_TASK_ID}`. If a material defect remains, recommend `AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-REPAIR-01`.",
            "",
        ]
    )
