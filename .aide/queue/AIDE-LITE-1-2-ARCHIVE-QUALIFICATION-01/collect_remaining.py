"""Preserve both terminal remaining-group attempts without converting interruption to pass."""
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


def main():
    raw = (EVIDENCE / 'remaining-execution.log').read_bytes()
    group = json.loads(raw)
    assert group['state'] == 'stopped' and group['current_case'] == 'predecessor'
    assert [item['case'] for item in group['remaining_results']] == ['additions', 'predecessor']
    subject = group['remaining_subject']
    plan = json.loads((EVIDENCE / 'remaining-effect.json').read_bytes())
    templates = json.loads((EVIDENCE / 'remaining-job-templates.json').read_bytes())
    built = json.loads((EVIDENCE / 'build-result.json').read_bytes())
    for name, value in built['assets'].items():
        assert workspace.file_digest(ROOT / name) == value['sha256']
    rows = []
    for item in group['remaining_results']:
        case, record = item['case'], item['receipt']
        submitted = dict(templates[case], source_commit=subject['commit'], source_tree=subject['tree'])
        assert record['job'] == submitted and record['manifest_digest'] == workspace.digest(submitted)
        assert record['config_digest'] == plan['qualification_config_digest']
        assert record['phase'] == 'retired' and record['scratch_absent'] and record['reservation_released']
        assert not Path(record['scratch']).exists()
        retained = Path(record['retained'])
        for name, expected in record['collected_manifest'].items():
            assert workspace.content_digest(retained / name) == expected
        files = {p.relative_to(retained).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
                 for p in sorted(retained.rglob('*')) if p.is_file()}
        packed = bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files))
        save(EVIDENCE / f'remaining-{case}-retained.json', packed)
        partial_cases = []
        if case == 'additions':
            assert record['result']['exit_code'] == 0 and record['result']['quiescent']
            assert not record['result']['io_errors']
            summary = json.loads((retained / 'output/summary.json').read_bytes())
            assert summary['status'] == 'PASS' and summary['fixture_retired'] and len(summary['forms']) == 18
            assert summary['assets'] == built['assets']
            state = 'PASS_ALL_EIGHTEEN_ADDITIVE_FORMS'
        else:
            assert record['result']['exit_code'] is None
            assert record['result']['reason'] == 'WorkspaceRefused'
            assert record['result']['message'] == 'hardlink outside owned scratch or transient link set'
            assert record['reconciliation']['quiescent']
            assert not (retained / 'output/predecessor-result.json').exists()
            for path in sorted((retained / 'output').glob('*.case.json')):
                partial_cases.append(json.loads(path.read_bytes()))
            assert len(partial_cases) == 1 and partial_cases[0]['shape'] == 'published-upgrade-fresh'
            assert partial_cases[0]['native_acceptance']
            summary = {'status': 'INCOMPLETE', 'terminal_result': record['result'],
                       'completed_scenarios': partial_cases, 'unfinished_scenarios': ['published-upgrade-brownfield'],
                       'interpretation': 'The runner interrupted this attempt; its scenario evidence is preserved without an overall pass or product-defect claim.'}
            state = 'INCOMPLETE_RUNNER_HARDLINK_REFUSAL'
        save(EVIDENCE / f'remaining-{case}-summary.json', summary)
        rows.append({'case': case, 'state': state, 'job_id': record['job_id'],
                     'manifest_digest': record['manifest_digest'], 'collected_manifest': record['collected_manifest'],
                     'retained': record['retained'], 'retained_files': len(files),
                     'retained_transport_bytes': packed['uncompressed_bytes'], 'peaks': record['peaks'],
                     'result': record['result'], 'reconciliation': record.get('reconciliation'),
                     'scratch_absent': True, 'reservation_released': True})
    save(EVIDENCE / 'remaining-source-execution.json', bundle(raw))
    save(EVIDENCE / 'remaining-results.json', {'state': 'ADDITIONS_PASS_PREDECESSOR_INCOMPLETE',
         'subject': subject, 'cases': rows, 'archive_qualification': 'remaining obligations pending',
         'local_jobs_consumed': 12, 'local_ceiling': 13, 'hosted_runs_consumed': 0,
         'worker_model_requests': 0, 'whole_model_usage': 'unknown'})
    print(json.dumps({'state': 'ADDITIONS_PASS_PREDECESSOR_INCOMPLETE', 'groups': len(rows),
                      'retained_files': sum(r['retained_files'] for r in rows), 'subject': subject}))


if __name__ == '__main__':
    main()
