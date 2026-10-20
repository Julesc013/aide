"""Preserve the completed consumer group's exact existing collections."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
EVIDENCE = TASK / 'evidence'


def save(path, value):
    data = (json.dumps(value, indent=2) + '\n').encode()
    if path.exists():
        assert path.read_bytes() == data, 'existing evidence differs: ' + str(path)
    else:
        path.write_bytes(data)


def bundle(raw, *, files=None):
    compressed = gzip.compress(raw, mtime=0)
    assert len(raw) < 8 * 1024 * 1024 and len(compressed) < 2 * 1024 * 1024
    value = {'encoding': 'gzip+base64', 'data': base64.b64encode(compressed).decode('ascii'),
             'gzip_sha256': hashlib.sha256(compressed).hexdigest(),
             'sha256': hashlib.sha256(raw).hexdigest(), 'uncompressed_bytes': len(raw)}
    if files is not None:
        value['files'] = files
    return value


raw = (EVIDENCE / 'consumer-execution.log').read_bytes()
group = json.loads(raw)
assert group['state'] == 'all_eight_consumers_terminal_pass'
assert [item['case'] for item in group['consumer_results']] == list(range(8))
subject = group['consumer_subject']
plan = json.loads((EVIDENCE / 'consumer-effect.json').read_bytes())
template = json.loads((EVIDENCE / 'consumer-job-template.json').read_bytes())
built = json.loads((EVIDENCE / 'build-result.json').read_bytes())
for name, value in built['assets'].items():
    assert workspace.file_digest(ROOT / name) == value['sha256']
rows = []
for item in group['consumer_results']:
    index, record = item['case'], item['receipt']
    submitted = dict(template, argv=[*template['argv'], str(index)],
                     source_commit=subject['commit'], source_tree=subject['tree'])
    assert record['job'] == submitted and record['manifest_digest'] == workspace.digest(submitted)
    assert record['config_digest'] == plan['qualification_config_digest']
    assert record['phase'] == 'retired' and record['scratch_absent'] and record['reservation_released']
    assert not Path(record['scratch']).exists()
    assert record['result']['exit_code'] == 0 and record['result']['quiescent'] and not record['result']['io_errors']
    retained = Path(record['retained'])
    for name, expected in record['collected_manifest'].items():
        assert workspace.content_digest(retained / name) == expected
    files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
             for p in sorted(retained.rglob('*')) if p.is_file()}
    packed = bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files))
    save(EVIDENCE / f'consumer-case-{index:02d}-retained.json', packed)
    result = json.loads((retained / 'output/consumer-result.json').read_bytes())
    assert result['status'] == 'PASS' and result['case'] == index and result['fixture_retired']
    assert result['assets'] == json.loads((EVIDENCE / 'build-result.json').read_bytes())['assets']
    summary = json.loads((retained / f'output/case-{index:02d}/summary.json').read_bytes())
    assert summary['status'] == 'PASS'
    save(EVIDENCE / f'consumer-case-{index:02d}-summary.json', summary)
    rows.append({'case': index, 'job_id': record['job_id'], 'result': result,
                 'phase': record['phase'], 'manifest_digest': record['manifest_digest'],
                 'collected_manifest': record['collected_manifest'], 'retained': record['retained'],
                 'retained_files': len(files), 'retained_raw_bytes': packed['uncompressed_bytes'],
                 'peaks': record['peaks'], 'scratch_absent': True, 'reservation_released': True})
save(EVIDENCE / 'consumer-source-execution.json', bundle(raw))
save(EVIDENCE / 'consumer-results.json', {'state': 'PASS_ORIGINAL_EIGHT_CONSUMERS',
     'subject': subject, 'cases': rows, 'archive_qualification': 'remaining obligations pending',
     'local_jobs_consumed': 10, 'local_ceiling': 13, 'hosted_runs_consumed': 0,
     'worker_model_requests': 0, 'whole_model_usage': 'unknown'})
print(json.dumps({'state': 'PASS_ORIGINAL_EIGHT_CONSUMERS', 'cases': len(rows),
                  'retained_files': sum(r['retained_files'] for r in rows), 'subject': subject}))
