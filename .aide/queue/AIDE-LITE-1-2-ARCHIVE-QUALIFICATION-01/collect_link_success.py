"""Preserve the successful shared-owner repair and exact refreshed export subject."""
import base64
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

spec = importlib.util.spec_from_file_location('link_success_collection_helpers', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
raw = (E / 'link-corrected-execution.log').read_bytes()
group = json.loads(raw)
record = group['job_result']
assert group['state'] == 'local_terminal' and 'error_type' not in group
assert record['phase'] == 'retired' and record['result']['exit_code'] == 0
assert record['result']['quiescent'] and not record['result']['io_errors']
assert record['scratch_absent'] and record['reservation_released'] and not Path(record['scratch']).exists()
effect = json.loads((E / 'link-corrected-effect.json').read_bytes())
template = json.loads((E / 'link-corrected-job-template.json').read_bytes())
submitted = dict(template, source_commit=group['commit']['candidate_commit'], source_tree=group['commit']['expected_tree'])
assert record['job'] == group['job'] == submitted and workspace.digest(submitted) == record['manifest_digest']
assert record['config_digest'] == effect['qualification_config_digest']
retained = Path(record['retained'])
for name, expected in record['collected_manifest'].items():
    assert workspace.content_digest(retained / name) == expected
files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
         for p in sorted(retained.rglob('*')) if p.is_file()}
h.save(E / 'link-corrected-retained.json', h.bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files)))
h.save(E / 'link-corrected-source-execution.json', h.bundle(raw))
result = json.loads((retained / 'output/link-result.json').read_bytes())
tests = json.loads((retained / 'output/link-regressions.json').read_bytes())
original = json.loads((retained / 'output/original-legal-transition.json').read_bytes())
assert tests['successful'] and tests['tests_run'] == 20 and not tests['skips'] and not tests['errors'] and not tests['failures']
assert result['state'] == 'passed' and result['export_refreshed'] and result['original_legal_transition_rejected']
assert original['tests_run'] == 1 and not original['successful'] and len(original['errors']) == 1
assert 'WorkspaceRefused: hardlink outside owned scratch or transient link set' in original['errors'][0][1]
after = json.loads((retained / 'output/export-after.json').read_bytes())
assert after['source_commit'] == submitted['source_commit'] and len(after['members']) == 879
assert after['changed_members'] == ['checksums.json', 'files/core/execution/managed_workspace.py', 'manifest.yaml']
assert all(workspace.file_digest(ROOT / '.aide/export/aide-lite-pack-v0' / name) == digest
           for name, digest in after['members'].items())
baseline = json.loads((E / 'link-baseline.json').read_bytes())
assert all(workspace.file_digest(ROOT / name) == digest for name, digest in baseline['stable_assets'].items())
h.save(E / 'link-qualified-export.json', after)
h.save(E / 'link-qualified-result.json', {'state': 'PASS_SHARED_OWNER_AND_OWNED_EXPORT',
    'job_id': record['job_id'], 'subject': {'commit': submitted['source_commit'], 'tree': submitted['source_tree']},
    'result': result, 'tests': tests, 'original_probe': original,
    'manifest_digest': record['manifest_digest'], 'collected_manifest': record['collected_manifest'],
    'retained': record['retained'], 'retained_files': len(files), 'peaks': record['peaks'],
    'scratch_absent': True, 'reservation_released': True, 'local_jobs_consumed': 14,
    'total_local_ceiling': 16, 'export_refreshes_consumed': 2, 'total_export_ceiling': 2,
    'candidate_state': 'Original candidate bytes preserved; they precede the qualified export and require the separately reviewed revised build.'})
print(json.dumps({'state': 'PASS_SHARED_OWNER_AND_OWNED_EXPORT', 'source': submitted['source_commit'],
                  'job_id': record['job_id'], 'retained_files': len(files), 'tests': 20, 'export_files': 879}))
