"""Independent refusal fixtures; Git metadata is a declared fixture oracle."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pack_inventory as inventory
from core.execution.managed_workspace import WorkspaceRefused


class PackOwnershipTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.pack = self.root / inventory.PACK_REL
        (self.pack / 'files').mkdir(parents=True)
        (self.pack / 'files/member.txt').write_bytes(b'known generated fixture\n')
        (self.pack / 'manifest.yaml').write_bytes(b'fixture manifest\n')
        (self.pack / 'export-report.md').write_bytes(b'fixture report\n')
        (self.pack / 'checksums.json').write_text(json.dumps({'checksums': {
            'files/member.txt': hashlib.sha256((self.pack / 'files/member.txt').read_bytes()).hexdigest()}}))
        self.names = ['files/member.txt', 'manifest.yaml', 'checksums.json', 'export-report.md']
        self.rows = self.git_rows()
        self.addCleanup(patch.stopall)
        patch.object(inventory, 'REPO', self.root).start()
        patch.object(inventory.subprocess, 'check_output', side_effect=self.fake_git).start()

    def git_rows(self):
        rows = []
        for name in self.names:
            data = (self.pack / name).read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            rows.append(f'100644 blob {blob} {len(data)}\t{inventory.PACK_REL}/{name}\0'.encode())
        return b''.join(rows)

    def fake_git(self, argv, **kwargs):
        return self.rows if 'ls-tree' in argv else 'fixture-subject\n'

    def test_complete_owned_fixture_is_accepted(self):
        observed = inventory.observe()
        self.assertEqual(observed['file_count'], 4)
        self.assertEqual(set(observed['directories']), {'.', 'files'})
        inventory.require_same(observed)

    def test_unknown_file_refuses_without_retiring_it(self):
        unknown = self.pack / 'files/keep.txt'
        unknown.write_bytes(b'preserve unknown bytes')
        with self.assertRaises(ValueError):
            inventory.observe()
        self.assertEqual(unknown.read_bytes(), b'preserve unknown bytes')

    def test_unknown_directory_refuses_before_descending(self):
        unknown = self.pack / 'unknown'
        unknown.mkdir()
        with self.assertRaises(ValueError):
            inventory.observe()
        self.assertTrue(unknown.is_dir())

    def test_changed_tracked_bytes_refuse(self):
        member = self.pack / 'files/member.txt'
        member.write_bytes(b'changed locally')
        with self.assertRaises(ValueError):
            inventory.observe()
        self.assertEqual(member.read_bytes(), b'changed locally')

    def test_incomplete_checksum_coverage_refuses(self):
        (self.pack / 'checksums.json').write_text(json.dumps({'checksums': {}}))
        self.rows = self.git_rows()
        with self.assertRaises(ValueError):
            inventory.observe()

    def test_multiply_linked_member_refuses(self):
        member = self.pack / 'files/member.txt'
        alias = self.pack / 'files/owned-alias.txt'
        alias.hardlink_to(member)
        try:
            with self.assertRaisesRegex(WorkspaceRefused, 'single-link'):
                inventory.observe()
            self.assertEqual(member.read_bytes(), b'known generated fixture\n')
        finally:
            alias.unlink()  # Exact freshly created fixture alias; no recursive cleanup.


if __name__ == '__main__':
    unittest.main()
