"""Regenerate frozen archive payloads in admitted scratch and verify current source."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def main():
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    spec = importlib.util.spec_from_file_location('replay_common', TASK / 'run_consumer.py')
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    lite = common.load('replay_source_lite', ROOT / '.aide/scripts/aide_lite.py')
    subject = json.loads((TASK / 'evidence/build-result-repaired.json').read_text(encoding='utf-8'))
    frozen = json.loads((TASK / 'evidence/pack-subject-repaired.json').read_text(encoding='utf-8'))
    pack = ROOT / '.aide/export/aide-lite-pack-v0'
    before = {p.relative_to(ROOT).as_posix(): common.sha(p)
              for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}
    assert all(common.sha(ROOT / p) == d for p, d in frozen.items())
    assert all(before[p] == v['sha256'] for p, v in subject['assets'].items())

    operations = {}
    for label, arguments in [('doctor', ['doctor']), ('validate', ['validate']),
                             ('stable-validate', ['release', 'stable-validate', '--version', '1.1.0']),
                             ('pack-status', ['pack-status'])]:
        argv = [sys.executable, '-B', '.aide/scripts/aide_lite.py', *arguments]
        with (OUT / (label + '.stdout')).open('xb') as stdout, (OUT / (label + '.stderr')).open('xb') as stderr:
            process = subprocess.run(argv, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=120)
        operations[label] = {'argv': argv, 'exit_code': process.returncode,
                             'stdout_sha256': common.sha(OUT / (label + '.stdout')),
                             'stderr_sha256': common.sha(OUT / (label + '.stderr'))}
        common.write(OUT / 'operations.json', operations)
        assert process.returncode == 0, (label, process.returncode)

    fixture = TMP / 'case-archive-replay'
    fixture.mkdir()
    projected = fixture / lite.RELEASE_ARCHIVE_ROOT
    lite.build_release_pack_projection(pack, projected)
    lite.write_text_if_changed(projected / 'stable-release.json', lite.stable_json_text(subject['identity']))
    lite.write_text_if_changed(projected / 'checksums.json', lite.stable_json_text(lite.build_pack_checksums(projected)))
    okay, problems = lite.validate_pack_checksums(projected)
    assert okay, problems
    replay = {}
    for suffix, writer in [('zip', lite.write_release_zip), ('tar.gz', lite.write_release_tar_gz)]:
        path = fixture / ('aide-lite-v1.1.0.' + suffix)
        writer(projected, path)
        relative = '.aide/release/stable/' + path.name
        observed = {'sha256': common.sha(path), 'size_bytes': path.stat().st_size}
        assert observed == subject['assets'][relative], suffix
        replay[relative] = observed

    after = {p.relative_to(ROOT).as_posix(): common.sha(p)
             for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}
    assert after == before
    assert all(common.sha(ROOT / p) == d for p, d in frozen.items())
    result = {'status': 'PASS', 'replay': replay, 'identity': subject['identity'],
              'recipe': 'existing release projection and archive writers; validated frozen identity',
              'preserved_release_files': len(before), 'preserved_pack_files': len(frozen),
              'operations': operations, 'model_calls': 0, 'publication': 'not performed',
              'fixture_retired': False}
    common.write(OUT / 'replay-result.json', result)
    worker = common.load('replay_retirement', common.ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(fixture)
    result['fixture_retired'] = True
    common.write(OUT / 'replay-result.json', result)
    print('PASS exact scratch archive replay and current source checks')


if __name__ == '__main__':
    main()
