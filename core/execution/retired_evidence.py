"""Finite lossless custody for evidence already collected by the job owner.

Administrative operations reuse a caller-selected owner and its estate lock.
They grant no worker write access and are not an OS quota or host sandbox.
Original owner/receipt files stay untouched. A pending active.json blocks old
and new managed owners until complete custody retirement is reconciled.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import time
import zipfile

SCHEMA = 'aide.retired-evidence-custody.v1'
PENDING = 'aide.retired-evidence-custody-pending.v1'
MAX_BYTES = 16 * 1048576
MAX_ENTRIES = 4096
METADATA_RESERVE = 4 * 1048576


def _encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode('utf-8')


def _identity(info):
    return [info.st_dev, info.st_ino]


class _LimitedFile:
    def __init__(self, stream, maximum, refused):
        self.stream, self.maximum, self.refused = stream, maximum, refused

    def write(self, data):
        if self.stream.tell() + len(data) > self.maximum:
            raise self.refused('custody archive staging limit exceeded')
        return self.stream.write(data)

    def __getattr__(self, name):
        return getattr(self.stream, name)


class Custody:
    def __init__(self, owner, config_path):
        self.owner = owner
        self.config_path = config_path
        self.config, self.roots, self.working = owner.load_config(config_path)
        self.active = self.roots['control'] / 'active.json'
        self.ceiling = self.config.get('execution_host', {}).get('aggregate_bytes')
        if type(self.ceiling) is not int or not 0 < self.ceiling <= 2**63-1:
            self.refuse('custody requires a finite configured aggregate ceiling')

    def refuse(self, reason):
        raise self.owner.WorkspaceRefused(reason)

    def path(self, job_id):
        if not isinstance(job_id, str) or not re.fullmatch('[0-9a-f]{32}', job_id):
            self.refuse('exact retired job identity required')
        root = self.roots['retained'] / job_id
        self.owner.root_path(str(root))
        return root

    def anchors(self, root):
        receipt = self.owner.read_json(root / 'receipt.json')
        marker = self.owner.read_json(root / 'owner.json')
        if (receipt.get('job_id') != root.name or receipt.get('phase') != 'retired'
                or receipt.get('scratch_absent') is not True
                or receipt.get('reservation_released') is not True
                or (receipt.get('result') or {}).get('quiescent') is not True
                or receipt.get('manifest_digest') != self.owner.digest(receipt.get('job'))
                or marker != {'job_id': root.name, 'manifest_digest': receipt['manifest_digest']}
                or os.path.lexists(self.roots['scratch'] / root.name)
                or set(receipt.get('collected_manifest', {})) != {'logs', 'output'}):
            self.refuse('only owned quiescent collected retired evidence is eligible')
        return receipt, {name: self.owner.file_digest(root / name)
                         for name in ('owner.json', 'receipt.json')}

    def idle(self):
        if os.path.lexists(self.active) or os.path.lexists(self.active.with_name('active.json.next')):
            self.refuse('existing active operation requires explicit reconciliation')

    def relative(self, name):
        if (not isinstance(name, str) or not name or '\\' in name or ':' in name
                or '\0' in name or str(PurePosixPath(name)) != name
                or PurePosixPath(name).is_absolute()
                or any(part in ('', '.', '..') for part in name.split('/'))
                or name.split('/')[0] not in ('logs', 'output')):
            self.refuse('exact logs/output evidence member required')
        return name

    def snapshot(self, root):
        files, directories = [], []
        count = total = 0
        deadline = time.monotonic() + 20

        def visit(path):
            nonlocal count, total
            info = self.owner.ordinary(path, directory=True)
            directories.append({'path': path.relative_to(root).as_posix(),
                                'identity': _identity(info)})
            for child in sorted(path.iterdir(), key=lambda p: p.name):
                count += 1
                if count > MAX_ENTRIES or time.monotonic() > deadline:
                    self.refuse('custody observation incomplete within finite budget')
                name = self.relative(child.relative_to(root).as_posix())
                info = child.lstat()
                if stat.S_ISDIR(info.st_mode):
                    visit(child)
                else:
                    info = self.owner.ordinary(child)
                    total += info.st_size
                    if total > MAX_BYTES:
                        self.refuse('custody evidence byte limit exceeded')
                    files.append({'path': name, 'bytes': info.st_size,
                                  'sha256': self.owner.file_digest(child),
                                  'identity': _identity(info)})
                    if _identity(self.owner.ordinary(child)) != _identity(info):
                        self.refuse('custody evidence identity changed during observation')

        for tree in ('logs', 'output'):
            visit(root / tree)
        if len(files) + len(directories) > MAX_ENTRIES:
            self.refuse('custody entry limit exceeded')
        return files, directories, total

    def tree_digests(self, files, directories):
        by_file = {v['path']: v for v in files}
        dirs = {v['path'] for v in directories}
        result = {}
        for tree in ('logs', 'output'):
            value = hashlib.sha256()

            def visit(parent):
                children = sorted(p for p in (set(by_file) | dirs)
                                  if str(PurePosixPath(p).parent) == parent)
                for name in children:
                    relative = name[len(tree) + 1:]
                    if name in dirs:
                        value.update(json.dumps(['dir', relative]).encode())
                        visit(name)
                    else:
                        value.update(json.dumps(['file', relative, by_file[name]['sha256']]).encode())

            visit(tree)
            result[tree] = value.hexdigest()
        return result

    def inventory(self):
        used, entries = 0, 0
        deadline = time.monotonic() + 20
        observed = list(self.roots.values())
        canonical = self.config.get('execution_host', {}).get('canonical_outputs', [])
        if not isinstance(canonical, list) or len(canonical) != len(set(canonical)):
            self.refuse('invalid custody canonical inventory selection')
        for relative in canonical:
            if relative not in self.owner.CANONICAL_OUTPUT_PATHS:
                self.refuse('unknown custody canonical inventory destination')
            for work in self.working:
                path = work / relative
                if os.path.lexists(path):
                    observed.append(self.owner.root_path(str(path)))
        for root in observed:
            pending = [root]
            while pending:
                for child in pending.pop().iterdir():
                    entries += 1
                    if entries > self.config['limits']['max_files'] or time.monotonic() > deadline:
                        self.refuse('custody aggregate observation incomplete')
                    directory = stat.S_ISDIR(child.lstat().st_mode)
                    info = self.owner.ordinary(child, directory=directory)
                    if directory:
                        pending.append(child)
                    else:
                        used += info.st_size
        return used

    def _plan(self, job_id):
        root = self.path(job_id)
        receipt, anchors = self.anchors(root)
        if os.path.lexists(root / 'custody.json'):
            manifest = self.verify(job_id)
            return {'state': 'CUSTODIED', 'plan_digest': self.owner.digest(manifest['plan']),
                    'plan': manifest['plan'], 'writes': False}
        if {v.name for v in root.iterdir()} != {'owner.json', 'receipt.json', 'logs', 'output'}:
            self.refuse('unknown retained members require separate disposition')
        self.idle()
        files, directories, total = self.snapshot(root)
        collected = self.tree_digests(files, directories)
        if collected != receipt['collected_manifest']:
            self.refuse('retained collection digest changed')
        plan = {'schema': SCHEMA, 'job_id': job_id, 'root_identity': _identity(root.stat()),
                'config_digest': self.owner.digest(self.config), 'anchors': anchors,
                'collected_manifest': collected, 'files': files, 'directories': directories,
                'original_bytes': total, 'archive_limit_bytes': total + 1024 * (len(files) + len(directories)) + 65536,
                'metadata_reserve_bytes': METADATA_RESERVE, 'aggregate_limit_bytes': self.ceiling}
        if len(_encoded({'schema': PENDING, 'plan': plan})) > 1048576:
            self.refuse('custody intent record limit exceeded')
        used = self.inventory()
        reservation = plan['archive_limit_bytes'] + METADATA_RESERVE
        if used + reservation > self.ceiling:
            self.refuse('custody staging cannot fit configured aggregate budget')
        volume = self.owner.volume_identity(root)
        if self.owner.capacity(self.roots)['disk_free'][volume] - reservation < self.config['limits']['disk_reserve_bytes']:
            self.refuse('custody staging would consume configured disk headroom')
        return {'state': 'PLANNED', 'plan': plan, 'plan_digest': self.owner.digest(plan),
                'logical_bytes': used, 'reserved_bytes': reservation, 'writes': False}

    def plan(self, job_id):
        with self.owner.estate_lock(self.roots['control']):
            return self._plan(job_id)

    def check_plan(self, plan, *, mutation=True):
        root = self.path(plan['job_id'])
        receipt, anchors = self.anchors(root)
        if (plan.get('schema') != SCHEMA
                or (mutation and plan.get('config_digest') != self.owner.digest(self.config))
                or anchors != plan['anchors'] or _identity(root.stat()) != plan['root_identity']
                or receipt['collected_manifest'] != plan['collected_manifest']
                or (mutation and plan['aggregate_limit_bytes'] != self.ceiling)
                or plan['metadata_reserve_bytes'] != METADATA_RESERVE
                or type(plan['original_bytes']) is not int or not 0 <= plan['original_bytes'] <= MAX_BYTES
                or not 0 < len(plan['files']) + len(plan['directories']) <= MAX_ENTRIES
                or sum(v['bytes'] for v in plan['files']) != plan['original_bytes']
                or plan['archive_limit_bytes'] != plan['original_bytes'] + 1024 * (len(plan['files']) + len(plan['directories'])) + 65536):
            self.refuse('custody intent identity or bound changed')
        names = [self.relative(v['path']) for v in plan['files'] + plan['directories']]
        if len(names) != len(set(names)) or not {'logs', 'output'}.issubset(v['path'] for v in plan['directories']):
            self.refuse('custody member set invalid')
        if any(type(v['bytes']) is not int or not 0 <= v['bytes'] <= MAX_BYTES
               or not re.fullmatch('[0-9a-f]{64}', v['sha256']) for v in plan['files']):
            self.refuse('custody member bound invalid')
        if self.tree_digests(plan['files'], plan['directories']) != plan['collected_manifest']:
            self.refuse('custody original collection map changed')
        return root

    def remaining(self, plan):
        root = self.check_plan(plan)
        permitted = {'owner.json', 'receipt.json', 'logs', 'output',
                     'custody.json', 'custody.json.next', 'custody.zip', 'custody.zip.next'}
        if any(v.name not in permitted for v in root.iterdir()):
            self.refuse('unknown retained member preserved')
        expected_files = {v['path']: v for v in plan['files']}
        expected_dirs = {v['path']: v for v in plan['directories']}
        for tree in ('logs', 'output'):
            if not os.path.lexists(root / tree):
                continue
            pending = [root / tree]
            count = 0
            while pending:
                directory = pending.pop()
                name = directory.relative_to(root).as_posix()
                info = self.owner.ordinary(directory, directory=True)
                if name not in expected_dirs or _identity(info) != expected_dirs[name]['identity']:
                    self.refuse('remaining raw directory changed')
                for child in directory.iterdir():
                    count += 1
                    if count > MAX_ENTRIES:
                        self.refuse('remaining raw entry limit exceeded')
                    name = child.relative_to(root).as_posix()
                    if stat.S_ISDIR(child.lstat().st_mode):
                        pending.append(child)
                    else:
                        info = self.owner.ordinary(child)
                        expected = expected_files.get(name)
                        if (expected is None or _identity(info) != expected['identity']
                                or info.st_size != expected['bytes']
                                or self.owner.file_digest(child) != expected['sha256']):
                            self.refuse('remaining raw evidence changed')
        return root

    def verify_archive(self, root, plan):
        archive = root / 'custody.zip'
        if self.owner.ordinary(archive).st_size > plan['archive_limit_bytes']:
            self.refuse('custody archive size limit exceeded')
        expected = {v['path']: v for v in plan['files']}
        expected.update({v['path'] + '/': {'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
                         for v in plan['directories']})
        with zipfile.ZipFile(archive) as stream:
            entries = stream.infolist()
            if len(entries) != len(expected) or len({v.filename for v in entries}) != len(entries):
                self.refuse('custody archive member set changed')
            for entry in entries:
                match = expected.get(entry.filename)
                if (match is None or entry.file_size != match['bytes'] or entry.flag_bits & 1
                        or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)):
                    self.refuse('custody archive member identity or bound changed')
                value = hashlib.sha256()
                size = 0
                with stream.open(entry) as member:
                    while data := member.read(65536):
                        size += len(data)
                        if size > match['bytes']:
                            self.refuse('custody expanded member exceeds bound')
                        value.update(data)
                if size != match['bytes'] or value.hexdigest() != match['sha256']:
                    self.refuse('custody archive bytes changed')
        return {'archive_sha256': self.owner.file_digest(archive),
                'archive_bytes': self.owner.ordinary(archive).st_size}

    def verify(self, job_id):
        root = self.path(job_id)
        manifest = self.owner.read_json(root / 'custody.json')
        plan = manifest['plan']
        self.check_plan(plan, mutation=False)
        if (set(manifest) != {'schema', 'plan', 'archive_sha256', 'archive_bytes'}
                or manifest['schema'] != SCHEMA or plan['job_id'] != job_id
                or self.verify_archive(root, plan) != {k: manifest[k] for k in ('archive_sha256', 'archive_bytes')}):
            self.refuse('custody manifest/archive mismatch')
        return manifest

    def build(self, root, plan):
        staging = root / 'custody.zip.next'
        if os.path.lexists(staging):
            # Only explicit recovery reaches this owned staging path. Keep all
            # raw bytes until their complete snapshot is verified again.
            files, directories, _ = self.snapshot(root)
            if files != plan['files'] or directories != plan['directories']:
                self.refuse('interrupted archive source changed')
            if self.owner.ordinary(staging).st_size > plan['archive_limit_bytes']:
                self.refuse('interrupted archive exceeds its bound')
            staging.unlink()
        with staging.open('xb') as output:
            limited = _LimitedFile(output, plan['archive_limit_bytes'], self.owner.WorkspaceRefused)
            with zipfile.ZipFile(limited, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                for directory in plan['directories']:
                    archive.writestr(directory['path'] + '/', b'')
                for member in plan['files']:
                    source = root / member['path']
                    info = self.owner.ordinary(source)
                    if _identity(info) != member['identity'] or info.st_size != member['bytes']:
                        self.refuse('archive source identity changed')
                    value, size = hashlib.sha256(), 0
                    with source.open('rb') as raw, archive.open(member['path'], 'w') as target:
                        while data := raw.read(65536):
                            size += len(data)
                            if size > member['bytes']:
                                self.refuse('archive source grew')
                            value.update(data)
                            target.write(data)
                    if size != member['bytes'] or value.hexdigest() != member['sha256']:
                        self.refuse('archive source bytes changed')
            output.flush()
            os.fsync(output.fileno())
        if os.path.lexists(root / 'custody.zip'):
            self.refuse('unexpected custody archive preserved')
        os.rename(staging, root / 'custody.zip')

    def finish(self, pending, checkpoint=lambda _: None):
        plan = pending['plan']
        root = self.remaining(plan)
        if self.owner.read_json(self.active) != pending:
            self.refuse('pending custody reservation changed')
        if not os.path.lexists(root / 'custody.zip'):
            files, directories, _ = self.snapshot(root)
            if files != plan['files'] or directories != plan['directories']:
                self.refuse('custody source incomplete before archive')
            self.build(root, plan)
        checkpoint('archive_written')
        archive = self.verify_archive(root, plan)
        manifest = {'schema': SCHEMA, 'plan': plan, **archive}
        encoded = _encoded(manifest)
        if len(encoded) > 1048576 or archive['archive_bytes'] + len(encoded) >= plan['original_bytes']:
            self.refuse('complete custody does not reduce retained logical bytes')
        pointer = root / 'custody.json'
        if os.path.lexists(pointer):
            if self.owner.read_json(pointer) != manifest:
                self.refuse('custody manifest changed')
        else:
            stage = root / 'custody.json.next'
            if os.path.lexists(stage):
                if self.owner.read_json(stage) != manifest:
                    self.refuse('custody manifest staging changed')
                os.rename(stage, pointer)
            else:
                self.owner.write_json(pointer, manifest)
        checkpoint('manifest_verified')
        self.remaining(plan)
        # Cooperating owners are locked and workers cannot write this pool.
        # This is not an ACL guarantee against an unrestricted outside writer.
        for member in plan['files']:
            path = root / member['path']
            if os.path.lexists(path):
                info = self.owner.ordinary(path)
                if (_identity(info) != member['identity'] or info.st_size != member['bytes']
                        or self.owner.file_digest(path) != member['sha256']):
                    self.refuse('raw evidence changed before retirement')
                path.unlink()
                checkpoint('raw_file_retired')
        for directory in sorted(plan['directories'], key=lambda v: len(PurePosixPath(v['path']).parts), reverse=True):
            path = root / directory['path']
            if os.path.lexists(path):
                if _identity(self.owner.ordinary(path, directory=True)) != directory['identity']:
                    self.refuse('raw directory changed before retirement')
                path.rmdir()
        self.verify(plan['job_id'])
        if os.path.lexists(root / 'custody.zip.next') or os.path.lexists(root / 'custody.json.next'):
            self.refuse('custody staging requires reconciliation')
        checkpoint('raw_retired')
        if self.owner.read_json(self.active) != pending:
            self.refuse('pending custody reservation changed')
        self.active.unlink()
        return {'state': 'CUSTODIED', 'job_id': plan['job_id'], 'plan_digest': self.owner.digest(plan),
                **archive, 'original_bytes': plan['original_bytes'],
                'saved_logical_bytes': plan['original_bytes'] - archive['archive_bytes'] - len(encoded),
                'receipt_sha256': plan['anchors']['receipt.json'], 'pending_absent': True, 'writes': True}

    def apply(self, job_id, expected_digest, *, checkpoint=lambda _: None):
        with self.owner.estate_lock(self.roots['control']):
            view = self._plan(job_id)
            if view['plan_digest'] != expected_digest:
                self.refuse('custody plan changed; exact reviewed digest required')
            if view['state'] == 'CUSTODIED':
                self.idle()
                return view
            pending = {'schema': PENDING, 'phase': 'custody_pending', 'job_id': job_id,
                       'plan': view['plan'], 'plan_digest': expected_digest}
            if len(_encoded(pending)) > 1048576:
                self.refuse('custody intent record limit exceeded')
            self.owner.write_json(self.active, pending)
            checkpoint('intent_persisted')
            return self.finish(pending, checkpoint)

    def recover(self, job_id, expected_digest, *, checkpoint=lambda _: None):
        with self.owner.estate_lock(self.roots['control']):
            if not os.path.lexists(self.active):
                view = self._plan(job_id)
                if view['state'] != 'CUSTODIED' or view['plan_digest'] != expected_digest:
                    self.refuse('no matching pending custody operation')
                return view
            if os.path.lexists(self.active.with_name('active.json.next')):
                self.refuse('custody intent staging requires separate reconciliation')
            pending = self.owner.read_json(self.active)
            if (pending.get('schema') != PENDING or pending.get('phase') != 'custody_pending'
                    or pending.get('job_id') != job_id or pending.get('plan_digest') != expected_digest
                    or self.owner.digest(pending.get('plan')) != expected_digest):
                self.refuse('pending operation does not match exact custody intent')
            self.check_plan(pending['plan'])
            # Already allocated staging is included in inventory. Additional
            # space is needed only for missing archive/metadata, conservatively.
            root = self.path(job_id)
            reserve = METADATA_RESERVE
            if not os.path.lexists(root / 'custody.zip'):
                reserve += pending['plan']['archive_limit_bytes']
            if self.inventory() + reserve > self.ceiling:
                self.refuse('custody recovery cannot fit finite aggregate budget')
            return self.finish(pending, checkpoint)

    def read(self, job_id, member, *, offset=0, limit=2048, expected_sha256=None):
        self.relative(member)
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 0 < limit <= 65536:
            self.refuse('finite evidence slice required')
        root = self.path(job_id)
        if os.path.lexists(root / 'custody.json'):
            manifest = self.verify(job_id)
            entries = {v['path']: v for v in manifest['plan']['files']}
            item = entries.get(member)
            if item is None:
                self.refuse('evidence member not in complete custody map')
            with zipfile.ZipFile(root / 'custody.zip') as archive, archive.open(member) as stream:
                stream.seek(min(offset, item['bytes']))
                data = stream.read(limit)
            state = 'ARCHIVED'
        else:
            self.anchors(root)
            files, dirs, _ = self.snapshot(root)
            receipt = self.owner.read_json(root / 'receipt.json')
            if self.tree_digests(files, dirs) != receipt['collected_manifest']:
                self.refuse('raw evidence no longer matches collection')
            item = next((v for v in files if v['path'] == member), None)
            if item is None:
                self.refuse('raw evidence member absent')
            with (root / member).open('rb') as stream:
                stream.seek(min(offset, item['bytes']))
                data = stream.read(limit)
            state = 'RAW'
        if expected_sha256 is not None and expected_sha256 != item['sha256']:
            self.refuse('requested evidence digest does not match custody')
        return {'state': state, 'job_id': job_id, 'member': member, 'bytes': item['bytes'],
                'sha256': item['sha256'], 'offset': offset, 'returned_bytes': len(data),
                'slice_base64': base64.b64encode(data).decode('ascii'), 'writes': False}
