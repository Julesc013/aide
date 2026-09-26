from __future__ import annotations
import hashlib
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from core.execution import managed_workspace as workspace


class ManagedWorkspaceTests(unittest.TestCase):
    def setUp(self):
        # The bootstrap test command must name an existing bounded parent.
        # Never let tempfile pick a machine-wide fallback for these fixtures.
        parent = workspace.root_path(os.environ['AIDE_RESOURCE_TEST_PARENT'])
        self.temp = tempfile.TemporaryDirectory(prefix='tiny-runner-', dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.roots = {name: self.root / name for name in ('scratch', 'retained', 'control')}
        for path in self.roots.values(): path.mkdir()
        self.source = self.root / 'source'; self.source.mkdir()
        self.config = {'schema': 'aide.managed-workspace.local.v1',
            'roots': {key: str(value) for key, value in self.roots.items()},
            'volume_ids': {key: workspace.volume_identity(value) for key, value in self.roots.items()},
            'working_roots': [str(self.source)],
            'limits': {'disk_reserve_bytes': 1024, 'physical_reserve_bytes': 1024,
                'commit_reserve_bytes': 1024, 'scratch_bytes': 1024 * 1024,
                'retained_bytes': 65536, 'memory_bytes': 128 * 1024 * 1024,
                'log_bytes': 4096, 'runtime_seconds': 3, 'processes': 4, 'max_files': 100}}
        self.config_path = self.root / 'config.json'
        workspace.write_json(self.config_path, self.config)
        self.ample = {'disk_free': {workspace.volume_identity(self.root): 2**40},
                      'physical_free': 2**40, 'commit_free': 2**40}
        self.job = {'schema': 'aide.maintainer-job.v1', 'owner': 'synthetic_fixture',
                    'workunit': 'AIDE-CAMPAIGN-RESOURCE-CLEANUP-01', 'cwd': str(self.source),
                    'argv': [sys.executable, 'fixture.py'], 'adapter': 'python'}

    def real_job(self, text):
        script = self.source / 'fixture.py'; script.write_text(text, encoding='utf-8')
        env = workspace.sanitized_environment()
        for args in (('init',), ('add', '--', 'fixture.py'),
                     ('-c', 'user.name=AIDE Fixture', '-c', 'user.email=fixture@example.invalid',
                      'commit', '-m', 'test(fixture): pin tiny bounded job input')):
            subprocess.run(['git', '-C', str(self.source), *args], env=env, capture_output=True, check=True, timeout=10)
        def git(*args):
            return subprocess.run(['git', '-C', str(self.source), *args], env=env, capture_output=True, text=True, check=True, timeout=10).stdout.strip()
        self.job.update(source_commit=git('rev-parse', 'HEAD'), source_tree=git('rev-parse', 'HEAD^{tree}'),
            executable_sha256=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
            inputs={'fixture.py': hashlib.sha256(script.read_bytes()).hexdigest()})
        return self.job

    def test_disk_and_memory_refusal_allocate_nothing(self):
        for changed in ({'disk_free': {workspace.volume_identity(self.root): 1024}}, {'physical_free': 1024}, {'commit_free': 1024}):
            with self.subTest(changed=changed):
                observed = {**self.ample, **changed}
                with mock.patch.object(workspace, 'validate_job', return_value=self.source):
                    with self.assertRaises(workspace.WorkspaceRefused):
                        workspace.run(self.config_path, self.job, probe=lambda _: observed)
                self.assertEqual(list(self.roots['scratch'].iterdir()), [])
                self.assertFalse((self.roots['control']/'active.json').exists())

    def test_concurrent_reservation_refused_by_os_lock(self):
        code = 'import sys;sys.path.insert(0,sys.argv[1]);from pathlib import Path;from core.execution.managed_workspace import estate_lock;\nwith estate_lock(Path(sys.argv[2])): print("BAD")'
        with workspace.estate_lock(self.roots['control']):
            child = subprocess.run([sys.executable, '-B', '-c', code, str(REPO), str(self.roots['control'])],
                capture_output=True, timeout=5, env=workspace.sanitized_environment())
            self.assertNotEqual(child.returncode, 0)
            self.assertIn(b'another heavy job', child.stderr)

    def test_missing_pool_wrong_volume_and_escape_have_no_fallback(self):
        original = json.loads(json.dumps(self.config))
        for edit in ('missing', 'escape', 'volume'):
            value = json.loads(json.dumps(original))
            if edit == 'missing': value['roots']['scratch'] = str(self.root/'not-created')
            elif edit == 'escape': value['roots']['scratch'] += '/../../escape'
            else: value['volume_ids']['scratch'] = 'wrong-volume'
            workspace.write_json(self.config_path, value)
            with self.assertRaises((OSError, workspace.WorkspaceRefused)):
                workspace.inspect(self.config_path)
            self.assertFalse((self.root/'not-created').exists())
            self.assertEqual(list(self.roots['scratch'].iterdir()), [])

    def test_inspection_is_nonmutating(self):
        def snapshot():
            return {str(p.relative_to(self.root)): (p.stat().st_size, p.stat().st_mtime_ns)
                    for p in self.root.rglob('*')}
        before = snapshot()
        with mock.patch.object(workspace, 'capacity', return_value=self.ample):
            self.assertFalse(workspace.inspect(self.config_path)['writes'])
        self.assertEqual(snapshot(), before)

    def test_git_queries_only_project_reports_when_requested(self):
        spec = importlib.util.spec_from_file_location('managed_workspace_aide_lite', REPO/'.aide/scripts/aide_lite.py')
        lite = importlib.util.module_from_spec(spec); sys.modules[spec.name] = lite; spec.loader.exec_module(lite)
        args = argparse.Namespace(repo_root=REPO, write_reports=False)
        with mock.patch.object(lite, 'write_git_workflow_detection') as detection_writer, \
             mock.patch.object(lite, 'write_aide_dev_main_plan') as aide_writer, \
             mock.patch.object(lite, 'write_git_helper_plan') as helper_writer, \
             mock.patch.object(lite, 'collect_git_workflow_detection', return_value={}), \
             mock.patch.object(lite, 'make_git_helper_plan', return_value={}), \
             mock.patch('builtins.print'):
            self.assertEqual(lite.command_git_detect(args), 0)
            self.assertEqual(lite.command_git_plan(args), 0)
            detection_writer.assert_not_called(); aide_writer.assert_not_called(); helper_writer.assert_not_called()
            args.write_reports = True
            helper_writer.return_value = (lite.WriteResult(Path('fixture.json'), 'unchanged'), lite.WriteResult(Path('fixture.md'), 'unchanged'))
            aide_writer.return_value = ({}, *helper_writer.return_value)
            lite.command_git_plan(args)
            helper_writer.assert_called_once(); aide_writer.assert_called_once()

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_junction_root_and_cleanup_escape_refused(self):
        link = self.root/'junction'; outside = self.root/'outside'; outside.mkdir()
        (outside/'valuable').write_text('retain')
        child = subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.addCleanup(lambda: os.rmdir(link) if link.exists() else None)
        with self.assertRaises(workspace.WorkspaceRefused): workspace.root_path(link)
        with self.assertRaises(workspace.WorkspaceRefused):
            workspace.tree_usage(self.root, maximum=2**20, max_files=100)
        self.assertEqual((outside/'valuable').read_text(), 'retain')

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_success_retires_scratch_and_preserves_output(self):
        job = self.real_job('import os,tempfile\nfrom pathlib import Path\nassert tempfile.gettempdir()==os.environ["AIDE_JOB_TMP"]\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("required result")\nprint("small result")\n')
        result = workspace.run(self.config_path, job)
        self.assertEqual(result['result']['exit_code'], 0, result)
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])
        self.assertFalse((self.roots['control']/'active.json').exists())
        self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'required result')
        self.assertIn('creation_filetime', result['process'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_log_growth_is_bounded_and_reported(self):
        job = self.real_job('import sys\nfor i in range(1000):\n sys.stdout.write("x"*8192);sys.stdout.flush()\n')
        result = workspace.run(self.config_path, job)
        self.assertEqual(result['result']['reason'], 'output_limit_or_io_error')
        self.assertLessEqual(sum(p.stat().st_size for p in (Path(result['retained'])/'logs').iterdir()), 4096)
        self.assertTrue(result['reservation_released'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_cancellation_preserves_output_and_releases_reservation(self):
        job = self.real_job('import os,time\nfrom pathlib import Path\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("partial result")\ntime.sleep(30)\n')
        def cancelled():
            return any((p/'output/unique.txt').exists() for p in self.roots['scratch'].iterdir())
        result = workspace.run(self.config_path, job, cancelled=cancelled)
        self.assertEqual(result['result']['reason'], 'cancelled')
        self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'partial result')
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_monitor_failure_stops_owned_job_and_reports_failure(self):
        job = self.real_job('import time\ntime.sleep(30)\n')
        calls = 0
        def probe(_):
            nonlocal calls
            calls += 1
            if calls == 2: raise OSError('synthetic resource monitor failure')
            return self.ample
        result = workspace.run(self.config_path, job, probe=probe)
        self.assertEqual(result['result']['reason'], 'OSError')
        self.assertIn('monitor failure', result['result']['message'])
        self.assertTrue(result['reconciliation']['quiescent']); self.assertTrue(result['scratch_absent'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_interrupted_retirement_recovers_without_losing_collected_output(self):
        job = self.real_job('import os\nfrom pathlib import Path\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("retirement result")\n')
        def interrupted(root):
            (Path(root)/'owner.json').unlink()
            raise InterruptedError('synthetic interruption during retirement')
        with mock.patch.object(workspace.shutil, 'rmtree', side_effect=interrupted):
            with self.assertRaises(InterruptedError): workspace.run(self.config_path, job)
        result = workspace.recover(self.config_path)
        self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'retirement result')
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_controller_crash_recovery_retains_unique_output(self):
        job = self.real_job('import os,time\nfrom pathlib import Path\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("crash result")\ntime.sleep(30)\n')
        manifest = self.root/'job.json'; workspace.write_json(manifest, job)
        code = 'import sys;sys.path.insert(0,sys.argv[1]);from core.execution.managed_workspace import run,read_json;run(sys.argv[2],read_json(sys.argv[3]))'
        child = subprocess.Popen([sys.executable, '-B', '-c', code, str(REPO), str(self.config_path), str(manifest)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=workspace.sanitized_environment())
        try:
            deadline = time.monotonic()+8
            while not any((p/'output/unique.txt').exists() for p in self.roots['scratch'].iterdir()):
                if child.poll() is not None: self.fail(child.stderr.read().decode())
                if time.monotonic()>deadline: self.fail('owned child did not create result')
                time.sleep(.02)
            child.terminate(); child.wait(timeout=5)
            result = workspace.recover(self.config_path)
            self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'crash result')
            self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])
        finally:
            if child.poll() is None: child.terminate(); child.wait(timeout=5)
            child.stderr.close()


if __name__ == '__main__': unittest.main()
