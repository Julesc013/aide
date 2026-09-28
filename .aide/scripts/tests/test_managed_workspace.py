from __future__ import annotations
import hashlib
import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
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
    def lite_module(self):
        name = 'managed_workspace_aide_lite'
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, REPO/'.aide/scripts/aide_lite.py')
            lite = importlib.util.module_from_spec(spec); sys.modules[name] = lite; spec.loader.exec_module(lite)
        return sys.modules[name]

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

    def codex_job(self):
        self.real_job('pass\n')
        prompt = self.source / 'task-packet.txt'
        schema = self.source / 'result-schema.json'
        prompt.write_text('Return one bounded result for subject fixture.\n', encoding='utf-8')
        schema.write_text('{"type":"object","properties":{"status":{"type":"string"}}}\n', encoding='utf-8')
        subprocess.run(['git', '-C', str(self.source), 'add', '--', prompt.name, schema.name],
                       capture_output=True, check=True, timeout=10)
        subprocess.run(['git', '-C', str(self.source), '-c', 'user.name=AIDE Fixture',
                        '-c', 'user.email=fixture@example.invalid', 'commit', '-m',
                        'test(fixture): bind one Codex task packet'], capture_output=True,
                       check=True, timeout=10)
        executable = self.root / 'codex.exe'
        executable.write_bytes(b'MZ synthetic executable for captured host only')
        def git(*args):
            return subprocess.run(['git', '-C', str(self.source), *args], capture_output=True,
                                  text=True, check=True, timeout=10).stdout.strip()
        self.job.update(adapter='codex_exec', argv=[str(executable)],
            executable_sha256=workspace.file_digest(executable),
            source_commit=git('rev-parse', 'HEAD'), source_tree=git('rev-parse', 'HEAD^{tree}'),
            inputs={name: workspace.file_digest(self.source / name)
                    for name in ('task-packet.txt', 'result-schema.json')},
            prompt_file=prompt.name, schema_file=schema.name,
            model='gpt-6-sol', effort='medium')
        return self.job

    def test_codex_adapter_uses_existing_owner_with_bound_ephemeral_readonly_turn(self):
        job = self.codex_job()
        host = mock.Mock()
        host.run.return_value = {'reason': 'exited', 'exit_code': 0, 'quiescent': True}
        result = workspace.run(self.config_path, job, host=host, probe=lambda _: self.ample)
        argv = host.run.call_args.args[0]
        options = host.run.call_args.kwargs
        self.assertEqual(argv[:4], [job['argv'][0], 'exec', '--ephemeral', '--ignore-user-config'])
        self.assertIn('--json', argv)
        self.assertIn('read-only', argv)
        self.assertIn('gpt-6-sol', argv)
        self.assertIn('model_reasoning_effort="medium"', argv)
        self.assertIn('forced_login_method="chatgpt"', argv)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', argv)
        self.assertEqual(options['input_bytes'], (self.source / job['prompt_file']).read_bytes())
        self.assertEqual(options['cwd'], Path(result['scratch']) / 'tmp')
        self.assertEqual(result['result']['exit_code'], 0)
        self.assertTrue(result['scratch_absent'])
        self.assertTrue(result['reservation_released'])

    def test_codex_adapter_refuses_unbound_or_unbounded_requests_before_allocation(self):
        job = self.codex_job()
        for edit in ({'argv': [*job['argv'], '--full-auto']}, {'effort': 'unspecified'},
                     {'prompt_file': '../outside'}, {'canonical_outputs': {'.aide/release': {}}}):
            with self.subTest(edit=edit), self.assertRaises(workspace.WorkspaceRefused):
                workspace.validate_job({**job, **edit}, [self.source])
        (self.source / job['prompt_file']).write_text('changed after binding\n', encoding='utf-8')
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'source input changed'):
            workspace.run(self.config_path, job, probe=lambda _: self.ample)
        self.assertEqual(list(self.roots['scratch'].iterdir()), [])

    def test_paused_dispatch_refuses_before_allocation_and_is_durable(self):
        job = self.codex_job()
        paused = workspace.set_dispatch(self.config_path, 'paused')
        self.assertEqual((paused['mode'], paused['epoch']), ('paused', 1))
        self.assertFalse(workspace.set_dispatch(self.config_path, 'paused')['writes'])
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'dispatch is paused'):
            workspace.run(self.config_path, job, probe=lambda _: self.ample)
        self.assertEqual(list(self.roots['scratch'].iterdir()), [])
        self.assertEqual(workspace.inspect(self.config_path)['dispatch']['mode'], 'paused')
        resumed = workspace.set_dispatch(self.config_path, 'running')
        self.assertEqual((resumed['mode'], resumed['epoch']), ('running', 2))

    def test_pause_resume_race_refuses_stale_suspended_codex_child(self):
        job = self.codex_job()
        host = mock.Mock()
        def before_resume(*args, **kwargs):
            workspace.set_dispatch(self.config_path, 'paused')
            workspace.set_dispatch(self.config_path, 'running')
            kwargs['checkpoint']('created_suspended')
            self.fail('stale child resumed')
        host.run.side_effect = before_resume
        host.reconcile.return_value = {'quiescent': True}
        result = workspace.run(self.config_path, job, host=host, probe=lambda _: self.ample)
        self.assertEqual(result['result']['reason'], 'WorkspaceRefused')
        self.assertIn('dispatch epoch changed', result['result']['message'])
        self.assertTrue(result['scratch_absent'])
        self.assertTrue(result['reservation_released'])

    def test_pause_cannot_interleave_suspended_check_and_resume(self):
        job = self.codex_job()
        host = mock.Mock()
        def checked_resume(*args, **kwargs):
            kwargs['checkpoint']('created_suspended')
            child = subprocess.run([sys.executable, '-B', str(REPO/'.aide/scripts/aide_lite.py'),
                                    '--repo-root', str(REPO), 'job', 'pause-dispatch',
                                    '--config', str(self.config_path)], capture_output=True,
                                   text=True, timeout=10, env=workspace.sanitized_environment())
            self.assertEqual(child.returncode, 1, child.stdout + child.stderr)
            self.assertIn('dispatch control is busy', child.stdout)
            self.assertEqual(workspace.dispatch_state(self.roots['control'])['mode'], 'running')
            kwargs['checkpoint']('resumed')
            return {'reason': 'exited', 'exit_code': 0, 'quiescent': True}
        host.run.side_effect = checked_resume
        result = workspace.run(self.config_path, job, host=host, probe=lambda _: self.ample)
        self.assertEqual(result['result']['exit_code'], 0)
        self.assertEqual(workspace.set_dispatch(self.config_path, 'paused')['mode'], 'paused')

    def test_ambiguous_dispatch_state_fails_closed_before_allocation(self):
        job = self.codex_job()
        (self.roots['control'] / 'dispatch.json').write_text(
            '{"schema":"aide.job-dispatch.v1","mode":"paused",'
            '"mode":"running","epoch":1}\n', encoding='utf-8')
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'duplicate JSON object key'):
            workspace.run(self.config_path, job, probe=lambda _: self.ample)
        self.assertEqual(list(self.roots['scratch'].iterdir()), [])

    def test_checkpoint_retries_transient_windows_reader_contention(self):
        path = self.roots['control'] / 'checkpoint.json'
        workspace.write_json(path, {'phase': 'old'})
        replace = os.replace
        calls = []
        def contested(source, target):
            calls.append(1)
            if len(calls) == 1:
                raise PermissionError(32, 'transient sharing violation')
            return replace(source, target)
        with mock.patch.object(workspace.os, 'replace', side_effect=contested), \
             mock.patch.object(workspace.time, 'sleep') as sleep:
            workspace.write_json(path, {'phase': 'new'})
        self.assertEqual(len(calls), 2)
        sleep.assert_called_once_with(0.05)
        self.assertEqual(workspace.read_json(path), {'phase': 'new'})
        self.assertFalse(path.with_name(path.name + '.next').exists())

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

    def setup_selection(self, *, roots=None, working=None):
        selection = {'schema': self.config['schema'],
            'roots': {key: str(value) for key, value in (roots or self.roots).items()},
            'working_roots': [str(value) for value in (working or [self.source])],
            'limits': dict(self.config['limits'])}
        selection['limits']['canonical_bytes'] = 1024 * 1024
        path = self.root / 'setup-selection.json'
        workspace.write_json(path, selection)
        return path

    def test_selected_root_setup_is_idempotent_and_cli_uses_it(self):
        roots = {key: self.root / 'owned-pool' / key for key in self.roots}
        selection = self.setup_selection(roots=roots)
        destination = self.source / '.aide.local' / 'execution.json'
        first = workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(first['result'], 'CONFIGURED')
        self.assertTrue(first['writes'])
        self.assertTrue(all(path.is_dir() for path in roots.values()))
        config = workspace.read_json(destination)
        self.assertEqual(config['volume_ids'], {key: workspace.volume_identity(value) for key, value in roots.items()})
        before = (destination.read_bytes(), destination.stat().st_mtime_ns)
        second = workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(second['result'], 'ALREADY_CONFIGURED')
        self.assertFalse(second['writes'])
        self.assertEqual((destination.read_bytes(), destination.stat().st_mtime_ns), before)
        with mock.patch.object(Path, 'cwd', return_value=self.source):
            relative = workspace.configure(Path('.aide.local/execution.json'), selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(relative['result'], 'ALREADY_CONFIGURED')
        command = [sys.executable, '-B', str(REPO/'.aide/scripts/aide_lite.py'), 'job', 'setup',
            '--config', str(destination), '--selection', str(selection), '--approved-parent', str(self.root)]
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True,
            env=workspace.sanitized_environment(), timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['result'], 'ALREADY_CONFIGURED')

    def test_setup_shares_existing_populated_roots_with_second_checkout(self):
        second_source = self.root / 'second-source'; second_source.mkdir()
        selection = self.setup_selection(working=[self.source, second_source])
        first = self.source / '.aide.local' / 'execution.json'
        second = second_source / '.aide.local' / 'execution.json'
        workspace.configure(first, selection, self.root, probe=lambda _: self.ample)
        (self.roots['retained'] / 'existing-evidence.txt').write_text('preserve', encoding='utf-8')
        result = workspace.configure(second, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(result['result'], 'CONFIGURED')
        self.assertEqual(workspace.read_json(first), workspace.read_json(second))
        self.assertEqual((self.roots['retained'] / 'existing-evidence.txt').read_text(), 'preserve')

    def test_setup_refuses_low_capacity_without_creating_selected_roots(self):
        roots = {key: self.root / 'new-pool' / key for key in self.roots}
        selection = self.setup_selection(roots=roots)
        destination = self.source / '.aide.local' / 'execution.json'
        scarce = {**self.ample, 'disk_free': {workspace.volume_identity(self.root): 1024}}
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'free-space reserve'):
            workspace.configure(destination, selection, self.root, probe=lambda _: scarce)
        self.assertFalse((self.root / 'new-pool').exists())
        self.assertFalse(destination.exists())
        limits = workspace.read_json(selection)['limits']
        reserved = limits['scratch_bytes'] + limits['retained_bytes'] + 2 * limits['log_bytes'] + 1024 * 1024
        near_limit = {**self.ample, 'disk_free': {workspace.volume_identity(self.root):
            limits['disk_reserve_bytes'] + reserved + 512 * 1024}}
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'local config would consume'):
            workspace.configure(destination, selection, self.root, probe=lambda _: near_limit)
        self.assertFalse((self.root / 'new-pool').exists())
        self.assertFalse(destination.exists())

    def test_setup_retires_only_new_empty_roots_if_capacity_changes(self):
        roots = {key: self.root / 'new-pool' / key for key in self.roots}
        selection = self.setup_selection(roots=roots)
        destination = self.source / '.aide.local' / 'execution.json'
        scarce = {**self.ample, 'disk_free': {workspace.volume_identity(self.root): 1024}}
        observations = iter((self.ample, scarce))
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'free-space reserve'):
            workspace.configure(destination, selection, self.root, probe=lambda _: next(observations))
        self.assertFalse((self.root / 'new-pool').exists())
        self.assertFalse(destination.parent.exists())

    def test_setup_refuses_escape_unknown_contents_and_changed_config(self):
        destination = self.source / '.aide.local' / 'execution.json'
        roots = dict(self.roots)
        roots['scratch'] = self.root.parent / 'outside-approved-parent'
        selection = self.setup_selection(roots=roots)
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'escapes approved'):
            workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertFalse(destination.exists())
        with self.assertRaises((OSError, workspace.WorkspaceRefused)):
            workspace.configure(destination, selection, self.root / 'missing-parent', probe=lambda _: self.ample)
        self.assertFalse((self.root / 'missing-parent').exists())
        selection = self.setup_selection()
        unknown = self.roots['retained'] / 'unknown.txt'; unknown.write_text('unique', encoding='utf-8')
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'nonempty storage'):
            workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(unknown.read_text(), 'unique')
        unknown.unlink()
        workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        old = destination.read_bytes()
        changed = workspace.read_json(selection); changed['limits']['scratch_bytes'] += 1
        workspace.write_json(selection, changed)
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'existing local config differs'):
            workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(destination.read_bytes(), old)

    def test_setup_refuses_reparse_root_without_writing_target(self):
        target = self.root / 'junction-target'; target.mkdir()
        link = self.root / 'junction'
        command = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)],
            capture_output=True, text=True, timeout=10)
        self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
        self.addCleanup(lambda: link.rmdir() if link.exists() else None)
        roots = {key: link / key for key in self.roots}
        selection = self.setup_selection(roots=roots)
        destination = self.source / '.aide.local' / 'execution.json'
        with self.assertRaises(workspace.WorkspaceRefused):
            workspace.configure(destination, selection, self.root, probe=lambda _: self.ample)
        self.assertEqual(list(target.iterdir()), [])
        self.assertFalse(destination.exists())

    def test_inspection_is_nonmutating(self):
        def snapshot():
            return {str(p.relative_to(self.root)): (p.stat().st_size, p.stat().st_mtime_ns)
                    for p in self.root.rglob('*')}
        before = snapshot()
        with mock.patch.object(workspace, 'capacity', return_value=self.ample):
            self.assertFalse(workspace.inspect(self.config_path)['writes'])
        self.assertEqual(snapshot(), before)

    def declare_canonical(self, relative='.aide/release', amount=2048):
        path = self.source/relative; path.mkdir(parents=True, exist_ok=True)
        self.config['limits']['canonical_bytes'] = amount
        workspace.write_json(self.config_path, self.config)
        self.job['canonical_outputs'] = {relative: {'volume_id': workspace.volume_identity(path), 'bytes': amount}}
        return path

    def test_canonical_outputs_have_finite_reservations_and_no_fallback(self):
        path = self.declare_canonical()
        for failure in ('unconfigured', 'over_budget', 'wrong_volume', 'unknown', 'missing'):
            config = json.loads(json.dumps(self.config)); job = json.loads(json.dumps(self.job))
            if failure == 'unconfigured': del config['limits']['canonical_bytes']
            elif failure == 'over_budget': config['limits']['canonical_bytes'] = 1
            elif failure == 'wrong_volume': job['canonical_outputs']['.aide/release']['volume_id'] = 'wrong'
            elif failure == 'unknown': job['canonical_outputs'] = {'outside': {'bytes': 1}}
            elif failure == 'missing':
                job['canonical_outputs'] = {'.aide/evals/runs': job['canonical_outputs']['.aide/release']}
            with self.subTest(failure=failure), self.assertRaises((OSError, workspace.WorkspaceRefused)):
                workspace.canonical_roots(config, job, self.source)
        self.assertFalse((self.source/'.aide/evals/runs').exists())
        (path/'retained.txt').write_text('keep source output')
        roots = {**self.roots, **workspace.canonical_roots(self.config, self.job, self.source)}
        reservations = workspace.admission(self.config, self.roots, self.ample)
        full = workspace.admission(self.config, roots, self.ample, self.job['canonical_outputs'])
        volume = workspace.volume_identity(path)
        self.assertEqual(full[volume]-reservations[volume], 2048)
        observed = {**self.ample, 'disk_free': {volume: reservations[volume]+self.config['limits']['disk_reserve_bytes']+1024}}
        with self.assertRaises(workspace.WorkspaceRefused):
            workspace.admission(self.config, roots, observed, self.job['canonical_outputs'])

    def test_canonical_volume_is_in_capacity_sampling_and_inspection(self):
        path = self.declare_canonical()
        def volume(value): return 'canonical-volume' if Path(value) == path else 'scratch-volume'
        self.job['canonical_outputs']['.aide/release']['volume_id'] = 'canonical-volume'
        with mock.patch.object(workspace, 'volume_identity', side_effect=volume):
            roots = {**self.roots, **workspace.canonical_roots(self.config, self.job, self.source)}
            observed = workspace.capacity(roots)
            self.assertEqual(set(observed['disk_free']), {'scratch-volume', 'canonical-volume'})
            observed['disk_free']['canonical-volume'] = 1
            with self.assertRaises(workspace.WorkspaceRefused):
                workspace.admission(self.config, roots, observed, self.job['canonical_outputs'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_canonical_junction_refuses_without_touching_target(self):
        target = self.root/'unowned'; target.mkdir(); sentinel = target/'keep.txt'; sentinel.write_text('keep')
        path = self.source/'.aide/release'; path.parent.mkdir(parents=True)
        child = subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(path), str(target)], capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.addCleanup(lambda: os.rmdir(path) if os.path.lexists(path) else None)
        self.job['canonical_outputs'] = {'.aide/release': {'volume_id': workspace.volume_identity(target), 'bytes': 2048}}
        self.config['limits']['canonical_bytes'] = 2048
        with self.assertRaises(workspace.WorkspaceRefused):
            workspace.canonical_roots(self.config, self.job, self.source)
        self.assertEqual(sentinel.read_text(), 'keep')

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_quick_canonical_overrun_fails_and_preserves_source_output(self):
        path = self.declare_canonical(amount=1024)
        job = self.real_job('from pathlib import Path\nPath(".aide/release/result.bin").write_bytes(b"x"*1025)\n')
        result = workspace.run(self.config_path, job)
        self.assertEqual(result['result']['reason'], 'canonical_output_limit_or_identity')
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])
        self.assertEqual((path/'result.bin').stat().st_size, 1025)

    def test_source_generators_require_bound_canonical_output_manifests(self):
        lite = self.lite_module()
        record = {'job': {'canonical_outputs': {lite.EXPORT_PACK_PATH: {}, '.aide/release': {}}}}
        with mock.patch.object(workspace, 'current_context', return_value=record), mock.patch('builtins.print'):
            self.assertTrue(lite.source_maintainer_job_guard(REPO, packaging=True))
            self.assertFalse(lite.source_maintainer_job_guard(REPO, canonical_paths=('.aide/evals/runs',)))
            del record['job']['canonical_outputs']['.aide/release']
            self.assertFalse(lite.source_maintainer_job_guard(REPO, packaging=True))

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_crash_before_final_canonical_check_cannot_recover_as_success(self):
        path = self.declare_canonical(amount=1024)
        host = mock.Mock()
        def complete(*args, **kwargs):
            (path/'overrun.bin').write_bytes(b'x'*1025)
            return {'reason': 'exited', 'exit_code': 0}
        host.run.side_effect = complete
        with mock.patch.object(workspace, 'validate_job', return_value=self.source), \
             mock.patch.object(workspace, 'qualify_canonical_outputs', side_effect=InterruptedError('crash after quiescent checkpoint')):
            with self.assertRaises(InterruptedError):
                workspace.run(self.config_path, self.job, host=host)
        active = self.roots['control']/'active.json'
        self.assertEqual(workspace.read_json(active)['result']['exit_code'], 0)
        result = workspace.recover(self.config_path)
        self.assertEqual(result['result']['reason'], 'canonical_output_limit_or_identity')
        self.assertEqual(result['prior_result']['exit_code'], 0)
        self.assertEqual((path/'overrun.bin').stat().st_size, 1025)
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_crash_recovery_rechecks_canonical_volume_identity(self):
        path = self.declare_canonical()
        host = mock.Mock(); host.run.return_value = {'reason': 'exited', 'exit_code': 0}
        with mock.patch.object(workspace, 'validate_job', return_value=self.source), \
             mock.patch.object(workspace, 'qualify_canonical_outputs', side_effect=InterruptedError('crash')):
            with self.assertRaises(InterruptedError): workspace.run(self.config_path, self.job, host=host)
        actual_volume = workspace.volume_identity
        with mock.patch.object(workspace, 'volume_identity', side_effect=lambda p: 'changed' if Path(p) == path else actual_volume(p)):
            result = workspace.recover(self.config_path)
        self.assertEqual(result['result']['reason'], 'canonical_output_limit_or_identity')
        self.assertIn('volume identity changed', result['canonical_after_error'])
        self.assertTrue(path.exists()); self.assertTrue(result['scratch_absent'])

    def test_git_queries_only_project_reports_when_requested(self):
        lite = self.lite_module()
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

    def test_task_status_inspection_preserves_files_and_explicit_reports_work(self):
        lite = self.lite_module(); args = argparse.Namespace(repo_root=self.source, write_reports=False)
        index = self.source/'.aide/queue/index.yaml'; index.parent.mkdir(parents=True)
        index.write_text('schema_version: aide.queue-index.v0\ntasks: []\n')
        def snapshot():
            return {p.relative_to(self.source).as_posix(): (p.stat().st_mtime_ns, p.read_bytes())
                    for p in self.source.rglob('*') if p.is_file()}
        before = snapshot()
        with mock.patch('builtins.print'):
            self.assertEqual(lite.command_task_status(args), 1)
        self.assertEqual(snapshot(), before)
        self.assertFalse((self.source/lite.TASK_OS_TASK_STATUS_REPORT_PATH).exists())
        args.write_reports = True
        with mock.patch('builtins.print'):
            self.assertEqual(lite.command_task_status(args), 1)
        self.assertTrue((self.source/lite.TASK_OS_TASK_STATUS_REPORT_PATH).is_file())
        self.assertTrue((self.source/lite.TASK_OS_COMMAND_STATUS_REPORT_PATH).is_file())

    def test_source_heavy_entrypoints_refuse_outside_owned_job(self):
        lite = self.lite_module(); args = argparse.Namespace(repo_root=REPO)
        with mock.patch.object(workspace, 'current_context', side_effect=workspace.WorkspaceRefused('outside job')), \
             mock.patch.object(lite, 'run_selftest') as selftest, \
             mock.patch.object(lite, 'build_export_pack') as export, \
             mock.patch.object(lite, 'build_release_bundle_outputs') as release, \
             mock.patch.object(lite, 'run_golden_tasks') as golden, mock.patch('builtins.print'):
            for handler in (lite.command_test, lite.command_selftest, lite.command_export_pack,
                            lite.command_release_bundle, lite.command_eval_run):
                self.assertEqual(handler(args), 1)
            for builder in (selftest, export, release, golden): builder.assert_not_called()
        with mock.patch.object(workspace, 'current_context', return_value={}), \
             mock.patch.object(lite, 'build_export_pack') as export, \
             mock.patch.object(lite, 'build_release_bundle_outputs') as release, mock.patch('builtins.print'):
            self.assertEqual(lite.command_export_pack(args), 1)
            self.assertEqual(lite.command_release_bundle(args), 1)
            export.assert_not_called(); release.assert_not_called()

    def test_portable_compatibility_and_source_only_test_export(self):
        lite = self.lite_module()
        with mock.patch.object(lite, 'run_selftest', return_value=(True, ['PASS tiny portable fixture'])) as body, mock.patch('builtins.print'):
            self.assertEqual(lite.command_test(argparse.Namespace(repo_root=self.source)), 0)
            body.assert_called_once()
        self.assertTrue(lite.is_source_only_export_test('.aide/scripts/tests/test_managed_workspace.py'))

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_environment_spoof_does_not_grant_job_context(self):
        with mock.patch.dict(os.environ, {'AIDE_JOB_ID': 'a'*32, 'AIDE_JOB_CONTROL': str(self.roots['control'])}):
            with self.assertRaises(workspace.WorkspaceRefused): workspace.current_context(self.source)

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_owned_child_proves_named_job_context(self):
        source = ('import os,sys\nfrom pathlib import Path\nsys.path.insert(0,'+repr(str(REPO))+')\n'
                  'from core.execution.managed_workspace import current_context\n'
                  'r=current_context(Path.cwd());assert r["job_id"]==os.environ["AIDE_JOB_ID"]\nprint("admitted context")\n')
        job = self.real_job(source)
        stub = self.source/'.aide/scripts/aide_lite.py'; stub.parent.mkdir(parents=True)
        stub.write_text('# bound synthetic CLI input\n')
        job['inputs']['.aide/scripts/aide_lite.py'] = workspace.file_digest(stub)
        task = self.source/'.aide/queue'/job['workunit']/'task.yaml'; task.parent.mkdir(parents=True)
        task.write_text('planning_state: admitted\n')
        result = workspace.run(self.config_path, job)
        self.assertEqual(result['result']['exit_code'], 0, result)
        self.assertIn('admitted context', (Path(result['retained'])/'logs/stdout').read_text())

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
        with self.assertRaises(workspace.WorkspaceRefused):
            workspace.tree_usage(self.root, maximum=2**20, max_files=100,
                                 allow_transient_hardlinks=True)
        self.assertEqual((outside/'valuable').read_text(), 'retain')

    def test_live_usage_counts_transient_hardlink_but_collection_refuses_it(self):
        scratch = self.roots['scratch']
        first = scratch/'first.txt'; second = scratch/'second.txt'
        first.write_bytes(b'tiny')
        os.link(first, second)
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'unexpected job member'):
            workspace.tree_usage(scratch, maximum=1024, max_files=10)
        self.assertEqual(workspace.tree_usage(scratch, maximum=1024, max_files=10,
                                              allow_transient_hardlinks=True), 8)
        second.unlink()
        self.assertEqual(workspace.tree_usage(scratch, maximum=1024, max_files=10), 4)

    def test_live_usage_refuses_hardlink_to_outside_scratch(self):
        scratch = self.roots['scratch']
        outside = self.root/'outside.txt'; outside.write_bytes(b'private')
        os.link(outside, scratch/'linked.txt')
        with self.assertRaisesRegex(workspace.WorkspaceRefused, 'hardlink outside owned scratch'):
            workspace.tree_usage(scratch, maximum=1024, max_files=10,
                                 allow_transient_hardlinks=True)
        self.assertEqual(outside.read_bytes(), b'private')

    def test_usage_scan_tolerates_disappearing_owned_scratch_entries(self):
        scratch = self.roots['scratch']
        transient_file = scratch/'transient.txt'
        transient_file.write_text('temporary', encoding='utf-8')
        transient_dir = scratch/'transient-dir'
        transient_dir.mkdir()
        original_lstat = Path.lstat
        seen_dir = 0

        def vanishing_lstat(path, *args, **kwargs):
            nonlocal seen_dir
            if path == transient_file:
                raise FileNotFoundError(str(path))
            if path == transient_dir:
                seen_dir += 1
                if seen_dir > 1:
                    raise FileNotFoundError(str(path))
            return original_lstat(path, *args, **kwargs)

        with mock.patch.object(Path, 'lstat', vanishing_lstat):
            with self.assertRaises(FileNotFoundError):
                workspace.tree_usage(scratch, maximum=1024, max_files=10)
            self.assertEqual(workspace.tree_usage(scratch, maximum=1024, max_files=10,
                                                  allow_transient_absence=True), 0)

    @unittest.skipUnless(os.name == 'nt', 'Windows execution profile')
    def test_success_retires_scratch_and_preserves_output(self):
        job = self.real_job('import os,tempfile\nfrom pathlib import Path\nassert tempfile.gettempdir()==os.environ["AIDE_JOB_TMP"]\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("required result")\nprint("small result")\n')
        result = workspace.run(self.config_path, job)
        self.assertEqual(result['result']['exit_code'], 0, result)
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])
        self.assertFalse((self.roots['control']/'active.json').exists())
        self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'required result')
        self.assertIn('creation_filetime', result['process'])

    @unittest.skipUnless(os.name == 'nt', 'Windows readonly scratch retirement')
    def test_readonly_disposable_git_object_retires_after_output_custody(self):
        script = ('import os,stat\nfrom pathlib import Path\n'
                  'leaf=Path(os.environ["AIDE_JOB_TMP"])/"brownfield/.git/objects/00/object"\n'
                  'leaf.parent.mkdir(parents=True)\nleaf.write_bytes(b"disposable git fixture")\n'
                  'leaf.chmod(stat.S_IREAD)\n'
                  'Path(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("retained result")\n')
        job = self.real_job(script)
        try:
            result = workspace.run(self.config_path, job)
        finally:
            # Keep the tiny fixture removable if a future regression fails.
            for leaf in self.roots['scratch'].glob('*/tmp/brownfield/.git/objects/00/object'):
                if leaf.exists(): leaf.chmod(stat.S_IWRITE)
        self.assertEqual(result['result']['exit_code'], 0, result)
        self.assertTrue(result['scratch_absent']); self.assertTrue(result['reservation_released'])
        self.assertGreaterEqual(result['scratch_readonly_cleared'], 1)
        self.assertEqual((Path(result['retained'])/'output/unique.txt').read_text(), 'retained result')
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
    def test_broken_scratch_junction_preserves_recovery_state(self):
        job = self.real_job('import os\nfrom pathlib import Path\nPath(os.environ["AIDE_JOB_OUTPUT"],"unique.txt").write_text("retained result")\n')
        remove = workspace.shutil.rmtree
        with mock.patch.object(workspace.shutil, 'rmtree', side_effect=InterruptedError('stop before retirement')):
            with self.assertRaises(InterruptedError): workspace.run(self.config_path, job)
        active = self.roots['control']/'active.json'; record = workspace.read_json(active)
        scratch = Path(record['scratch']); remove(scratch)
        target = self.root/'missing-junction-target'
        child = subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(scratch), str(target)], capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.addCleanup(lambda: os.rmdir(scratch) if os.path.lexists(scratch) else None)
        self.assertFalse(scratch.exists()); self.assertTrue(os.path.lexists(scratch))
        with self.assertRaises(workspace.WorkspaceRefused): workspace.recover(self.config_path)
        self.assertTrue(active.exists()); self.assertTrue(os.path.lexists(scratch))
        self.assertEqual((Path(record['retained'])/'output/unique.txt').read_text(), 'retained result')

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
