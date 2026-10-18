"""Qualify scoped syntax evidence with all 23 existing quality/repo tests."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path.cwd()
SUBJECT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"])
label = "source" if SUBJECT == ROOT else "delivered"
suite = unittest.TestSuite()
inputs = {}
counts = {}
for name in ["test_q37_repo_intelligence", "test_q38_file_quality", "test_quality_symbols"]:
    path = SUBJECT / ".aide/scripts/tests" / (name + ".py")
    spec = importlib.util.spec_from_file_location("symbols_" + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    binding = module.aide if name == "test_quality_symbols" else module.aide_lite
    assert Path(binding.__file__).resolve() == SUBJECT / ".aide/scripts/aide_lite.py"
    tests = unittest.defaultTestLoader.loadTestsFromModule(module)
    counts[name] = tests.countTestCases()
    suite.addTests(tests)
    inputs[path.relative_to(SUBJECT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
assert counts == {"test_q37_repo_intelligence": 7, "test_q38_file_quality": 16, "test_quality_symbols": 21}
for relative in [".aide/scripts/aide_lite.py", ".aide/scripts/quality_symbols.py"]:
    inputs[relative] = hashlib.sha256((SUBJECT / relative).read_bytes()).hexdigest()

def ids(tests):
    for test in tests:
        if isinstance(test, unittest.TestSuite):
            yield from ids(test)
        else:
            yield test.id()

expected = list(ids(suite))
assert len(expected) == len(set(expected)) == 44
with (OUTPUT / (label + "-tests.log")).open("w", encoding="utf-8") as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
record = {"subject": label, "test_ids": expected, "tests_run": result.testsRun, "counts": counts,
          "failures": len(result.failures), "errors": len(result.errors),
          "skips": [(case.id(), why) for case, why in result.skipped], "inputs": inputs,
          "original_tests_retained": 23, "models_requested": 0, "whole_outcome_usage": "unknown"}
(OUTPUT / (label + "-tests.json")).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
assert result.testsRun == 44 and result.wasSuccessful() and not result.skipped
for path, digest in inputs.items():
    assert hashlib.sha256((SUBJECT / path).read_bytes()).hexdigest() == digest
print(json.dumps({"status": "PASS", "subject": label, "tests": result.testsRun}))
