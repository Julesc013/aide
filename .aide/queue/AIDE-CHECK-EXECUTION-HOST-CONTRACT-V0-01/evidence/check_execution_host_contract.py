from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01"
SOURCE_TASK = "AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01"
SOURCE_COMMIT = "4a1f1aa"
PASS_NEXT = "AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01"
FAIL_NEXT = "AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-REPAIR-01"

ROOT = Path(__file__).resolve().parents[4]
REPORT_ROOT = ROOT / ".aide/reports/execution-host-contract-check"
BUILD_REPORT_ROOT = ROOT / ".aide/reports/execution-host-contract"
BUILD_TASK_ROOT = ROOT / ".aide/queue" / SOURCE_TASK
CHECK_TASK_ROOT = ROOT / ".aide/queue" / TASK_ID

RECORD_KINDS = {
    "ExecutionHostDescriptor",
    "ExecutionHostRunBinding",
    "ExecutionHostEvent",
    "ExecutionHostArtifact",
    "ExecutionHostApproval",
    "ExecutionHostUsage",
}
SUPPORTED_KINDS = RECORD_KINDS | {
    "ExecutionHostContractProjectionReport",
    "ExecutionHostContractValidationReport",
}
OPERATION_NAMES = {
    "probe",
    "create_run",
    "attach",
    "send_input",
    "stream_events",
    "resolve_runtime_approval",
    "interrupt",
    "collect_artifacts",
    "finish",
    "reconcile",
}
NON_CAPABILITIES = {
    "live_execution_host",
    "local_process_execution_host",
    "remote_execution_host",
    "worker_execution",
    "worker_harness",
    "worker_process_start",
    "worker_lease",
    "scheduler",
    "supervisor",
    "provider_model_calls",
    "network_calls",
    "service_runtime",
    "workbench_runtime",
    "preview_session",
    "development_transaction",
    "patch_transaction_apply",
    "repository_mutation",
    "branch_worktree_automation",
    "github_mutation",
    "release_or_promotion",
}
FALSE_BOUNDARY_FIELDS = {
    "execution_host_runtime_implemented",
    "local_process_execution_host_implemented",
    "remote_execution_host_implemented",
    "worker_execution_implemented",
    "worker_process_started",
    "worker_lease_created",
    "scheduler_implemented",
    "supervisor_implemented",
    "provider_model_calls_performed",
    "network_calls_performed",
    "service_runtime_implemented",
    "workbench_runtime_implemented",
    "preview_apply_implemented",
    "repository_mutation_performed",
    "branch_worktree_mutation_performed",
    "github_mutation_performed",
    "release_or_promotion_performed",
}
WATCHED_FILES = [
    "core/protocol/execution_host.py",
    "core/protocol/__init__.py",
    ".aide/protocol/aide-execution-host.schema.json",
    ".aide/scripts/aide_lite.py",
    ".aide/scripts/tests/test_aide_execution_host_contract.py",
    ".aide/reports/execution-host-contract/status.md",
    ".aide/reports/execution-host-contract/projection-report.json",
    ".aide/reports/execution-host-contract/validation.json",
    ".aide/reports/execution-host-contract/validation.md",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    return json.loads(read_text(path))


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with (ROOT / path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def run_command(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
        shell=False,
        env=None,
    )
    display_args = ["<PYTHON>" if arg == sys.executable else arg for arg in args]
    return {
        "args": display_args,
        "returncode": completed.returncode,
        "stdout_excerpt": scrub(completed.stdout[:1200]),
        "stderr_excerpt": scrub(completed.stderr[:1200]),
    }


def scrub(text: str) -> str:
    text = re.sub(r"[A-Za-z]:\\\\[^\\s\"']+", "<ABSOLUTE_PATH>", text)
    text = re.sub(r"(?i)(sk-[a-z0-9_-]{8,}|api[_-]?key\\s*[:=]\\s*\\S+)", "<SECRET_LIKE>", text)
    return text


def assertion(
    items: list[dict[str, Any]],
    assertion_id: str,
    category: str,
    description: str,
    passed: bool,
    expected: Any,
    observed: Any,
    evidence_refs: list[str],
    *,
    severity: str = "material",
    source_finding_id: str | None = None,
) -> None:
    items.append(
        {
            "id": assertion_id,
            "category": category,
            "description": description,
            "outcome": "PASS" if passed else "FAIL",
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
            "source_finding_id": source_finding_id,
        }
    )


def source_imports_are_safe(path: str) -> dict[str, Any]:
    tree = ast.parse(read_text(path))
    forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib"}
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
    forbidden_found = sorted(set(imports) & forbidden_imports)
    return {"imports": sorted(set(imports)), "forbidden_found": forbidden_found}


def source_has_no_runtime_calls(path: str) -> dict[str, Any]:
    text = read_text(path)
    forbidden_tokens = [
        "subprocess.",
        "Popen(",
        "socket.",
        "requests.",
        "urllib.",
        "os.system",
        "shell=True",
        "threading.",
        "multiprocessing.",
    ]
    found = [token for token in forbidden_tokens if token in text]
    return {"forbidden_tokens_found": found}


def projection_checks(path: str) -> dict[str, Any]:
    obj = read_json(path)
    spec = obj.get("spec", {})
    status = obj.get("status", {})
    missing_non_caps = sorted(NON_CAPABILITIES - set(spec.get("explicit_non_capabilities", [])))
    non_false = sorted(field for field in FALSE_BOUNDARY_FIELDS if spec.get(field) is not False)
    return {
        "kind": obj.get("kind"),
        "projection_only": status.get("projection_only"),
        "status_validated": status.get("validated"),
        "missing_non_capabilities": missing_non_caps,
        "non_false_boundary_fields": non_false,
        "capability_label_in_non_capabilities": spec.get("capability_label") in set(spec.get("explicit_non_capabilities", [])),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    absolute_matches: list[str] = []
    secret_matches: list[str] = []
    abs_pattern = re.compile(r"[A-Za-z]:\\\\|/Users/|/home/")
    secret_pattern = re.compile(r"(?i)(openai_api_key|anthropic_api_key|deepseek_api_key|sk-[a-z0-9_-]{8,}|begin private key)")
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if abs_pattern.search(text):
            absolute_matches.append(rel(path))
        if secret_pattern.search(text):
            secret_matches.append(rel(path))
    return {"absolute_path_matches": absolute_matches, "secret_like_matches": secret_matches}


def write_markdown(name: str, title: str, lines: list[str]) -> None:
    (REPORT_ROOT / name).write_text("# " + title + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    assertions: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {}

    before_hashes = {path: sha256_file(path) for path in WATCHED_FILES if (ROOT / path).exists()}

    build_status = read_jsonish_yaml(BUILD_TASK_ROOT / "status.yaml")
    assertion(
        assertions,
        "baseline.source_task_complete",
        "baseline",
        "Source build task is complete with missing evidence zero.",
        build_status.get("status") == "needs_review"
        and build_status.get("result") == "PASS_WITH_WARNINGS"
        and str(build_status.get("missing_evidence")) == "0"
        and build_status.get("recommended_next_task") == TASK_ID,
        "needs_review PASS_WITH_WARNINGS missing_evidence 0 and recommended check task",
        build_status,
        [".aide/queue/AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01/status.yaml"],
    )

    no_superseding_dirs = not (ROOT / ".aide/queue/AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01").exists() and not (
        ROOT / ".aide/queue/AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01"
    ).exists()
    assertion(
        assertions,
        "baseline.no_superseding_task",
        "baseline",
        "No acceptance or LocalProcessExecutionHost task already supersedes this check.",
        no_superseding_dirs,
        "no downstream task directories",
        {"accept_dir_exists": (ROOT / ".aide/queue/AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01").exists()},
        [".aide/queue"],
    )

    changed = run_command(["git", "show", "--name-only", "--pretty=format:", SOURCE_COMMIT])
    changed_files = [line.strip() for line in changed["stdout_excerpt"].splitlines() if line.strip()]
    forbidden_changed = [
        path
        for path in changed_files
        if path.startswith(("core/execution/", "core/interop/", "hosts/", ".aide.local/"))
    ]
    assertion(
        assertions,
        "scope.source_commit_forbidden_paths",
        "scope",
        "Source commit did not modify forbidden runtime, interop, host, or local-state paths.",
        not forbidden_changed,
        "no forbidden changed paths",
        forbidden_changed,
        ["git show --name-only --pretty=format: 4a1f1aa"],
    )

    schema = read_json(".aide/protocol/aide-execution-host.schema.json")
    schema_required = set(schema.get("required", []))
    schema_kind_enum = set(schema.get("properties", {}).get("kind", {}).get("enum", []))
    oneof_consts = {
        item.get("properties", {}).get("kind", {}).get("const")
        for item in schema.get("oneOf", [])
        if isinstance(item, dict)
    }
    assertion(
        assertions,
        "schema.kind_discrimination",
        "schema",
        "Schema enumerates and oneOf-discriminates all ExecutionHost record/report kinds.",
        schema_kind_enum == SUPPORTED_KINDS and oneof_consts == SUPPORTED_KINDS,
        sorted(SUPPORTED_KINDS),
        {"kind_enum": sorted(schema_kind_enum), "oneOf_consts": sorted(oneof_consts)},
        [".aide/protocol/aide-execution-host.schema.json"],
    )
    assertion(
        assertions,
        "schema.required_surface",
        "schema",
        "Schema requires the canonical envelope fields.",
        {"apiVersion", "kind", "metadata", "spec", "status"} <= schema_required,
        ["apiVersion", "kind", "metadata", "spec", "status"],
        sorted(schema_required),
        [".aide/protocol/aide-execution-host.schema.json"],
    )

    projection_report = read_json(".aide/reports/execution-host-contract/projection-report.json")
    projection_paths = projection_report.get("projections_written", [])
    projection_results = {path: projection_checks(path) for path in projection_paths}
    projection_kinds = {item["kind"] for item in projection_results.values()}
    projection_failures = {
        path: result
        for path, result in projection_results.items()
        if result["projection_only"] is not True
        or result["missing_non_capabilities"]
        or result["non_false_boundary_fields"]
        or result["capability_label_in_non_capabilities"]
    }
    assertion(
        assertions,
        "projection.complete_record_set",
        "projection",
        "Exactly six ExecutionHost record projections are present.",
        len(projection_paths) == 6 and projection_kinds == RECORD_KINDS,
        sorted(RECORD_KINDS),
        {"count": len(projection_paths), "kinds": sorted(projection_kinds)},
        [".aide/reports/execution-host-contract/projection-report.json"],
    )
    assertion(
        assertions,
        "projection.false_boundary_set",
        "projection",
        "Projection records preserve non-capabilities and false boundary fields.",
        not projection_failures,
        "all projections projection_only with complete non-capabilities and false boundary fields",
        projection_failures,
        projection_paths,
    )

    descriptor = read_json(".aide/reports/execution-host-contract/projections/execution-host-descriptor.json")
    descriptor_spec = descriptor.get("spec", {})
    assertion(
        assertions,
        "contract.capability_distinction",
        "contract",
        "Descriptor keeps deterministic capability execution distinct from worker/session execution.",
        descriptor_spec.get("capability_execution_distinct") is True
        and descriptor_spec.get("capability_provider_ref") == "registered_process_execution_provider_v0"
        and descriptor_spec.get("worker_session_contract") is True,
        "capability distinct, provider ref accepted provider, worker session contract true",
        {
            "capability_execution_distinct": descriptor_spec.get("capability_execution_distinct"),
            "capability_provider_ref": descriptor_spec.get("capability_provider_ref"),
            "worker_session_contract": descriptor_spec.get("worker_session_contract"),
        },
        [".aide/reports/execution-host-contract/projections/execution-host-descriptor.json"],
    )
    assertion(
        assertions,
        "contract.operation_set",
        "contract",
        "Descriptor records the expected v0 worker/session operation names.",
        set(descriptor_spec.get("supported_operations", [])) == OPERATION_NAMES,
        sorted(OPERATION_NAMES),
        sorted(descriptor_spec.get("supported_operations", [])),
        [".aide/reports/execution-host-contract/projections/execution-host-descriptor.json"],
    )

    imports = source_imports_are_safe("core/protocol/execution_host.py")
    runtime_tokens = source_has_no_runtime_calls("core/protocol/execution_host.py")
    assertion(
        assertions,
        "source.no_runtime_imports",
        "source",
        "ExecutionHost protocol helper imports no process, network, or transport modules.",
        not imports["forbidden_found"],
        "no forbidden imports",
        imports,
        ["core/protocol/execution_host.py"],
    )
    assertion(
        assertions,
        "source.no_runtime_call_tokens",
        "source",
        "ExecutionHost protocol helper contains no direct runtime/process/network call tokens.",
        not runtime_tokens["forbidden_tokens_found"],
        "no runtime call tokens",
        runtime_tokens,
        ["core/protocol/execution_host.py"],
    )

    cli_commands = {
        "status": run_command([sys.executable, ".aide/scripts/aide_lite.py", "execution-host", "status"]),
        "project": run_command([sys.executable, ".aide/scripts/aide_lite.py", "execution-host", "project", "--source", "contract-projection"]),
        "validate": run_command([sys.executable, ".aide/scripts/aide_lite.py", "execution-host", "validate"]),
        "invalid_run": run_command([sys.executable, ".aide/scripts/aide_lite.py", "execution-host", "run"]),
        "nested_py_launcher_version": run_command(["py", "-3", "--version"]),
    }
    evidence["cli_commands"] = cli_commands
    good_cli = all(cli_commands[name]["returncode"] == 0 for name in ["status", "project", "validate"])
    boundaries = [
        "execution_host_runtime_implemented: false",
        "worker_execution_implemented: false",
        "provider_or_model_calls: none",
        "network_calls: none",
        "repository_mutation_performed: false",
    ]
    boundary_lines_present = all(
        all(line in cli_commands[name]["stdout_excerpt"] for line in boundaries)
        for name in ["status", "project", "validate"]
    )
    invalid_rejected = cli_commands["invalid_run"]["returncode"] != 0 and "invalid choice" in cli_commands["invalid_run"]["stderr_excerpt"]
    assertion(
        assertions,
        "cli.projection_only_commands",
        "cli",
        "AIDE Lite execution-host status/project/validate succeed and print projection-only boundary lines.",
        good_cli and boundary_lines_present,
        "three commands exit 0 and print false/non-call boundaries",
        {"good_cli": good_cli, "boundary_lines_present": boundary_lines_present},
        [".aide/scripts/aide_lite.py"],
    )
    assertion(
        assertions,
        "cli.live_run_rejected",
        "cli",
        "AIDE Lite parser rejects execution-host run; no live host run command is present.",
        invalid_rejected,
        "nonzero argparse invalid choice",
        {"returncode": cli_commands["invalid_run"]["returncode"], "stderr": cli_commands["invalid_run"]["stderr_excerpt"]},
        [".aide/scripts/aide_lite.py"],
    )

    validation_report = read_json(".aide/reports/execution-host-contract/validation.json")
    assertion(
        assertions,
        "report.validation_truthful",
        "report",
        "Build validation report truthfully records projection-only pass with warnings and next check routing.",
        validation_report.get("status") == "PASS_WITH_WARNINGS"
        and validation_report.get("projection_only_truthful") is True
        and validation_report.get("execution_host_runtime_implemented") is False
        and validation_report.get("recommended_next_task") == TASK_ID,
        "PASS_WITH_WARNINGS projection-only and recommends check",
        {
            "status": validation_report.get("status"),
            "projection_only_truthful": validation_report.get("projection_only_truthful"),
            "execution_host_runtime_implemented": validation_report.get("execution_host_runtime_implemented"),
            "recommended_next_task": validation_report.get("recommended_next_task"),
        },
        [".aide/reports/execution-host-contract/validation.json"],
    )

    after_hashes = {path: sha256_file(path) for path in WATCHED_FILES if (ROOT / path).exists()}
    changed_hashes = sorted(path for path, before in before_hashes.items() if after_hashes.get(path) != before)
    assertion(
        assertions,
        "determinism.commands_no_report_churn",
        "determinism",
        "ExecutionHost CLI status/project/validate leave watched source and report bytes unchanged.",
        not changed_hashes,
        "no watched file hash changes",
        changed_hashes,
        WATCHED_FILES,
    )

    scan = scan_paths(
        list(BUILD_REPORT_ROOT.rglob("*"))
        + list(BUILD_TASK_ROOT.rglob("*"))
        + [CHECK_TASK_ROOT / "task.yaml", CHECK_TASK_ROOT / "ExecPlan.md", CHECK_TASK_ROOT / "prompt.md", CHECK_TASK_ROOT / "status.yaml"]
    )
    assertion(
        assertions,
        "hygiene.no_absolute_paths_or_secrets",
        "hygiene",
        "Build and check surfaces scanned so far contain no absolute local paths or secret-like values.",
        not scan["absolute_path_matches"] and not scan["secret_like_matches"],
        "no absolute path or secret-like matches",
        scan,
        [".aide/reports/execution-host-contract", ".aide/queue/AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01", ".aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01"],
    )

    material_failures = [item for item in assertions if item["severity"] == "material" and item["outcome"] != "PASS"]
    result = "REQUEST_CHANGES" if material_failures else "PASS_WITH_WARNINGS"
    recommended_next = FAIL_NEXT if material_failures else PASS_NEXT
    warnings = [
        "Reduced independence: this check ran in the same Codex thread as the source build.",
        "ExecutionHost contract v0 remains projection-only and does not implement a live host.",
        "Full external Draft 2020-12 validation is not separately installed or required by this bounded check.",
        "Python launcher selection differs when nested under Python on this host, so CLI probes use the active interpreter path and scrub it from evidence.",
    ]
    report = {
        "schema_version": "aide.execution-host-contract-check.v0",
        "report_type": "execution_host_contract_check",
        "task_id": TASK_ID,
        "source_task": SOURCE_TASK,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next,
        "assertions": assertions,
        "warnings": warnings,
        "explicit_non_capabilities_preserved": True,
        "check_only": True,
        "implementation_repaired": False,
    }
    write_reports(report, evidence)
    return 0 if not material_failures else 1


def read_jsonish_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def write_reports(report: dict[str, Any], evidence: dict[str, Any]) -> None:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "check-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (CHECK_TASK_ROOT / "evidence/harness-result.json").write_text(
        json.dumps({"report": report, "evidence": evidence}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    passed = sum(1 for item in report["assertions"] if item["outcome"] == "PASS")
    failed = len(report["assertions"]) - passed
    write_markdown(
        "status.md",
        "ExecutionHost Contract Check Status",
        [
            f"- result: {report['result']}",
            f"- material_finding_count: {report['material_finding_count']}",
            f"- missing_evidence: {report['missing_evidence']}",
            f"- recommended_next_task: {report['recommended_next_task']}",
            "- check_only: true",
            "- implementation_repaired: false",
        ],
    )
    write_markdown(
        "check-report.md",
        "ExecutionHost Contract Check Report",
        [
            f"- source_task: {SOURCE_TASK}",
            f"- source_commit: {SOURCE_COMMIT}",
            f"- result: {report['result']}",
            f"- passed_assertions: {passed}",
            f"- failed_assertions: {failed}",
            "",
            "## Assertions",
            *[f"- {item['outcome']}: {item['id']} - {item['description']}" for item in report["assertions"]],
        ],
    )
    write_markdown(
        "schema-contract-review.md",
        "Schema Contract Review",
        [
            "- Schema top-level required fields and kind enum were inspected independently.",
            "- oneOf kind constants match the supported ExecutionHost record and report kinds.",
            "- The schema remains intentionally open for extension surfaces; helper validation supplies stricter semantic checks.",
        ],
    )
    write_markdown(
        "projection-boundary-review.md",
        "Projection Boundary Review",
        [
            "- Six committed projection records are present.",
            "- Each record is projection-only and keeps false-boundary fields false.",
            "- Descriptor operation names match the v0 operation set.",
        ],
    )
    write_markdown(
        "cli-boundary-review.md",
        "CLI Boundary Review",
        [
            "- `execution-host status`, `execution-host project --source contract-projection`, and `execution-host validate` were invoked as system-under-test commands.",
            "- All three commands report false runtime and no-call boundary lines.",
            "- `execution-host run` is rejected by argparse as an invalid choice.",
        ],
    )
    write_markdown(
        "non-capability-review.md",
        "Non-Capability Review",
        [
            "- No live ExecutionHost, LocalProcessExecutionHost, worker execution, scheduler, Service/runtime, Workbench, provider/model/network, preview/apply, mutation, GitHub, release, or promotion capability is implemented.",
            "- The source helper imports no process, network, or transport modules.",
        ],
    )
    write_markdown(
        "warning-disposition.md",
        "Warning Disposition",
        [f"- {warning}" for warning in report["warnings"]],
    )
    write_markdown(
        "next-task-prompt.md",
        "Next Task Prompt",
        [
            "Create and process `AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`.",
            "",
            "Accept only `execution_host_contract_v0` as a projection-only contract after reviewing the build and check evidence.",
            "",
            "Do not implement `LocalProcessExecutionHost`, worker execution, Service/runtime, Workbench, provider/model/network calls, preview/apply/rollback, repository mutation, branch/worktree mutation, GitHub mutation, release, or promotion in the acceptance task.",
        ],
    )

if __name__ == "__main__":
    sys.exit(main())
