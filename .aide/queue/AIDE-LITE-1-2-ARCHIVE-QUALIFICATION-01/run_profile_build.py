"""Metadata-only candidate build through the existing stable-release owner."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
spec = importlib.util.spec_from_file_location('profile_build_existing_owner', TASK / 'run_revised_build.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert not sys.argv[1:]
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    old = json.loads((E / 'revised-build-result.json').read_bytes())
    before = json.loads((E / 'profile-release-before.json').read_bytes())
    pack = json.loads((E / 'revised-pack-subject.json').read_bytes())
    change = json.loads((E / 'profile-candidate-delta.json').read_bytes())
    candidate = json.loads((ROOT / '.aide/release/successor-candidate.json').read_bytes())
    assert h.sha(ROOT / '.aide/release/successor-candidate.json') == change['new_sha256']
    assert h.inventory() == before
    assert all(h.sha(ROOT / name) == value for name, value in pack.items())
    actual = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
              'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(), 'version': platform.python_version()}}
    assert actual == next(p for p in old['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')['environment']
    names = set(old['assets'])
    originals = {name: h.original_blob('4f85bb0c95ef7fc29667edd351346d684a80bb48', name, row['sha256']) for name, row in old['assets'].items()}
    record = {'state': 'started', 'model_requests': 0, 'whole_model_usage': 'unknown', 'support_claimed': False}
    try:
        for action in ('stable-build', 'stable-validate'):
            argv = [sys.executable, '-I', '-B', '.aide/scripts/aide_lite.py', 'release', action, '--version', '1.2.0']
            row = {'argv': argv, 'state': 'started', 'exit_code': None}
            h.save(OUT / (action + '.json'), row)
            streams = [OUT / (action + suffix) for suffix in ('.stdout', '.stderr')]
            try:
                with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
                    process = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=240)
                row.update(state='completed', exit_code=process.returncode)
            except BaseException as error:
                row.update(state='exception', error_type=type(error).__name__, error=str(error))
                raise
            finally:
                row['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': h.sha(p)} for p in streams if p.exists()}
                h.save(OUT / (action + '.json'), row)
            assert process.returncode == 0, action
        after = h.inventory()
        assert set(after) == set(before)
        assert {name for name in before if before[name] != after[name]} == names
        assert all(h.sha(ROOT / name) == value for name, value in pack.items())
        inventories = {}
        for suffix, reader in (('zip', h.zip_members), ('tar.gz', h.tar_members)):
            name = '.aide/release/stable/aide-lite-v1.2.0.' + suffix
            left, right = reader(originals[name]), reader((ROOT / name).read_bytes())
            assert set(left) == set(right) and len(left) == 879
            changed = {p for p in left if left[p] != right[p]}
            assert changed == {'aide-lite-pack-v0/stable-release.json', 'aide-lite-pack-v0/checksums.json'}
            for path in changed:
                assert {k: v for k, v in left[path].items() if k not in ('size_bytes', 'sha256')} == {
                    k: v for k, v in right[path].items() if k not in ('size_bytes', 'sha256')}
            inventories[suffix] = {'old': left, 'new': right, 'changed': sorted(changed)}
        for path, row in inventories['zip']['new'].items():
            assert all(row[key] == inventories['tar.gz']['new'][path][key] for key in ('kind', 'size_bytes', 'sha256'))
        manifest = json.loads((ROOT / '.aide/release/stable/aide-lite-v1.2.0.manifest.json').read_bytes())
        identity = manifest['identity']
        expected = copy.deepcopy(old['identity'])
        expected['successor_contract_sha256'] = change['new_sha256']
        next(p for p in expected['profiles'] if p['profile_id'] == 'aide-lite-local-linux')['environment'] = change['new_environment']
        assert identity == expected and identity['profiles'] == candidate['profiles']
        with zipfile.ZipFile(ROOT / '.aide/release/stable/aide-lite-v1.2.0.zip') as archive:
            assert json.loads(archive.read('aide-lite-pack-v0/stable-release.json')) == identity
            assert h.digest(archive.read('aide-lite-pack-v0/files/.aide/scripts/aide_lite.py')) == old['delivered_cli_sha256']
        h.save(OUT / 'profile-archive-member-delta.json', {'state': 'PASS_METADATA_ONLY_COMPLETE_DELTA',
            'original_checkpoint': '4f85bb0c95ef7fc29667edd351346d684a80bb48',
            'original_assets': old['assets'], 'new_assets': {n: after[n] for n in sorted(names)},
            'inventories': inventories, 'changed_executable_files': [], 'unchanged_members_per_archive': 877,
            'identity_change': change, 'source_provenance': 'unchanged',
            'reuse': 'Original macOS and other observations retain their archive subjects; applicability needs independent review.'})
        h.save(OUT / 'profile-build-result.json', {'status': 'PASS_BUILD_ONLY', 'assets': {n: after[n] for n in sorted(names)},
            'identity': identity, 'delivered_cli_sha256': old['delivered_cli_sha256'], 'archive_members': 879,
            'preserved_release_files': len(before) - 4, 'preserved_pack_files': len(pack),
            'support_claimed': False, 'model_requests': 0, 'whole_model_usage': 'unknown'})
        record['state'] = 'passed_metadata_build_only'
    except BaseException as error:
        record.update(state='stopped', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record['observed_assets'] = {n: {'sha256': h.sha(ROOT / n), 'size_bytes': (ROOT / n).stat().st_size} for n in sorted(names) if (ROOT / n).is_file()}
        h.save(OUT / 'profile-build-command.json', record)
    print('PASS Linux environment metadata-only build; executable/export bytes preserved')


if __name__ == '__main__':
    main()
