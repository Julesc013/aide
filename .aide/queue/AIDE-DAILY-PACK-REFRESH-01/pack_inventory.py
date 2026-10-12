"""Task-local ownership oracle; reuse existing path checks, never delete."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from core.execution.managed_workspace import ordinary, root_path

PACK_REL = '.aide/export/aide-lite-pack-v0'
EXCLUDED = {'manifest.yaml', 'checksums.json', 'export-report.md'}


def observe():
    root = root_path(str(REPO / PACK_REL))
    raw = subprocess.check_output(['git', 'ls-tree', '-rlz', 'HEAD', '--', PACK_REL], cwd=REPO)
    tracked = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        metadata, path = entry.decode('utf-8').split('\t', 1)
        mode, kind, blob, size = metadata.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('non-ordinary tracked pack member')
        relative = path.removeprefix(PACK_REL + '/')
        tracked[relative] = {'git_blob': blob, 'bytes': int(size)}
    if not tracked:
        raise ValueError('tracked generated pack required')
    expected_directories = {'.'}
    for name in tracked:
        expected_directories.update(str(parent).replace('\\', '/') for parent in Path(name).parents)
    files, directories, pending = {}, [], [root]
    while pending:
        directory = pending.pop()
        ordinary(directory, directory=True)
        relative_dir = directory.relative_to(root).as_posix() or '.'
        if relative_dir not in expected_directories:
            raise ValueError('unknown generated directory')
        directories.append(relative_dir)
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                info = path.lstat()
                if (stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400):
                    raise ValueError('linked or redirected descendant')
                if stat.S_ISDIR(info.st_mode):
                    ordinary(path, directory=True)
                    pending.append(path)
                else:
                    ordinary(path)
                    relative = path.relative_to(root).as_posix()
                    if relative not in tracked:
                        raise ValueError('untracked or unknown generated file')
                    data = path.read_bytes()
                    blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
                    if blob != tracked[relative]['git_blob'] or len(data) != tracked[relative]['bytes']:
                        raise ValueError('generated file differs from recoverable Git identity')
                    files[relative] = {'sha256': hashlib.sha256(data).hexdigest(),
                                       **tracked[relative], 'identity': [info.st_dev, info.st_ino]}
                if len(files) + len(directories) + len(pending) > 5000:
                    raise ValueError('generated inventory exceeds finite file allowance')
    if set(files) != set(tracked) or set(directories) != expected_directories:
        raise ValueError('incomplete generated inventory')
    checksums = json.loads((root / 'checksums.json').read_text(encoding='utf-8'))['checksums']
    if set(checksums) != set(files) - EXCLUDED:
        raise ValueError('checksum map does not cover the exact known inventory')
    if any(files[name]['sha256'] != value for name, value in checksums.items()):
        raise ValueError('generated checksum mismatch')
    info = ordinary(root, directory=True)
    return {'schema': 'aide.pack-ownership-inventory.v1', 'root': str(root),
            'root_identity': [info.st_dev, info.st_ino], 'files': files,
            'directories': sorted(directories), 'metadata_excluded_from_checksums': sorted(EXCLUDED),
            'file_count': len(files), 'total_bytes': sum(value['bytes'] for value in files.values()),
            'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()}


def require_same(expected):
    observed = observe()
    # The reviewed baseline may be an ancestor preparation commit. Content,
    # inode identity and complete inventory still must match immediately now.
    for key in ('root', 'root_identity', 'files', 'directories', 'metadata_excluded_from_checksums'):
        if observed[key] != expected[key]:
            raise ValueError('reviewed generated ownership changed: ' + key)
    return observed


if __name__ == '__main__':
    print(json.dumps(observe(), sort_keys=True, indent=2))
