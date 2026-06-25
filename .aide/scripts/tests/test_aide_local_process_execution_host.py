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
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True, shell=False)
    return result.stdout.strip()


def create_aide_fixture(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True, text=True, shell=False)
    run_git(root, "config", "user.email", "aide-tests@example.invalid")
    run_git(root, "config", "user.name", "AIDE Tests")
    source_worker = REPO_ROOT / host.FIXTURE_WORKER_REL
    write_text(root, host.FIXTURE_WORKER_REL.as_posix(), source_worker.read_text(encoding="utf-8"))
    write_text(root, host.HOST_MODULE_REL.as_posix(), "fixture local_process_host module\n")
    write_text(root, host.PROVIDER_REL.as_posix(), "fixture registered process provider\n")
    write_text(root, host.PROCESS_INVOCATION_REL.as_posix(), "fixture process invocation\n")
    write_text(root, host.EXECUTION_RECEIPT_REL.as_posix(), "fixture execution receipt\n")
    write_text(root, host.AIDE_LITE_REL.as_posix(), "fixture aide lite\n")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "fixture: add local process host sources")
    return run_git(root, "rev-parse", "HEAD")


def stable_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def event(kind: str, sequence: int, payload: dict | None = None, *, run_ref: str = host.RUN_REF) -> dict:
    return {
        "schema_version": host.FIXTURE_EVENT_SCHEMA,
        "run_ref": run_ref,
        "sequence": sequence,
        "event_kind": kind,
        "timestamp": host.DETERMINISTIC_TIMESTAMP,
        "payload": payload or {},
    }


def event_stream(*, artifact_path: str = host.ARTIFACT_MEMBER, artifact_text: str | None = None, run_ref: str = host.RUN_REF) -> str:
    if artifact_text is None:
        artifact_text = stable_json({"fixture_version": "test", "result": "PASS", "run_ref": host.RUN_REF, "workunit_ref": host.TASK_ID})
    digest = host.sha256_text(artifact_text)
    size = len(artifact_text.encode("utf-8"))
    events = [
        event("run_created", 1, {"workunit_ref": host.WORKUNIT_REF}, run_ref=run_ref),
        event("run_started", 2, {"worker_kind": "local_reference_worker"}, run_ref=run_ref),
        event("worker_message", 3, {"message": "fixture worker executed"}, run_ref=run_ref),
        event("artifact_produced", 4, {"path": artifact_path, "media_type": "application/json", "byte_count": size, "sha256": digest}, run_ref=run_ref),
        event("usage_updated", 5, {"events": 6, "artifacts": 1, "processes": 1}, run_ref=run_ref),
        event("run_completed", 6, {"result": "PASS"}, run_ref=run_ref),
    ]
    return "\n".join(json.dumps(item, sort_keys=True) for item in events) + "\n"


class FakeRunner:
    def __init__(
        self,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int = 0,
        timeout: bool = False,
        artifact_text: str | None = None,
        artifact_path: str = host.ARTIFACT_MEMBER,
        unexpected_member: str | None = None,
        mutate: Path | None = None,
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.artifact_text = artifact_text
        self.artifact_path = artifact_path
        self.unexpected_member = unexpected_member
        self.mutate = mutate
        self.calls: list[dict] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append(
            {
                "argv": list(argv),
                "cwd": cwd,
                "env": dict(env),
                "timeout": timeout,
                "shell": False,
                "staged_worker_existed": Path(argv[1]).is_file(),
            }
        )
        if self.mutate is not None:
            self.mutate.write_text("changed\n", encoding="utf-8")
        if self.timeout:
            raise subprocess.TimeoutExpired(list(argv), timeout, output="", stderr="timeout")
        if self.artifact_text is not None:
            artifact = host.resolve_workspace_member(Path(cwd), self.artifact_path)
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(self.artifact_text, encoding="utf-8", newline="\n")
        if self.unexpected_member is not None:
            unexpected = host.resolve_workspace_member(Path(cwd), self.unexpected_member)
            unexpected.parent.mkdir(parents=True, exist_ok=True)
            unexpected.write_text("unexpected\n", encoding="utf-8")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class LocalProcessExecutionHostRepairTests(unittest.TestCase):
    def test_disposable_workspace_exact_argv_environment_artifacts_and_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            artifact_text = stable_json({"fixture_version": "test", "result": "PASS", "run_ref": host.RUN_REF, "workunit_ref": host.TASK_ID})
            fake = FakeRunner(stdout=event_stream(artifact_text=artifact_text), artifact_text=artifact_text)

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
            self.assertTrue(call["staged_worker_existed"])
            self.assertNotEqual(Path(call["cwd"]).resolve(), root.resolve())
            self.assertFalse(host.is_under(Path(call["cwd"]), root))
            self.assertEqual(call["argv"][2:], ["--run-id", host.RUN_REF, "--workunit-ref", host.TASK_ID, "--event-stream"])
            self.assertEqual(Path(call["argv"][1]).parent.parent, Path(call["cwd"]))
            self.assertFalse(call["shell"])
            self.assertEqual(call["env"]["PYTHONDONTWRITEBYTECODE"], "1")
            self.assertEqual(call["env"]["PYTHONNOUSERSITE"], "1")
            self.assertEqual(call["env"]["PYTHONUTF8"], "1")
            self.assertEqual(call["env"]["PYTHONHASHSEED"], "0")
            self.assertTrue(result["workspace_cleanup"]["removed"])
            self.assertTrue(result["raw_event_stream_artifact"]["persisted"])
            self.assertEqual(result["worker_artifacts"][0]["sha256"], host.sha256_text(artifact_text))
            self.assertEqual(result["worker_run_lifecycle"]["final_state"], "completed")
            descriptor = host.build_host_descriptor(result)
            self.assertEqual(descriptor["supported_operations"], ["probe", "create_run"])
            self.assertIn("cancel", descriptor["unsupported_operations"])

    def test_invalid_requests_launch_zero_processes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            fake = FakeRunner(stdout=event_stream(), artifact_text=stable_json({"result": "PASS"}))

            unsupported = host.run_host(root, expected_revision=revision, capability_id="aide.future.unsupported", python_executable=sys.executable, runner=fake, write_reports=False)
            self.assertEqual(unsupported["reason_code"], host.REFUSAL_CODES["unsupported_capability"])
            self.assertEqual(unsupported["process_call_count"], 0)

            wrong_revision = host.run_host(root, expected_revision="0" * 40, python_executable=sys.executable, runner=fake, write_reports=False)
            self.assertEqual(wrong_revision["reason_code"], host.REFUSAL_CODES["revision_mismatch"])
            self.assertEqual(wrong_revision["process_call_count"], 0)

            changed_digests = {rel.as_posix(): "sha256:" + ("0" * 64) for rel in host.RELEVANT_SOURCE_RELS}
            digest_mismatch = host.run_host(root, expected_revision=revision, python_executable=sys.executable, expected_digests=changed_digests, runner=fake, write_reports=False)
            self.assertEqual(digest_mismatch["reason_code"], host.REFUSAL_CODES["digest_mismatch"])
            self.assertEqual(digest_mismatch["process_call_count"], 0)

            inside_workspace = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=fake, write_reports=False, workspace_root=root / "tmp" / "inside")
            self.assertEqual(inside_workspace["reason_code"], host.REFUSAL_CODES["workspace_inside_source"])
            self.assertEqual(inside_workspace["process_call_count"], 0)
            self.assertEqual(fake.calls, [])

    def test_workspace_containment_rejects_traversal_absolute_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            safe = host.resolve_workspace_member(workspace, "nested/file.txt")
            safe.parent.mkdir(parents=True)
            safe.write_text("ok\n", encoding="utf-8")
            self.assertEqual(safe, workspace.resolve() / "nested" / "file.txt")
            with self.assertRaises(host.LocalProcessHostError) as traversal:
                host.resolve_workspace_member(workspace, "../outside.txt")
            self.assertEqual(traversal.exception.reason_code, host.REFUSAL_CODES["workspace_path_traversal"])
            with self.assertRaises(host.LocalProcessHostError):
                host.resolve_workspace_member(workspace, "/absolute.txt")
            link = workspace / "link"
            try:
                link.symlink_to(Path(tmp))
            except OSError:
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(host.LocalProcessHostError) as symlink:
                host.resolve_workspace_member(workspace, "link/file.txt")
            self.assertEqual(symlink.exception.reason_code, host.REFUSAL_CODES["workspace_symlink_escape"])

    def test_event_stream_fail_closed(self) -> None:
        cases = [
            ("not json\n", host.REFUSAL_CODES["malformed_event_stream"]),
            ("\n", host.REFUSAL_CODES["empty_output"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 1), event("run_started", 1)]) + "\n", host.REFUSAL_CODES["event_sequence_duplicate"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 2)]) + "\n", host.REFUSAL_CODES["event_sequence_gap"]),
            (event_stream(run_ref="aide://wrong-run"), host.REFUSAL_CODES["wrong_run_ref"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 1), event("run_started", 2)]) + "\n", host.REFUSAL_CODES["terminal_event_missing"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 1), event("run_completed", 2), event("worker_message", 3)]) + "\n", host.REFUSAL_CODES["event_after_terminal"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 1), event("run_started", 2), event("future_event", 3)]) + "\n", host.REFUSAL_CODES["malformed_event_stream"]),
            ("\n".join(json.dumps(item) for item in [event("run_created", 1), event("run_started", 2), event("run_failed", 3)]) + "\n", host.REFUSAL_CODES["worker_failed"]),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(host.LocalProcessHostError) as raised:
                    host.parse_fixture_event_stream(text, 0)
                self.assertEqual(raised.exception.reason_code, expected)

    def test_artifact_integrity_failures_are_refusals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            declared = stable_json({"fixture_version": "test", "result": "PASS", "run_ref": host.RUN_REF, "workunit_ref": host.TASK_ID})
            wrong = stable_json({"fixture_version": "test", "result": "WRONG"})

            mismatch = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=declared), artifact_text=wrong), write_reports=False)
            self.assertEqual(mismatch["reason_code"], host.REFUSAL_CODES["artifact_digest_mismatch"])

            missing = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=declared)), write_reports=False)
            self.assertEqual(missing["reason_code"], host.REFUSAL_CODES["artifact_missing"])

            unexpected = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=declared), artifact_text=declared, unexpected_member="artifacts/extra.json"), write_reports=False)
            self.assertEqual(unexpected["reason_code"], host.REFUSAL_CODES["artifact_unexpected"])

            escape = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_path="../escape.json", artifact_text=declared), artifact_text=declared, artifact_path=host.ARTIFACT_MEMBER), write_reports=False)
            self.assertEqual(escape["reason_code"], host.REFUSAL_CODES["artifact_path_escape"])

    def test_lifecycle_transitions_and_unsupported_operations(self) -> None:
        parsed = host.parse_fixture_event_stream(event_stream(), 0)
        lifecycle = host.validate_lifecycle(parsed.events)
        self.assertEqual(lifecycle["initial_state"], "proposed")
        self.assertEqual(lifecycle["final_state"], "completed")
        invalid_events = [event("run_created", 1), event("worker_message", 2)]
        with self.assertRaises(host.LocalProcessHostError) as raised:
            host.validate_lifecycle(invalid_events)
        self.assertEqual(raised.exception.reason_code, host.REFUSAL_CODES["invalid_lifecycle_transition"])
        self.assertEqual(host.validate_required_operations(["probe", "create_run"])["result"], "PASS")
        unsupported = host.validate_required_operations(["probe", "cancel"])
        self.assertEqual(unsupported["result"], "REFUSED")
        self.assertEqual(unsupported["reason_code"], host.REFUSAL_CODES["unsupported_operation"])
        refusal = host.refuse_unsupported_operation("cancel")
        self.assertEqual(refusal["result"], "REFUSED")
        self.assertEqual(refusal["operation"], "cancel")

    def test_deterministic_projection_report_scrubbing_and_mutation_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            revision = create_aide_fixture(root)
            artifact_text = stable_json({"fixture_version": "test", "result": "PASS", "run_ref": host.RUN_REF, "workunit_ref": host.TASK_ID})
            secret_like = "sk-" + "testsecret000000"
            stderr = f"path={root} token={secret_like}"

            first = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=artifact_text), artifact_text=artifact_text, stderr=stderr))
            first_projection = (root / host.PROJECTION_JSON).read_text(encoding="utf-8")
            second = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=artifact_text), artifact_text=artifact_text, stderr=stderr))
            second_projection = (root / host.PROJECTION_JSON).read_text(encoding="utf-8")

            self.assertEqual(first["validation_status"], "PASS_WITH_WARNINGS")
            self.assertEqual(second["validation_status"], "PASS_WITH_WARNINGS")
            self.assertEqual(first_projection, second_projection)
            for path in (root / host.REPORT_ROOT).rglob("*"):
                if path.is_file():
                    text = path.read_text(encoding="utf-8", errors="replace")
                    self.assertNotIn(str(root), text)
                    self.assertNotIn(secret_like, text)

            mutated = host.run_host(root, expected_revision=revision, python_executable=sys.executable, runner=FakeRunner(stdout=event_stream(artifact_text=artifact_text), artifact_text=artifact_text, mutate=root / host.FIXTURE_WORKER_REL), write_reports=False)
            self.assertEqual(mutated["reason_code"], host.REFUSAL_CODES["unexpected_mutation"])
            self.assertEqual(mutated["process_call_count"], 1)
            self.assertFalse(mutated["workspace_state_unchanged"])


if __name__ == "__main__":
    unittest.main()
