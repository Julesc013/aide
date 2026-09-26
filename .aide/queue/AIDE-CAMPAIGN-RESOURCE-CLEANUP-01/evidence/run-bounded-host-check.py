"""Small actual AIDE regression through the admitted runner, no bulk pool.

The temporary fixture lives only under the existing cleanup receipt directory.
This is not adoption of that location as the machine build/test pool.
"""
import json
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
with tempfile.TemporaryDirectory(prefix='tiny-aide-validation-', dir=parent) as temporary:
    fixture = Path(temporary)
    roots = {key: fixture/key for key in ('scratch', 'retained', 'control')}
    for root in roots.values(): root.mkdir()
    config = {'schema': 'aide.managed-workspace.local.v1',
        'roots': {key: str(value) for key, value in roots.items()},
        'volume_ids': {key: workspace.volume_identity(value) for key, value in roots.items()},
        'working_roots': [str(REPO)],
        'limits': {'disk_reserve_bytes': 10*1024**3, 'physical_reserve_bytes': 4*1024**3,
            'commit_reserve_bytes': 4*1024**3, 'scratch_bytes': 8*1024**2,
            'retained_bytes': 1024**2, 'memory_bytes': 512*1024**2,
            'log_bytes': 65536, 'runtime_seconds': 120, 'processes': 16, 'max_files': 1000}}
    config_path = fixture/'config.json'; workspace.write_json(config_path, config)
    def git(*args):
        return subprocess.run(['git', '-C', str(REPO), *args], capture_output=True,
                              text=True, check=True, timeout=15).stdout.strip()
    files = ['core/execution/managed_workspace.py', 'core/runtime/continuous_worker/windows_job.py',
             '.aide/scripts/tests/test_continuous_worker_host.py']
    job = {'schema': 'aide.maintainer-job.v1', 'owner': 'AIDE campaign controller',
        'workunit': 'AIDE-CAMPAIGN-RESOURCE-CLEANUP-01', 'adapter': 'python', 'cwd': str(REPO),
        'source_commit': git('rev-parse', 'HEAD'), 'source_tree': git('rev-parse', 'HEAD^{tree}'),
        'inputs': {path: workspace.file_digest(REPO/path) for path in files},
        'executable_sha256': workspace.file_digest(sys.executable),
        'argv': [sys.executable, '-m', 'unittest', 'discover', '-s', '.aide/scripts/tests',
                 '-p', 'test_continuous_worker_host.py', '-v']}
    result = workspace.run(config_path, job)
    retained = Path(result['retained'])
    log = (retained/'logs/stdout').read_bytes() + (retained/'logs/stderr').read_bytes()
    # One durable result and one bounded log; fixture copies are retired below.
    (evidence/'bounded-host-check.log').write_bytes(log)
    result['retention_disposition'] = 'bounded log and receipt collected here; tiny fixture retired'
    result['fixture_parent'] = str(parent)
    workspace.write_json(evidence/'bounded-host-check.json', result)
    print(json.dumps({'exit_code': result['result']['exit_code'], 'reason': result['result']['reason'],
        'peaks': result['peaks'], 'scratch_absent': result['scratch_absent'],
        'reservation_released': result['reservation_released'], 'log_bytes': len(log)}))
    if result['result']['exit_code'] != 0 or result['result']['reason'] != 'exited':
        print(log.decode(errors='replace')); raise SystemExit(1)
