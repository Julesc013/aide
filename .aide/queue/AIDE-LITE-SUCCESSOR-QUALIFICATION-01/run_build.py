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
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    before = json.loads((TASK / 'evidence/release-before.json').read_text(encoding='utf-8'))
    assert inventory() == before
    pack = json.loads((TASK / 'evidence/pack-subject.json').read_text(encoding='utf-8'))
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    expected = {'.aide/release/stable/aide-lite-v1.1.0.' + suffix
                for suffix in ('zip', 'tar.gz', 'manifest.json', 'SHA256SUMS.txt')}
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
    assert set(after) - set(before) == expected
    assert all(after[name] == value for name, value in before.items())
    assert all(sha(ROOT / name) == digest for name, digest in pack.items())
    manifest = json.loads((ROOT / '.aide/release/stable/aide-lite-v1.1.0.manifest.json').read_text(encoding='utf-8'))
    identity = manifest['identity']
    assert identity['version'] == '1.1.0' and len(identity['public_cli_forms']) == 56
    assert identity['predecessor_matrix'][0]['version'] == '1.0.0'
    with zipfile.ZipFile(ROOT / '.aide/release/stable/aide-lite-v1.1.0.zip') as archive:
        cli_sha = hashlib.sha256(archive.read('aide-lite-pack-v0/files/.aide/scripts/aide_lite.py')).hexdigest()
    result = {'status': 'PASS_BUILD_ONLY', 'assets': {name: after[name] for name in sorted(expected)},
              'identity': identity, 'delivered_cli_sha256': cli_sha,
              'preserved_release_files': len(before), 'preserved_pack_files': len(pack),
              'consumer_qualification': 'pending', 'public_release': 'unchanged_1.0.0',
              'route': 'existing Windows Job managed resource runner',
              'outer_containment': 'unqualified', 'read_isolation': 'unqualified', 'model_calls': 0}
    (OUTPUT / 'build-result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('PASS: four new candidate assets; all prior release and pack bytes preserved')


if __name__ == '__main__':
    main()
