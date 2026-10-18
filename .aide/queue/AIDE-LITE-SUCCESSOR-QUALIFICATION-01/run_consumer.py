"""Select one unchanged original canary for the exact successor archives."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
ORIGINAL = ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01'
CAN = ORIGINAL / 'canaries'
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
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main():
    assert len(sys.argv) in (2, 3) and sys.argv[1] in tuple(map(str, range(8)))
    assert sys.argv[2:] in ([], ['--repair'])
    index = int(sys.argv[1])
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    subject_name = 'build-result-repaired.json' if sys.argv[2:] else 'build-result.json'
    subject = json.loads((TASK / 'evidence' / subject_name).read_text(encoding='utf-8'))
    for name, value in subject['assets'].items():
        assert sha(ROOT / name) == value['sha256']
    stable = ROOT / '.aide/release/stable'
    z, t = str(stable / 'aide-lite-v1.1.0.zip'), str(stable / 'aide-lite-v1.1.0.tar.gz')
    zs, ts, cs = sha(Path(z)), sha(Path(t)), subject['delivered_cli_sha256']
    hs = sha(CAN / 'lifecycle_helper.py')
    cases = [
        ('consumer_canary_runner.py', ['--candidate-zip', z, '--candidate-tar', t,
            '--candidate-zip-sha256', zs, '--candidate-tar-sha256', ts,
            '--bundled-cli-sha256', cs, '--source-commit', subject['identity']['source_commit']]),
        ('lifecycle_canary_runner.py', [z, zs, hs]),
        ('context_offline_canary.py', [z, zs, hs]),
        ('partial_cli_canary.py', [z, t, zs, ts, cs]),
        ('public_cli_canary.py', [z, zs, hs]),
        ('forced_restart_runner.py', [z, zs]),
        ('job_forms_canary.py', ['--zip', z, '--zip-sha256', zs, '--cli-sha256', cs, '--out', 'unused.json']),
        ('taskos_delivered_canary.py', [z, zs, cs]),
    ]
    name, parameters = cases[index]
    scratch = TMP / f'case-{index:02d}'
    retained = OUTPUT / f'case-{index:02d}'
    scratch.mkdir(); retained.mkdir()
    env = {**os.environ, 'AIDE_JOB_TMP': str(scratch), 'AIDE_JOB_OUTPUT': str(retained),
           'AIDE_RESOURCE_TEST_PARENT': str(scratch), 'TEMP': str(scratch),
           'TMP': str(scratch), 'TMPDIR': str(scratch), 'GIT_CONFIG_COUNT': '1',
           'GIT_CONFIG_KEY_0': 'safe.directory', 'GIT_CONFIG_VALUE_0': str(ROOT)}
    argv = [sys.executable, '-I', '-B', str(CAN / name), *parameters]
    if index == 6:
        # Preserve the original module path, implementation and assertions. Only
        # its explicit fixture CONFIG changes to the reviewed current volume.
        bootstrap = ("import sys,importlib.util; p,c=sys.argv[1:3]; "
                     "sys.argv=[p,*sys.argv[3:]]; "
                     "s=importlib.util.spec_from_file_location('successor_job_forms',p); "
                     "m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; "
                     "s.loader.exec_module(m); m.CONFIG=m.Path(c); m.main()")
        argv = [sys.executable, '-I', '-B', '-c', bootstrap, str(CAN / name),
                str(TASK / 'evidence/consumer-config.json'), *parameters]
    capture = load('successor_capture', ROOT / '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py')
    process_record = {'argv': argv, 'case': index, 'started_unix_ns': time.time_ns(),
                      'source_canary_sha256': sha(CAN / name), 'exit_code': None}
    write(retained / 'process.json', process_record)
    try:
        result = capture.capture_streams(argv, cwd=ROOT, env=env,
            stdout_path=retained / 'stdout.log', stderr_path=retained / 'stderr.log', timeout=600)
        process_record['exit_code'] = result.returncode
    except BaseException as exc:
        process_record['exception'] = repr(exc)
        raise
    finally:
        process_record['finished_unix_ns'] = time.time_ns()
        write(retained / 'process.json', process_record)
    assert result.returncode == 0, 'original canary failed; raw result retained'
    summary = json.loads((retained / 'summary.json').read_text(encoding='utf-8'))
    assert summary['status'] == 'PASS', 'canary needs classification; not a pass'
    if index == 0:
        assert json.loads((retained / 'partial-recovery-result.json').read_text(encoding='utf-8'))['status'] == 'PASS'
    for name, value in subject['assets'].items():
        assert sha(ROOT / name) == value['sha256']
    # All unique canary reports and process streams are retained before cleanup.
    worker = load('successor_owned_retirement', ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(scratch)
    write(OUTPUT / 'consumer-result.json', {
        'status': 'PASS', 'case': index, 'assets': subject['assets'],
        'summary_sha256': sha(retained / 'summary.json'), 'original_assertions': 'unchanged',
        'fixture_retired': True, 'route': 'current Windows Job managed resource runner',
        'historical_restricted_account_route': 'not exercised',
        'outer_containment': 'unqualified', 'read_isolation': 'unqualified', 'model_calls': 0})
    print(f'PASS original consumer case {index}; exact successor assets preserved')


if __name__ == '__main__':
    main()
