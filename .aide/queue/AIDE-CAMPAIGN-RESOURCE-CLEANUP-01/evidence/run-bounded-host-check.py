"""Small actual AIDE regression through the admitted runner, no bulk pool.

The temporary fixture lives only under the existing cleanup receipt directory.
This is not adoption of that location as the machine build/test pool.
"""
import json
import argparse
import faulthandler
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from core.execution import managed_workspace as workspace

parent = workspace.root_path(os.environ['AIDE_RESOURCE_TEST_PARENT'])
evidence = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument('--suite', choices=('host', 'task-status', 'feedback-boundary', 'importer-recovery', 'importer-controls-diagnostic', 'importer-recovery-remaining'), default='host')
parser.add_argument('--diagnostic-child', action='store_true')
options = parser.parse_args()
if options.diagnostic_child:
    # Same real test/oracle; bounded stack samples make timeout diagnosis
    # deterministic rather than repeated controller polling or model guesses.
    import unittest
    import time
    sys.path.insert(0, str(REPO/'.aide/scripts/tests'))
    faulthandler.dump_traceback_later(30, repeat=True)
    started = time.monotonic()
    selected = unittest.defaultTestLoader.loadTestsFromName('test_export_import.ExportImportTests.test_partial_recovery_blocks_controls_change_during_publication_and_retirement')
    result = unittest.TextTestRunner(verbosity=2).run(selected)
    faulthandler.cancel_dump_traceback_later()
    print(json.dumps({'test_elapsed_seconds': time.monotonic()-started}), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)
suite = options.suite
importer = suite.startswith('importer')
diagnostic = suite == 'importer-controls-diagnostic'
remaining = suite == 'importer-recovery-remaining'
task_status = suite == 'task-status'
feedback = suite == 'feedback-boundary'
oracle = 'test_x_os_01_task_os_commands.py' if task_status else 'test_export_import.py' if importer or feedback else 'test_continuous_worker_host.py'
result_name = 'bounded-feedback-boundary-check' if feedback else 'bounded-task-status-check' if task_status else 'bounded-importer-recovery-remaining' if remaining else 'bounded-importer-controls-diagnostic' if diagnostic else 'bounded-importer-recovery-check' if importer else 'bounded-host-check'
with tempfile.TemporaryDirectory(prefix='tiny-aide-validation-', dir=parent) as temporary:
    fixture = Path(temporary)
    roots = {key: fixture/key for key in ('scratch', 'retained', 'control')}
    for root in roots.values(): root.mkdir()
    config = {'schema': 'aide.managed-workspace.local.v1',
        'roots': {key: str(value) for key, value in roots.items()},
        'volume_ids': {key: workspace.volume_identity(value) for key, value in roots.items()},
        'working_roots': [str(REPO)],
        'limits': {'disk_reserve_bytes': 10*1024**3, 'physical_reserve_bytes': 4*1024**3,
            'commit_reserve_bytes': 4*1024**3, 'scratch_bytes': (128 if importer else 8)*1024**2,
            'retained_bytes': 1024**2, 'memory_bytes': 512*1024**2,
            'log_bytes': 65536, 'runtime_seconds': 600 if remaining else 300 if importer else 120,
            'processes': 16, 'max_files': 12000 if importer else 1000}}
    config_path = fixture/'config.json'; workspace.write_json(config_path, config)
    def git(*args):
        return subprocess.run(['git', '-C', str(REPO), *args], capture_output=True,
                              text=True, check=True, timeout=15).stdout.strip()
    files = ['core/execution/managed_workspace.py', 'core/runtime/continuous_worker/windows_job.py',
             '.aide/scripts/tests/' + oracle]
    if task_status or feedback:
        files.append('.aide/scripts/aide_lite.py')
    if importer:
        # Bind the source and the actual fixture inputs, not just the test name.
        import importlib.util
        spec = importlib.util.spec_from_file_location('bounded_lite_inputs', REPO/'.aide/scripts/aide_lite.py')
        lite = importlib.util.module_from_spec(spec); sys.modules[spec.name] = lite; spec.loader.exec_module(lite)
        files.extend([*lite.PORTABLE_SOURCE_FILES, *lite.Q21_REQUIRED_FILES])
        for directory in (*lite.PORTABLE_SOURCE_DIRS, '.aide/import'):
            path = REPO/directory
            if path.exists():
                files.extend(p.relative_to(REPO).as_posix() for p in path.rglob('*') if p.is_file())
        files = sorted({p for p in files if (REPO/p).is_file()})
    if diagnostic:
        files.append(Path(__file__).relative_to(REPO).as_posix())
    argv = [sys.executable, '-m', 'unittest', 'discover', '-s', '.aide/scripts/tests', '-p', oracle, '-v']
    if feedback:
        argv.extend(['-k', 'feedback_boundary'])
    elif diagnostic:
        argv = [sys.executable, str(Path(__file__)), '--diagnostic-child']
    elif remaining:
        argv.extend(['-k', 'partial_recovery_refuses', '-k', 'partial_recovery_requires', '-k', 'redigested_partial_intent'])
    elif importer:
        # Dependency-ready product regressions only; the full importer gate stays open.
        argv.extend(['-k', 'partial_recovery', '-k', 'redigested_partial_intent', '-k', 'missing_controls_guard'])
    job = {'schema': 'aide.maintainer-job.v1', 'owner': 'AIDE campaign controller',
        'workunit': 'AIDE-DELIVERED-PACK-CUSTOMIZATION-01' if feedback else 'AIDE-CAMPAIGN-RESOURCE-CLEANUP-01', 'adapter': 'python', 'cwd': str(REPO),
        'source_commit': git('rev-parse', 'HEAD'), 'source_tree': git('rev-parse', 'HEAD^{tree}'),
        'inputs': {path: workspace.file_digest(REPO/path) for path in files},
        'executable_sha256': workspace.file_digest(sys.executable),
        'argv': argv}
    result = workspace.run(config_path, job)
    retained = Path(result['retained'])
    log = (retained/'logs/stdout').read_bytes() + (retained/'logs/stderr').read_bytes()
    # Keep one raw original outside Git; a receipt/digest points to it. Raw
    # unittest progress may contain meaningful trailing spaces on interruption.
    log_path = parent/(result_name+'-'+result['job_id']+'.log')
    with log_path.open('xb') as stream: stream.write(log)
    result['log_capture'] = {'path': str(log_path), 'bytes': len(log),
                             'sha256': workspace.file_digest(log_path)}
    result['retention_disposition'] = 'task receipt references one raw log at log_capture.path; tiny fixture retired'
    result['fixture_parent'] = str(parent)
    workspace.write_json(evidence/(result_name+'.json'), result)
    print(json.dumps({'exit_code': result['result']['exit_code'], 'reason': result['result']['reason'],
        'peaks': result['peaks'], 'scratch_absent': result['scratch_absent'],
        'reservation_released': result['reservation_released'], 'log_bytes': len(log)}))
    if result['result']['exit_code'] != 0 or result['result']['reason'] != 'exited':
        print(log.decode(errors='replace')); raise SystemExit(1)
