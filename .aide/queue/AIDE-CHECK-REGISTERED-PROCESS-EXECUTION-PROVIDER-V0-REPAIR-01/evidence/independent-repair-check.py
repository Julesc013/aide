from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution.registered_process import (  # noqa: E402
    CANCELLATION_SUPPORTED,
    EXPLICIT_NON_CAPABILITIES,
    DecoderResult,
    PreconditionResult,
    RegisteredProcessExecutionProvider,
    RegisteredProcessSpec,
)
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation  # noqa: E402


TASK_ID = "AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01"
SOURCE_TASK_ID = "AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01"
REPORT_DIR = REPO_ROOT / ".aide" / "reports" / "registered-process-execution-provider-v0-repair-check"
REPORT_JSON = REPORT_DIR / "check-report.json"
REPORT_MD = REPORT_DIR / "check-report.md"


class FakeRunner:
    def __init__(
        self,
        *,
        stdout: str = '{"status": "ok"}',
        stderr: str = "",
        returncode: int = 0,
        timeout: bool = False,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.calls: list[dict[str, Any]] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append(
            {
                "argv": list(argv),
                "cwd_name": Path(cwd).name,
                "env_keys": sorted(dict(env)),
                "timeout": timeout,
                "shell": False,
            }
        )
        if self.timeout:
            raise subprocess.TimeoutExpired(list(argv), timeout, output="", stderr="timeout")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class SequenceProbe:
    def __init__(
        self,
        *,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
        coverage: list[str] | None = None,
        fail_capture: bool = False,
        fail_mutation: bool = False,
    ) -> None:
        self.states = [
            before or {"tracked": "same"},
            after if after is not None else before or {"tracked": "same"},
        ]
        self.coverage = coverage or ["tracked"]
        self.fail_capture = fail_capture
        self.fail_mutation = fail_mutation
        self.calls = 0

    def capture(self):
        if self.fail_capture:
            raise RuntimeError("probe capture failed")
        index = min(self.calls, len(self.states) - 1)
        self.calls += 1
        return dict(self.states[index])

    def mutation_observation(self, before_state, after_state):
        if self.fail_mutation:
            raise RuntimeError("probe mutation check failed")
        if dict(before_state) == dict(after_state):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


class StaticPrecondition:
    def __init__(self, ok: bool = True, reason_code: str = "precondition_refused") -> None:
        self.ok = ok
        self.reason_code = reason_code

    def check(self, invocation, binding, spec, before_state):
        if self.ok:
            return PreconditionResult(True)
        return PreconditionResult(False, self.reason_code, "precondition refused")


class StatusDecoder:
    decoder_id = "repair-check-decoder-v0"

    def __init__(self, *, raise_error: bool = False) -> None:
        self.raise_error = raise_error

    def decode(self, stdout, stderr, returncode):
        if self.raise_error:
            raise RuntimeError("decoder failed")
        if '"status": "refused"' in stdout:
            return DecoderResult(
                "decoded",
                "typed_refusal",
                domain_result={"status": "refused"},
                refusal={"status": "refused"},
            )
        return DecoderResult("decoded", "typed_result", domain_result={"status": "ok"})


class ReplacementScrubber:
    scrubber_id = "repair-check-scrubber-v0"

    def scrub(self, text: str) -> str:
        return text.replace("sensitive-value", "<redacted>")


def make_spec(executable: Path, workspace: Path, *, argument: str = "--first") -> RegisteredProcessSpec:
    return RegisteredProcessSpec(
        capability_ref="aide://capability/repair-check",
        executable=str(executable),
        argument_plan=[ArgumentToken("literal", argument)],
        working_directory=str(workspace),
        timeout_seconds=5.0,
        environment={"PYTHONHASHSEED": "0", "REPAIR_CHECK": "1"},
        decoder_id="repair-check-decoder-v0",
        state_probe_id="repair-check-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id="repair-check-scrubber-v0",
        provider_spec_ref="aide://provider-spec/repair-check",
        conformance_profile_ref="aide://conformance-profile/repair-check",
    )


def make_binding(spec: RegisteredProcessSpec, *, capability_ref: str | None = None, provider_id: str | None = None) -> CapabilityBinding:
    return CapabilityBinding(
        capability_ref=capability_ref or spec.capability_ref or "aide://capability/repair-check",
        provider_id=provider_id or RegisteredProcessExecutionProvider.provider_id,
        provider_spec_ref=spec.provider_spec_ref,
        provider_spec=spec,
        decoder_id=spec.decoder_id,
        state_probe_id=spec.state_probe_id,
        scrubber_id=spec.scrubber_id,
        conformance_profile_ref=spec.conformance_profile_ref,
    )


def make_invocation(capability_ref: str = "aide://capability/repair-check", ref: str = "aide://invocation/repair-check-01") -> CapabilityInvocation:
    return CapabilityInvocation(invocation_ref=ref, capability_ref=capability_ref)


def assert_true(condition: bool, finding_id: str, message: str, findings: list[dict[str, Any]]) -> None:
    if not condition:
        findings.append({"finding_id": finding_id, "severity": "material", "summary": message})


def scan_generic_sources() -> dict[str, Any]:
    forbidden = [
        "dominium",
        "validation.run",
        "AIDE-BUILD",
        "AIDE-CHECK",
        ".aide/queue",
        ".aide/reports",
        "REPORT_ROOT",
        "write_outputs",
    ]
    matches: list[dict[str, str]] = []
    for rel in [
        "core/execution/registered_process.py",
        "core/execution/provider.py",
        "core/protocol/process_invocation.py",
        "core/protocol/execution_receipt.py",
    ]:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        lowered = text.lower()
        for token in forbidden:
            if token.lower() in lowered:
                matches.append({"path": rel, "token": token})
    return {"forbidden_match_count": len(matches), "matches": matches}


def scan_committed_reports() -> dict[str, int]:
    targets = [
        REPO_ROOT / ".aide" / "reports" / "registered-process-execution-provider-v0-repair",
        REPO_ROOT / ".aide" / "reports" / "registered-process-execution-provider-v0-repair-check",
        REPO_ROOT / ".aide" / "queue" / TASK_ID,
    ]
    absolute_markers = ["C" + ":/", "C" + ":\\", "\\" + "Users\\", "/" + "Users/"]
    sensitive_pattern = re.compile(r"(?i)\b(?:sk|ghp|github_pat|xoxb)-[A-Za-z0-9_\-]{8,}")
    absolute_count = 0
    sensitive_count = 0
    for target in targets:
        if not target.exists():
            continue
        for path in sorted(item for item in target.rglob("*") if item.is_file()):
            if path.name == "independent-repair-check.py" or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(marker in text for marker in absolute_markers):
                absolute_count += 1
            if sensitive_pattern.search(text):
                sensitive_count += 1
    return {"absolute_path_match_count": absolute_count, "sensitive_match_count": sensitive_count}


def run_behavior_checks() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    observations: dict[str, Any] = {}
    findings: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        executable = workspace / "tool.py"
        executable.write_text("print('ok')\n", encoding="utf-8")
        spec = make_spec(executable, workspace)

        mismatch_runner = FakeRunner()
        receipt, outcome = RegisteredProcessExecutionProvider(
            runner=mismatch_runner,
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec, capability_ref="aide://capability/other"))
        observations["binding_capability_mismatch"] = {
            "calls": len(mismatch_runner.calls),
            "launcher_call_count": receipt.launcher_call_count,
            "reason_code": outcome.reason_code,
            "evidence_completeness": outcome.evidence_completeness,
        }
        assert_true(len(mismatch_runner.calls) == 0, "binding.mismatch_launches_process", "Capability binding mismatch launched a process.", findings)
        assert_true(outcome.reason_code == "binding_mismatch", "binding.mismatch_not_classified", "Capability binding mismatch was not classified as binding_mismatch.", findings)

        wrong_provider_runner = FakeRunner()
        wrong_provider_receipt, wrong_provider_outcome = RegisteredProcessExecutionProvider(
            runner=wrong_provider_runner,
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec, provider_id="wrong-provider"))
        observations["binding_provider_mismatch"] = {
            "calls": len(wrong_provider_runner.calls),
            "launcher_call_count": wrong_provider_receipt.launcher_call_count,
            "provider_ref_is_current_provider": wrong_provider_receipt.provider_ref == RegisteredProcessExecutionProvider.provider_id,
            "reason_code": wrong_provider_outcome.reason_code,
        }
        assert_true(len(wrong_provider_runner.calls) == 0, "binding.mismatch_launches_process", "Provider binding mismatch launched a process.", findings)
        assert_true(wrong_provider_outcome.reason_code == "binding_mismatch", "binding.mismatch_not_classified", "Provider binding mismatch was not classified as binding_mismatch.", findings)

        precondition_runner = FakeRunner()
        precondition_receipt, precondition_outcome = RegisteredProcessExecutionProvider(
            runner=precondition_runner,
            precondition=StaticPrecondition(False, "wrong_workspace_identity"),
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        observations["precondition_refusal"] = {
            "calls": len(precondition_runner.calls),
            "launcher_call_count": precondition_receipt.launcher_call_count,
            "reason_code": precondition_outcome.reason_code,
        }
        assert_true(len(precondition_runner.calls) == 0, "precondition.failure_launches_process", "Precondition refusal launched a process.", findings)

        invalid_runner = FakeRunner()
        invalid_spec = RegisteredProcessSpec(
            capability_ref="",
            executable="",
            argument_plan=[],
            working_directory="",
            timeout_seconds=0,
            environment={},
            decoder_id="",
            state_probe_id="",
            mutation_policy="",
            scrubber_id="",
            immutable=False,
        )
        invalid_receipt, invalid_outcome = RegisteredProcessExecutionProvider(runner=invalid_runner).execute(make_invocation(), make_binding(invalid_spec))
        observations["invalid_spec"] = {
            "calls": len(invalid_runner.calls),
            "launcher_call_count": invalid_receipt.launcher_call_count,
            "reason_code": invalid_outcome.reason_code,
        }
        assert_true(len(invalid_runner.calls) == 0, "spec.invalid_launches_process", "Invalid spec launched a process.", findings)

        repeat_runner = FakeRunner()
        provider = RegisteredProcessExecutionProvider(
            runner=repeat_runner,
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        )
        first_receipt, _ = provider.execute(make_invocation(ref="aide://invocation/repair-check-01"), make_binding(make_spec(executable, workspace, argument="--first")))
        second_receipt, _ = provider.execute(make_invocation(ref="aide://invocation/repair-check-02"), make_binding(make_spec(executable, workspace, argument="--second")))
        second_argv = second_receipt.metadata.get("launch", {}).get("argv", [])
        observations["repeat_invocation"] = {
            "runner_call_count": len(repeat_runner.calls),
            "first_receipt_launcher_call_count": first_receipt.launcher_call_count,
            "second_receipt_launcher_call_count": second_receipt.launcher_call_count,
            "second_receipt_has_current_argument": "--second" in second_argv and "--first" not in second_argv,
        }
        assert_true(first_receipt.launcher_call_count == 1 and second_receipt.launcher_call_count == 1, "receipt.launch_accounting_is_cumulative_or_stale", "Launch accounting is not per invocation.", findings)
        assert_true("--second" in second_argv and "--first" not in second_argv, "receipt.launch_metadata_is_stale", "Launch metadata does not describe the current invocation.", findings)

        decoder_runner = FakeRunner(stdout='{"status": "ok"}')
        _, decoder_outcome = RegisteredProcessExecutionProvider(
            runner=decoder_runner,
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(raise_error=True),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        observations["decoder_failure"] = decoder_outcome.to_dict()
        assert_true(decoder_outcome.validation_outcome == "incomplete", "decoder.failure_marked_complete", "Decoder failure reported complete validation.", findings)
        assert_true(decoder_outcome.evidence_completeness == "incomplete", "decoder.failure_marked_complete", "Decoder failure reported complete evidence.", findings)

        probe_runner = FakeRunner(stdout='{"status": "ok"}')
        probe_receipt, probe_outcome = RegisteredProcessExecutionProvider(
            runner=probe_runner,
            state_probe=SequenceProbe(fail_mutation=True),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        observations["state_probe_failure"] = {
            "calls": len(probe_runner.calls),
            "mutation_observation_is_failure": probe_receipt.mutation_observation.startswith("probe_failure:"),
            "outcome": probe_outcome.to_dict(),
        }
        assert_true(probe_outcome.reason_code == "state_probe_failure", "state_probe.failure_not_failed_closed", "State probe failure was not classified.", findings)
        assert_true(probe_outcome.domain_outcome == "none", "state_probe.failure_not_failed_closed", "State probe failure preserved a typed domain outcome.", findings)
        assert_true(probe_outcome.validation_outcome == "incomplete", "state_probe.failure_not_failed_closed", "State probe failure reported complete validation.", findings)

        timeout_runner = FakeRunner(timeout=True)
        timeout_receipt, timeout_outcome = RegisteredProcessExecutionProvider(
            runner=timeout_runner,
            state_probe=SequenceProbe(),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        observations["timeout"] = {
            "timed_out": timeout_receipt.timed_out,
            "cancelled": timeout_receipt.cancelled,
            "outcome": timeout_outcome.to_dict(),
        }
        assert_true(timeout_outcome.validation_outcome == "incomplete", "timeout.failure_marked_complete", "Timeout reported complete validation.", findings)
        assert_true(timeout_outcome.evidence_completeness == "incomplete", "timeout.failure_marked_complete", "Timeout reported complete evidence.", findings)

        valid_runner = FakeRunner(stdout='{"status": "refused"} sensitive-value')
        valid_receipt, valid_outcome = RegisteredProcessExecutionProvider(
            runner=valid_runner,
            state_probe=SequenceProbe(coverage=["tracked"]),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        launch_metadata = valid_receipt.metadata.get("launch", {})
        observations["valid_invocation"] = {
            "runner_call_count": len(valid_runner.calls),
            "launcher_call_count": valid_receipt.launcher_call_count,
            "shell": valid_receipt.shell,
            "runner_shell": valid_runner.calls[0]["shell"],
            "domain_outcome": valid_outcome.domain_outcome,
            "probe_coverage": valid_receipt.probe_coverage,
            "mutation_observation": valid_receipt.mutation_observation,
            "launch_has_raw_env": "env" in launch_metadata,
            "launch_has_manifest_digest": "environment_manifest_digest" in launch_metadata,
            "stdout_scrubbed": "sensitive-value" not in str(valid_receipt.stdout.get("excerpt", "")),
        }
        assert_true(len(valid_runner.calls) == 1 and valid_receipt.launcher_call_count == 1, "invocation.launch_count_invalid", "Valid invocation did not launch exactly once.", findings)
        assert_true(valid_receipt.shell is False and valid_runner.calls[0]["shell"] is False, "invocation.shell_not_false", "Invocation did not preserve shell=False.", findings)
        assert_true(valid_receipt.probe_coverage == ["tracked"], "state.coverage_not_declared", "Probe coverage was not preserved.", findings)
        assert_true("env" not in launch_metadata and "environment_manifest_digest" in launch_metadata, "evidence.environment_not_redacted", "Launch metadata includes raw environment or lacks manifest digest.", findings)
        assert_true("sensitive-value" not in str(valid_receipt.stdout.get("excerpt", "")), "evidence.stream_not_scrubbed", "Committed stream summary was not scrubbed.", findings)

        before_failure_runner = FakeRunner()
        before_failure_receipt, before_failure_outcome = RegisteredProcessExecutionProvider(
            runner=before_failure_runner,
            state_probe=SequenceProbe(fail_capture=True),
            output_decoder=StatusDecoder(),
            stream_scrubber=ReplacementScrubber(),
        ).execute(make_invocation(), make_binding(spec))
        observations["before_probe_failure"] = {
            "calls": len(before_failure_runner.calls),
            "launcher_call_count": before_failure_receipt.launcher_call_count,
            "reason_code": before_failure_outcome.reason_code,
            "validation_outcome": before_failure_outcome.validation_outcome,
            "evidence_completeness": before_failure_outcome.evidence_completeness,
        }
        assert_true(len(before_failure_runner.calls) == 0, "state_probe.before_failure_launches_process", "Before-state probe failure launched a process.", findings)
        assert_true(before_failure_outcome.validation_outcome != "complete", "state_probe.before_failure_marked_complete", "Before-state probe failure reported complete validation.", findings)

    cancellation_declared = (CANCELLATION_SUPPORTED is False) and ("process_cancellation" in EXPLICIT_NON_CAPABILITIES)
    observations["cancellation"] = {
        "cancellation_supported": CANCELLATION_SUPPORTED,
        "process_cancellation_declared_non_capability": "process_cancellation" in EXPLICIT_NON_CAPABILITIES,
    }
    assert_true(cancellation_declared, "cancellation.not_implemented_or_declared", "Cancellation is not implemented or explicitly declared unsupported.", findings)
    return observations, findings


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Registered Process Execution Provider v0 Repair Check",
        "",
        f"- task_id: `{report['task_id']}`",
        f"- result: `{report['result']}`",
        f"- material_finding_count: `{report['material_finding_count']}`",
        f"- missing_evidence: `{report['missing_evidence']}`",
        f"- provider_accepted: `{str(report['provider_accepted']).lower()}`",
        f"- implementation_repaired: `{str(report['implementation_repaired']).lower()}`",
        f"- recommended_next_task: `{report['recommended_next_task']}`",
        "",
        "## Finding Closure",
        "",
    ]
    if report["findings"]:
        for finding in report["findings"]:
            lines.extend(
                [
                    f"### {finding['finding_id']}",
                    "",
                    f"- severity: `{finding['severity']}`",
                    f"- summary: {finding['summary']}",
                    "",
                ]
            )
    else:
        lines.append("- No material findings remain in the task-local independent behavior harness.")
        lines.append("")
    lines.extend(
        [
            "## Non-Capabilities",
            "",
            "- The provider remains proposed and unaccepted.",
            "- Process cancellation remains explicitly unsupported in v0.",
            "- No worker, runtime, Service, Workbench, provider/model/network, preview/apply/rollback, branch/worktree, GitHub, release, or target-repository behavior was performed.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    behavior, findings = run_behavior_checks()
    genericity = scan_generic_sources()
    if genericity["forbidden_match_count"]:
        findings.append(
            {
                "finding_id": "genericity.domain_or_queue_leak",
                "severity": "material",
                "summary": "Generic provider/protocol source contains domain, queue, or report-specific tokens.",
            }
        )
    committed_leaks = scan_committed_reports()
    if committed_leaks["absolute_path_match_count"] or committed_leaks["sensitive_match_count"]:
        findings.append(
            {
                "finding_id": "evidence.unscrubbed_committed_summary",
                "severity": "material",
                "summary": "Committed task or report surfaces contain local path or sensitive-like markers.",
            }
        )
    result = "PASS_WITH_WARNINGS" if not findings else "REQUEST_CHANGES"
    report = {
        "schema_version": "aide.registered-process-execution-provider-v0.repair-check-report.v1",
        "kind": "RegisteredProcessExecutionProviderRepairCheckReport",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_repair_commit": "7f043d09ae0c5bbb73d68ad293e6dafaaaa8ddd6",
        "result": result,
        "validation_status": "PASS_WITH_WARNINGS" if not findings else "FAILED_VALIDATION",
        "provider_accepted": False,
        "implementation_repaired": not findings,
        "material_finding_count": len(findings),
        "missing_evidence": 0,
        "findings": findings,
        "observations": {
            "behavior": behavior,
            "genericity": genericity,
            "committed_leaks": committed_leaks,
        },
        "five_source_findings_closed": not findings,
        "live_dominium_command_rerun": False,
        "dominium_modified": False,
        "network_call_performed": False,
        "provider_or_model_called": False,
        "worker_executed": False,
        "runtime_started": False,
        "preview_or_apply_performed": False,
        "target_repository_mutated": False,
        "branch_or_worktree_created": False,
        "github_mutation_performed": False,
        "release_or_promotion_performed": False,
        "recommended_next_task": "AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01"
        if not findings
        else "AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-02",
    }
    write_json(REPORT_JSON, report)
    REPORT_MD.write_text(render_markdown(report), encoding="utf-8")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
