"""Bounded old/new scratch scanner regression under a separate pinned owner."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest

REPO = Path(__file__).resolve().parents[4]
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
TEST = REPO / '.aide/scripts/tests/test_managed_workspace.py'
BASE = REPO / '.aide/export/aide-lite-pack-v0/files/core/execution/managed_workspace.py'
BASE_SHA = 'd9338d9d25470b1a39f8c74566f7c108249a98dc564ac395f21b66ebc4eccfe3'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def baseline():
    if sha(BASE) != BASE_SHA:
        raise AssertionError('known-good baseline changed')
    tests = load('zero_link_regression_tests', TEST)
    tests.workspace = load('zero_link_known_good_baseline', BASE)
    names = sorted(n for n in dir(tests.ManagedWorkspaceTests)
                   if n.startswith('test_') and 'zero_link' in n)
    if len(names) != 8:
        raise AssertionError('eight exact added regressions required')
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(
        tests.ManagedWorkspaceTests(n) for n in names))
    actual = {test._testMethodName for test, _ in result.errors + result.failures}
    expected = set(names) - {'test_quiescent_zero_link_member_is_refused_without_retry'}
    proof = {'schema': 'aide.zero-link-original-baseline.v1',
             'baseline_sha256': BASE_SHA, 'test_sha256': sha(TEST),
             'run': result.testsRun, 'failures': len(result.failures),
             'errors': len(result.errors), 'skips': len(result.skipped),
             'failed_methods': sorted(actual), 'expected_failed_methods': sorted(expected),
             'original_scanner_regression_demonstrated': actual == expected,
             'status': 'EXPECTED_RED' if actual == expected else 'UNEXPECTED_RESULT'}
    save(OUTPUT / 'zero-link-baseline.json', proof)
    if (result.testsRun != 8 or result.skipped or len(result.failures) != 4
            or len(result.errors) != 3 or actual != expected):
        raise AssertionError('baseline did not demonstrate the exact expected regression')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    os.environ['AIDE_RESOURCE_TEST_PARENT'] = str(TMP)
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if 'CodexSandboxOffline' not in identity.value:
        raise AssertionError('restricted worker identity required')
    if args.baseline:
        baseline()
        return
    proof = {'schema': 'aide.active-zero-link-source-qualification.v1',
             'status': 'RUNNING', 'windows_identity': identity.value,
             'candidate_sha256': sha(REPO / 'core/execution/managed_workspace.py'),
             'test_sha256': sha(TEST), 'known_good_supervisor_sha256': BASE_SHA,
             'commands': [], 'model_calls': 0, 'outer_session_contained': False}
    path = OUTPUT / 'zero-link-qualification.json'
    save(path, proof)
    for label, argv in (
        ('original-baseline', [sys.executable, '-I', '-B', str(Path(__file__)), '--baseline']),
        ('candidate-workspace60', [sys.executable, '-I', '-B', str(TEST), '-v']),
    ):
        out, err = OUTPUT / (label + '.stdout'), OUTPUT / (label + '.stderr')
        row = {'label': label, 'argv': argv, 'timeout_seconds': 90, 'state': 'RUNNING'}
        proof['commands'].append(row)
        save(path, proof)
        # Retain bytes before completion; interrupted work remains RUNNING,
        # never a guessed exit or silently accepted test count.
        with out.open('xb') as stdout, err.open('xb') as stderr:
            result = subprocess.run(argv, cwd=REPO, stdout=stdout, stderr=stderr,
                                    env=os.environ.copy(), timeout=90)
        row.update(state='EXITED', exit_code=result.returncode,
                   stdout_sha256=sha(out), stderr_sha256=sha(err))
        save(path, proof)
        if result.returncode:
            raise AssertionError(label + ' failed; raw streams retained')
        if label == 'candidate-workspace60':
            text = (out.read_bytes() + err.read_bytes()).decode('utf-8', errors='replace')
            if not re.search(r'Ran 60 tests? in ', text) or 'skipped=' in text:
                raise AssertionError('candidate count changed or skipped')
    if list(TMP.iterdir()):
        raise AssertionError('source fixture retirement incomplete')
    proof.update(status='PASS', candidate_tests=60, added_regressions=8,
                 unchanged_cases=52, baseline_expected_red=True,
                 all_source_fixtures_retired=True, runtime_promoted=False,
                 stable_or_consumer_acceptance=False)
    save(path, proof)
    print(json.dumps({'status': 'PASS', 'candidate_tests': 60,
                      'baseline_expected_red': True, 'qualification_sha256': sha(path)}), flush=True)


if __name__ == '__main__':
    main()
