"""One fresh-process consumer plus frozen legacy-reader and unchanged-pack checks."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib, json, os, subprocess, tempfile, types, unittest
from pathlib import Path
ROOT = Path.cwd()
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"])
SCRATCH = Path(os.environ["AIDE_JOB_TMP"])
assert Path(tempfile.gettempdir()) == SCRATCH and SCRATCH.parent == OUTPUT.parent
sys.path.insert(0, str(ROOT / ".aide/scripts/tests"))
tests = importlib.import_module("test_continuous_worker_request_cancellation")
suite = unittest.defaultTestLoader.loadTestsFromTestCase(tests.CancellationWorkflowTests)
assert suite.countTestCases() == 1
with (OUTPUT / "workflow-tests.log").open("x", encoding="utf-8") as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {"tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
          "skips": [(t.id(), why) for t, why in result.skipped]}
(OUTPUT / "workflow-tests.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
assert result.wasSuccessful() and result.testsRun == 1 and not result.skipped
base = "8fe2d12cbc9d91f034cf7f68c58beda09809dc58"
raw = subprocess.check_output(["git", "show", base + ":core/runtime/continuous_worker/requests.py"], timeout=15)
assert hashlib.sha256(raw).hexdigest() == "87ba68e7aefb3521956dafa00f3570ffa0ca9df2ef9ea6975ff20a21cf703cf8"
legacy = types.ModuleType("core.runtime.continuous_worker.legacy_requests")
legacy.__package__ = "core.runtime.continuous_worker"
exec(compile(raw, base + ":requests.py", "exec"), legacy.__dict__)
from core.runtime.continuous_worker.state import State, Refused, digest
from core.runtime.continuous_worker.requests import Requests
with tempfile.TemporaryDirectory(prefix="legacy-reader-") as directory:
    root = Path(directory).resolve()
    old_config = tests.configuration(root)
    legacy.configuration(old_config, root)
    config = old_config | {"schema": "aide.dependency-configuration.v2"}
    state = State(root)
    try:
        Requests.initialize(state, config)
        before = list(state.db.iterdump())
        for operation in (lambda: legacy.configuration(config, root),
                          lambda: legacy.Requests(state, digest(config))):
            try:
                operation()
            except Refused:
                pass
            else:
                raise AssertionError("old reader silently accepted required cancellation semantics")
        assert list(state.db.iterdump()) == before
    finally:
        state.close()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pack = ROOT / ".aide/export/aide-lite-pack-v0"
prior = json.loads((ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01/evidence/attempt-02-delivered-result.json").read_text(encoding="utf-8"))["after_sha256s"]
actual = {p.relative_to(pack).as_posix(): sha(p) for p in pack.rglob("*") if p.is_file()}
assert len(actual) == 870 and actual == prior
release = json.loads((ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01/evidence/attempt-02-release-before.json").read_text(encoding="utf-8"))
for p, expected in release.items(): assert sha(ROOT / p) == expected, p
record.update(result="PASS", old_reader_source=base, old_reader_sha256=hashlib.sha256(raw).hexdigest(),
              old_reader_v2_refused=True, pack_files_unchanged=len(actual), release_files_unchanged=len(release),
              live_deliveries=0, models_requested=0, native_cancellation_enforced=False)
(OUTPUT / "workflow-result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record))
