from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution.registered_process import (
    DecoderResult,
    PreconditionResult,
    RegisteredProcessExecutionProvider,
    RegisteredProcessSpec,
)
from core.protocol.process_invocation import ArgumentToken, CapabilityBinding, CapabilityInvocation


class FakeRunner:
    def __init__(self, *, stdout: str = "{}", stderr: str = "", returncode: int = 0, timeout: bool = False):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.calls: list[dict] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append({"argv": list(argv), "cwd": cwd, "env": dict(env), "timeout": timeout, "shell": False})
        if self.timeout:
            raise subprocess.TimeoutExpired(list(argv), timeout, output="", stderr="timeout")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class SequenceProbe:
    def __init__(self, before: dict | None = None, after: dict | None = None, coverage: list[str] | None = None, fail_mutation: bool = False):
        self.states = [before or {"tracked": "same", "untracked": "same"}, after or before or {"tracked": "same", "untracked": "same"}]
        self.coverage = coverage or ["tracked", "untracked"]
        self.fail_mutation = fail_mutation
        self.calls = 0

    def capture(self):
        index = min(self.calls, len(self.states) - 1)
        self.calls += 1
        return dict(self.states[index])

    def mutation_observation(self, before_state, after_state):
        if self.fail_mutation:
            raise RuntimeError("probe failed")
        if dict(before_state) == dict(after_state):
            return "none_detected_within_probe_coverage"
        return "mutation_detected_within_probe_coverage"


class StaticPrecondition:
    def __init__(self, ok: bool = True, reason_code: str = "preflight_refused", message: str = "preflight refused"):
        self.ok = ok
        self.reason_code = reason_code
        self.message = message

    def check(self, invocation, binding, spec, before_state):
        return PreconditionResult(self.ok, "" if self.ok else self.reason_code, "" if self.ok else self.message)


class StatusDecoder:
    decoder_id = "status-json-decoder-v0"

    def __init__(self, *, raise_error: bool = False):
        self.raise_error = raise_error

    def decode(self, stdout, stderr, returncode):
        if self.raise_error:
            raise RuntimeError("decoder failed")
        if not stdout:
            return DecoderResult("refused", "none", reason_code="empty_output", message="empty output")
        if not stdout.startswith("{"):
            return DecoderResult("refused", "none", reason_code="malformed_output", message="malformed output")
        if '"status": "refused"' in stdout:
            return DecoderResult("decoded", "typed_refusal", domain_result={"status": "refused"}, refusal={"status": "refused"})
        return DecoderResult("decoded", "typed_result", domain_result={"status": "ok"})


class ReplacementScrubber:
    scrubber_id = "replacement-scrubber-v0"

    def __init__(self, *needles: str):
        self.needles = needles

    def scrub(self, text: str) -> str:
        result = text
        for index, needle in enumerate(self.needles):
            result = result.replace(needle, f"<redacted-{index}>")
        return result


def make_spec(executable: Path, workspace: Path, *, digest: str = "", timeout: float = 5.0) -> RegisteredProcessSpec:
    return RegisteredProcessSpec(
        capability_ref="aide://capability/test-registered-process",
        executable=str(executable),
        argument_plan=[
            ArgumentToken("literal", "--mode"),
            ArgumentToken("bounded_invocation_value", "check"),
            ArgumentToken("workspace_path", str(workspace)),
        ],
        working_directory=str(workspace),
        timeout_seconds=timeout,
        environment={"PYTHONHASHSEED": "0", "CUSTOM_ALLOWED": "1"},
        decoder_id="status-json-decoder-v0",
        state_probe_id="test-state-probe-v0",
        mutation_policy="none_detected_within_probe_coverage",
        scrubber_id="replacement-scrubber-v0",
        provider_spec_ref="aide://provider-spec/test-registered-process",
        conformance_profile_ref="aide://conformance-profile/test-registered-process",
        executable_digest=digest,
    )


def binding(spec) -> CapabilityBinding:
    return CapabilityBinding(
        capability_ref="aide://capability/test-registered-process",
        provider_id=RegisteredProcessExecutionProvider.provider_id,
        provider_spec_ref=getattr(spec, "provider_spec_ref", ""),
        provider_spec=spec,
        decoder_id="status-json-decoder-v0",
        state_probe_id="test-state-probe-v0",
        scrubber_id="replacement-scrubber-v0",
        conformance_profile_ref="aide://conformance-profile/test-registered-process",
    )


def invocation() -> CapabilityInvocation:
    return CapabilityInvocation(
        invocation_ref="aide://invocation/test-registered-process-01",
        capability_ref="aide://capability/test-registered-process",
    )


class RegisteredProcessProviderTests(unittest.TestCase):
    def test_preflight_refusals_and_invalid_specs_do_not_launch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "tool.py"
            executable.write_text("print('ok')\n", encoding="utf-8")
            spec = make_spec(executable, root)
            runner = FakeRunner(stdout='{"status": "ok"}')
            provider = RegisteredProcessExecutionProvider(
                runner=runner,
                precondition=StaticPrecondition(False, "wrong_workspace_identity", "wrong workspace identity"),
                state_probe=SequenceProbe(),
                output_decoder=StatusDecoder(),
                stream_scrubber=ReplacementScrubber(),
            )
            receipt, outcome = provider.execute(invocation(), binding(spec))
            self.assertEqual(receipt.launcher_call_count, 0)
            self.assertEqual(runner.calls, [])
            self.assertEqual(outcome.reason_code, "wrong_workspace_identity")

            missing = make_spec(root / "missing-tool.py", root)
            receipt, outcome = RegisteredProcessExecutionProvider(runner=runner).execute(invocation(), binding(missing))
            self.assertEqual(receipt.launcher_call_count, 0)
            self.assertEqual(outcome.reason_code, "missing_executable")

            mismatch = make_spec(executable, root, digest="sha256:not-real")
            receipt, outcome = RegisteredProcessExecutionProvider(runner=runner).execute(invocation(), binding(mismatch))
            self.assertEqual(receipt.launcher_call_count, 0)
            self.assertEqual(outcome.reason_code, "digest_mismatch")

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
            receipt, outcome = RegisteredProcessExecutionProvider(runner=runner).execute(invocation(), binding(invalid))
            self.assertEqual(receipt.launcher_call_count, 0)
            self.assertEqual(outcome.reason_code, "invalid_spec")

    def test_exact_argv_shell_false_environment_and_deterministic_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "tool.py"
            executable.write_text("print('ok')\n", encoding="utf-8")
            spec = make_spec(executable, root)
            runner = FakeRunner(stdout='{"status": "ok"}', stderr="clean")
            provider = RegisteredProcessExecutionProvider(
                runner=runner,
                precondition=StaticPrecondition(),
                state_probe=SequenceProbe(),
                output_decoder=StatusDecoder(),
                stream_scrubber=ReplacementScrubber(),
            )
            receipt, outcome = provider.execute(invocation(), binding(spec))
            self.assertEqual(outcome.domain_outcome, "typed_result")
            self.assertEqual(receipt.launcher_call_count, 1)
            self.assertFalse(receipt.shell)
            self.assertEqual(runner.calls[0]["argv"], [str(executable), "--mode", "check", str(root)])
            self.assertEqual(str(runner.calls[0]["cwd"]), str(root))
            self.assertEqual(runner.calls[0]["env"], {"PYTHONHASHSEED": "0", "CUSTOM_ALLOWED": "1"})
            first = receipt.to_dict()
            self.assertNotIn("env", first["metadata"]["launch"])
            self.assertIn("environment_manifest_digest", first["metadata"]["launch"])
            self.assertEqual(receipt.mutation_observation, "none_detected_within_probe_coverage")

            runner2 = FakeRunner(stdout='{"status": "ok"}', stderr="clean")
            receipt2, _ = RegisteredProcessExecutionProvider(
                runner=runner2,
                precondition=StaticPrecondition(),
                state_probe=SequenceProbe(),
                output_decoder=StatusDecoder(),
                stream_scrubber=ReplacementScrubber(),
            ).execute(invocation(), binding(spec))
            self.assertEqual(first["argv_digest"], receipt2.to_dict()["argv_digest"])
            self.assertEqual(first["redacted_environment_manifest_digest"], receipt2.to_dict()["redacted_environment_manifest_digest"])

    def test_timeout_and_decoder_outcomes_are_separate_from_process_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "tool.py"
            executable.write_text("print('ok')\n", encoding="utf-8")
            spec = make_spec(executable, root)

            timeout_receipt, timeout_outcome = RegisteredProcessExecutionProvider(
                runner=FakeRunner(timeout=True),
                state_probe=SequenceProbe(),
                output_decoder=StatusDecoder(),
            ).execute(invocation(), binding(spec))
            self.assertTrue(timeout_receipt.timed_out)
            self.assertEqual(timeout_outcome.process_outcome, "timed_out")
            self.assertEqual(timeout_outcome.decoder_outcome, "not_decoded")

            cases = [
                (FakeRunner(stdout='{"status": "refused"}', returncode=1), "exit_nonzero", "typed_refusal", "decoded"),
                (FakeRunner(stdout="", returncode=1), "exit_nonzero", "none", "refused"),
                (FakeRunner(stdout="not-json", returncode=0), "exit_zero", "none", "refused"),
            ]
            for runner, process_outcome, domain_outcome, decoder_outcome in cases:
                _, outcome = RegisteredProcessExecutionProvider(
                    runner=runner,
                    state_probe=SequenceProbe(),
                    output_decoder=StatusDecoder(),
                ).execute(invocation(), binding(spec))
                self.assertEqual(outcome.process_outcome, process_outcome)
                self.assertEqual(outcome.domain_outcome, domain_outcome)
                self.assertEqual(outcome.decoder_outcome, decoder_outcome)

            _, exception_outcome = RegisteredProcessExecutionProvider(
                runner=FakeRunner(stdout='{"status": "ok"}'),
                state_probe=SequenceProbe(),
                output_decoder=StatusDecoder(raise_error=True),
            ).execute(invocation(), binding(spec))
            self.assertEqual(exception_outcome.decoder_outcome, "exception")

    def test_state_probe_mutation_failure_partial_coverage_and_scrubbing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "tool.py"
            executable.write_text("print('ok')\n", encoding="utf-8")
            spec = make_spec(executable, root)
            secret = "sk-testsecret0000000000000000"
            runner = FakeRunner(stdout=f'{{"status": "ok", "path": "{root}", "token": "{secret}"}}')
            receipt, outcome = RegisteredProcessExecutionProvider(
                runner=runner,
                state_probe=SequenceProbe(before={"tracked": "a"}, after={"tracked": "b"}, coverage=["tracked"]),
                output_decoder=StatusDecoder(),
                stream_scrubber=ReplacementScrubber(str(root), secret),
            ).execute(invocation(), binding(spec))
            self.assertEqual(outcome.domain_outcome, "typed_result")
            self.assertEqual(receipt.mutation_observation, "mutation_detected_within_probe_coverage")
            self.assertEqual(receipt.probe_coverage, ["tracked"])
            self.assertNotIn(str(root), receipt.stdout["excerpt"])
            self.assertNotIn(secret, receipt.stdout["excerpt"])
            self.assertEqual(receipt.capability_ref, "aide://capability/test-registered-process")
            self.assertEqual(receipt.invocation_ref, "aide://invocation/test-registered-process-01")
            self.assertEqual(receipt.provider_ref, RegisteredProcessExecutionProvider.provider_id)

            failure_receipt, _ = RegisteredProcessExecutionProvider(
                runner=FakeRunner(stdout='{"status": "ok"}'),
                state_probe=SequenceProbe(fail_mutation=True),
                output_decoder=StatusDecoder(),
            ).execute(invocation(), binding(spec))
            self.assertTrue(failure_receipt.mutation_observation.startswith("probe_failure:"))

    def test_generic_provider_sources_do_not_embed_domain_names(self) -> None:
        generic_paths = [REPO_ROOT / "core/execution/registered_process.py", REPO_ROOT / "core/execution/provider.py"]
        for path in generic_paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("dominium", text.lower())
            self.assertNotIn("validation.run", text.lower())


if __name__ == "__main__":
    unittest.main()
