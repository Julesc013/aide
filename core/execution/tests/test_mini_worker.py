"""Actual Mini fixture scenarios, each run in its own isolated native process."""
import sys
import json
import os
from pathlib import Path
import runpy
import subprocess
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.execution.mini_worker import MiniAttempt, MiniRefused, run_attempt, verify_dependencies
from core.execution.managed_workspace import digest, file_digest


class Model:
    config = None

    def __init__(self, scenario):
        self.scenario = scenario
        self.calls = 0

    def query(self, messages):
        self.calls += 1
        if self.scenario == "malformed":
            from minisweagent.exceptions import FormatError
            raise FormatError({"role": "assistant", "content": "malformed"})
        if self.scenario == "interrupt" and self.calls == 2:
            raise KeyboardInterrupt()
        if self.scenario == "cancel" and self.calls == 2:
            # Fixed owned descendant proves process-tree cancellation, not shell access.
            subprocess.Popen([sys.executable, "-I", "-B", "-c",
                              "import time; time.sleep(60)"],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            (OUTPUT / "cancel-ready").write_text("ready", encoding="utf-8")
            time.sleep(60)
        operation = "write" if self.calls == 1 else "submit"
        if self.scenario == "resume" and self.calls == 1:
            operation = "read"
        if self.scenario == "step":
            operation = "read"
        return {"role": "assistant", "content": operation, "extra": {"actions": [{"op": operation}]}}

    def format_message(self, **kwargs):
        return kwargs

    def format_observation_messages(self, message, outputs, template_vars=None):
        return [{"role": "tool", "content": json.dumps(outputs)}]

    def get_template_vars(self, **kwargs):
        return {}

    def serialize(self):
        # Demonstrate why trajectory-supplied identities are not acceptance.
        return {"info": {"aide_work_unit": "untrusted", "accepted": True}}


class Environment:
    config = None

    def __init__(self, project, scenario):
        self.project, self.scenario = project, scenario
        self.effects = 0

    def execute(self, action, cwd=""):
        if self.scenario == "environment_failure":
            raise RuntimeError("controlled environment failure")
        if action == {"op": "write"}:
            self.effects += 1
            if self.effects != 1:
                raise AssertionError("effect repeated")
            (self.project / "arithmetic.py").write_text(
                "def add(a, b):\n    return a + b\n", encoding="utf-8")
            return {"written": "arithmetic.py"}
        if action == {"op": "read"}:
            return {"content": (self.project / "arithmetic.py").read_text()}
        if action == {"op": "submit"}:
            from minisweagent.exceptions import Submitted
            raise Submitted({"role": "exit", "content": "candidate",
                             "extra": {"exit_status": "Submitted", "submission": "arithmetic.py"}})
        raise ValueError("unknown fixed fixture action")

    def get_template_vars(self, **kwargs):
        return {}

    def serialize(self):
        return {}


class MiniFixture(unittest.TestCase):
    def test_selected_scenario(self):
        recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
        before = {p.name: file_digest(p) for p in PROJECT.iterdir()}
        model, env = Model(SCENARIO), Environment(PROJECT, SCENARIO)
        spec = MiniAttempt("MINI-FIXTURE", SCENARIO, SOURCE, digest(recipe),
                           "Repair addition; preserve notes and submit a candidate.")
        root = OUTPUT / SCENARIO

        def execute(**changes):
            values = dict(enabled=True, dependencies=DEPS, recipe=recipe, attempt_root=root)
            values.update(changes)
            return run_attempt(spec, model, env, **values)

        if SCENARIO == "disabled":
            with self.assertRaisesRegex(MiniRefused, "disabled"):
                execute(enabled=False)
            self.assertNotIn("minisweagent", sys.modules)
        elif SCENARIO == "missing":
            target = DEPS / "mdurl/__init__.py"
            original = target.read_bytes()
            target.unlink()
            try:
                with self.assertRaisesRegex(MiniRefused, "missing"):
                    execute()
            finally:
                target.write_bytes(original)
        elif SCENARIO == "changed":
            target = DEPS / "mdurl/__init__.py"
            original = target.read_bytes()
            target.write_bytes(original + b"\n# changed\n")
            try:
                with self.assertRaisesRegex(MiniRefused, "altered"):
                    execute()
            finally:
                target.write_bytes(original)
        elif SCENARIO == "version":
            changed = {**recipe, "mini_version": "0.0.0"}
            with self.assertRaisesRegex(MiniRefused, "unqualified"):
                verify_dependencies(DEPS, changed, digest(changed))
        elif SCENARIO == "distribution":
            changed = {**recipe, "distributions": {**recipe["distributions"], "pydantic": "0.0.0"}}
            with self.assertRaisesRegex(MiniRefused, "distribution identity"):
                verify_dependencies(DEPS, changed, digest(changed))
        elif SCENARIO == "bounds":
            from dataclasses import replace
            for changes in ({"step_limit": 0}, {"wall_time_limit_seconds": 0},
                            {"cost_limit": float("nan")}):
                with self.assertRaises(MiniRefused):
                    replace(spec, **changes).validate()
        elif SCENARIO == "preloaded":
            import types
            sys.modules["jinja2"] = types.ModuleType("jinja2")
            try:
                with self.assertRaisesRegex(MiniRefused, "preloaded"):
                    execute()
            finally:
                del sys.modules["jinja2"]
        elif SCENARIO == "duplicate":
            root.mkdir()
            (root / "preserved").write_text("prior attempt", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                execute()
            self.assertEqual((root / "preserved").read_text(), "prior attempt")
        elif SCENARIO in ("environment_failure", "interrupt"):
            error = RuntimeError if SCENARIO == "environment_failure" else KeyboardInterrupt
            with self.assertRaises(error):
                execute()
            observed = json.loads((root / "attempt.json").read_text())
            self.assertEqual(observed["status"], "FAILED" if error is RuntimeError else "INTERRUPTED")
            self.assertFalse(observed["accepted"])
            self.assertIsNotNone(observed["trajectory_sha256"])
        else:
            observed = execute()
            self.assertEqual(observed["identity"]["work_unit"], "MINI-FIXTURE")
            self.assertEqual(observed["identity"]["source_revision"], SOURCE)
            self.assertEqual(observed["identity"]["recipe_sha256"], digest(recipe))
            self.assertFalse(observed["accepted"])
            self.assertIsNone(observed["model_usage"])
            if SCENARIO in ("success", "resume"):
                self.assertTrue(observed["candidate_submitted"])
                self.assertEqual(observed["model_queries"], 2)
                # Behavioral oracle is independent of the worker's own submission.
                add = runpy.run_path(str(PROJECT / "arithmetic.py"))["add"]
                for a, b, expected in ((2, 3, 5), (-4, 1, -3), (0, 0, 0)):
                    self.assertEqual(add(a, b), expected)
                self.assertEqual(env.effects, 0 if SCENARIO == "resume" else 1)
                self.assertEqual(Path(os.environ["MSWEA_GLOBAL_CONFIG_DIR"]), root / "config")
                self.assertFalse((root / "config/.env").exists())
                trajectory = json.loads((root / "trajectory.json").read_text())
                self.assertTrue(trajectory["info"]["accepted"])
                import difflib
                patch = "".join(difflib.unified_diff(
                    ["def add(a, b):\n", "    return a - b\n"],
                    (PROJECT / "arithmetic.py").read_text().splitlines(keepends=True),
                    fromfile="a/arithmetic.py", tofile="b/arithmetic.py"))
                (OUTPUT / "candidate.patch").write_text(patch, encoding="utf-8")
            else:
                self.assertFalse(observed["candidate_submitted"])
                self.assertEqual(observed["exit_status"],
                                 "RepeatedFormatError" if SCENARIO == "malformed" else "LimitsExceeded")
        self.assertEqual(file_digest(PROJECT / "notes.txt"), before["notes.txt"])
        if SCENARIO not in ("success", "interrupt", "cancel"):
            self.assertEqual(file_digest(PROJECT / "arithmetic.py"), before["arithmetic.py"])
            self.assertEqual(env.effects, 0)
        self.assertNotIn("litellm", sys.modules)
        self.assertNotIn("openai", sys.modules)


if __name__ == "__main__":
    SCENARIO, deps, recipe, project, output, SOURCE = sys.argv[1:]
    DEPS, RECIPE, PROJECT, OUTPUT = map(Path, (deps, recipe, project, output))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MiniFixture)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (OUTPUT / "test-result.json").write_text(json.dumps({
        "scenario": SCENARIO, "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skips": len(result.skipped),
        "real_model_requests": 0, "fixture_only": True}) + "\n", encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)

