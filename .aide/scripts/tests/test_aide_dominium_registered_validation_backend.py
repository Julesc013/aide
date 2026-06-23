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

from core.interop.dominium import registered_validation_backend as backend


def write_text(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(root: Path, rel: str, payload: dict) -> None:
    write_text(root, rel, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def create_dominium_fixture(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True, text=True)
    run_git(root, "config", "user.email", "aide-tests@example.invalid")
    run_git(root, "config", "user.name", "AIDE Tests")
    run_git(root, "remote", "add", "origin", "https://github.com/Julesc013/dominium.git")
    write_text(root, "AGENTS.md", "# Dominium Operating Law\n")
    write_text(
        root,
        "apps/workbench/module/validation/cli.py",
        "\n".join(
            [
                "from apps.workbench.module.validation.command import run_validation_command",
                "def main(argv=None):",
                "    return run_validation_command({})",
                "",
            ]
        ),
    )
    write_text(
        root,
        "apps/workbench/module/validation/command.py",
        "\n".join(
            [
                'COMMAND_ID = "dominium.validation.run"',
                "def run_validation_command(input_payload=None, *, repo_root=None, invocation_surface='headless', service=None):",
                "    from apps.workbench.module.validation.service_adapter import ValidationServiceAdapter",
                "    service = service or ValidationServiceAdapter(repo_root)",
                "    return service.run_validation(input_payload or {})",
                "",
            ]
        ),
    )
    write_text(
        root,
        "apps/workbench/module/validation/service_adapter.py",
        "\n".join(
            [
                "class ValidationServiceAdapter:",
                "    def __init__(self, repo_root=None):",
                "        self.repo_root = repo_root",
                "    def run_validation(self, request):",
                "        return {}",
                "",
            ]
        ),
    )
    write_json(root, "contracts/command/validation_run_input.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "input", "type": "object", "properties": {}})
    write_json(root, "contracts/command/validation_run_result.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "result", "type": "object", "properties": {"command_id": {"const": "dominium.validation.run"}}})
    write_json(root, "contracts/schema/validation_result.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "validation", "type": "object", "properties": {}})
    write_text(root, "contracts/command/command_surface.contract.toml", 'id = "dominium.validation.run"\n')
    write_json(root, "contracts/refusal/refusal_code.registry.json", {"codes": []})
    write_json(root, "contracts/diagnostic/diagnostic_code.registry.json", {"codes": []})
    write_json(root, "contracts/action/validation_actions.registry.json", {"actions": []})
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "fixture: add validation command")
    return run_git(root, "rev-parse", "HEAD")


def success_stdout() -> str:
    return json.dumps(
        {
            "command_id": backend.CAPABILITY_ID,
            "run_id": "dominium.validation.run.test",
            "status": "ok",
            "summary": "validation command ok",
            "diagnostics": [],
            "evidence": ["contracts/command/validation_run_result.schema.json"],
            "payload": {"validation_report": {"result": "complete", "message": "ok"}},
        },
        sort_keys=True,
    )


def refused_stdout() -> str:
    return json.dumps(
        {
            "command_id": backend.CAPABILITY_ID,
            "run_id": "dominium.validation.run.refused",
            "status": "refused",
            "summary": "aggregate validation suite service is not bound in the Workbench validation slice",
            "diagnostics": [{"code": "DOM-EVIDENCE-MISSING", "severity": "error"}],
            "evidence": ["contracts/refusal/refusal_code.registry.json"],
            "payload": {"refusal": {"code": "dominium.refusal.validation.tool_unavailable"}},
        },
        sort_keys=True,
    )


class FakeRunner:
    def __init__(self, *, stdout: str = "", stderr: str = "", returncode: int = 0, timeout: bool = False, mutate: Path | None = None):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timeout = timeout
        self.mutate = mutate
        self.calls: list[dict] = []

    def __call__(self, argv, cwd, env, timeout):
        self.calls.append({"argv": list(argv), "cwd": cwd, "env": dict(env), "timeout": timeout})
        if self.mutate is not None:
            self.mutate.write_text("changed\n", encoding="utf-8")
        if self.timeout:
            raise subprocess.TimeoutExpired(list(argv), timeout, output="", stderr="timeout")
        return subprocess.CompletedProcess(list(argv), self.returncode, self.stdout, self.stderr)


class DominiumRegisteredValidationBackendTests(unittest.TestCase):
    def test_exact_argv_environment_and_exactly_one_process_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            fake = FakeRunner(stdout=refused_stdout(), returncode=1)
            result = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(result["process_call_count"], 1)
            self.assertEqual(result["launcher_call_count"], 1)
            self.assertEqual(result["proposed_capability_label"], "dominium_registered_validation_command_boundary_invocation_v0")
            self.assertTrue(result["process_started"])
            self.assertTrue(result["structured_output_parsed"])
            self.assertEqual(result["registered_command_boundary_reached"], "proven")
            self.assertEqual(result["service_adapter_boundary_reached"], "unproven")
            self.assertFalse(result["aggregate_validation_executed"])
            self.assertFalse(result["aggregate_validation_succeeded"])
            self.assertEqual(result["mutation_observation"], "none_detected_within_probe_coverage")
            self.assertEqual(len(fake.calls), 1)
            call = fake.calls[0]
            self.assertEqual(call["argv"][0], str(Path(sys.executable).resolve()))
            self.assertEqual(Path(call["argv"][1]), dom / backend.CLI_REL)
            self.assertEqual(call["argv"][2:], ["--repo-root", str(dom.resolve()), "--target", "all", "--profile", "FAST", "--surface", "aide", "--mode", "dry_run"])
            self.assertNotIn("--write-reports", call["argv"])
            self.assertNotIn("--json-out", call["argv"])
            self.assertEqual(call["env"]["PYTHONDONTWRITEBYTECODE"], "1")
            self.assertEqual(call["env"]["PYTHONNOUSERSITE"], "1")
            self.assertEqual(call["env"]["PYTHONUTF8"], "1")
            self.assertEqual(call["env"]["PYTHONHASHSEED"], "0")

    def test_unsupported_capability_causes_zero_process_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            fake = FakeRunner(stdout=success_stdout())
            request = backend.build_invocation_request(
                repo_root=REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                capability_id="dominium.future.unsupported",
                python_executable=sys.executable,
            )
            result = backend.invoke_registered_validation(request, runner=fake)
            self.assertEqual(result["result"], "REFUSED")
            self.assertEqual(result["reason_code"], backend.REFUSAL_CODES["unsupported_capability"])
            self.assertEqual(result["process_call_count"], 0)
            self.assertEqual(fake.calls, [])

    def test_dirty_or_wrong_revision_checkout_causes_zero_process_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            fake = FakeRunner(stdout=success_stdout())
            wrong = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision="0" * 40,
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(wrong["reason_code"], backend.REFUSAL_CODES["revision_mismatch"])
            self.assertEqual(wrong["process_call_count"], 0)
            (dom / "untracked.txt").write_text("dirty\n", encoding="utf-8")
            dirty = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=fake,
                write_reports=False,
            )
            self.assertEqual(dirty["reason_code"], backend.REFUSAL_CODES["dirty_checkout"])
            self.assertEqual(dirty["process_call_count"], 0)

    def test_timeout_malformed_and_nonzero_refusals_are_typed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            timeout = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(timeout=True),
                write_reports=False,
            )
            self.assertEqual(timeout["reason_code"], backend.REFUSAL_CODES["timeout"])
            malformed = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout="not json"),
                write_reports=False,
            )
            self.assertEqual(malformed["reason_code"], backend.REFUSAL_CODES["malformed_json"])
            nonzero = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=refused_stdout(), returncode=1),
                write_reports=False,
            )
            self.assertEqual(nonzero["reason_code"], backend.REFUSAL_CODES["nonzero_exit"])
            self.assertTrue(nonzero["dominium_stdout_json_parsed"])
            self.assertEqual(nonzero["dominium_command_result"]["status"], "refused")
            self.assertEqual(nonzero["domain_outcome"], "typed_refusal")
            self.assertEqual(nonzero["service_adapter_boundary_reached"], "unproven")
            self.assertFalse(nonzero["aggregate_validation_succeeded"])

    def test_digest_mismatch_causes_zero_process_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            result = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                expected_digests={backend.CLI_REL.as_posix(): "sha256:not-real"},
                runner=FakeRunner(stdout=success_stdout()),
                write_reports=False,
            )
            self.assertEqual(result["reason_code"], backend.REFUSAL_CODES["digest_mismatch"])
            self.assertEqual(result["process_call_count"], 0)

    def test_typed_success_mapping_projection_determinism_and_scrubbing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "aide"
            dom = Path(tmp) / "dominium"
            root.mkdir()
            revision = create_dominium_fixture(dom)
            stderr = f"path={dom} token=sk-testsecret000000"
            first = backend.run_backend(
                root,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(), stderr=stderr),
            )
            first_projection = (root / backend.PROJECTION_JSON).read_text(encoding="utf-8")
            second = backend.run_backend(
                root,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(), stderr=stderr),
            )
            second_projection = (root / backend.PROJECTION_JSON).read_text(encoding="utf-8")
            self.assertEqual(first["result"], "PASS")
            self.assertEqual(second["result"], "PASS")
            self.assertEqual(first_projection, second_projection)
            for path in (root / backend.REPORT_ROOT).rglob("*"):
                if path.is_file():
                    text = path.read_text(encoding="utf-8", errors="replace")
                    self.assertNotIn(str(dom), text)
                    self.assertNotIn("sk-testsecret", text)

    def test_unexpected_repository_mutation_is_refused_after_process(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dom = Path(tmp) / "dominium"
            revision = create_dominium_fixture(dom)
            target = dom / "apps/workbench/module/validation/cli.py"
            result = backend.run_backend(
                REPO_ROOT,
                dominium_root=dom,
                expected_revision=revision,
                python_executable=sys.executable,
                runner=FakeRunner(stdout=success_stdout(), mutate=target),
                write_reports=False,
            )
            self.assertEqual(result["reason_code"], backend.REFUSAL_CODES["unexpected_mutation"])
            self.assertEqual(result["process_call_count"], 1)
            self.assertFalse(result["checkout_state_unchanged"])


if __name__ == "__main__":
    unittest.main()
