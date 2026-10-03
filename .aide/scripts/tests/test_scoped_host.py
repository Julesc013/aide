"""Small owned fixtures for public scoped entry admission and identity checks."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('scoped_host_fixture', REPO/'core/execution/scoped_host.py')
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)


class ScopedHostTests(unittest.TestCase):
    def setUp(self):
        parent = scope.bounded_path(os.environ['AIDE_RESOURCE_TEST_PARENT'], directory=True)
        self.temp = tempfile.TemporaryDirectory(prefix='tiny-scope-', dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.roots = {key: self.root/key for key in ('scratch', 'retained', 'control')}
        for path in self.roots.values():
            path.mkdir()
        self.limits = {'scratch_bytes': 16, 'retained_bytes': 8,
                       'log_bytes': 4, 'max_files': 30}

    def test_aggregate_counts_all_pools_and_reserves_before_launch(self):
        for key, size in (('scratch', 7), ('retained', 11), ('control', 13)):
            (self.roots[key]/'owned').write_bytes(b'x'*size)
        required = 31 + 16 + 8 + 8 + 2*1048576
        view = scope.aggregate_admission(self.roots, self.limits, required)
        self.assertEqual(view['logical_bytes'], 31)
        self.assertEqual(view['by_pool'], {'scratch': 7, 'retained': 11, 'control': 13})
        with self.assertRaisesRegex(scope.ScopeRefused, 'aggregate pool budget'):
            scope.aggregate_admission(self.roots, self.limits, required-1)
        self.assertEqual(set(self.roots['scratch'].iterdir()), {self.roots['scratch']/'owned'})

    def test_incomplete_inventory_refuses(self):
        (self.roots['retained']/'one').write_bytes(b'1')
        with self.assertRaisesRegex(scope.ScopeRefused, 'incomplete'):
            scope.aggregate_admission(self.roots, {**self.limits, 'max_files': 0}, 2**30)

    def test_linked_pool_member_refuses(self):
        member = self.roots['retained']/'one'; member.write_bytes(b'1')
        os.link(member, self.roots['retained']/'two')
        with self.assertRaisesRegex(scope.ScopeRefused, 'single-link'):
            scope.aggregate_admission(self.roots, self.limits, 2**30)

    def test_tampered_executable_refuses_before_runtime_import(self):
        exe = self.root/'codex.exe'; exe.write_bytes(b'fixture')
        selection = {'schema': 'aide.scoped-host.local.v1', 'kind': 'codex_sandbox_readonly',
            'codex_executable': str(exe), 'codex_sha256': '0'*64,
            'read_roots': [str(self.root)], 'aggregate_bytes': 2**30, 'runtime': {}}
        with mock.patch.object(scope.importlib, 'import_module') as imported:
            with self.assertRaisesRegex(scope.ScopeRefused, 'executable changed'):
                scope.load_owner(selection, self.root)
            imported.assert_not_called()

    def test_unqualified_workloads_refuse_without_allocating(self):
        owner = mock.Mock(); host = mock.Mock()
        host.canonical_outputs = []
        for job in ({'adapter': 'codex_exec'}, {'adapter': 'python', 'canonical_outputs': {'any': {}}}):
            with self.assertRaisesRegex(scope.ScopeRefused, 'Python checks'):
                scope.run(owner, host, self.root/'config.json', job)
        owner.run.assert_not_called()

    def test_config_replacement_refuses_before_owner_admission(self):
        owner = mock.Mock()
        owner.digest.side_effect = lambda value: json.dumps(value, sort_keys=True)
        owner.load_config.return_value = ({'limits': {'scratch_bytes': 100}}, {}, [])
        path = self.root/'config.json'
        bound = scope.bind_config(owner, path, {'limits': {'scratch_bytes': 16}})
        with self.assertRaisesRegex(scope.ScopeRefused, 'envelope changed'):
            bound(path)

    def test_artifact_bytes_and_reservation_are_in_aggregate_budget(self):
        artifact = self.root/'artifact'; artifact.mkdir()
        (artifact/'accepted').write_bytes(b'12345678')
        roots = {**self.roots, 'canonical:.aide/export/aide-lite-pack-v0': artifact}
        required = 8 + 16 + 8 + 8 + 2*1048576 + 32
        view = scope.aggregate_admission(roots, self.limits, required, canonical_reservation=32)
        self.assertEqual(view['logical_bytes'], 8)
        with self.assertRaisesRegex(scope.ScopeRefused, 'aggregate pool budget'):
            scope.aggregate_admission(roots, self.limits, required-1, canonical_reservation=32)


if __name__ == '__main__':
    unittest.main()
