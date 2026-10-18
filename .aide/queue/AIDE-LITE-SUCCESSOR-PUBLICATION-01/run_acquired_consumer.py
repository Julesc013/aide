"""Bind the original case 0 to acquired bytes; retain every original assertion."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01'
ORIGINAL = ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01'
ACQUIRED = ROOT / '.aide/release/acquired-aide-lite-v1.1.0.log'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def main():
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    subject = json.loads((TASK / 'evidence/release-selection.json').read_text())
    receipt = json.loads((ACQUIRED / 'acquisition.json').read_text())
    assert receipt['status'] == 'PASS'
    for path, identity in subject['assets'].items():
        acquired = ACQUIRED / Path(path).name
        assert acquired.stat().st_size == identity['size_bytes'] and sha(acquired) == identity['sha256']
    original = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/build-result-repaired.json'
    build = json.loads(original.read_text())
    assert build['assets'] == subject['assets']
    scratch, retained = TMP / 'case-00', OUTPUT / 'case-00'
    scratch.mkdir(); retained.mkdir()
    canary = ORIGINAL / 'canaries/consumer_canary_runner.py'
    archive = ACQUIRED / 'aide-lite-v1.1.0.zip'
    tar = ACQUIRED / 'aide-lite-v1.1.0.tar.gz'
    argv = [sys.executable, '-I', '-B', str(canary),
            '--candidate-zip', str(archive), '--candidate-tar', str(tar),
            '--candidate-zip-sha256', sha(archive), '--candidate-tar-sha256', sha(tar),
            '--bundled-cli-sha256', build['delivered_cli_sha256'],
            '--source-commit', subject['archive_source']]
    env = {**os.environ, 'AIDE_JOB_TMP': str(scratch), 'AIDE_JOB_OUTPUT': str(retained),
           'AIDE_RESOURCE_TEST_PARENT': str(scratch), 'TEMP': str(scratch),
           'TMP': str(scratch), 'TMPDIR': str(scratch), 'GIT_CONFIG_COUNT': '1',
           'GIT_CONFIG_KEY_0': 'safe.directory', 'GIT_CONFIG_VALUE_0': str(ROOT)}
    capture = load('publication_capture', ROOT / '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py')
    process = {'argv': argv, 'started_unix_ns': time.time_ns(),
               'canary_sha256': sha(canary), 'exit_code': None}
    write(retained / 'process.json', process)
    try:
        result = capture.capture_streams(argv, cwd=ROOT, env=env,
            stdout_path=retained / 'stdout.log', stderr_path=retained / 'stderr.log', timeout=600)
        process['exit_code'] = result.returncode
    except BaseException as exc:
        process['exception'] = repr(exc)
        raise
    finally:
        process['finished_unix_ns'] = time.time_ns()
        write(retained / 'process.json', process)
    assert result.returncode == 0
    for name in ['summary.json', 'partial-recovery-result.json']:
        assert json.loads((retained / name).read_text())['status'] == 'PASS', name
    for path, identity in subject['assets'].items():
        assert sha(ACQUIRED / Path(path).name) == identity['sha256']
    load('publication_retirement', ORIGINAL / 'worker.py').retire_owned_fixture(scratch)
    write(OUTPUT / 'acquired-consumer.json', {
        'status': 'PASS', 'case': 0, 'assets': subject['assets'],
        'acquisition_receipt_sha256': sha(ACQUIRED / 'acquisition.json'),
        'summary_sha256': sha(retained / 'summary.json'), 'fixture_retired': True,
        'original_assertions': 'unchanged', 'model_calls': 0,
        'outer_containment': 'unqualified', 'read_isolation': 'unqualified'})
    print('PASS: original fresh/brownfield consumer and recovery on acquired bytes')


if __name__ == '__main__':
    main()
