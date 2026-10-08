"""Candidate regressions under the unchanged pinned native process/storage owner."""
import ast
import ctypes
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    record = json.loads((Path(os.environ['AIDE_JOB_CONTROL']) / 'active.json').read_text(encoding='utf-8'))
    inputs = record['job']['inputs']
    assert all(sha(REPO / name) == expected for name, expected in inputs.items())
    assert not list(TMP.iterdir())
    name = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(name))
    if not ctypes.windll.secur32.GetUserNameExW(2, name, ctypes.byref(size)):
        raise ctypes.WinError()
    assert name.value.endswith('\\CodexSandboxOffline')
    os.environ['AIDE_RESOURCE_TEST_PARENT'] = str(TMP)
    scoped = load('aide_ordinary_known_scope', REPO / 'core/execution/scoped_host.py')
    # Pin process primitives before loading the candidate under test. This is
    # not promotion: the external unchanged owner supervises this whole worker.
    original = scoped.load_owner(record['job']['trusted_runtime_selection'], REPO)
    windows_job = sys.modules['core.runtime.continuous_worker.windows_job']
    candidate = load('core.execution.managed_workspace', REPO / 'core/execution/managed_workspace.py')
    sys.modules['core.execution'].managed_workspace = candidate
    assert candidate.WindowsJobHost is windows_job.WindowsJobHost
    assert candidate is not original
    tests = load('aide_ordinary_workspace_tests', REPO / '.aide/scripts/tests/test_managed_workspace.py')
    assert tests.workspace is candidate
    expected = {node.name for node in ast.walk(ast.parse(
        (REPO / '.aide/scripts/tests/test_managed_workspace.py').read_text(encoding='utf-8')))
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
    suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
    def cases(group):
        for member in group:
            if isinstance(member, unittest.TestSuite):
                yield from cases(member)
            else:
                yield member
    identifiers = [case.id() for case in cases(suite)]
    assert len(identifiers) == len(expected)
    assert {value.rsplit('.', 1)[-1] for value in identifiers} == expected
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    text = stream.getvalue()
    if len(text.encode('utf-8')) > 131072:
        raise RuntimeError('fixture evidence exceeds declared retention')
    (OUTPUT / 'tests.txt').write_text(text, encoding='utf-8', newline='\n')
    unchanged = all(sha(REPO / path) == expected for path, expected in inputs.items())
    proof = {'status': 'PASS' if result.wasSuccessful() and not result.skipped and unchanged else 'FAIL',
             'tests_run': result.testsRun, 'failures': len(result.failures),
             'errors': len(result.errors), 'skips': len(result.skipped),
             'case_ids': identifiers, 'source_inputs_unchanged': unchanged,
             'candidate_sha256': sha(REPO / 'core/execution/managed_workspace.py'),
             'windows_identity': name.value, 'model_calls': 0,
             'mock_model_boundary': True, 'actual_model_editing_qualified': False,
             'outer_session_contained': False}
    (OUTPUT / 'qualification.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in proof.items() if key != 'case_ids'}), flush=True)
    if proof['status'] != 'PASS':
        print(text, flush=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
