"""Draft: rebuild only the unpublished candidate and retain a complete archive-member delta."""
import ast
import hashlib
import io
import json
import os
import platform
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
sys.dont_write_bytecode = True


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True) + '\n').encode())


def inventory():
    return {p.relative_to(ROOT).as_posix(): {'sha256': sha(p), 'size_bytes': p.stat().st_size}
            for p in sorted((ROOT / '.aide/release').rglob('*')) if p.is_file()}


def zip_members(raw):
    result = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for member in archive.infolist():
            assert member.filename not in result
            mode = member.external_attr >> 16
            assert stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR)
            assert not member.is_dir() or stat.S_IFMT(mode) in (0, stat.S_IFDIR)
            data = b'' if member.is_dir() else archive.read(member)
            result[member.filename] = {'kind': 'directory' if member.is_dir() else 'file',
                'mode': mode, 'size_bytes': len(data), 'sha256': digest(data),
                'create_system': member.create_system, 'external_attr': member.external_attr}
    return result


def tar_members(raw):
    result = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        for member in archive:
            assert member.name not in result and (member.isfile() or member.isdir())
            data = archive.extractfile(member).read() if member.isfile() else b''
            result[member.name] = {'kind': 'directory' if member.isdir() else 'file',
                'mode': member.mode, 'size_bytes': len(data), 'sha256': digest(data),
                'type': member.type.decode('ascii'), 'linkname': member.linkname,
                'uid': member.uid, 'gid': member.gid, 'uname': member.uname, 'gname': member.gname}
    return result


def original_blob(checkpoint, path, expected):
    raw = subprocess.check_output(['git', 'show', checkpoint + ':' + path], cwd=ROOT)
    assert digest(raw) == expected
    return raw


def main():
    assert not sys.argv[1:]
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    before = json.loads((E / 'revised-release-before.json').read_bytes())
    pack = json.loads((E / 'revised-pack-subject.json').read_bytes())
    original = json.loads((E / 'build-result.json').read_bytes())
    environment = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
                   'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(),
                                                            'version': platform.python_version()}}
    profile = next(p for p in original['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    assert environment == profile['environment']
    baseline = json.loads((E / 'link-baseline.json').read_bytes())
    assert inventory() == before
    assert all(sha(ROOT / name) == expected for name, expected in pack.items())
    names = {'.aide/release/stable/aide-lite-v1.2.0.' + suffix
             for suffix in ('zip', 'tar.gz', 'manifest.json', 'SHA256SUMS.txt')}
    assert names == set(original['assets']) and names <= set(before)
    checkpoint = baseline['original_candidate_checkpoint']
    originals = {name: original_blob(checkpoint, name, original['assets'][name]['sha256']) for name in names}
    record = {'state': 'started', 'qualified': False, 'original_candidate_checkpoint': checkpoint,
              'worker_model_requests': 0, 'whole_model_usage': 'unknown', 'support_claimed': False}
    try:
        for action in ('stable-build', 'stable-validate'):
            argv = [sys.executable, '-I', '-B', '.aide/scripts/aide_lite.py', 'release', action,
                    '--version', '1.2.0']
            entry = {'argv': argv, 'state': 'started', 'exit_code': None}
            save(OUT / (action + '.json'), entry)
            streams = [OUT / (action + suffix) for suffix in ('.stdout', '.stderr')]
            try:
                with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
                    process = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                                             stdout=stdout, stderr=stderr, timeout=240)
                entry.update(state='completed', exit_code=process.returncode)
            except BaseException as error:
                entry.update(state='exception', error_type=type(error).__name__, error=str(error))
                raise
            finally:
                entry['streams'] = {p.name: {'size_bytes': p.stat().st_size, 'sha256': sha(p)}
                                    for p in streams if p.exists()}
                save(OUT / (action + '.json'), entry)
            assert process.returncode == 0, action + ' failed; preserve actual partial effects'
        after = inventory()
        assert set(after) == set(before)
        assert {name for name in before if before[name] != after[name]} == names
        assert all(sha(ROOT / name) == expected for name, expected in pack.items())
        inventories = {}
        for extension, reader in (('zip', zip_members), ('tar.gz', tar_members)):
            name = '.aide/release/stable/aide-lite-v1.2.0.' + extension
            old, new = reader(originals[name]), reader((ROOT / name).read_bytes())
            assert set(old) == set(new)
            changed = {path for path in old if old[path] != new[path]}
            expected = {'aide-lite-pack-v0/' + path for path in
                        ('files/core/execution/managed_workspace.py', 'manifest.yaml',
                         'checksums.json', 'stable-release.json')}
            assert changed == expected, (extension, changed)
            for path in changed:
                assert {k: v for k, v in old[path].items() if k not in ('size_bytes', 'sha256')} == {
                    k: v for k, v in new[path].items() if k not in ('size_bytes', 'sha256')}
            inventories[extension] = {'old': old, 'new': new, 'changed': sorted(changed)}
        assert set(inventories['zip']['new']) == set(inventories['tar.gz']['new'])
        for path, row in inventories['zip']['new'].items():
            other = inventories['tar.gz']['new'][path]
            assert all(row[key] == other[key] for key in ('kind', 'size_bytes', 'sha256'))
        manifest = json.loads((ROOT / '.aide/release/stable/aide-lite-v1.2.0.manifest.json').read_bytes())
        identity = manifest['identity']
        source_fields = {'source_commit', 'source_tree', 'source_pack_checksums_sha256'}
        assert {k: v for k, v in original['identity'].items() if k not in source_fields} == {
            k: v for k, v in identity.items() if k not in source_fields}
        with zipfile.ZipFile(ROOT / '.aide/release/stable/aide-lite-v1.2.0.zip') as archive:
            assert json.loads(archive.read('aide-lite-pack-v0/stable-release.json')) == identity
            cli = digest(archive.read('aide-lite-pack-v0/files/.aide/scripts/aide_lite.py'))
            assert cli == original['delivered_cli_sha256']
            actual = archive.read('aide-lite-pack-v0/files/core/execution/managed_workspace.py')
            assert actual == (ROOT / 'core/execution/managed_workspace.py').read_bytes()
        with zipfile.ZipFile(io.BytesIO(originals['.aide/release/stable/aide-lite-v1.2.0.zip'])) as archive:
            prior = archive.read('aide-lite-pack-v0/files/core/execution/managed_workspace.py')
        def functions(raw):
            return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(raw).body
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        old_functions, new_functions = functions(prior), functions(actual)
        assert set(old_functions) == set(new_functions)
        assert {name for name in old_functions if old_functions[name] != new_functions[name]} == {'tree_usage'}
        save(OUT / 'archive-member-delta.json', {'status': 'PASS_COMPLETE_MEMBER_DELTA',
            'original_assets': original['assets'], 'revised_assets': {name: after[name] for name in sorted(names)},
            'original_checkpoint': checkpoint, 'inventories': inventories,
            'changed_executable_functions': ['core/execution/managed_workspace.py:tree_usage'],
            'changed_identity_fields': sorted(source_fields),
            'reuse_boundary': 'Inventory equivalence is necessary but not sufficient: actual dependency and assertion applicability requires independent review; original runs retain original archive subjects.'})
        save(OUT / 'revised-build-result.json', {'status': 'PASS_BUILD_ONLY',
            'assets': {name: after[name] for name in sorted(names)}, 'identity': identity,
            'delivered_cli_sha256': cli, 'preserved_release_files': len(before) - 4,
            'preserved_pack_files': len(pack), 'original_candidate_assets': original['assets'],
            'original_candidate_checkpoint': checkpoint, 'archive_members': len(inventories['zip']['new']),
            'qualification': 'affected consumers, applicability proof, hosted profiles and replay pending',
            'support_claimed': False, 'worker_model_requests': 0, 'whole_model_usage': 'unknown'})
        record.update(state='passed_revised_build_only', assets={name: after[name] for name in sorted(names)})
    except BaseException as error:
        record.update(state='stopped', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record['observed_assets'] = {name: {'sha256': sha(ROOT / name), 'size_bytes': (ROOT / name).stat().st_size}
                                    for name in sorted(names) if (ROOT / name).is_file()}
        save(OUT / 'revised-build-command.json', record)
    print('PASS revised candidate build and complete archive delta; no qualification or publication claim')


if __name__ == '__main__':
    main()
