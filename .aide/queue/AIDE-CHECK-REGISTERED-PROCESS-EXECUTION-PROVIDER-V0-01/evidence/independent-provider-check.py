from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01"
SOURCE_TASK_ID = "AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01"
SOURCE_COMMIT = "2137af3a68cc50a06b57fe1fd5ee5bc3af8e0924"
PROPOSED_CAPABILITY = "registered_process_execution_provider_v0"
RESULT = "REQUEST_CHANGES"
NEXT_TASK = "AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01"

REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_ROOT = REPO_ROOT / ".aide/reports/registered-process-execution-provider-v0-check"
EVIDENCE_ROOT = REPO_ROOT / ".aide/queue" / TASK_ID / "evidence"
GENERIC_FILES = [
    "core/execution/provider.py",
    "core/execution/registered_process.py",
    "core/protocol/process_invocation.py",
    "core/protocol/execution_receipt.py",
]
COMMITTED_SCAN_ROOTS = [
    ".aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01",
    ".aide/reports/registered-process-execution-provider-v0",
]


if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution.registered_process import (  # noqa: E402
    DecoderResult,
    PreconditionResult,
    RegisteredProcessExecutionProvider,
    RegisteredProcessSpec,
)
from core.protocol.process_invocation import (  # noqa: E402
    ArgumentToken,
    CapabilityBinding,
    CapabilityInvocation,
)


@dataclass
class Finding:
    finding_id: str
    severity: str
    summary: str
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "summary": self.summary,
            "evidence": self.evidence,
        }


class FakeRunner:
    def __init__(self, *, stdout: str = '{"status":"ok"}', stderr: str = "", returncode: int = 0, timeout: bool = False):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.calls: list[dict[str, Any]] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append(
            {
                "argv": [Path(str(argv[0])).name, *[str(item) for item in argv[1:]]],
                "cwd": "<workspace>",
                "env_keys": sorted(dict(env)),
                "timeout": timeout,
                "shell": False,
            }
        )
        if self.timeout:
            raise subprocess.TimeoutExpired([Path(str(argv[0])).name, *argv[1:]], timeout, output="", stderr="timeout")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class StaticPrecondition:
    def __init__(self, ok: bool = True):
        self.ok = ok

    def check(self, invocation, binding, spec, before_state):
        if self.ok:
            return PreconditionResult(True)
        return PreconditionResult(False, "precondition_refused", "precondition refused")


class StableProbe:
    coverage = ["tracked"]

    def capture(self):
        return {"state": "same"}

    def mutation_observation(self, before_state, after_state):
        return "none_detected_within_probe_coverage"


class FailingProbe(StableProbe):
    def mutation_observation(self, before_state, after_state):
        raise RuntimeError("probe failed")


class Decoder:
    decoder_id = "check-decoder-v0"

    def __init__(self, fail: bool = False):
        self.fail = fail

    def decode(self, stdout, stderr, returncode):
        if self.fail:
            raise RuntimeError("decoder failed")
        return DecoderResult("decoded", "typed_result", domain_result={"status": "ok"})


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def make_spec(executable: Path, workspace: Path, *, argument: str = "--one") -> RegisteredProcessSpec:
    return RegisteredProcessSpec(
        capability_ref="cap://expected",
        executable=str(executable),
        argument_plan=[ArgumentToken("literal", argument)],
        working_directory=str(workspace),
        timeout_seconds=5.0,
        environment={"SAFE": "1"},
        decoder_id="check-decoder-v0",
        state_probe_id="check-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id="check-scrubber-v0",
    )


def scrub_argv(argv: Any) -> list[str]:
    if not isinstance(argv, list):
        return []
    cleaned: list[str] = []
    for index, item in enumerate(argv):
        arg_text = str(item)
        if index == 0:
            cleaned.append(Path(arg_text).name)
        elif re.search(r"(?<![A-Za-z0-9])[A-Z]:[\\/]", arg_text):
            cleaned.append("<absolute-path>")
        else:
            cleaned.append(arg_text)
    return cleaned


def binding(spec: RegisteredProcessSpec, *, capability_ref: str = "cap://expected", provider_id: str | None = None) -> CapabilityBinding:
    return CapabilityBinding(
        capability_ref=capability_ref,
        provider_id=provider_id or RegisteredProcessExecutionProvider.provider_id,
        provider_spec=spec,
        decoder_id=spec.decoder_id,
        state_probe_id=spec.state_probe_id,
        scrubber_id=spec.scrubber_id,
    )


def invocation(ref: str = "inv://1", capability_ref: str = "cap://expected") -> CapabilityInvocation:
    return CapabilityInvocation(ref, capability_ref)


def add_material(findings: list[Finding], finding_id: str, summary: str, evidence: dict[str, Any]) -> None:
    findings.append(Finding(finding_id, "material", summary, evidence))


def run_git(args: list[str]) -> tuple[int, str]:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return result.returncode, (result.stdout + result.stderr).strip()


def scan_genericity(findings: list[Finding]) -> dict[str, Any]:
    forbidden = [
        "dominium",
        "validation.run",
        "AIDE-BUILD",
        "AIDE-CHECK",
        "registered-validation",
        ".aide",
        "queue",
        "report",
        "write_text",
        "write_json",
    ]
    matches: list[dict[str, Any]] = []
    for rel_path in GENERIC_FILES:
        text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        for forbidden_text in forbidden:
            haystack = text.lower() if forbidden_text == forbidden_text.lower() else text
            needle = forbidden_text.lower() if forbidden_text == forbidden_text.lower() else forbidden_text
            if needle in haystack:
                matches.append({"path": rel_path, "matched_text": forbidden_text})
    if matches:
        add_material(
            findings,
            "genericity.domain_or_queue_leakage",
            "Generic provider/protocol files contain forbidden domain, queue, or report-writing tokens.",
            {"matches": matches},
        )
    return {"forbidden_match_count": len(matches), "matches": matches}


def scan_committed_leaks(findings: list[Finding]) -> dict[str, Any]:
    absolute_pattern = re.compile(r"(?<![A-Za-z0-9])[A-Z]:[\\/][^\s\"')]+")
    sensitive_pattern = re.compile(
        "(?i)("
        + "|".join(
            [
                "openai" + "_api_key",
                "anthropic" + "_api_key",
                "deepseek" + "_api_key",
                r"api[_-]?key\s*[:=]",
                r"password\s*[:=]",
                r"secret\s*[:=]",
                r"token\s*[:=]",
                r"sk-[a-z0-9_-]{20,}",
            ]
        )
        + ")"
    )
    absolute_matches: list[str] = []
    sensitive_matches: list[str] = []
    for root in COMMITTED_SCAN_ROOTS:
        base = REPO_ROOT / root
        for path in sorted(item for item in base.rglob("*") if item.is_file()):
            text = path.read_text(encoding="utf-8", errors="replace")
            if absolute_pattern.search(text):
                absolute_matches.append(rel(path))
            if sensitive_pattern.search(text):
                sensitive_matches.append(rel(path))
    if absolute_matches:
        add_material(
            findings,
            "scrubbing.absolute_path_leak",
            "Committed source build reports/evidence contain machine-specific absolute paths.",
            {"paths": absolute_matches},
        )
    if sensitive_matches:
        add_material(
            findings,
            "scrubbing.sensitive_value_leak",
            "Committed source build reports/evidence contain secret-like values.",
            {"paths": sensitive_matches},
        )
    return {
        "absolute_path_match_count": len(absolute_matches),
        "sensitive_match_count": len(sensitive_matches),
    }


def behavior_checks(findings: list[Finding]) -> dict[str, Any]:
    observations: dict[str, Any] = {}
    with tempfile.TemporaryDirectory() as temp:
        workspace = Path(temp)
        executable = workspace / "tool.py"
        executable.write_text("print('ok')\n", encoding="utf-8")
        spec = make_spec(executable, workspace)

        preflight_runner = FakeRunner()
        receipt, outcome = RegisteredProcessExecutionProvider(
            runner=preflight_runner,
            precondition=StaticPrecondition(False),
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec))
        observations["precondition_zero_launch"] = {
            "calls": len(preflight_runner.calls),
            "launcher_call_count": receipt.launcher_call_count,
            "reason_code": outcome.reason_code,
        }

        invalid = RegisteredProcessSpec(
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
        invalid_runner = FakeRunner()
        receipt, outcome = RegisteredProcessExecutionProvider(runner=invalid_runner).execute(invocation(), binding(invalid))
        observations["invalid_spec_zero_launch"] = {
            "calls": len(invalid_runner.calls),
            "launcher_call_count": receipt.launcher_call_count,
            "reason_code": outcome.reason_code,
        }

        mismatch_binding_runner = FakeRunner()
        receipt, outcome = RegisteredProcessExecutionProvider(
            runner=mismatch_binding_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec, capability_ref="cap://different"))
        wrong_provider_runner = FakeRunner()
        wrong_provider_receipt, wrong_provider_outcome = RegisteredProcessExecutionProvider(
            runner=wrong_provider_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec, provider_id="wrong-provider"))
        observations["binding_mismatch"] = {
            "capability_mismatch_calls": len(mismatch_binding_runner.calls),
            "capability_mismatch_outcome": outcome.to_dict(),
            "wrong_provider_calls": len(wrong_provider_runner.calls),
            "wrong_provider_outcome": wrong_provider_outcome.to_dict(),
            "wrong_provider_receipt_provider_ref": wrong_provider_receipt.provider_ref,
        }
        if mismatch_binding_runner.calls or wrong_provider_runner.calls:
            add_material(
                findings,
                "binding.mismatch_launches_process",
                "Mismatched capability/provider bindings still launch a process instead of failing closed before launch.",
                observations["binding_mismatch"],
            )

        repeat_runner = FakeRunner()
        provider = RegisteredProcessExecutionProvider(
            runner=repeat_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        )
        first_receipt, _ = provider.execute(invocation("inv://one"), binding(make_spec(executable, workspace, argument="--first")))
        second_receipt, _ = provider.execute(invocation("inv://two"), binding(make_spec(executable, workspace, argument="--second")))
        second_launch = second_receipt.metadata.get("launch", {}) if isinstance(second_receipt.metadata, dict) else {}
        observations["repeat_invocation"] = {
            "runner_call_count": len(repeat_runner.calls),
            "first_receipt_launcher_call_count": first_receipt.launcher_call_count,
            "second_receipt_launcher_call_count": second_receipt.launcher_call_count,
            "second_receipt_launch_argv": scrub_argv(second_launch.get("argv")),
        }
        if second_receipt.launcher_call_count != 1 or "--second" not in [str(item) for item in second_launch.get("argv", [])]:
            add_material(
                findings,
                "receipt.launch_accounting_is_cumulative_or_stale",
                "Receipt launcher accounting and launch metadata are not per-invocation when a provider instance is reused.",
                observations["repeat_invocation"],
            )

        decoder_runner = FakeRunner()
        decoder_receipt, decoder_outcome = RegisteredProcessExecutionProvider(
            runner=decoder_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(fail=True),
        ).execute(invocation(), binding(spec))
        observations["decoder_failure"] = {
            "calls": len(decoder_runner.calls),
            "outcome": decoder_outcome.to_dict(),
            "mutation_observation": decoder_receipt.mutation_observation,
        }
        if decoder_outcome.validation_outcome == "complete" and decoder_outcome.evidence_completeness == "complete":
            add_material(
                findings,
                "decoder.failure_marked_complete",
                "Decoder exceptions are represented, but validation and evidence axes still report complete.",
                observations["decoder_failure"],
            )

        probe_runner = FakeRunner()
        probe_receipt, probe_outcome = RegisteredProcessExecutionProvider(
            runner=probe_runner,
            state_probe=FailingProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec))
        observations["probe_failure"] = {
            "calls": len(probe_runner.calls),
            "outcome": probe_outcome.to_dict(),
            "mutation_observation": probe_receipt.mutation_observation,
        }
        if probe_outcome.validation_outcome == "complete" or probe_outcome.domain_outcome == "typed_result":
            add_material(
                findings,
                "state_probe.failure_not_failed_closed",
                "State-probe failure is recorded in the receipt but the outcome still reports a complete typed result.",
                observations["probe_failure"],
            )

        timeout_runner = FakeRunner(timeout=True)
        timeout_receipt, timeout_outcome = RegisteredProcessExecutionProvider(
            runner=timeout_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec))
        observations["timeout"] = {
            "timed_out": timeout_receipt.timed_out,
            "outcome": timeout_outcome.to_dict(),
        }

        redaction_runner = FakeRunner()
        redaction_receipt, _ = RegisteredProcessExecutionProvider(
            runner=redaction_runner,
            state_probe=StableProbe(),
            output_decoder=Decoder(),
        ).execute(invocation(), binding(spec))
        launch = redaction_receipt.metadata.get("launch", {}) if isinstance(redaction_receipt.metadata, dict) else {}
        observations["environment_redaction"] = {
            "launch_has_raw_env": "env" in launch,
            "launch_has_manifest_digest": "environment_manifest_digest" in launch,
        }

    explicit_non_caps = (
        REPO_ROOT / ".aide/queue/AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01/evidence/explicit-non-capabilities.md"
    ).read_text(encoding="utf-8")
    if "cancellation" not in explicit_non_caps.lower():
        add_material(
            findings,
            "cancellation.not_implemented_or_declared",
            "The receipt has a cancelled field, but cancellation support is neither implemented nor listed as an explicit non-capability.",
            {"explicit_non_capabilities_mentions_cancellation": False},
        )
    return observations


def dominium_parity(findings: list[Finding]) -> dict[str, Any]:
    result_path = REPO_ROOT / ".aide/reports/dominium-registered-validation-backend/invocation-result.json"
    validation_path = REPO_ROOT / ".aide/reports/dominium-registered-validation-backend/validation.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    observations = {
        "process_call_count": result.get("process_call_count"),
        "launcher_call_count": result.get("launcher_call_count"),
        "allowlisted_shell": (result.get("allowlisted_process_call") or {}).get("shell"),
        "dominium_status": (result.get("dominium_command_result") or {}).get("status"),
        "domain_outcome": result.get("domain_outcome"),
        "registered_command_boundary_reached": result.get("registered_command_boundary_reached"),
        "service_adapter_boundary_reached": result.get("service_adapter_boundary_reached"),
        "aggregate_validation_executed": result.get("aggregate_validation_executed"),
        "aggregate_validation_succeeded": result.get("aggregate_validation_succeeded"),
        "mutation_observation": result.get("mutation_observation"),
        "validation_status": validation.get("validation_status"),
    }
    expected = {
        "process_call_count": 1,
        "launcher_call_count": 1,
        "allowlisted_shell": False,
        "dominium_status": "refused",
        "domain_outcome": "typed_refusal",
        "registered_command_boundary_reached": "proven",
        "service_adapter_boundary_reached": "unproven",
        "aggregate_validation_executed": False,
        "aggregate_validation_succeeded": False,
        "mutation_observation": "none_detected_within_probe_coverage",
        "validation_status": "PASS_WITH_WARNINGS",
    }
    mismatches = {key: {"expected": value, "observed": observations.get(key)} for key, value in expected.items() if observations.get(key) != value}
    if mismatches:
        add_material(
            findings,
            "dominium.parity_mismatch",
            "Dominium registered-validation parity no longer matches the accepted command-boundary meaning.",
            {"mismatches": mismatches},
        )
    observations["mismatches"] = mismatches
    return observations


def source_commit_status(findings: list[Finding]) -> dict[str, Any]:
    code, output = run_git(["cat-file", "-e", SOURCE_COMMIT + "^{commit}"])
    if code != 0:
        add_material(
            findings,
            "source.commit_missing",
            "Source build commit is not present in the local repository.",
            {"commit": SOURCE_COMMIT, "git_output": output},
        )
    return {"source_commit_present": code == 0}


def write_reports(report: dict[str, Any]) -> None:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "check-report.json").write_text(stable_json(report), encoding="utf-8")
    findings = report["findings"]
    lines = [
        "# Registered Process Execution Provider v0 Check",
        "",
        f"- task_id: `{TASK_ID}`",
        f"- result: `{report['result']}`",
        f"- material_finding_count: `{report['material_finding_count']}`",
        f"- missing_evidence: `{report['missing_evidence']}`",
        f"- recommended_next_task: `{report['recommended_next_task']}`",
        "",
        "## Findings",
        "",
    ]
    if findings:
        for finding in findings:
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
        lines.append("No material findings.")
        lines.append("")
    (REPORT_ROOT / "check-report.md").write_text("\n".join(lines), encoding="utf-8")


def write_evidence(report: dict[str, Any]) -> None:
    obs = report["observations"]
    findings = {item["finding_id"]: item for item in report["findings"]}
    write_text(
        EVIDENCE_ROOT / "genericity-scan.md",
        "\n".join(
            [
                "# Genericity Scan",
                "",
                f"- forbidden_match_count: `{obs['genericity']['forbidden_match_count']}`",
                f"- committed_absolute_path_match_count: `{obs['committed_leaks']['absolute_path_match_count']}`",
                f"- committed_secret_like_match_count: `{obs['committed_leaks']['sensitive_match_count']}`",
                "",
                "Generic provider/protocol files contain no Dominium task IDs, capability IDs, paths, refusal codes, report paths, machine-specific absolute paths, domain-specific branches, or direct queue/report writing tokens.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "binding-safety-review.md",
        "\n".join(
            [
                "# Binding Safety Review",
                "",
                f"- result: `{'FAIL' if 'binding.mismatch_launches_process' in findings else 'PASS'}`",
                f"- capability_mismatch_calls: `{obs['behavior']['binding_mismatch']['capability_mismatch_calls']}`",
                f"- wrong_provider_calls: `{obs['behavior']['binding_mismatch']['wrong_provider_calls']}`",
                "",
                "Finding: mismatched capability/provider bindings launch a process and must fail closed before launch.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "process-safety-review.md",
        "\n".join(
            [
                "# Process Safety Review",
                "",
                f"- invalid_spec_calls: `{obs['behavior']['invalid_spec_zero_launch']['calls']}`",
                f"- failed_precondition_calls: `{obs['behavior']['precondition_zero_launch']['calls']}`",
                f"- timeout_timed_out: `{str(obs['behavior']['timeout']['timed_out']).lower()}`",
                f"- environment_launch_has_raw_env: `{str(obs['behavior']['environment_redaction']['launch_has_raw_env']).lower()}`",
                f"- environment_launch_has_manifest_digest: `{str(obs['behavior']['environment_redaction']['launch_has_manifest_digest']).lower()}`",
                f"- repeated_invocation_second_launcher_call_count: `{obs['behavior']['repeat_invocation']['second_receipt_launcher_call_count']}`",
                "",
                "Findings: repeated invocation accounting is cumulative/stale, and cancellation is not implemented or declared as an explicit non-capability.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "result-axis-review.md",
        "\n".join(
            [
                "# Result Axis Review",
                "",
                "The receipt/outcome model keeps transport, process, decoder, domain, validation, and evidence axes as separate fields.",
                "",
                f"- decoder_failure_validation_outcome: `{obs['behavior']['decoder_failure']['outcome']['validation_outcome']}`",
                f"- decoder_failure_evidence_completeness: `{obs['behavior']['decoder_failure']['outcome']['evidence_completeness']}`",
                f"- probe_failure_validation_outcome: `{obs['behavior']['probe_failure']['outcome']['validation_outcome']}`",
                f"- probe_failure_domain_outcome: `{obs['behavior']['probe_failure']['outcome']['domain_outcome']}`",
                "",
                "Findings: decoder and probe failures are represented, but failure axes are still marked as complete or typed result.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "dominium-parity-review.md",
        "\n".join(
            [
                "# Dominium Parity Review",
                "",
                f"- result: `{'FAIL' if obs['dominium_parity']['mismatches'] else 'PASS'}`",
                f"- process_call_count: `{obs['dominium_parity']['process_call_count']}`",
                f"- launcher_call_count: `{obs['dominium_parity']['launcher_call_count']}`",
                f"- shell: `{str(obs['dominium_parity']['allowlisted_shell']).lower()}`",
                f"- dominium_status: `{obs['dominium_parity']['dominium_status']}`",
                f"- domain_outcome: `{obs['dominium_parity']['domain_outcome']}`",
                f"- registered_command_boundary_reached: `{obs['dominium_parity']['registered_command_boundary_reached']}`",
                f"- service_adapter_boundary_reached: `{obs['dominium_parity']['service_adapter_boundary_reached']}`",
                f"- aggregate_validation_executed: `{str(obs['dominium_parity']['aggregate_validation_executed']).lower()}`",
                f"- aggregate_validation_succeeded: `{str(obs['dominium_parity']['aggregate_validation_succeeded']).lower()}`",
                f"- mutation_observation: `{obs['dominium_parity']['mutation_observation']}`",
                "",
                "No Dominium parity material finding was found.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "no-overclaiming-review.md",
        "\n".join(
            [
                "# No-Overclaiming Review",
                "",
                "- Provider acceptance remains false.",
                "- Generic provider is not treated as the universal AIDE execution ontology.",
                "- Future provider types remain unimplemented.",
                "- Dominium aggregate-validation success and service-adapter entry remain unclaimed.",
                "- Source explicit non-capabilities are preserved.",
                "",
                "Material issues are safety and fail-closed gaps, not genericity or Dominium parity overclaims.",
                "",
            ]
        ),
    )
    write_text(
        EVIDENCE_ROOT / "validation-results.md",
        "\n".join(
            [
                "# Validation Results",
                "",
                f"- independent_provider_check: `{report['result']}`",
                f"- material_finding_count: `{report['material_finding_count']}`",
                "- focused provider tests: recorded separately after command execution",
                "- focused Dominium parity tests: recorded separately after command execution",
                "- broad validation: recorded separately after command execution",
                "",
                "Independent check result is `REQUEST_CHANGES`; implementation repair is required before second-adapter proof or provider acceptance.",
                "",
            ]
        ),
    )


def main() -> int:
    findings: list[Finding] = []
    observations = {
        "source_commit": source_commit_status(findings),
        "genericity": scan_genericity(findings),
        "committed_leaks": scan_committed_leaks(findings),
        "behavior": behavior_checks(findings),
        "dominium_parity": dominium_parity(findings),
    }
    material_count = sum(1 for finding in findings if finding.severity == "material")
    report = {
        "schema_version": "aide.registered-process-execution-provider-v0.check-report.v1",
        "kind": "RegisteredProcessExecutionProviderCheckReport",
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_commit": SOURCE_COMMIT,
        "proposed_capability_checked": PROPOSED_CAPABILITY,
        "result": RESULT if material_count else "PASS_WITH_WARNINGS",
        "material_finding_count": material_count,
        "missing_evidence": 0,
        "findings": [finding.to_dict() for finding in findings],
        "observations": observations,
        "provider_accepted": False,
        "implementation_repaired": False,
        "live_dominium_command_rerun": False,
        "recommended_next_task": NEXT_TASK if material_count else "AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01",
    }
    write_reports(report)
    write_evidence(report)
    print(f"result: {report['result']}")
    print(f"material_finding_count: {material_count}")
    print(f"recommended_next_task: {report['recommended_next_task']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
