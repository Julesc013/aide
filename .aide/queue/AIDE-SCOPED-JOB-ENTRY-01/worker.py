"""Run unchanged required validation through the public scoped entry."""
import ctypes
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from core.execution import managed_workspace

output = Path(os.environ['AIDE_JOB_OUTPUT'])
scratch = output.parent
result = {'model_calls': 0, 'outer_session_contained': False,
          'read_isolation': 'unqualified'}
identity = ctypes.create_unicode_buffer(256)
size = ctypes.c_ulong(len(identity))
if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
    raise ctypes.WinError()
result['windows_identity'] = identity.value
result['named_job_membership'] = managed_workspace.WindowsJobHost().contains_current_process(os.environ['AIDE_JOB_ID'])
(output/'allowed.fixture').write_bytes(b'allowed')
denied = scratch/'unapproved.fixture'
try:
    denied.write_bytes(b'escape')
    result['unapproved_write_denied'] = False
except PermissionError:
    result['unapproved_write_denied'] = True
child = subprocess.run([sys.executable, '-B', '-c',
    'import pathlib,sys\ntry: pathlib.Path(sys.argv[1]).write_bytes(b"child")\nexcept PermissionError: sys.exit(19)', str(denied)],
    capture_output=True, timeout=30)
result['child_unapproved_write_denied'] = child.returncode == 19 and not denied.exists()
result['child_probe_exit_code'] = child.returncode
result['config_write_denied'] = False
try:
    with (REPO/'.aide.local/execution.json').open('r+b'):
        pass
except PermissionError:
    result['config_write_denied'] = True
for name, path in (
    ('trusted_archive_write_denied', REPO/'.aide/release/stable/aide-lite-v1.0.0.zip'),
    ('control_write_denied', Path(os.environ['AIDE_JOB_CONTROL'])/'active.json')):
    try:
        with path.open('r+b'):
            pass
        result[name] = False
    except PermissionError:
        result[name] = True
os.environ['AIDE_RESOURCE_TEST_PARENT'] = os.environ['AIDE_JOB_TMP']
os.environ['GIT_CONFIG_COUNT'] = '1'
os.environ['GIT_CONFIG_KEY_0'] = 'safe.directory'
os.environ['GIT_CONFIG_VALUE_0'] = str(REPO)
suite = unittest.TestSuite()
for filename, names in (
    ('test_scoped_host.py', None),
    ('test_managed_workspace.py', None)):
    spec = importlib.util.spec_from_file_location('qualification_'+filename[:-3], REPO/'.aide/scripts/tests'/filename)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    if names is None:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    else:
        suite.addTests(module.ManagedWorkspaceTests(name) for name in names)
tests = unittest.TextTestRunner(verbosity=2).run(suite)
result['tests'] = {'run': tests.testsRun, 'failures': len(tests.failures),
                   'errors': len(tests.errors), 'skips': len(tests.skipped)}
began = time.monotonic()
if '--refresh-export' in sys.argv:
    refreshed = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', 'export-pack'],
        cwd=REPO, timeout=180)
    result['export_exit_code'] = refreshed.returncode
validation = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', 'validate'],
    cwd=REPO, timeout=180)
result['validation_exit_code'] = validation.returncode
result['validation_seconds'] = round(time.monotonic()-began, 3)
result['passed'] = (tests.wasSuccessful() and not tests.skipped and validation.returncode == 0
    and result.get('export_exit_code', 0) == 0
    and result['named_job_membership'] and result['unapproved_write_denied']
    and result['child_unapproved_write_denied'] and result['config_write_denied']
    and result['trusted_archive_write_denied'] and result['control_write_denied']
    and 'Jules' not in identity.value)
(output/'qualification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result), flush=True)
sys.exit(0 if result['passed'] else 1)
