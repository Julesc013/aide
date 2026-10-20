"""Run existing published-predecessor oracles on the frozen actual 1.2 archives."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = Path(__file__).parent
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True) + '\n').encode())


import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    assert not sys.argv[1:]
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    built = json.loads((TASK / 'evidence/build-result.json').read_bytes())
    predecessor = built['identity']['predecessor_matrix'][0]
    assert predecessor['version'] == '1.1.0' and built['identity']['version'] == '1.2.0'
    assert subprocess.check_output(['git', 'rev-parse', predecessor['tag'] + '^{commit}'],
                                   text=True).strip() == predecessor['tag_commit']
    pins = {name: value['sha256'] for name, value in built['assets'].items()}
    pins.update({value['path']: value['sha256'] for value in predecessor['assets']})
    assert all(sha(ROOT / name) == expected for name, expected in pins.items())
    common = load('archive12_predecessor_common', TASK / 'run_consumer.py')
    helper = common.load('archive12_predecessor_helpers', common.CAN / 'lifecycle_helper.py')
    evaluation = common.load('archive12_predecessor_oracles', ROOT / 'evals/lite/lifecycle.py')
    capture = common.load('archive12_predecessor_capture',
        ROOT / '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py')
    work = TMP / 'case-predecessor'
    work.mkdir()
    tempfile.tempdir = str(work)
    os.environ.update(TEMP=str(work), TMP=str(work), TMPDIR=str(work), AIDE_RESOURCE_TEST_PARENT=str(work))

    class Recorder(helper.Recorder):
        def run(self, label, script, root, *parts, exits=(0,), offline_text=False):
            argv = [sys.executable, '-I', '-B', str(script), '--repo-root', str(root), *parts]
            row = {'argv': argv, 'exit_code': None, 'state': 'started'}
            stdout, stderr = OUT / (label + '.stdout'), OUT / (label + '.stderr')
            save(OUT / (label + '.json'), row)
            try:
                result = capture.capture_streams(argv, cwd=ROOT, env=dict(os.environ),
                    stdout_path=stdout, stderr_path=stderr, timeout=180)
                row.update(state='completed', exit_code=result.returncode)
            except BaseException as error:
                row.update(state='exception', error_type=type(error).__name__, error=str(error))
                raise
            finally:
                row['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                                  for p in (stdout, stderr) if p.exists()}
                save(OUT / (label + '.json'), row)
                self.commands.append({'label': label, 'record': label + '.json',
                                      'record_sha256': sha(OUT / (label + '.json'))})
            text = stdout.read_bytes().decode('utf-8', errors='replace')
            assert result.returncode in exits, (label, result.returncode)
            if offline_text:
                assert 'network_calls: none' in text
            return subprocess.CompletedProcess(argv, result.returncode, text,
                stderr.read_bytes().decode('utf-8', errors='replace'))

    packs = {}
    for version in ('1.1.0', '1.2.0'):
        stable = ROOT / '.aide/release/stable'
        members = helper.extract_zip(stable / f'aide-lite-v{version}.zip', work / ('zip-' + version))
        tar_members = helper.extract_tar(stable / f'aide-lite-v{version}.tar.gz', work / ('tar-' + version))
        assert members == tar_members
        packs[version] = work / ('zip-' + version) / helper.PACK_NAME
    recorder = Recorder(OUT)
    cases = evaluation.qualify_successor(work, OUT, recorder, helper, packs['1.1.0'], packs['1.2.0'],
                                         subject='aide-lite-v1.2.0-actual-archive')
    summary = {'status': 'PASS' if len(cases) == 2 and all(c['native_acceptance'] for c in cases) else 'FAIL',
               'cases': cases, 'commands': recorder.commands, 'assets': built['assets'],
               'predecessor': predecessor, 'fixture_retired': False, 'worker_model_requests': 0,
               'whole_model_usage': 'unknown', 'support_claimed': False}
    save(OUT / 'predecessor-result.json', summary)
    assert summary['status'] == 'PASS', 'existing predecessor oracle failed; original cases retained'
    assert all(sha(ROOT / name) == expected for name, expected in pins.items())
    worker = common.load('archive12_predecessor_retirement', common.ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(work)
    summary['fixture_retired'] = True
    save(OUT / 'predecessor-result.json', summary)
    print('PASS actual published 1.1 predecessor and frozen 1.2 archive conflict/recovery/preservation/exit')


if __name__ == '__main__':
    main()
