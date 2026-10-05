"""Complete the original pending recovery canary under the selected owner."""
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[4]
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
STABLE = REPO / '.aide/release/stable'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


def main():
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if identity.value != 'BLACKGLASS-WIN1\\CodexSandboxOffline':
        raise AssertionError('restricted worker identity required')
    source = REPO / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py'
    spec = importlib.util.spec_from_file_location('original_normal_retirement', source)
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)
    before = {p.name: sha(p) for p in STABLE.iterdir()}
    zipped, tar = STABLE / 'aide-lite-v1.0.0.zip', STABLE / 'aide-lite-v1.0.0.tar.gz'
    if sha(zipped) != '5cba4ff6658f8f74ea91ec44442e4d566eea20dac90f7f57c53eb903763587fe':
        raise AssertionError('current consumer subject changed')
    with zipfile.ZipFile(zipped) as archive:
        if len(archive.namelist()) != 854:
            raise AssertionError('current archive membership changed')
        cli_sha = hashlib.sha256(archive.read(
            'aide-lite-pack-v0/files/.aide/scripts/aide_lite.py')).hexdigest()
    scratch, retained = TMP / 'case-03', OUTPUT / 'case-03'
    scratch.mkdir(); retained.mkdir()
    argv = [sys.executable, '-I', '-B', str(worker.CAN / 'partial_cli_canary.py'),
            str(zipped), str(tar), sha(zipped), sha(tar), cli_sha]
    proof = {'schema': 'aide.active-zero-link-normal-path.v1', 'status': 'RUNNING',
             'windows_identity': identity.value, 'case_indices': [3], 'argv': argv,
             'assets_before': before, 'model_calls': 0, 'outer_session_contained': False,
             'read_isolation': 'unqualified', 'retired_fixtures': []}
    path = OUTPUT / 'normal-path.json'
    save(path, proof)
    out, err = retained / 'case-03.stdout', retained / 'case-03.stderr'
    env = {**os.environ, 'AIDE_JOB_TMP': str(scratch), 'AIDE_JOB_OUTPUT': str(retained),
           'AIDE_RESOURCE_TEST_PARENT': str(scratch), 'TEMP': str(scratch),
           'TMP': str(scratch), 'TMPDIR': str(scratch), 'GIT_CONFIG_COUNT': '1',
           'GIT_CONFIG_KEY_0': 'safe.directory', 'GIT_CONFIG_VALUE_0': str(REPO)}
    print(json.dumps({'stage': 'original-case03-start'}), flush=True)
    with out.open('xb') as stdout, err.open('xb') as stderr:
        result = subprocess.run(argv, cwd=REPO, env=env, stdout=stdout,
                                stderr=stderr, timeout=600)
    proof.update(process_exit_code=result.returncode,
                 stdout_sha256=sha(out), stderr_sha256=sha(err))
    save(path, proof)
    if result.returncode:
        raise AssertionError('original case03 failed; full raw streams retained')
    summary = json.loads((retained / 'summary.json').read_text())
    if (summary['status'] != 'PASS' or summary['member_count'] != 854
            or summary['zip_sha256'] != sha(zipped)
            or summary['tar_sha256'] != sha(tar) or summary['cli_sha256'] != cli_sha):
        raise AssertionError('original case03 oracle or subject changed')
    worker.retire_owned_fixture(scratch)
    if list(TMP.iterdir()):
        raise AssertionError('normal-path fixture retirement incomplete')
    after = {p.name: sha(p) for p in STABLE.iterdir()}
    if after != before:
        raise AssertionError('normal-path task changed release assets')
    proof.update(status='PASS', retired_fixtures=['case-03'], assets_after=after,
                 original_oracle='PASS', summary_sha256=sha(retained / 'summary.json'),
                 all_source_fixtures_retired=True, stable_release_acceptance=False,
                 delivered_repaired_scanner_qualified=False)
    save(path, proof)
    print(json.dumps({'stage': 'original-case03-complete', 'status': 'PASS',
                      'proof_sha256': sha(path)}), flush=True)


if __name__ == '__main__':
    main()
