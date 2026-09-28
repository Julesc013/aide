"""Registered local process execution provider v0.

This provider executes immutable registered process specs only. It is not a
general command runner and exposes no CLI or discovery surface.
"""

from __future__ import annotations

import hashlib
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from core.protocol.execution_receipt import (
    CapabilityOutcome,
    ProcessExecutionReceipt,
    digest_json,
    stream_summary,
)
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


PROVIDER_ID = "registered_process_execution_provider_v0"
TRANSPORT_REFUSED = "transport_refused"
TRANSPORT_STARTED = "transport_started"
TRANSPORT_TIMEOUT = "transport_timeout"
CANCELLATION_SUPPORTED = False
EXPLICIT_NON_CAPABILITIES = ("process_cancellation",)


class CompletedProcessLike(Protocol):
    stdout: str
    stderr: str
    returncode: int


class Runner(Protocol):
    def __call__(
        self,
        argv: Sequence[str],
        cwd: Path,
        env: Mapping[str, str],
        timeout: float,
    ) -> CompletedProcessLike:
        """Launch exactly one registered process invocation."""


class WorkspacePrecondition(Protocol):
    def check(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
        spec: "RegisteredProcessSpec",
        before_state: Mapping[str, Any],
    ) -> "PreconditionResult":
        """Return whether launch is permitted for this immutable spec."""


class StateProbe(Protocol):
    coverage: Sequence[str]

    def capture(self) -> Mapping[str, Any]:
        """Capture provider-specific state evidence."""

    def mutation_observation(
        self,
        before_state: Mapping[str, Any],
        after_state: Mapping[str, Any],
    ) -> str:
        """Describe mutation only within the probe's declared coverage."""


class OutputDecoder(Protocol):
    decoder_id: str

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> "DecoderResult":
        """Decode process output into neutral decoder/domain status."""


class StreamScrubber(Protocol):
    scrubber_id: str

    def scrub(self, text: str) -> str:
        """Remove local or secret-like values from committed stream summaries."""


@dataclass(frozen=True)
class PreconditionResult:
    ok: bool
    reason_code: str = ""
    message: str = ""


@dataclass(frozen=True)
class DecoderResult:
    decoder_outcome: str
    domain_outcome: str
    domain_result: Mapping[str, Any] | None = None
    refusal: Mapping[str, Any] | None = None
    reason_code: str = ""
    message: str = ""


@dataclass(frozen=True)
class RegisteredProcessSpec:
    capability_ref: str
    executable: str
    argument_plan: Sequence[ArgumentToken]
    working_directory: str
    timeout_seconds: float
    environment: Mapping[str, str]
    decoder_id: str
    state_probe_id: str
    mutation_policy: str
    scrubber_id: str
    provider_ref: str = PROVIDER_ID
    executable_digest: str = ""
    allowed_exit_codes: Sequence[int] | None = None
    stdout_limit: int = 800
    stderr_limit: int = 800
    provider_spec_ref: str = ""
    conformance_profile_ref: str = ""
    immutable: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.capability_ref:
            errors.append("capability_ref is required")
        if not self.executable:
            errors.append("executable is required")
        if not self.argument_plan:
            errors.append("argument_plan is required")
        if not self.working_directory:
            errors.append("working_directory is required")
        if self.timeout_seconds <= 0:
            errors.append("timeout_seconds must be positive")
        if not self.decoder_id:
            errors.append("decoder_id is required")
        if not self.state_probe_id:
            errors.append("state_probe_id is required")
        if not self.scrubber_id:
            errors.append("scrubber_id is required")
        if not self.immutable:
            errors.append("registered specs must be immutable")
        return errors

    def argv(self) -> list[str]:
        return [self.executable, *[token.value for token in self.argument_plan]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_ref": self.capability_ref,
            "executable": self.executable,
            "argument_plan": [token.to_dict() for token in self.argument_plan],
            "working_directory": self.working_directory,
            "timeout_seconds": self.timeout_seconds,
            "environment_keys": sorted(self.environment),
            "decoder_id": self.decoder_id,
            "state_probe_id": self.state_probe_id,
            "mutation_policy": self.mutation_policy,
            "scrubber_id": self.scrubber_id,
            "provider_ref": self.provider_ref,
            "executable_digest": self.executable_digest,
            "allowed_exit_codes": list(self.allowed_exit_codes) if self.allowed_exit_codes is not None else None,
            "stdout_limit": self.stdout_limit,
            "stderr_limit": self.stderr_limit,
            "provider_spec_ref": self.provider_spec_ref,
            "conformance_profile_ref": self.conformance_profile_ref,
            "immutable": self.immutable,
            "metadata": dict(self.metadata),
        }


@dataclass
class StaticStateProbe:
    coverage: Sequence[str] = field(default_factory=lambda: ["not_declared"])
    state: Mapping[str, Any] = field(default_factory=dict)

    def capture(self) -> Mapping[str, Any]:
        return dict(self.state)

    def mutation_observation(
        self,
        before_state: Mapping[str, Any],
        after_state: Mapping[str, Any],
    ) -> str:
        if dict(before_state) == dict(after_state):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


@dataclass
class NoopPrecondition:
    def check(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
        spec: RegisteredProcessSpec,
        before_state: Mapping[str, Any],
    ) -> PreconditionResult:
        return PreconditionResult(True)


@dataclass
class IdentityScrubber:
    scrubber_id: str = "identity_stream_scrubber_v0"

    def scrub(self, text: str) -> str:
        return text


@dataclass
class JsonObjectDecoder:
    decoder_id: str = "json_object_decoder_v0"

    def decode(self, stdout: str, stderr: str, returncode: int | None) -> DecoderResult:
        import json

        if not stdout.strip():
            return DecoderResult("refused", "none", reason_code="empty_output", message="stdout was empty")
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            return DecoderResult("refused", "none", reason_code="malformed_output", message="stdout was not JSON")
        if not isinstance(payload, dict):
            return DecoderResult("refused", "none", reason_code="malformed_output", message="stdout JSON was not an object")
        status = str(payload.get("status", "")).lower()
        if status == "refused":
            return DecoderResult("decoded", "typed_refusal", domain_result=payload, refusal=payload)
        return DecoderResult("decoded", "typed_result", domain_result=payload)


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


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _environment_manifest(environment: Mapping[str, str]) -> dict[str, Any]:
    return {
        "keys": sorted(environment),
        "value_digests": {key: digest_json(str(environment[key])) for key in sorted(environment)},
    }


def _executable_identity(spec: RegisteredProcessSpec) -> str:
    declared = spec.metadata.get("executable_identity") if isinstance(spec.metadata, Mapping) else ""
    if declared:
        return str(declared)
    if spec.executable:
        return Path(spec.executable).name
    return ""


def _zero_receipt(
    *,
    invocation: CapabilityInvocation,
    binding: CapabilityBinding,
    spec: RegisteredProcessSpec,
    before_state: Mapping[str, Any],
    after_state: Mapping[str, Any],
    mutation_observation: str,
    probe_coverage: Sequence[str],
    reason: str,
    provider_ref: str | None = None,
) -> ProcessExecutionReceipt:
    argv = spec.argv() if spec.executable else []
    return ProcessExecutionReceipt(
        capability_ref=invocation.capability_ref,
        invocation_ref=invocation.invocation_ref,
        provider_ref=provider_ref or binding.provider_id,
        launcher_call_count=0,
        executable_identity=_executable_identity(spec),
        executable_digest=spec.executable_digest,
        argv_digest=digest_json(argv),
        redacted_environment_manifest_digest=digest_json(_environment_manifest(spec.environment)),
        return_code=None,
        timed_out=False,
        cancelled=False,
        stdout=stream_summary("", limit=spec.stdout_limit),
        stderr=stream_summary(reason, limit=spec.stderr_limit),
        decoder_ref=binding.decoder_id or spec.decoder_id,
        before_state_ref=digest_json(before_state),
        after_state_ref=digest_json(after_state),
        mutation_observation=mutation_observation,
        probe_coverage=list(probe_coverage),
        started_at="deterministic",
        ended_at="deterministic",
        shell=False,
        working_directory_ref=digest_json(spec.working_directory),
        metadata={
            "before_state": dict(before_state),
            "after_state": dict(after_state),
            "launch": None,
        },
    )


def _binding_errors(
    invocation: CapabilityInvocation,
    binding: CapabilityBinding,
    spec: RegisteredProcessSpec,
    provider_id: str,
) -> list[str]:
    errors: list[str] = []
    if binding.provider_id != provider_id:
        errors.append("binding provider_id does not match this provider")
    if spec.provider_ref != provider_id:
        errors.append("spec provider_ref does not match this provider")
    if invocation.capability_ref != binding.capability_ref:
        errors.append("invocation capability_ref does not match binding capability_ref")
    if binding.capability_ref != spec.capability_ref:
        errors.append("binding capability_ref does not match spec capability_ref")
    if binding.provider_spec_ref and spec.provider_spec_ref and binding.provider_spec_ref != spec.provider_spec_ref:
        errors.append("binding provider_spec_ref does not match spec provider_spec_ref")
    if binding.decoder_id and binding.decoder_id != spec.decoder_id:
        errors.append("binding decoder_id does not match spec decoder_id")
    if binding.state_probe_id and binding.state_probe_id != spec.state_probe_id:
        errors.append("binding state_probe_id does not match spec state_probe_id")
    if binding.scrubber_id and binding.scrubber_id != spec.scrubber_id:
        errors.append("binding scrubber_id does not match spec scrubber_id")
    if (
        binding.conformance_profile_ref
        and spec.conformance_profile_ref
        and binding.conformance_profile_ref != spec.conformance_profile_ref
    ):
        errors.append("binding conformance_profile_ref does not match spec conformance_profile_ref")
    return errors


def _probe_failure_reason(state: Mapping[str, Any]) -> str:
    if "probe_error" not in state:
        return ""
    detail = str(state.get("probe_error") or "unknown")
    message = str(state.get("message") or "")
    return f"probe_failure:{detail}" + (f":{message}" if message else "")


def _validation_and_evidence_axes(*, decoder_result: DecoderResult, probe_failed: bool, timed_out: bool) -> tuple[str, str]:
    if probe_failed or timed_out or decoder_result.decoder_outcome != "decoded":
        return "incomplete", "incomplete"
    return "complete", "complete"


class RegisteredProcessExecutionProvider:
    provider_id = PROVIDER_ID

    def __init__(
        self,
        *,
        runner: Runner | None = None,
        precondition: WorkspacePrecondition | None = None,
        state_probe: StateProbe | None = None,
        output_decoder: OutputDecoder | None = None,
        stream_scrubber: StreamScrubber | None = None,
    ) -> None:
        self.runner = runner or default_process_runner
        self.precondition = precondition or NoopPrecondition()
        self.state_probe = state_probe or StaticStateProbe()
        self.output_decoder = output_decoder or JsonObjectDecoder()
        self.stream_scrubber = stream_scrubber or IdentityScrubber()
        self.launches: list[dict[str, Any]] = []

    def execute(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
    ) -> tuple[ProcessExecutionReceipt, CapabilityOutcome]:
        spec = binding.provider_spec
        if not isinstance(spec, RegisteredProcessSpec):
            empty = RegisteredProcessSpec(
                capability_ref=invocation.capability_ref,
                executable="",
                argument_plan=[],
                working_directory=".",
                timeout_seconds=1.0,
                environment={},
                decoder_id=binding.decoder_id,
                state_probe_id=binding.state_probe_id,
                mutation_policy="none_detected_within_probe_coverage",
                scrubber_id=binding.scrubber_id,
            )
            before = self._capture_state()
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=empty,
                before_state=before,
                after_state=before,
                mutation_observation="unproven_invalid_spec",
                probe_coverage=self._coverage(),
                reason="binding provider_spec is not a RegisteredProcessSpec",
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "invalid_spec",
                "incomplete",
                reason_code="invalid_spec",
                message="binding provider_spec is not a RegisteredProcessSpec",
            )

        before_state = self._capture_state()
        before_probe_failure = _probe_failure_reason(before_state)
        if before_probe_failure:
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation=before_probe_failure,
                probe_coverage=self._coverage(),
                reason=before_probe_failure,
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "state_probe_failure",
                "incomplete",
                reason_code="state_probe_failure",
                message=before_probe_failure,
            )
        validation_errors = spec.validate()
        if validation_errors:
            message = "; ".join(validation_errors)
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation="none_detected_within_probe_coverage",
                probe_coverage=self._coverage(),
                reason=message,
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "invalid_spec",
                "incomplete",
                reason_code="invalid_spec",
                message=message,
            )

        binding_errors = _binding_errors(invocation, binding, spec, self.provider_id)
        if binding_errors:
            message = "; ".join(binding_errors)
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation="none_detected_within_probe_coverage",
                probe_coverage=self._coverage(),
                reason=message,
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "binding_mismatch",
                "incomplete",
                reason_code="binding_mismatch",
                message=message,
            )

        executable = Path(spec.executable)
        if not executable.exists() or not executable.is_file():
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation="none_detected_within_probe_coverage",
                probe_coverage=self._coverage(),
                reason="registered executable is missing",
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "missing_executable",
                "incomplete",
                reason_code="missing_executable",
                message="registered executable is missing",
            )

        executable_digest = _file_digest(executable)
        if spec.executable_digest and executable_digest != spec.executable_digest:
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation="none_detected_within_probe_coverage",
                probe_coverage=self._coverage(),
                reason="registered executable digest mismatch",
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "digest_mismatch",
                "incomplete",
                reason_code="digest_mismatch",
                message="registered executable digest mismatch",
            )

        precondition = self.precondition.check(invocation, binding, spec, before_state)
        if not precondition.ok:
            receipt = _zero_receipt(
                invocation=invocation,
                binding=binding,
                spec=spec,
                before_state=before_state,
                after_state=before_state,
                mutation_observation="none_detected_within_probe_coverage",
                probe_coverage=self._coverage(),
                reason=precondition.message,
                provider_ref=self.provider_id,
            )
            return receipt, CapabilityOutcome(
                TRANSPORT_REFUSED,
                "not_started",
                "not_decoded",
                "none",
                "precondition_refused",
                "incomplete",
                reason_code=precondition.reason_code,
                message=precondition.message,
            )

        argv = spec.argv()
        cwd = Path(spec.working_directory)
        stdout = ""
        stderr = ""
        returncode: int | None = None
        timed_out = False
        environment_manifest = _environment_manifest(spec.environment)
        launch_record = {
            "argv": list(argv),
            "cwd": str(cwd),
            "environment_manifest": environment_manifest,
            "environment_manifest_digest": digest_json(environment_manifest),
            "timeout": spec.timeout_seconds,
            "shell": False,
        }
        self.launches.append(launch_record)
        try:
            completed = self.runner(argv, cwd, dict(spec.environment), spec.timeout_seconds)
            stdout = str(completed.stdout or "")
            stderr = str(completed.stderr or "")
            returncode = int(completed.returncode)
        except subprocess.TimeoutExpired as exc:
            stdout = str(exc.stdout or "")
            stderr = str(exc.stderr or "")
            timed_out = True

        probe_failed = False
        try:
            after_state = self._capture_state()
            after_probe_failure = _probe_failure_reason(after_state)
            if after_probe_failure:
                probe_failed = True
                mutation_observation = after_probe_failure
            else:
                mutation_observation = self.state_probe.mutation_observation(before_state, after_state)
        except Exception as exc:  # pragma: no cover - defensive fallback
            after_state = {}
            probe_failed = True
            mutation_observation = f"probe_failure:{type(exc).__name__}"

        decoder_result: DecoderResult
        if probe_failed:
            decoder_result = DecoderResult(
                "not_decoded",
                "none",
                reason_code="state_probe_failure",
                message=mutation_observation,
            )
        elif timed_out:
            decoder_result = DecoderResult("not_decoded", "none", reason_code="timeout", message="registered process timed out")
        else:
            try:
                decoder_result = self.output_decoder.decode(stdout, stderr, returncode)
            except Exception as exc:
                decoder_result = DecoderResult("exception", "none", reason_code="decoder_exception", message=str(exc))

        process_outcome = "timed_out" if timed_out else ("exit_zero" if returncode == 0 else "exit_nonzero")
        validation_outcome, evidence_completeness = _validation_and_evidence_axes(
            decoder_result=decoder_result,
            probe_failed=probe_failed,
            timed_out=timed_out,
        )
        receipt = ProcessExecutionReceipt(
            capability_ref=invocation.capability_ref,
            invocation_ref=invocation.invocation_ref,
            provider_ref=self.provider_id,
            launcher_call_count=1,
            executable_identity=_executable_identity(spec),
            executable_digest=executable_digest,
            argv_digest=digest_json(argv),
            redacted_environment_manifest_digest=digest_json(environment_manifest),
            return_code=returncode,
            timed_out=timed_out,
            cancelled=False,
            stdout=stream_summary(self.stream_scrubber.scrub(stdout), limit=spec.stdout_limit),
            stderr=stream_summary(self.stream_scrubber.scrub(stderr), limit=spec.stderr_limit),
            decoder_ref=binding.decoder_id or spec.decoder_id,
            before_state_ref=digest_json(before_state),
            after_state_ref=digest_json(after_state),
            mutation_observation=mutation_observation,
            probe_coverage=self._coverage(),
            started_at="deterministic",
            ended_at="deterministic",
            shell=False,
            working_directory_ref=digest_json(str(cwd)),
            metadata={
                "before_state": dict(before_state),
                "after_state": dict(after_state),
                "launch": launch_record,
            },
        )
        outcome = CapabilityOutcome(
            TRANSPORT_TIMEOUT if timed_out else TRANSPORT_STARTED,
            process_outcome,
            decoder_result.decoder_outcome,
            decoder_result.domain_outcome,
            validation_outcome,
            evidence_completeness,
            reason_code=decoder_result.reason_code,
            message=decoder_result.message,
            domain_result=decoder_result.domain_result,
            refusal=decoder_result.refusal,
        )
        return receipt, outcome

    def _capture_state(self) -> Mapping[str, Any]:
        try:
            return self.state_probe.capture()
        except Exception as exc:
            return {"probe_error": type(exc).__name__, "message": str(exc)}

    def _coverage(self) -> list[str]:
        return list(getattr(self.state_probe, "coverage", []) or [])
