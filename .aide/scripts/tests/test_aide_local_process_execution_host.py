from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution import local_process_host as host


def write_text(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def create_aide_fixture(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True, text=True)
    run_git(root, "config", "user.email", "aide-tests@example.invalid")
    run_git(root, "config", "user.name", "AIDE Tests")
    write_text(
        root,
        host.FIXTURE_WORKER_REL.as_posix(),
        "import json\nprint(json.dumps({'schema_version':'aide.local-process-reference-worker-result.v0'}))\n",
    )
    write_text(root, host.HOST_MODULE_REL.as_posix(), "fixture local_process_host module\n")
    write_text(root, host.PROVIDER_REL.as_posix(), "fixture registered process provider\n")
    write_text(root, host.PROCESS_INVOCATION_REL.as_posix(), "fixture process invocation\n")
    write_text(root, host.EXECUTION_RECEIPT_REL.as_posix(), "fixture execution receipt\n")
    write_text(root, host.AIDE_LITE_REL.as_posix(), "fixture aide lite\n")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "fixture: add local process host sources")
    return run_git(root, "rev-parse", "HEAD")


def success_stdout(extra: str = "") -> str:
    payload = {
        "schema_version": "aide.local-process-reference-worker-result.v0",
        "worker_kind": "local_reference_worker",
        "run_id": host.RUN_REF,
        "workunit_ref": host.TASK_ID,
        "status": "PASS",
        "event_count": 3,
        "artifact_count": 1,
        "network_call_performed": False,
        "provider_or_model_called": False,
        "repository_mutation_performed": False,
        "preview_or_apply_performed": False,
        "release_or_promotion_performed": False,
        "detail": extra,
    }
    return json.dumps(payload, sort_keys=True)


class FakeRunner:
    def __init__(
        self,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int = 0,
        timeout: bool = False,
        mutate: Path | None = None,
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.mutate = mutate
        self.calls: list[dict] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append({"argv": list(argv), "cwd": cwd, "env": dict(env), "timeout": timeout, "shell": False})
        if self.mutate is not None:
            self.mutate.write_text("changed\n", encoding="utf-8")
        if self.timeout:
            raise subprocess.TimeoutExpired(list(argv), timeout, output="", stderr="timeout")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class LocalProcessExecutionHostTests(unittest.TestCase):
    def test_exact_argv_environment_and_exactly_one_process_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            fake = FakeRunner(stdout=success_stdout())

            result = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )

            self.assertEqual(result["result"], "PASS")
            self.assertEqual(result["process_call_count"], 1)
            self.assertTrue(result["reference_worker_process_started"])
            self.assertTrue(result["local_process_execution_host_implemented"])
            self.assertEqual(result["provider_ref"], "registered_process_execution_provider_v0")
            self.assertEqual(len(fake.calls), 1)
            call = fake.calls[0]
            self.assertEqual(call["argv"][0], str(Path(sys.executable).resolve()))
            self.assertEqual(Path(call["argv"][1]), root / host.FIXTURE_WORKER_REL)
            self.assertEqual(call["argv"][2:], ["--run-id", host.RUN_REF, "--workunit-ref", host.TASK_ID, "--json"])
            self.assertEqual(Path(call["cwd"]), root)
            self.assertFalse(call["shell"])
            self.assertEqual(call["env"]["PYTHONDONTWRITEBYTECODE"], "1")
            self.assertEqual(call["env"]["PYTHONNOUSERSITE"], "1")
            self.assertEqual(call["env"]["PYTHONUTF8"], "1")
            self.assertEqual(call["env"]["PYTHONHASHSEED"], "0")

    def test_invalid_preconditions_cause_zero_process_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            fake = FakeRunner(stdout=success_stdout())

            unsupported = host.run_host(
                root,
                expected_revision=revision,
                capability_id="aide.future.unsupported",
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(unsupported["reason_code"], host.REFUSAL_CODES["unsupported_capability"])
            self.assertEqual(unsupported["process_call_count"], 0)

            wrong_revision = host.run_host(
                root,
                expected_revision="0" * 40,
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(wrong_revision["reason_code"], host.REFUSAL_CODES["revision_mismatch"])
            self.assertEqual(wrong_revision["process_call_count"], 0)

            changed_digests = {rel.as_posix(): "sha256:" + ("0" * 64) for rel in host.RELEVANT_SOURCE_RELS}
            digest_mismatch = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                expected_digests=changed_digests,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(digest_mismatch["reason_code"], host.REFUSAL_CODES["digest_mismatch"])
            self.assertEqual(digest_mismatch["process_call_count"], 0)
            self.assertEqual(fake.calls, [])

    def test_timeout_malformed_nonzero_and_schema_refusals_are_typed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)

            timeout = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(timeout=True),
                write_reports=False,
            )
            self.assertEqual(timeout["reason_code"], host.REFUSAL_CODES["timeout"])
            self.assertEqual(timeout["process_call_count"], 1)

            malformed = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout="not json"),
                write_reports=False,
            )
            self.assertEqual(malformed["reason_code"], host.REFUSAL_CODES["malformed_json"])

            nonzero = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(), returncode=2),
                write_reports=False,
            )
            self.assertEqual(nonzero["reason_code"], host.REFUSAL_CODES["nonzero_exit"])

            bad_schema = json.loads(success_stdout())
            bad_schema["network_call_performed"] = True
            schema = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=json.dumps(bad_schema)),
                write_reports=False,
            )
            self.assertEqual(schema["reason_code"], host.REFUSAL_CODES["schema_mismatch"])

    def test_deterministic_projection_report_scrubbing_and_shared_models(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            secret_like = "sk-" + "testsecret000000"
            stderr = f"path={root} token={secret_like}"

            first = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(str(root)), stderr=stderr),
            )
            first_projection = (root / host.PROJECTION_JSON).read_text(encoding="utf-8")
            second = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(str(root)), stderr=stderr),
            )
            second_projection = (root / host.PROJECTION_JSON).read_text(encoding="utf-8")

            self.assertEqual(first["validation_status"], "PASS_WITH_WARNINGS")
            self.assertEqual(second["validation_status"], "PASS_WITH_WARNINGS")
            self.assertEqual(first_projection, second_projection)
            receipt = host.read_json(root / host.EXECUTION_RECEIPT_JSON)
            outcome = host.read_json(root / host.CAPABILITY_OUTCOME_JSON)
            self.assertEqual(receipt["provider_ref"], "registered_process_execution_provider_v0")
            self.assertEqual(outcome["domain_outcome"], "typed_result")
            for path in (root / host.REPORT_ROOT).rglob("*"):
                if path.is_file():
                    text = path.read_text(encoding="utf-8", errors="replace")
                    self.assertNotIn(str(root), text)
                    self.assertNotIn(secret_like, text)

    def test_unexpected_repository_mutation_is_refused_after_process(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            target = root / host.FIXTURE_WORKER_REL

            result = host.run_host(
                root,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(), mutate=target),
                write_reports=False,
            )

            self.assertEqual(result["reason_code"], host.REFUSAL_CODES["unexpected_mutation"])
            self.assertEqual(result["process_call_count"], 1)
            self.assertFalse(result["workspace_state_unchanged"])


if __name__ == "__main__":
    unittest.main()
