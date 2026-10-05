"""Prepare only the reviewed runtime closure in this managed allocation."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import zipfile

REPO = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    identity = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(length)):
        raise ctypes.WinError()
    if identity.value != 'BLACKGLASS-WIN1\\CodexSandboxOffline':
        raise AssertionError('restricted builder identity required')
    config = json.loads((EVIDENCE / 'active-zero-link-source-config.log').read_text())
    expected = json.loads((EVIDENCE / 'active-zero-link-normal-path-plan-v2.log').read_text())['expected_runtime']
    runtime = config['execution_host']['runtime']
    candidate = REPO / 'core/execution/managed_workspace.py'
    if sha(candidate) != expected['source_candidate_sha256']:
        raise AssertionError('qualified candidate changed')
    archive = OUTPUT / 'runtime-candidate.zip'
    files, changed = {}, []
    with archive.open('xb') as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9, allowZip64=False) as zipped:
            for path, original in sorted(runtime['files'].items()):
                source = REPO / path
                if sha(source) != original:
                    raise AssertionError('original runtime changed: ' + path)
                relative = Path(path).relative_to(runtime['root']).as_posix()
                if relative == 'core/execution/managed_workspace.py':
                    source = candidate
                data = source.read_bytes()
                name = 'runtime/' + relative
                files[name] = hashlib.sha256(data).hexdigest()
                if files[name] != original:
                    changed.append(relative)
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                zipped.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED,
                                compresslevel=9)
    if (files != expected['files'] or len(files) != 26
            or changed != ['core/execution/managed_workspace.py']
            or sha(archive) != expected['archive_sha256']
            or archive.stat().st_size != expected['archive_bytes']):
        raise AssertionError('runtime output differs from reviewed closure')
    with zipfile.ZipFile(archive) as zipped:
        if len(zipped.namelist()) != 26 or set(zipped.namelist()) != set(files):
            raise AssertionError('unexpected runtime members')
        for name, digest in files.items():
            if hashlib.sha256(zipped.read(name)).hexdigest() != digest:
                raise AssertionError('runtime readback failed')
    if list(TMP.iterdir()):
        raise AssertionError('builder left unexpected scratch')
    proof = {'schema': 'aide.active-zero-link-runtime-builder.v1', 'status': 'PASS',
             'windows_identity': identity.value, 'archive_sha256': sha(archive),
             'archive_bytes': archive.stat().st_size, 'files': files,
             'changed_components': changed, 'model_calls': 0,
             'supervisor_promoted': False, 'release_assets_modified': False,
             'whole_session_contained': False}
    (OUTPUT / 'runtime-builder.json').write_text(
        json.dumps(proof, sort_keys=True, indent=2) + '\n',
        encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'PASS', 'archive_sha256': sha(archive),
                      'archive_bytes': archive.stat().st_size}), flush=True)


if __name__ == '__main__':
    main()
