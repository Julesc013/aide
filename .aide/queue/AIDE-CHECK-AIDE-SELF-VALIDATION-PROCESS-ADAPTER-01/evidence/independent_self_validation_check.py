from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01"
SOURCE_TASK_ID = "AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01"
SOURCE_COMMIT = "d9cb3df8dbb9274b618956d6069666f4f4274528"
PASS_NEXT = "AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01"
FAIL_NEXT = "AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-REPAIR-01"
REPORT_ROOT = Path(".aide/reports/aide-self-validation-process-adapter-check")
EVIDENCE_ROOT = Path(".aide/queue/AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01/evidence")
BUILD_REPORT_ROOT = Path(".aide/reports/aide-self-validation-process-adapter")
BUILD_TASK_ROOT = Path(".aide/queue/AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01")


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def scrub(text: str, repo_root: Path) -> str:
    result = text.replace(str(repo_root), "<aide-root>").replace(str(repo_root).replace("\\", "/"), "<aide-root>")
    drive_pattern = r"(?<![A-Za-z0-9])" + r"[A-Za-z]" + r":" + r"[\\/]" + r"[^\s\"'\],}]+"
    result = re.sub(drive_pattern, "<absolute-path>", result)
    secret_prefixes = "(sk|ghp|github_pat|xox[baprs]?)"
    result = re.sub(r"(?i)\b" + secret_prefixes + r"-[A-Za-z0-9_\-]{8,}", "<secret-like-redacted>", result)
    return result


def run(repo_root: Path, args: list[str], timeout: int = 120) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        shell=False,
        timeout=timeout,
        check=False,
    )
    return {
        "argv": [scrub(str(arg), repo_root) for arg in args],
        "returncode": completed.returncode,
        "stdout_sha256": sha256_text(completed.stdout),
        "stderr_sha256": sha256_text(completed.stderr),
        "stdout_excerpt": scrub(completed.stdout[:1200], repo_root),
        "stderr_excerpt": scrub(completed.stderr[:1200], repo_root),
    }


def git(repo_root: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        shell=False,
        check=True,
    )
    return completed.stdout


def add_assertion(
    assertions: list[dict[str, Any]],
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
        {
            "id": assertion_id,
            "category": category,
            "description": description,
            "outcome": "PASS" if condition else "FAIL",
            "severity": severity,
            "expected": expected,
            "observed": observed,
            "evidence_refs": evidence_refs,
        }
    )


def write_fixture_file(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def fixture_git(root: Path, *args: str) -> str:
    completed = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def create_aide_fixture(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(root)], capture_output=True, text=True, check=True)
    fixture_git(root, "config", "user.email", "aide-check@example.invalid")
    fixture_git(root, "config", "user.name", "AIDE Check")
    write_fixture_file(root, ".aide/scripts/aide_lite.py", "print('AIDE Lite validate')\nprint('status: PASS')\n")
    fixture_git(root, "add", ".")
    fixture_git(root, "commit", "-m", "fixture: add aide lite validate")
    return fixture_git(root, "rev-parse", "HEAD")


class FakeRunner:
    def __init__(self, stdout: str = "AIDE Lite validate\nstatus: PASS\n", returncode: int = 0):
        self.stdout = stdout
        self.stderr = ""
        self.returncode = returncode
        self.calls: list[dict[str, Any]] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append({"argv": list(argv), "cwd": str(cwd), "env_keys": sorted(env), "timeout": timeout, "shell": False})
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


def normalize_fake_calls(calls: list[dict[str, Any]], fixture_root: Path, python_executable: str) -> list[dict[str, Any]]:
    fixture_root_text = str(fixture_root)
    fixture_root_posix = fixture_root_text.replace("\\", "/")
    python_text = str(Path(python_executable).resolve())
    python_posix = python_text.replace("\\", "/")
    normalized: list[dict[str, Any]] = []
    for call in calls:
        argv = [str(item) for item in call.get("argv", [])]
        argv_normalized: list[str] = []
        for item in argv:
            item_posix = item.replace("\\", "/")
            if item == python_text or item_posix == python_posix:
                argv_normalized.append("<python>")
            else:
                argv_normalized.append(item.replace(fixture_root_text, "<fixture-root>").replace(fixture_root_posix, "<fixture-root>"))
        cwd = str(call.get("cwd", ""))
        normalized.append(
            {
                "argv": argv_normalized,
                "cwd": cwd.replace(fixture_root_text, "<fixture-root>").replace(fixture_root_posix, "<fixture-root>"),
                "env_keys": list(call.get("env_keys", [])),
                "timeout": call.get("timeout"),
                "shell": call.get("shell"),
            }
        )
    return normalized


def call_matches_aide_validate(calls: list[dict[str, Any]], fixture_root: Path, python_executable: str) -> bool:
    if len(calls) != 1:
        return False
    argv = [str(item) for item in calls[0].get("argv", [])]
    expected = [
        str(Path(python_executable).resolve()),
        str((fixture_root / ".aide/scripts/aide_lite.py").resolve()),
        "validate",
    ]
    return argv == expected and calls[0].get("shell") is False


def run_fake_runner_checks(repo_root: Path) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from core.interop.aide import self_validation_process_adapter as adapter
    from core.execution.registered_process import RegisteredProcessExecutionProvider, RegisteredProcessSpec
    from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation

    results: dict[str, Any] = {}
    with tempfile.TemporaryDirectory() as tmp:
        fixture_root = Path(tmp) / "aide"
        revision = create_aide_fixture(fixture_root)
        fake = FakeRunner()
        success = adapter.run_adapter(fixture_root, expected_revision=revision, python_executable=sys.executable, runner=fake, write_reports=False)
        results["success"] = {
            "process_call_count": success.get("process_call_count"),
            "result": success.get("result"),
            "call_count": len(fake.calls),
            "argv_matches": call_matches_aide_validate(fake.calls, fixture_root, sys.executable),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        fake = FakeRunner()
        unsupported = adapter.run_adapter(
            fixture_root,
            expected_revision=revision,
            capability_id="aide.future.unsupported",
            python_executable=sys.executable,
            runner=fake,
            write_reports=False,
        )
        results["unsupported"] = {
            "process_call_count": unsupported.get("process_call_count"),
            "reason_code": unsupported.get("reason_code"),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        fake = FakeRunner()
        wrong_revision = adapter.run_adapter(fixture_root, expected_revision="0" * 40, python_executable=sys.executable, runner=fake, write_reports=False)
        results["wrong_revision"] = {
            "process_call_count": wrong_revision.get("process_call_count"),
            "reason_code": wrong_revision.get("reason_code"),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        fake = FakeRunner()
        missing_workspace = adapter.run_adapter(fixture_root / "missing", expected_revision=revision, python_executable=sys.executable, runner=fake, write_reports=False)
        results["missing_workspace"] = {
            "process_call_count": missing_workspace.get("process_call_count"),
            "reason_code": missing_workspace.get("reason_code"),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        fake = FakeRunner()
        missing_executable = adapter.run_adapter(
            fixture_root,
            expected_revision=revision,
            python_executable=fixture_root / "missing-python.exe",
            runner=fake,
            write_reports=False,
        )
        results["missing_executable"] = {
            "process_call_count": missing_executable.get("process_call_count"),
            "reason_code": missing_executable.get("reason_code"),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        fake = FakeRunner()
        digest_mismatch = adapter.run_adapter(
            fixture_root,
            expected_revision=revision,
            python_executable=sys.executable,
            expected_digests={adapter.AIDE_VALIDATE_SCRIPT_REL.as_posix(): "sha256:not-real"},
            runner=fake,
            write_reports=False,
        )
        results["digest_mismatch"] = {
            "process_call_count": digest_mismatch.get("process_call_count"),
            "reason_code": digest_mismatch.get("reason_code"),
            "calls": normalize_fake_calls(fake.calls, fixture_root, sys.executable),
        }

        provider_fake = FakeRunner(stdout='{"status": "ok"}')
        tool = fixture_root / "tool.py"
        tool.write_text("print('ok')\n", encoding="utf-8")
        spec = RegisteredProcessSpec(
            capability_ref="aide://capability/check",
            executable=str(tool),
            argument_plan=[ArgumentToken("literal", "--check")],
            working_directory=str(fixture_root),
            timeout_seconds=5,
            environment={"PYTHONHASHSEED": "0"},
            decoder_id="json_object_decoder_v0",
            state_probe_id="static",
            mutation_policy="none_detected_within_probe_coverage",
            scrubber_id="identity_stream_scrubber_v0",
            provider_spec_ref="aide://provider-spec/check",
        )
        receipt, outcome = RegisteredProcessExecutionProvider(runner=provider_fake).execute(
            CapabilityInvocation("aide://invocation/check", "aide://capability/check"),
            CapabilityBinding(
                capability_ref="aide://capability/different",
                provider_id=RegisteredProcessExecutionProvider.provider_id,
                provider_spec_ref=spec.provider_spec_ref,
                provider_spec=spec,
            ),
        )
        results["invalid_binding"] = {
            "process_call_count": receipt.launcher_call_count,
            "reason_code": outcome.reason_code,
            "calls": normalize_fake_calls(provider_fake.calls, fixture_root, sys.executable),
        }
    return results


def source_scan(repo_root: Path) -> dict[str, Any]:
    adapter_text = (repo_root / "core/interop/aide/self_validation_process_adapter.py").read_text(encoding="utf-8")
    aide_lite_text = (repo_root / ".aide/scripts/aide_lite.py").read_text(encoding="utf-8")
    allowed_domain_reference_fragments = [
        "dominium_adapter_mutation",
        "eureka_adapter",
        "core/interop/dominium/**",
        '"Dominium"',
        "Eureka reuse proof",
        "Eureka or another second external domain proof",
        "AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01",
    ]
    domain_reference_findings: list[dict[str, Any]] = []
    for lineno, line in enumerate(adapter_text.splitlines(), start=1):
        lowered = line.lower()
        if "dominium" not in lowered and "eureka" not in lowered:
            continue
        if any(fragment in line for fragment in allowed_domain_reference_fragments):
            continue
        domain_reference_findings.append({"line": lineno, "text": line.strip()})
    return {
        "adapter_contains_provider_use": "RegisteredProcessExecutionProvider(" in adapter_text,
        "adapter_defines_provider": "class RegisteredProcessExecutionProvider" in adapter_text,
        "adapter_shell_true": "shell=True" in adapter_text,
        "adapter_mentions_dominium": "dominium" in adapter_text.lower().replace("dominium_adapter_mutation", ""),
        "adapter_mentions_eureka": "eureka" in adapter_text.lower().replace("eureka_adapter", ""),
        "domain_behavior_reference_findings": domain_reference_findings,
        "aide_lite_has_adapter_command": "aide-self-validation-process-adapter" in aide_lite_text,
        "aide_lite_validate_dispatch_mentions_adapter_run": "aide-self-validation-process-adapter run" in aide_lite_text,
    }


def scan_for_leaks(repo_root: Path, paths: list[Path]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    drive_pattern = re.compile(r"(?<![A-Za-z0-9])" + r"[A-Za-z]" + r":" + r"[\\/]" + r"[^\s\"']+")
    secret_pattern = re.compile(r"(?i)\b" + r"(sk|ghp|github_pat|xox[baprs]?)" + r"-[A-Za-z0-9_\-]{8,}")
    for root in paths:
        base = repo_root / root
        if not base.exists():
            continue
        files = [base] if base.is_file() else [item for item in base.rglob("*") if item.is_file()]
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            if drive_pattern.search(text):
                findings.append({"path": path.relative_to(repo_root).as_posix(), "kind": "absolute_path"})
            if secret_pattern.search(text):
                findings.append({"path": path.relative_to(repo_root).as_posix(), "kind": "secret_like"})
    return findings


def main() -> int:
    repo_root = Path.cwd()
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    assertions: list[dict[str, Any]] = []

    head = git(repo_root, ["rev-parse", "HEAD"]).strip()
    add_assertion(
        assertions,
        assertion_id="baseline.head_is_source_commit",
        category="baseline",
        description="Check starts from the source build commit.",
        condition=head == SOURCE_COMMIT,
        expected=SOURCE_COMMIT,
        observed=head,
        evidence_refs=["git rev-parse HEAD"],
    )

    changed_files = git(repo_root, ["diff-tree", "--no-commit-id", "--name-only", "-r", SOURCE_COMMIT]).splitlines()
    provider_changed = any(path in {"core/execution/registered_process.py", "core/protocol/process_invocation.py", "core/protocol/execution_receipt.py"} for path in changed_files)
    add_assertion(
        assertions,
        assertion_id="source.provider_core_not_changed",
        category="source",
        description="Source build did not change generic provider or neutral receipt/invocation protocol files.",
        condition=not provider_changed,
        expected="no provider/protocol core files in source build diff",
        observed=changed_files,
        evidence_refs=["git diff-tree d9cb3df"],
    )

    build_status = (repo_root / BUILD_TASK_ROOT / "status.yaml").read_text(encoding="utf-8")
    add_assertion(
        assertions,
        assertion_id="baseline.source_status_pass_with_warnings",
        category="baseline",
        description="Source build status records PASS_WITH_WARNINGS, missing_evidence 0, and provider proposed/unaccepted.",
        condition=("result: PASS_WITH_WARNINGS" in build_status and "missing_evidence: 0" in build_status and "provider_status: proposed_unaccepted" in build_status),
        expected="PASS_WITH_WARNINGS, missing_evidence 0, provider proposed_unaccepted",
        observed=build_status,
        evidence_refs=[(BUILD_TASK_ROOT / "status.yaml").as_posix()],
    )

    validation = read_json(repo_root / BUILD_REPORT_ROOT / "validation.json")
    invocation_result = read_json(repo_root / BUILD_REPORT_ROOT / "invocation-result.json")
    receipt = read_json(repo_root / BUILD_REPORT_ROOT / "execution-receipt.json")
    outcome = read_json(repo_root / BUILD_REPORT_ROOT / "capability-outcome.json")
    capability = read_json(repo_root / BUILD_REPORT_ROOT / "capability-descriptor.json")
    projection = read_json(repo_root / BUILD_REPORT_ROOT / "projection.json")

    add_assertion(
        assertions,
        assertion_id="report.validation_clean",
        category="report",
        description="Source build validation report is internally clean.",
        condition=validation.get("validation_status") == "PASS_WITH_WARNINGS" and validation.get("missing_evidence") == 0 and validation.get("validation_errors") == [],
        expected={"validation_status": "PASS_WITH_WARNINGS", "missing_evidence": 0, "validation_errors": []},
        observed=validation,
        evidence_refs=[(BUILD_REPORT_ROOT / "validation.json").as_posix()],
    )

    scan = source_scan(repo_root)
    add_assertion(
        assertions,
        assertion_id="source.adapter_uses_provider_without_defining_provider",
        category="source",
        description="Adapter uses RegisteredProcessExecutionProvider and does not define or fork it.",
        condition=scan["adapter_contains_provider_use"] and not scan["adapter_defines_provider"],
        expected="uses provider, does not define provider",
        observed=scan,
        evidence_refs=["core/interop/aide/self_validation_process_adapter.py"],
    )
    add_assertion(
        assertions,
        assertion_id="source.adapter_aide_specific",
        category="source",
        description="Adapter source is AIDE-specific and has no Dominium or Eureka behavior branches.",
        condition=scan["domain_behavior_reference_findings"] == [],
        expected="no Dominium/Eureka behavior references outside explicit non-capability names",
        observed=scan,
        evidence_refs=["core/interop/aide/self_validation_process_adapter.py"],
    )
    add_assertion(
        assertions,
        assertion_id="source.no_shell_true",
        category="source",
        description="Adapter source does not enable shell=True.",
        condition=not scan["adapter_shell_true"],
        expected=False,
        observed=scan["adapter_shell_true"],
        evidence_refs=["core/interop/aide/self_validation_process_adapter.py"],
    )

    add_assertion(
        assertions,
        assertion_id="process.exact_argv_shell_false",
        category="process",
        description="Committed receipt records exact allowlisted AIDE Lite validate argv and shell false.",
        condition=receipt.get("launcher_call_count") == 1
        and receipt.get("shell") is False
        and receipt.get("return_code") == 0
        and (receipt.get("metadata", {}).get("launch", {}).get("argv", [])[-2:] == ["<aide-root>\\.aide\\scripts\\aide_lite.py", "validate"]),
        expected={"launcher_call_count": 1, "shell": False, "argv_suffix": ["<aide-root>\\.aide\\scripts\\aide_lite.py", "validate"]},
        observed=receipt,
        evidence_refs=[(BUILD_REPORT_ROOT / "execution-receipt.json").as_posix()],
    )

    add_assertion(
        assertions,
        assertion_id="process.axes_separated",
        category="process",
        description="Transport, process, decoder, domain, validation, and evidence axes remain distinct.",
        condition=outcome.get("transport_outcome") == "transport_started"
        and outcome.get("process_outcome") == "exit_zero"
        and outcome.get("decoder_outcome") == "decoded"
        and outcome.get("domain_outcome") == "typed_result"
        and outcome.get("validation_outcome") == "complete"
        and outcome.get("evidence_completeness") == "complete",
        expected="started/exit_zero/decoded/typed_result/complete/complete",
        observed=outcome,
        evidence_refs=[(BUILD_REPORT_ROOT / "capability-outcome.json").as_posix()],
    )

    add_assertion(
        assertions,
        assertion_id="result.stdout_origin",
        category="result",
        description="Successful outcome originates from AIDE Lite validate stdout, not constructed success.",
        condition=invocation_result.get("result_origin") == "aide_lite_validate_stdout"
        and invocation_result.get("constructed_success_result") is False
        and invocation_result.get("aide_validate_result", {}).get("status") == "PASS",
        expected={"origin": "aide_lite_validate_stdout", "constructed_success_result": False, "status": "PASS"},
        observed=invocation_result,
        evidence_refs=[(BUILD_REPORT_ROOT / "invocation-result.json").as_posix()],
    )

    add_assertion(
        assertions,
        assertion_id="state.workspace_unchanged",
        category="state",
        description="Before and after state evidence is identical within declared probe coverage.",
        condition=receipt.get("before_state_ref") == receipt.get("after_state_ref")
        and receipt.get("mutation_observation") == "none_detected_within_probe_coverage"
        and invocation_result.get("workspace_state_unchanged") is True,
        expected="before_state_ref == after_state_ref and no mutation observed",
        observed={"before": receipt.get("before_state_ref"), "after": receipt.get("after_state_ref"), "mutation": receipt.get("mutation_observation")},
        evidence_refs=[(BUILD_REPORT_ROOT / "execution-receipt.json").as_posix()],
    )

    expected_projection_digest = sha256_text(stable_json({key: value for key, value in projection.items() if key != "projection_digest"}))
    add_assertion(
        assertions,
        assertion_id="determinism.projection_digest",
        category="determinism",
        description="Projection digest recomputes from canonical JSON.",
        condition=projection.get("projection_digest") == expected_projection_digest,
        expected=expected_projection_digest,
        observed=projection.get("projection_digest"),
        evidence_refs=[(BUILD_REPORT_ROOT / "projection.json").as_posix()],
    )

    fake_results = run_fake_runner_checks(repo_root)
    add_assertion(
        assertions,
        assertion_id="behavior.fake_runner_success_once",
        category="behavior",
        description="Independent fake-runner success path launches exactly once with exact argv.",
        condition=fake_results["success"]["process_call_count"] == 1
        and fake_results["success"]["call_count"] == 1
        and fake_results["success"]["argv_matches"] is True,
        expected="one fake-runner call ending in .aide/scripts/aide_lite.py validate",
        observed=fake_results["success"],
        evidence_refs=["independent fake-runner harness"],
    )
    zero_launch_cases = ["unsupported", "wrong_revision", "missing_workspace", "missing_executable", "digest_mismatch", "invalid_binding"]
    add_assertion(
        assertions,
        assertion_id="behavior.zero_launch_refusals",
        category="behavior",
        description="Invalid capability, workspace, revision, executable, digest, and binding cases launch zero processes.",
        condition=all(fake_results[case]["process_call_count"] == 0 and fake_results[case]["calls"] == [] for case in zero_launch_cases),
        expected={case: 0 for case in zero_launch_cases},
        observed={case: fake_results[case] for case in zero_launch_cases},
        evidence_refs=["independent fake-runner harness"],
    )

    before_build_report_diff = git(repo_root, ["diff", "--name-only", "--", str(BUILD_REPORT_ROOT)]).splitlines()
    adapter_validate = run(repo_root, [sys.executable, ".aide/scripts/aide_lite.py", "aide-self-validation-process-adapter", "validate"])
    direct_validate = run(repo_root, [sys.executable, ".aide/scripts/aide_lite.py", "validate"], timeout=180)
    after_build_report_diff = git(repo_root, ["diff", "--name-only", "--", str(BUILD_REPORT_ROOT)]).splitlines()
    add_assertion(
        assertions,
        assertion_id="churn.report_validate_no_churn",
        category="churn",
        description="Report-only adapter validation leaves source build reports unchanged.",
        condition=adapter_validate["returncode"] == 0 and before_build_report_diff == [] and after_build_report_diff == [],
        expected={"returncode": 0, "build_report_diff": []},
        observed={"returncode": adapter_validate["returncode"], "before_diff": before_build_report_diff, "after_diff": after_build_report_diff},
        evidence_refs=["py -3 .aide/scripts/aide_lite.py aide-self-validation-process-adapter validate"],
    )
    direct_stdout = direct_validate["stdout_excerpt"]
    add_assertion(
        assertions,
        assertion_id="recursion.direct_validate_not_recursive",
        category="recursion",
        description="Direct AIDE Lite validate succeeds and does not dispatch the self-validation adapter run command.",
        condition=direct_validate["returncode"] == 0
        and "status: PASS" in direct_stdout
        and "aide-self-validation-process-adapter run" not in direct_stdout
        and "AIDE Lite aide-self-validation-process-adapter run" not in direct_stdout,
        expected="status PASS and no self-validation adapter run string",
        observed=direct_validate,
        evidence_refs=["py -3 .aide/scripts/aide_lite.py validate"],
    )

    leak_findings = scan_for_leaks(repo_root, [BUILD_REPORT_ROOT, BUILD_TASK_ROOT])
    add_assertion(
        assertions,
        assertion_id="hygiene.no_committed_build_leaks",
        category="hygiene",
        description="Committed source build reports and evidence contain no absolute local paths or secret-like values.",
        condition=leak_findings == [],
        expected=[],
        observed=leak_findings,
        evidence_refs=[BUILD_REPORT_ROOT.as_posix(), BUILD_TASK_ROOT.as_posix()],
    )

    capability_ok = capability.get("accepted") is False and capability.get("provider_acceptance_claimed") is False
    add_assertion(
        assertions,
        assertion_id="boundary.provider_not_accepted",
        category="boundary",
        description="Provider and adapter capability remain proposed and unaccepted.",
        condition=capability_ok,
        expected={"accepted": False, "provider_acceptance_claimed": False},
        observed=capability,
        evidence_refs=[(BUILD_REPORT_ROOT / "capability-descriptor.json").as_posix()],
    )

    provider_non_caps = (repo_root / ".aide/reports/registered-process-execution-provider-v0-repair/explicit-non-capabilities.md").read_text(encoding="utf-8")
    required_provider_non_caps = [
        "process_cancellation",
        "child_process_tree_termination",
        "persistent_idempotency",
        "resource_quota_enforcement",
        "streaming_artifact_storage",
        "non_git_state_providers",
    ]
    add_assertion(
        assertions,
        assertion_id="boundary.provider_non_capabilities_preserved",
        category="boundary",
        description="Provider-level non-capabilities remain explicit in provider repair evidence.",
        condition=all(item in provider_non_caps for item in required_provider_non_caps),
        expected=required_provider_non_caps,
        observed=provider_non_caps,
        evidence_refs=[".aide/reports/registered-process-execution-provider-v0-repair/explicit-non-capabilities.md"],
    )

    test_commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", ".aide/scripts/tests", "-p", "test_aide_self_validation_process_adapter.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", ".aide/scripts/tests", "-p", "test_aide_registered_process_provider.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", ".aide/scripts/tests", "-p", "test_aide_dominium_registered_validation_backend.py"],
    ]
    command_results = [run(repo_root, command, timeout=180) for command in test_commands]
    add_assertion(
        assertions,
        assertion_id="regression.focused_tests_pass",
        category="regression",
        description="Self adapter, generic provider, and Dominium parity focused tests pass.",
        condition=all(result["returncode"] == 0 for result in command_results),
        expected="all focused tests return 0",
        observed=command_results,
        evidence_refs=["focused unittest commands"],
    )

    material_failures = [item for item in assertions if item["outcome"] != "PASS" and item["severity"] == "material"]
    result = "PASS_WITH_WARNINGS" if not material_failures else "REQUEST_CHANGES"
    recommended_next = PASS_NEXT if not material_failures else FAIL_NEXT
    report = {
        "schema_version": "aide.self-validation-process-adapter-check.v1",
        "kind": "AideSelfValidationProcessAdapterCheckReport",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "result": result,
        "status": result,
        "material_finding_count": len(material_failures),
        "missing_evidence": 0,
        "recommended_next_task": recommended_next,
        "assertions": assertions,
        "warnings": [
            "RegisteredProcessExecutionProvider v0 remains proposed and unaccepted.",
            "Eureka remains required as the unrelated external-domain provider reuse proof.",
            "The source build allowed preexisting task-local dirty state and proved no additional state change across the process boundary.",
            "The independent harness uses its current Python executable for nested Python subprocesses to avoid WindowsApps py launcher drift; shell validation commands are recorded separately.",
        ],
        "explicit_non_capabilities": [
            "implementation_repair",
            "provider_acceptance",
            "eureka_adapter_build",
            "arbitrary_command_runner",
            "generic_command_cli",
            "provider_core_mutation",
            "service_runtime",
            "worker_execution",
            "provider_model_network_calls",
            "preview_apply_rollback",
            "repository_mutation",
            "branch_worktree_github_release_behavior",
        ],
    }
    write_json(REPORT_ROOT / "check-report.json", report)
    write_json(EVIDENCE_ROOT / "independent-check.json", report)
    summary_lines = [
        "# AIDE Self-Validation Process Adapter Check",
        "",
        f"- result: `{result}`",
        f"- material_finding_count: `{len(material_failures)}`",
        "- missing_evidence: `0`",
        f"- recommended_next_task: `{recommended_next}`",
        "",
        "## Assertions",
        "",
    ]
    summary_lines.extend(f"- `{item['id']}`: `{item['outcome']}`" for item in assertions)
    summary_lines.append("")
    write_text(REPORT_ROOT / "check-report.md", "\n".join(summary_lines))
    write_text(EVIDENCE_ROOT / "independent-check.md", "\n".join(summary_lines))
    write_text(
        REPORT_ROOT / "status.md",
        "\n".join(
            [
                "# AIDE Self-Validation Process Adapter Check Status",
                "",
                f"- task_id: `{TASK_ID}`",
                f"- result: `{result}`",
                f"- material_finding_count: `{len(material_failures)}`",
                "- missing_evidence: `0`",
                f"- recommended_next_task: `{recommended_next}`",
                "",
            ]
        ),
    )
    return 0 if not material_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
