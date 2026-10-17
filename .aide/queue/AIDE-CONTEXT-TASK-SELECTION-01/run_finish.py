"""Continue the completed export with delivered checks and one fixed preview."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-CONTEXT-TASK-SELECTION-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
spec = importlib.util.spec_from_file_location('context_finish_owner',
    ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
qualification = json.loads((TASK / 'evidence/attempt-02-qualification.json').read_text(encoding='utf-8'))
pack = ROOT / owner.PACK_REL
def observed_hashes():
    return {name: record['sha256'] for name, record in owner.ownership.observe()['files'].items()}

after = observed_hashes()
assert after == qualification['after_sha256s'], 'completed export changed'
before = json.loads((TASK / 'evidence/prior-pack-inventory.json').read_text(encoding='utf-8'))['files']
assert len(after) == 862 and set(after) == set(before)
changed = {name for name in after if before[name]['sha256'] != after[name]}
payload = {'files/.aide/scripts/aide_lite.py', 'files/.aide/scripts/tests/test_task_binding.py'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload
for name in payload:
    assert owner.sha(pack / name) == owner.sha(ROOT / name.removeprefix('files/'))
for label, command in [
    ('delivered', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')]),
    ('preview', [sys.executable, '-B', str(TASK / 'run_preview.py'), 'generate']),
]:
    with (OUTPUT / (label + '-process.log')).open('wb') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, timeout=120)
    assert result.returncode == 0, label + ' failed; output preserved'
    assert observed_hashes() == after, 'completed export mutated'
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'delivered_tests': 60, 'ownership_tests_reused': 6,
     'export_job': qualification['job_id'], 'changed_paths': sorted(changed),
     'after_sha256s': after, 'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 60, 'preview': 'PASS',
                  'export_rebuilt': False, 'changed_paths': sorted(changed)}))
