"""Read-only bounded proof for exact old consumer expansions; never deletes."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

BASE = Path(r'D:\Projects\AIDE\_review_scratch')
PARENTS = {
    'customization-consumer-cc34021a8351': 'extracted-consumer-receipt.json',
    'customization-consumer-fcb30471c2f8': 'extracted-consumer-receipt-final.json',
}
SOURCE = '260139d2d10804b66960f8a33e88f55bc5d246f4'
REPO = Path(__file__).resolve().parents[4]


def digest(stream):
    result = hashlib.sha256()
    for block in iter(lambda: stream.read(65536), b''):
        result.update(block)
    return result.hexdigest()


def ordinary(path):
    item = path.lstat()
    if getattr(item, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError('reparse point: ' + str(path))
    return item


def prove(parent):
    canonical = '.aide/queue/AIDE-DELIVERED-PACK-CUSTOMIZATION-01/evidence/' + PARENTS[parent]
    frozen = subprocess.run(['git', '-C', str(REPO), 'show', SOURCE+':'+canonical],
                            capture_output=True, check=True, timeout=15).stdout
    parent = BASE / parent
    root, archive, receipt = parent/'old-extract', parent/'prior.zip', parent/'receipt.json'
    for path in (BASE, parent, root, archive, receipt):
        ordinary(path)
        if os.path.normcase(str(path.resolve(strict=True))) != os.path.normcase(str(path)):
            raise ValueError('resolved path mismatch: ' + str(path))
    if not root.is_relative_to(BASE) or not root.is_dir():
        raise ValueError('root outside named estate')
    owner = json.loads(receipt.read_text(encoding='utf-8-sig'))
    if owner != json.loads(frozen):
        raise ValueError('external receipt differs from committed custody')
    if os.path.normcase(owner.get('run_root', '')) != os.path.normcase(str(parent)):
        raise ValueError('receipt does not bind this consumer root')
    with archive.open('rb') as stream:
        archive_hash = digest(stream)
    if archive_hash != owner['prior_zip_sha256']:
        raise ValueError('retained archive digest mismatch')
    files, directories = {}, set()
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                item = ordinary(path)
                rel = path.relative_to(root).as_posix()
                if path.name.casefold() == '.git':
                    raise ValueError('nested repository')
                if stat.S_ISDIR(item.st_mode):
                    directories.add(rel)
                    pending.append(path)
                elif stat.S_ISREG(item.st_mode):
                    files[rel] = item
                else:
                    raise ValueError('unexpected object')
                if len(files)+len(directories) > 2048:
                    raise ValueError('bounded entry limit exceeded')
    expected, expected_dirs, manifest = {}, set(), []
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        if len(members) > 2048 or sum(m.file_size for m in members) > 64*1024**2:
            raise ValueError('bounded archive limit exceeded')
        folded = set()
        for member in members:
            rel = member.filename.rstrip('/')
            name = PurePosixPath(rel)
            if not rel or name.is_absolute() or '..' in name.parts or '\\' in rel or ':' in rel:
                raise ValueError('unsafe archive member')
            if rel.casefold() in folded:
                raise ValueError('duplicate archive member')
            folded.add(rel.casefold())
            expected_dirs.update(str(p) for p in name.parents if str(p) != '.')
            if member.is_dir():
                expected_dirs.add(rel)
            else:
                expected[rel] = member
        if set(files) != set(expected) or directories != expected_dirs:
            raise ValueError('extra/missing file or directory; preserved')
        for rel, member in expected.items():
            with zipped.open(member) as stream:
                expected_hash = digest(stream)
            with (root/rel).open('rb') as stream:
                actual_hash = digest(stream)
            after = ordinary(root/rel)
            before = files[rel]
            if actual_hash != expected_hash or before.st_size != member.file_size:
                raise ValueError('changed archive member: ' + rel)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                    after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
                raise ValueError('file changed during verification')
            manifest.append([rel, member.file_size, actual_hash])
    identity = ordinary(root)
    return dict(root=str(root), retained_archive=str(archive), archive_sha256=archive_hash,
                owner_receipt=str(receipt), files=len(files), logical_bytes=sum(s.st_size for s in files.values()),
                custody_source=SOURCE, custody_path=canonical,
                custody_sha256=hashlib.sha256(frozen).hexdigest(),
                directories=len(directories),
                root_identity=[identity.st_dev, identity.st_ino],
                manifest_sha256=hashlib.sha256(json.dumps(sorted(manifest), separators=(',', ':')).encode()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    rows = []
    for name in PARENTS:
        try:
            rows.append(dict(eligible=True, **prove(name)))
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            rows.append(dict(eligible=False, parent=name, reason=str(error)))
    Path(args.output).write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    print(json.dumps([dict(eligible=r['eligible'], root=r.get('root', r.get('parent')),
                           files=r.get('files'), logical_bytes=r.get('logical_bytes'),
                           reason=r.get('reason')) for r in rows]))
