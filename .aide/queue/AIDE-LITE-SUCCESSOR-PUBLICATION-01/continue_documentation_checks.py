"""Continue unfinished documentation qualification, preserving every completed check."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01"
EVIDENCE = TASK / "evidence"
sys.path.insert(0, str(ROOT))
from core.execution.managed_workspace import content_digest


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    previous = json.loads((EVIDENCE / "documentation-attempt-01.json").read_bytes())
    assert previous["job_id"] == "586d4ad910764c86b6a92c00af927d72"
    assert previous["phase"] == "retired" and previous["result"]["reason"] == "timeout"
    assert previous["result"]["quiescent"] and previous["scratch_absent"] and previous["reservation_released"]
    retained = Path(previous["retained"])
    for path, expected in previous["collected_manifest"].items():
        assert content_digest(retained / path) == expected
    template = json.loads((EVIDENCE / "documentation-job-template.json").read_bytes())
    for path, expected in template["inputs"].items():
        assert sha(ROOT / path) == expected, path
    text = (retained / "output/source-tests.log").read_text(encoding="utf-8")
    completed = re.findall(r"^test_\w+ \(([^)]+)\) \.\.\. ok$", text, re.MULTILINE)
    assert len(completed) == len(set(completed)) == 25
    assert not re.search(r"\.\.\. (?:FAIL|ERROR|skipped)", text)
    spec = importlib.util.spec_from_file_location("documentation_original", TASK / "run_documentation_checks.py")
    original = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = original
    spec.loader.exec_module(original)
    original_checks = original.checks

    def continuation_checks(subject, label):
        if label != "source":
            return original_checks(subject, label)
        tests = []
        inputs = {}
        for name in original.MODULES:
            path = subject / ".aide/scripts/tests" / (name + ".py")
            module = original.load(label + "_" + name, path)
            for group in unittest.defaultTestLoader.loadTestsFromModule(module):
                tests.extend(group)
            inputs[path.relative_to(subject).as_posix()] = sha(path)
        all_ids = {test.id() for test in tests}
        assert len(tests) == len(all_ids) == 30 and set(completed) <= all_ids
        pending = [test for test in tests if test.id() not in completed]
        assert len(pending) == 5
        with (original.OUTPUT / "source-continuation-tests.log").open("w", encoding="utf-8") as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.TestSuite(pending))
        original.save("source-tests.json", {"tests_run": result.testsRun,
            "reused_completed": len(completed), "coverage_methods": len(all_ids),
            "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
            "inputs": inputs, "prior_job_id": previous["job_id"], "prior_log_sha256": sha(retained / "output/source-tests.log"),
            "reused_ids": completed, "executed_ids": [test.id() for test in pending]})
        assert result.testsRun == 5 and result.wasSuccessful() and not result.skipped
        assert all(sha(subject / path) == expected for path, expected in inputs.items())

    original.checks = continuation_checks
    original.main()
    original.save("continuation-result.json", {"status": "PASS", "original_attempt": previous["job_id"],
        "original_status": "INCOMPLETE_TIMEOUT", "reused_source_methods": 25, "new_source_methods": 5,
        "delivered_methods": 30, "semantic_assertions": "unchanged",
        "configuration": "existing unmodified 600-second qualification profile"})


if __name__ == "__main__":
    main()
