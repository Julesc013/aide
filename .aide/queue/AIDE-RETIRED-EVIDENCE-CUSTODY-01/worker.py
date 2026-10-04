"""One source-custody fixture qualification in the existing managed worker."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[3]
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def main():
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if 'CodexSandboxOffline' not in identity.value:
        raise AssertionError('restricted worker identity required')
    if list(TMP.iterdir()):
        raise AssertionError('test parent must be the existing empty allocated TMP')
    os.environ['AIDE_RESOURCE_TEST_PARENT'] = str(TMP)
    test = REPO / '.aide/scripts/tests/test_retired_evidence.py'
    result = subprocess.run([sys.executable, '-B', str(test)], cwd=REPO,
                            capture_output=True, timeout=150)
    sys.stdout.buffer.write(result.stdout)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(result.stderr)
    sys.stderr.buffer.flush()
    text = (result.stdout + result.stderr).decode('utf-8', errors='replace')
    proof = {'schema': 'aide.retired-custody-source-fixture.v1',
             'windows_identity': identity.value, 'test_exit_code': result.returncode,
             'tests_expected': 23, 'count_verified': bool(re.search(r'Ran 23 tests? in ', text)),
             'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
             'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
             'fixtures_retired': not list(TMP.iterdir()), 'model_calls': 0,
             'live_custody_effect': False, 'outer_session_contained': False}
    (OUTPUT / 'custody-source-fixture.json').write_text(
        json.dumps(proof, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    if result.returncode or not proof['count_verified'] or not proof['fixtures_retired'] or 'skipped=' in text:
        raise AssertionError('custody source fixture qualification failed; complete process output retained')
    print(json.dumps({'result': 'PASS', 'tests': 23, 'fixtures_retired': True}), flush=True)


if __name__ == '__main__':
    main()
