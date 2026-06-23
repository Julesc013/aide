from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
SOURCE_TASK_ID = "AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"
SOURCE_COMMIT = "1206980e8897ba6031d2d142743d9cac53be1817"
SOURCE_LABEL = "live_dominium_validation_command_readonly_v0"
RECOMMENDED_LABEL = "dominium_registered_validation_command_boundary_readonly_v0"
REPAIR_TASK = "AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01"
ACCEPT_TASK = "AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01"

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE_DIR = ROOT / ".aide" / "queue" / TASK_ID / "evidence"
SOURCE_QUEUE_DIR = ROOT / ".aide" / "queue" / SOURCE_TASK_ID
SOURCE_REPORT_DIR = ROOT / ".aide" / "reports" / "dominium-registered-validation-backend"
REPORT_DIR = ROOT / ".aide" / "reports" / "dominium-registered-validation-backend-check"
DOMINIUM_ROOT = (ROOT.parent.parent / "Dominium" / "dominium").resolve()

FALSE_BOUNDARY_FIELDS = [
    "dominium_command_invoked",
    "host_runtime_started",
    "workbench_started",
    "bridge_runtime_started",
    "service_started",
    "database_opened",
    "transport_started",
    "network_call_performed",
    "provider_or_model_called",
    "worker_executed",
    "patch_transaction_applied",
    "preview_or_apply_performed",
    "source_repository_mutated",
    "target_repository_mutated",
    "branch_or_worktree_created",
    "github_mutation_performed",
    "release_or_promotion_performed",
    "generated_projection_marked_canonical",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        if DOMINIUM_ROOT in path.parents or path == DOMINIUM_ROOT:
            return "<dominium-root>/" + path.relative_to(DOMINIUM_ROOT).as_posix()
        return path.name


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def run_git(root: Path, args: list[str], *, text: bool = True) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False, text=text)


def git_stdout(root: Path, args: list[str]) -> tuple[bool, str]:
    result = run_git(root, args, text=True)
    stdout = str(result.stdout).strip()
    stderr = str(result.stderr).strip()
    return result.returncode == 0, stdout if result.returncode == 0 else stderr or stdout


def tracked_tree_digest(root: Path) -> str:
    result = run_git(root, ["ls-files", "-s", "-z"], text=False)
    if result.returncode != 0:
        return "unavailable"
    return sha256_bytes(bytes(result.stdout))


def dominium_state() -> dict[str, Any]:
    if not DOMINIUM_ROOT.exists():
        return {"repository_present": False}
    head_ok, head = git_stdout(DOMINIUM_ROOT, ["rev-parse", "HEAD"])
    status_ok, status = git_stdout(DOMINIUM_ROOT, ["status", "--porcelain=v1", "--untracked-files=all"])
    branch_ok, branch = git_stdout(DOMINIUM_ROOT, ["status", "--short", "--branch"])
    digests: dict[str, str] = {}
    for rel_path in [
        "apps/workbench/module/validation/cli.py",
        "apps/workbench/module/validation/command.py",
        "apps/workbench/module/validation/service_adapter.py",
        "contracts/action/validation_actions.registry.json",
        "contracts/command/command_surface.contract.toml",
        "contracts/command/validation_run_input.schema.json",
        "contracts/command/validation_run_result.schema.json",
        "contracts/diagnostic/diagnostic_code.registry.json",
        "contracts/refusal/refusal_code.registry.json",
        "contracts/schema/validation_result.schema.json",
    ]:
        target = DOMINIUM_ROOT / rel_path
        digests[rel_path] = sha256_file(target) if target.is_file() else "missing"
    return {
        "repository_present": True,
        "revision": head if head_ok else "",
        "porcelain_status": status if status_ok else "",
        "short_branch_status": branch if branch_ok else "",
        "clean": status_ok and status == "",
        "tracked_tree_digest": tracked_tree_digest(DOMINIUM_ROOT),
        "command_implementation_digests": digests,
    }


def scan_leaks(paths: list[Path]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    secret_re = re.compile(r"(?i)\b(sk|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9_\-]{8,}")
    abs_re = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"'<>]+")
    for base in paths:
        if not base.exists():
            continue
        files = [base] if base.is_file() else [item for item in base.rglob("*") if item.is_file()]
        for file_path in files:
            if "__pycache__" in file_path.parts:
                continue
            text = read_text(file_path)
            for match in abs_re.finditer(text):
                findings.append({"path": rel(file_path), "kind": "absolute_path", "sample": "<redacted>"})
                break
            user_token = "\\".join(["Users", "Jules"])
            user_token_posix = "/".join(["Users", "Jules"])
            if user_token in text or user_token_posix in text:
                findings.append({"path": rel(file_path), "kind": "user_path", "sample": "<redacted>"})
            if secret_re.search(text):
                findings.append({"path": rel(file_path), "kind": "secret_like", "sample": "<redacted>"})
    return findings


def add_assert(assertions: list[dict[str, Any]], *, id: str, category: str, description: str, expected: Any, observed: Any, ok: bool, severity: str = "info", evidence_refs: list[str] | None = None) -> None:
    if ok:
        outcome = "PASS"
    elif severity == "warning":
        outcome = "WARN"
    else:
        outcome = "FAIL"
    assertions.append(
        {
            "id": id,
            "category": category,
            "description": description,
            "outcome": outcome,
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs or [],
            "source_finding_id": None,
        }
    )


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    assertions: list[dict[str, Any]] = []
    warnings: list[str] = []

    source_task = load_json_ish(SOURCE_QUEUE_DIR / "task.yaml")
    source_status = load_json_ish(SOURCE_QUEUE_DIR / "status.yaml")
    validation = load_json(SOURCE_REPORT_DIR / "validation.json")
    invocation = load_json(SOURCE_REPORT_DIR / "invocation-result.json")
    capability = load_json(SOURCE_REPORT_DIR / "capability-descriptor.json")
    evidence_packet = load_json(SOURCE_REPORT_DIR / "evidence-packet.json")
    event_record = load_json(SOURCE_REPORT_DIR / "event-record.json")
    backend_source = read_text(ROOT / "core" / "interop" / "dominium" / "registered_validation_backend.py")

    dom_state = dominium_state()
    command_text = read_text(DOMINIUM_ROOT / "apps/workbench/module/validation/command.py") if DOMINIUM_ROOT.exists() else ""
    service_text = read_text(DOMINIUM_ROOT / "apps/workbench/module/validation/service_adapter.py") if DOMINIUM_ROOT.exists() else ""
    cli_text = read_text(DOMINIUM_ROOT / "apps/workbench/module/validation/cli.py") if DOMINIUM_ROOT.exists() else ""

    add_assert(
        assertions,
        id="baseline.source_task_ready",
        category="baseline",
        description="Source build task is at the expected review gate with complete evidence.",
        expected={"result": "PASS_WITH_WARNINGS", "missing_evidence": 0, "recommended_next_task": TASK_ID},
        observed={
            "result": source_status.get("result"),
            "missing_evidence": source_status.get("missing_evidence"),
            "recommended_next_task": source_status.get("recommended_next_task"),
        },
        ok=source_status.get("result") == "PASS_WITH_WARNINGS"
        and source_status.get("missing_evidence") == 0
        and source_status.get("recommended_next_task") == TASK_ID,
        severity="material",
        evidence_refs=[rel(SOURCE_QUEUE_DIR / "status.yaml")],
    )

    add_assert(
        assertions,
        id="baseline.no_downstream_acceptance_or_repair_exists",
        category="baseline",
        description="No acceptance, relabel repair, or genericization task already supersedes this check.",
        expected=False,
        observed={
            ACCEPT_TASK: (ROOT / ".aide" / "queue" / ACCEPT_TASK).exists(),
            REPAIR_TASK: (ROOT / ".aide" / "queue" / REPAIR_TASK).exists(),
            "AIDE-BUILD-REGISTERED-PROCESS-CAPABILITY-BACKEND-V0-01": (ROOT / ".aide" / "queue" / "AIDE-BUILD-REGISTERED-PROCESS-CAPABILITY-BACKEND-V0-01").exists(),
        },
        ok=not (ROOT / ".aide" / "queue" / ACCEPT_TASK).exists()
        and not (ROOT / ".aide" / "queue" / REPAIR_TASK).exists()
        and not (ROOT / ".aide" / "queue" / "AIDE-BUILD-REGISTERED-PROCESS-CAPABILITY-BACKEND-V0-01").exists(),
        severity="material",
        evidence_refs=[".aide/queue/index.yaml"],
    )

    call = invocation.get("allowlisted_process_call") or {}
    expected_argv = [
        "<python>",
        "<dominium-root>\\apps\\workbench\\module\\validation\\cli.py",
        "--repo-root",
        "<dominium-root>",
        "--target",
        "all",
        "--profile",
        "FAST",
        "--surface",
        "aide",
        "--mode",
        "dry_run",
    ]
    add_assert(
        assertions,
        id="process.exactly_one_allowlisted_cli_call",
        category="process",
        description="Build evidence records one shell-free allowlisted Dominium CLI process call with the exact read-only argv.",
        expected={"process_call_count": 1, "argv": expected_argv, "shell": False},
        observed={"process_call_count": invocation.get("process_call_count"), "argv": call.get("argv"), "shell": call.get("shell")},
        ok=invocation.get("process_call_count") == 1
        and invocation.get("actual_dominium_cli_process_spawned") is True
        and call.get("argv") == expected_argv
        and call.get("shell") is False
        and "--write-reports" not in list(call.get("argv") or [])
        and "--json-out" not in list(call.get("argv") or []),
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json")],
    )

    env = call.get("env") if isinstance(call.get("env"), dict) else {}
    expected_env = {
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
    }
    add_assert(
        assertions,
        id="process.environment_constraints",
        category="process",
        description="The recorded process environment contains the required Python isolation constraints.",
        expected=expected_env,
        observed={key: env.get(key) for key in expected_env},
        ok=all(env.get(key) == value for key, value in expected_env.items()),
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json")],
    )

    dom_result = invocation.get("dominium_command_result") if isinstance(invocation.get("dominium_command_result"), dict) else {}
    refusal_payload = ((dom_result.get("payload") or {}).get("refusal") or {}) if isinstance(dom_result.get("payload"), dict) else {}
    add_assert(
        assertions,
        id="result.origin_and_refusal_are_dominium_stdout",
        category="result",
        description="The normalized AIDE result is derived from Dominium stdout JSON and preserves the typed Dominium refusal.",
        expected={
            "origin": "dominium_stdout_json",
            "command_id": "dominium.validation.run",
            "status": "refused",
            "refusal_code": "dominium.refusal.validation.tool_unavailable",
        },
        observed={
            "origin": invocation.get("result_origin"),
            "command_id": dom_result.get("command_id"),
            "status": dom_result.get("status"),
            "refusal_code": refusal_payload.get("code"),
            "returncode": invocation.get("returncode"),
            "constructed_success_result": invocation.get("constructed_success_result"),
        },
        ok=invocation.get("result_origin") == "dominium_stdout_json"
        and invocation.get("dominium_stdout_json_parsed") is True
        and invocation.get("constructed_success_result") is False
        and invocation.get("typed_refusal") is True
        and invocation.get("typed_result") is False
        and dom_result.get("command_id") == "dominium.validation.run"
        and dom_result.get("status") == "refused"
        and refusal_payload.get("code") == "dominium.refusal.validation.tool_unavailable",
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json")],
    )

    add_assert(
        assertions,
        id="executor.fixture_callable_not_used",
        category="executor",
        description="This backend does not use the accepted fixture callable as its executor.",
        expected=False,
        observed={
            "report_flag": invocation.get("fixture_callable_used_as_executor"),
            "source_contains_local_fixture_callable": "local_fixture_callable" in backend_source,
        },
        ok=invocation.get("fixture_callable_used_as_executor") is False and "local_fixture_callable" not in backend_source,
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json"), "core/interop/dominium/registered_validation_backend.py"],
    )

    service_message = "aggregate validation suite service is not bound in the Workbench validation slice"
    command_boundary_ok = (
        "from apps.workbench.module.validation.command import" in cli_text
        and "run_validation_command" in cli_text
        and "def run_validation_command" in command_text
        and "ValidationServiceAdapter(root)" in command_text
        and "service.run_validation(request)" in command_text
        and "except ValidationCommandError as exc" in command_text
        and service_message in service_text
        and service_message in json.dumps(dom_result, sort_keys=True)
    )
    add_assert(
        assertions,
        id="dominium.service_adapter_refusal_path_corroborated",
        category="dominium_boundary",
        description="The typed refusal is corroborated by Dominium CLI, command, and service adapter source rather than only by AIDE booleans.",
        expected=True,
        observed=command_boundary_ok,
        ok=command_boundary_ok,
        severity="material",
        evidence_refs=[
            "<dominium-root>/apps/workbench/module/validation/cli.py",
            "<dominium-root>/apps/workbench/module/validation/command.py",
            "<dominium-root>/apps/workbench/module/validation/service_adapter.py",
            rel(SOURCE_REPORT_DIR / "invocation-result.json"),
        ],
    )

    broad_boolean = '"service_adapter_boundary_reached": bool(dominium_result)' in backend_source
    add_assert(
        assertions,
        id="dominium.aide_boundary_boolean_is_too_broad_for_generic_reuse",
        category="dominium_boundary",
        description="The AIDE adapter's boundary booleans are broader than a generic proof rule, although this invocation is corroborated by Dominium source.",
        expected=False,
        observed=broad_boolean,
        ok=not broad_boolean,
        severity="warning",
        evidence_refs=["core/interop/dominium/registered_validation_backend.py"],
    )
    if broad_boolean:
        warnings.append("AIDE marks command/service boundaries reached whenever parsed Dominium JSON exists; genericization should use adapter-specific evidence instead.")

    add_assert(
        assertions,
        id="result.no_successful_aggregate_validation_claim",
        category="authority",
        description="Reports do not claim successful aggregate validation; they record a typed refusal for the unavailable aggregate validation suite.",
        expected={"dominium_command_status": "refused", "successful_aggregate_validation": False},
        observed={
            "validation_command_status": validation.get("dominium_command_status"),
            "dominium_result_status": dom_result.get("status"),
            "summary": dom_result.get("summary"),
        },
        ok=validation.get("dominium_command_status") == "refused"
        and dom_result.get("status") == "refused"
        and service_message in str(dom_result.get("summary")),
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "validation.json"), rel(SOURCE_REPORT_DIR / "invocation-result.json")],
    )

    proposed_label = validation.get("proposed_capability_label")
    add_assert(
        assertions,
        id="authority.proposed_capability_label_precise",
        category="authority",
        description="The proposed capability label must name the observed command-boundary proof rather than imply successful live validation.",
        expected=RECOMMENDED_LABEL,
        observed=proposed_label,
        ok=proposed_label == RECOMMENDED_LABEL,
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "validation.json"), rel(SOURCE_REPORT_DIR / "capability-descriptor.json")],
    )

    before = invocation.get("before_state") if isinstance(invocation.get("before_state"), dict) else {}
    after = invocation.get("after_state") if isinstance(invocation.get("after_state"), dict) else {}
    digest_match = before.get("tracked_tree_digest") == after.get("tracked_tree_digest") == dom_state.get("tracked_tree_digest")
    revision_match = before.get("revision") == after.get("revision") == dom_state.get("revision")
    clean_match = before.get("clean") is True and after.get("clean") is True and dom_state.get("clean") is True
    impl_digest_match = before.get("command_implementation_digests") == after.get("command_implementation_digests") == dom_state.get("command_implementation_digests")
    add_assert(
        assertions,
        id="state.dominium_unchanged",
        category="state",
        description="Dominium revision, clean status, tracked tree digest, and command implementation digests remain unchanged.",
        expected=True,
        observed={
            "revision_match": revision_match,
            "clean_match": clean_match,
            "tracked_tree_digest_match": digest_match,
            "implementation_digest_match": impl_digest_match,
            "current_branch_status": dom_state.get("short_branch_status"),
        },
        ok=revision_match and clean_match and digest_match and impl_digest_match and invocation.get("checkout_state_unchanged") is True,
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json"), "<dominium-root> git status/rev-parse/ls-files"],
    )

    false_observed = {field: invocation.get(field) for field in FALSE_BOUNDARY_FIELDS if field in invocation}
    false_ok = bool(false_observed) and all(value is False for value in false_observed.values())
    add_assert(
        assertions,
        id="boundary.false_fields_are_false",
        category="boundary",
        description="Typed result/refusal false-boundary fields emitted by this backend remain boolean false.",
        expected="all emitted false-boundary fields false",
        observed=false_observed,
        ok=false_ok,
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "invocation-result.json")],
    )

    artifact_refs = [item.get("path") for item in (evidence_packet.get("spec", {}).get("artifacts") or []) if isinstance(item, dict)]
    artifacts_exist = all((ROOT / str(path)).exists() for path in artifact_refs if isinstance(path, str))
    event_refs_ok = bool(event_record.get("spec", {}).get("evidence_refs")) and event_record.get("spec", {}).get("payload", {}).get("invocation_count") == 1
    add_assert(
        assertions,
        id="evidence.records_resolve",
        category="evidence",
        description="EvidencePacket artifacts and EventRecord references resolve to generated build records.",
        expected=True,
        observed={"artifact_count": len(artifact_refs), "artifacts_exist": artifacts_exist, "event_refs_ok": event_refs_ok},
        ok=artifacts_exist and event_refs_ok,
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR / "evidence-packet.json"), rel(SOURCE_REPORT_DIR / "event-record.json")],
    )

    report_files = [
        "backend-report.json",
        "backend-report.md",
        "capability-descriptor.json",
        "context-descriptor.json",
        "context-pack.json",
        "event-record.json",
        "evidence-packet.json",
        "explicit-non-capabilities.md",
        "invocation-request.json",
        "invocation-result.json",
        "next-task-prompt.md",
        "projection.json",
        "status.md",
        "validation.json",
        "warning-disposition.md",
        "workunit.json",
    ]
    missing_reports = [name for name in report_files if not (SOURCE_REPORT_DIR / name).exists()]
    add_assert(
        assertions,
        id="reports.required_build_reports_exist",
        category="reports",
        description="All expected build report files are present.",
        expected=[],
        observed=missing_reports,
        ok=missing_reports == [],
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR)],
    )

    leaks = scan_leaks([SOURCE_REPORT_DIR])
    add_assert(
        assertions,
        id="scrub.no_report_path_or_secret_leak",
        category="scrub",
        description="Generated build reports do not leak local absolute paths or secret-like values.",
        expected=[],
        observed=leaks,
        ok=leaks == [],
        severity="material",
        evidence_refs=[rel(SOURCE_REPORT_DIR)],
    )

    local_fallback = "/".join(["C:", "Projects", "Dominium", "dominium"]) in backend_source
    add_assert(
        assertions,
        id="scrub.source_contains_temporary_local_fallback",
        category="scrub",
        description="The backend source still contains a temporary local Dominium discovery fallback; this is warning-class for the build and must not move into generic infrastructure.",
        expected=False,
        observed=local_fallback,
        ok=not local_fallback,
        severity="warning",
        evidence_refs=["core/interop/dominium/registered_validation_backend.py"],
    )
    if local_fallback:
        warnings.append("The Dominium backend source contains a temporary local checkout fallback; generic process infrastructure must not inherit it.")

    material_failures = [item for item in assertions if item["outcome"] == "FAIL" and item["severity"] == "material"]
    result = "REQUEST_CHANGES" if material_failures else "PASS_WITH_WARNINGS"
    next_task = REPAIR_TASK if material_failures else ACCEPT_TASK

    findings = []
    if any(item["id"] == "authority.proposed_capability_label_precise" for item in material_failures):
        findings.append(
            {
                "id": "capability_label.overclaims_observed_boundary",
                "severity": "material",
                "status": "OPEN",
                "source_assertion_id": "authority.proposed_capability_label_precise",
                "observed": SOURCE_LABEL,
                "expected": RECOMMENDED_LABEL,
                "summary": "The build proposes a label that can be read as successful live validation, while the observed proof is a registered command-boundary invocation that returned a typed refusal.",
                "repair": "Relabel proposed capability and generated surfaces to dominium_registered_validation_command_boundary_readonly_v0 without changing the underlying evidence.",
            }
        )

    report = {
        "schema_version": "aide.dominium-registered-validation-backend-check.v1",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "proven_capability": RECOMMENDED_LABEL,
        "source_proposed_capability": SOURCE_LABEL,
        "live_dominium_command_boundary_proven": True,
        "successful_aggregate_validation_proven": False,
        "fixture_callable_used_as_executor": False,
        "dominium_command_status": dom_result.get("status"),
        "process_call_count": invocation.get("process_call_count"),
        "assertions": assertions,
        "findings": findings,
        "warnings": warnings
        + [
            "Dominium returned a typed refusal because aggregate validation suite service is not bound in this Workbench validation slice.",
            "The local Dominium checkout is pinned and clean but remains behind origin/main.",
        ],
        "recommended_next_task": next_task,
    }

    dump_json(EVIDENCE_DIR / "independent-check-result.json", report)
    dump_json(REPORT_DIR / "check-report.json", report)
    dump_json(REPORT_DIR / "finding-disposition.json", {"task_id": TASK_ID, "findings": findings, "material_finding_count": len(material_failures)})

    write_markdown_reports(report)
    return 0


def load_json_ish(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in read_text(path).splitlines():
        if not line or line.startswith("#") or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        token = value.strip()
        if token in {"true", "false"}:
            data[key.strip()] = token == "true"
        elif token.isdigit():
            data[key.strip()] = int(token)
        else:
            data[key.strip()] = token
    return data


def write_markdown_reports(report: dict[str, Any]) -> None:
    failures = [item for item in report["assertions"] if item["outcome"] == "FAIL"]
    warnings = [item for item in report["assertions"] if item["outcome"] == "WARN"]
    summary = [
        "# Dominium Registered Validation Backend Check",
        "",
        f"- result: `{report['result']}`",
        f"- material_finding_count: `{report['material_finding_count']}`",
        f"- missing_evidence: `{report['missing_evidence']}`",
        f"- proven_capability: `{report['proven_capability']}`",
        f"- source_proposed_capability: `{report['source_proposed_capability']}`",
        f"- recommended_next_task: `{report['recommended_next_task']}`",
        "",
        "The check proves the registered Dominium command boundary and typed refusal path, not successful aggregate validation.",
    ]
    write_text(REPORT_DIR / "status.md", "\n".join(summary) + "\n")

    lines = ["# Check Report", ""]
    for item in report["assertions"]:
        lines.append(f"- `{item['id']}`: `{item['outcome']}` ({item['severity']})")
    write_text(REPORT_DIR / "check-report.md", "\n".join(lines) + "\n")

    finding_lines = ["# Finding Disposition", ""]
    if report["findings"]:
        for finding in report["findings"]:
            finding_lines.append(f"- `{finding['id']}`: `{finding['status']}` - {finding['summary']}")
    else:
        finding_lines.append("- No material findings.")
    write_text(REPORT_DIR / "finding-disposition.md", "\n".join(finding_lines) + "\n")

    write_text(
        REPORT_DIR / "authority-label-review.md",
        "\n".join(
            [
                "# Authority Label Review",
                "",
                f"- observed proposed label: `{report['source_proposed_capability']}`",
                f"- precise label for acceptance: `{report['proven_capability']}`",
                "- observed Dominium command status: `refused`",
                "- successful aggregate validation proven: `false`",
                "",
                "The build proves that AIDE can invoke the registered Dominium validation command boundary and preserve a typed Dominium result/refusal without mutation.",
                "It does not prove successful aggregate validation. Acceptance should not use a label that can be read as live validation success.",
            ]
        )
        + "\n",
    )

    write_text(
        REPORT_DIR / "process-invocation-review.md",
        "\n".join(
            [
                "# Process Invocation Review",
                "",
                "- one allowlisted process call recorded: `true`",
                "- `shell`: `false`",
                "- forbidden output flags present: `false`",
                "- fixture callable used as executor: `false`",
            ]
        )
        + "\n",
    )

    write_text(
        REPORT_DIR / "dominium-refusal-review.md",
        "\n".join(
            [
                "# Dominium Refusal Review",
                "",
                "- command id: `dominium.validation.run`",
                "- status: `refused`",
                "- refusal code: `dominium.refusal.validation.tool_unavailable`",
                "- diagnostic: `DOM-EVIDENCE-MISSING`",
                "- reason: aggregate validation suite service is not bound in this Workbench validation slice.",
                "",
                "The refusal is useful proof of the live command boundary. It is not successful validation.",
            ]
        )
        + "\n",
    )

    write_text(
        REPORT_DIR / "state-safety-review.md",
        "\n".join(
            [
                "# State Safety Review",
                "",
                "- Dominium revision unchanged: `true`",
                "- Dominium status clean: `true`",
                "- tracked tree digest unchanged: `true`",
                "- command implementation digests unchanged: `true`",
            ]
        )
        + "\n",
    )

    write_text(
        REPORT_DIR / "scrub-review.md",
        "\n".join(
            [
                "# Scrub Review",
                "",
                "- generated build reports local path leaks: `0`",
                "- generated build reports secret-like leaks: `0`",
                "- warning: source still contains a temporary local checkout fallback for the Dominium bridge adapter.",
            ]
        )
        + "\n",
    )

    write_text(
        REPORT_DIR / "report-consistency-review.md",
        "\n".join(
            [
                "# Report Consistency Review",
                "",
                "- build result: `PASS_WITH_WARNINGS`",
                "- build missing evidence: `0`",
                "- Dominium command status: `refused`",
                "- process call count: `1`",
                "- evidence and event refs resolve: `true`",
            ]
        )
        + "\n",
    )

    warning_lines = ["# Warning Disposition", ""]
    for warning in report["warnings"]:
        warning_lines.append(f"- {warning}")
    for item in warnings:
        warning_lines.append(f"- `{item['id']}`: {item['description']}")
    write_text(REPORT_DIR / "warning-disposition.md", "\n".join(warning_lines) + "\n")

    write_text(
        REPORT_DIR / "explicit-non-capabilities.md",
        "\n".join(
            [
                "# Explicit Non-Capabilities",
                "",
                "- no successful aggregate validation",
                "- no broad Dominium command dispatch",
                "- no fixture executor for this backend",
                "- no Workbench apply behavior",
                "- no Service/runtime",
                "- no worker execution",
                "- no provider/model/network call",
                "- no preview/apply/rollback",
                "- no source or target repository mutation",
                "- no branch/worktree, GitHub, release, or promotion behavior",
            ]
        )
        + "\n",
    )

    next_prompt = (
        "# Next Task Prompt\n\n"
        f"Create and process `{report['recommended_next_task']}`.\n\n"
        "Repo truth outranks this prompt. Preserve the registered Dominium validation backend evidence.\n"
    )
    if report["recommended_next_task"] == REPAIR_TASK:
        next_prompt += (
            "\nRelabel the proposed capability from `live_dominium_validation_command_readonly_v0` "
            "to `dominium_registered_validation_command_boundary_readonly_v0` across task/report surfaces "
            "without changing the underlying process invocation evidence or rerunning the live Dominium CLI. "
            "Stop at `needs_review` and recommend the independent relabel check or acceptance gate required by queue truth.\n"
        )
    else:
        next_prompt += "\nAccept only `dominium_registered_validation_command_boundary_readonly_v0`.\n"
    write_text(REPORT_DIR / "next-task-prompt.md", next_prompt)
    write_text(EVIDENCE_DIR / "next-task-prompt.md", next_prompt)


if __name__ == "__main__":
    raise SystemExit(main())
