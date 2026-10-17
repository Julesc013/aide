"""One admitted successor build using the existing stable release owner."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    return {p.relative_to(ROOT).as_posix(): {'sha256': sha(p), 'size_bytes': p.stat().st_size}
            for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}


def main():
    assert sys.argv[1:] in ([], ['--repair'])
    repair = sys.argv[1:] == ['--repair']
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    before_name = 'release-before-rebuild.json' if repair else 'release-before.json'
    pack_name = 'pack-subject-repaired.json' if repair else 'pack-subject.json'
    before = json.loads((TASK / 'evidence' / before_name).read_text(encoding='utf-8'))
    assert inventory() == before
    pack = json.loads((TASK / 'evidence' / pack_name).read_text(encoding='utf-8'))
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    expected = {'.aide/release/stable/aide-lite-v1.1.0.' + suffix
                for suffix in ('zip', 'tar.gz', 'manifest.json', 'SHA256SUMS.txt')}
    previous = None
    if repair:
        previous = json.loads((TASK / 'evidence/build-result.json').read_text(encoding='utf-8'))
        assert set(previous['assets']) == expected
        assert all(before[name] == value for name, value in previous['assets'].items())
    else:
        assert not expected.intersection(before)
    for command in ('stable-build', 'stable-validate'):
        argv = [sys.executable, '-B', '.aide/scripts/aide_lite.py',
                'release', command, '--version', '1.1.0']
        with (OUTPUT / (command + '.stdout')).open('xb') as out, (OUTPUT / (command + '.stderr')).open('xb') as err:
            result = subprocess.run(argv, cwd=ROOT, stdout=out, stderr=err, timeout=120)
        (OUTPUT / (command + '-process.json')).write_text(json.dumps({
            'argv': argv, 'exit_code': result.returncode}, indent=2) + '\n', encoding='utf-8')
        assert result.returncode == 0, command + ' failed; raw output retained'
    after = inventory()
    assert set(after) == set(before) | expected
    preserved = {name: value for name, value in before.items() if name not in expected}
    assert all(after[name] == value for name, value in preserved.items())
    if repair:
        assert all(after[name] != before[name] for name in expected)
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    manifest = json.loads((ROOT / '.aide/release/stable/aide-lite-v1.1.0.manifest.json').read_text(encoding='utf-8'))
    identity = manifest['identity']
    assert identity['version'] == '1.1.0' and len(identity['public_cli_forms']) == 56
    assert identity['predecessor_matrix'][0]['version'] == '1.0.0'
    with zipfile.ZipFile(ROOT / '.aide/release/stable/aide-lite-v1.1.0.zip') as archive:
        cli_sha = hashlib.sha256(archive.read('aide-lite-pack-v0/files/.aide/scripts/aide_lite.py')).hexdigest()
    result = {'status': 'PASS_BUILD_ONLY', 'assets': {name: after[name] for name in sorted(expected)},
              'identity': identity, 'delivered_cli_sha256': cli_sha,
              'preserved_release_files': len(preserved), 'preserved_pack_files': len(pack),
              'consumer_qualification': 'pending', 'public_release': 'unchanged_1.0.0',
              'route': 'existing Windows Job managed resource runner',
              'outer_containment': 'unqualified', 'read_isolation': 'unqualified', 'model_calls': 0}
    if repair:
        result['superseded_candidate'] = previous['assets']
        result['prior_candidate_evidence'] = 'preserved; not evidence for replacement bytes'
    output_name = 'build-result-repaired.json' if repair else 'build-result.json'
    (OUTPUT / output_name).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('PASS: four candidate assets; all other release and pack bytes preserved')


if __name__ == '__main__':
    main()
