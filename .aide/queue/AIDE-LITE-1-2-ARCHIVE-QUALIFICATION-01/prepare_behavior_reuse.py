"""Freeze exact dependency applicability; original observations keep their subjects."""
import ast
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    old = json.loads((E / 'build-result.json').read_bytes())
    new = json.loads((E / 'revised-build-result.json').read_bytes())
    delta = json.loads((E / 'revised-archive-member-delta.json').read_bytes())
    coverage = json.loads((E / 'current-cli-coverage.json').read_bytes())
    consumers = json.loads((E / 'consumer-results.json').read_bytes())
    remaining = json.loads((E / 'remaining-results.json').read_bytes())
    with zipfile.ZipFile(ROOT / '.aide/release/stable/aide-lite-v1.2.0.zip') as archive:
        cli_name = next(n for n in archive.namelist() if n.endswith('/files/.aide/scripts/aide_lite.py'))
        cli = archive.read(cli_name)
    assert sha(cli) == old['delivered_cli_sha256'] == new['delivered_cli_sha256']
    source = cli.decode('utf-8')
    syntax = ast.parse(source)
    node = next(n for n in syntax.body if isinstance(n, ast.FunctionDef) and n.name == 'import_scope_skip_reason')
    skip = ast.get_source_segment(source, node)
    assert 'IMPORT_SAFE_EXCLUDED_PREFIXES' in skip and 'startswith' in skip
    excluded = next(n.value for n in syntax.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'IMPORT_SAFE_EXCLUDED_PREFIXES' for t in n.targets))
    assert ast.literal_eval(excluded) == ('core/',)
    changed = delta['inventories']['zip']['changed']
    unchanged = {n: v for n, v in delta['inventories']['zip']['new'].items() if n not in changed}
    assert len(unchanged) == 875
    notes = {
        0: 'Safe importer/update/conflict/health dispatch and synthetic prompt changes; core/ is excluded from installed targets.',
        1: 'Owned repair/removal/rollback primitives, managed prompt, receipts and authored guidance; no managed-job observation dispatch.',
        2: 'Context/pack/verify and existing policy/templates with a Python socket fixture; no execution supervisor.',
        3: 'Safe partial-import/resolution recovery and local feedback; unchanged importer and synthetic prompts.',
        4: 'Import explanation/feedback, validation and task inspection; unchanged CLI and project fixtures.',
        5: 'Forced exits at importer/repair/removal boundaries; no live managed-job observation.',
        7: 'Extracts unchanged delivered CLI and task-state fixtures; no managed supervisor.'}
    cases = []
    for row in consumers['cases']:
        index = row['case']
        cases.append({'case': index, 'original_job_id': row['job_id'],
                      'disposition': 'fresh_revised_execution_required' if index == 6 else 'behavior_applicability_proposed',
                      'dependency_reason': notes.get(index, 'Direct delivered managed-job dispatch reaches revised tree_usage; rerun all original case-6 assertions.'),
                      'original_result': row['result']})
    forms = []
    for row in coverage['forms']:
        witness = row['evidence']
        fresh = 'consumer-case-06-retained.json' in witness['bundle']
        forms.append({'form': row['form'], 'original_witness': witness,
                      'disposition': 'fresh_revised_execution_required' if fresh else 'behavior_applicability_proposed',
                      'observation_subject': 'original candidate only',
                      'reason': 'Affected delivered runner' if fresh else 'Unchanged public dispatch, safe-import payload, dynamic adjacent helpers, policy/templates and fixture transformations; all archive executable bytes unchanged except excluded managed owner.'})
    assert sum(r['disposition'] == 'fresh_revised_execution_required' for r in forms) == 10
    fresh = json.loads((E / 'remaining-predecessor-summary.json').read_bytes())
    assert len(fresh['completed_scenarios']) == 1 and fresh['completed_scenarios'][0]['native_acceptance']
    result = {'status': 'DEPENDENCY_PROOF_PENDING_INDEPENDENT_REVIEW',
              'original_assets': old['assets'], 'revised_assets': new['assets'],
              'original_consumers_source': consumers['subject'], 'original_remaining_source': remaining['subject'],
              'member_delta_sha256': sha((E / 'revised-archive-member-delta.json').read_bytes()),
              'changed_members': changed, 'unchanged_member_dependency_envelope': unchanged,
              'unchanged_delivered_cli_sha256': sha(cli),
              'safe_import_exclusion': {'prefix': 'core/', 'function': 'import_scope_skip_reason',
                  'function_sha256': sha(skip.encode()), 'source': skip,
                  'effect': 'The changed supervisor implementation is excluded from ordinary safe imports; working-directory choice is not an isolation claim.'},
              'cases': cases, 'forms': forms,
              'additional_forms': 'All 41 original assertions and 18 forms remain original observations; unchanged task/git/review/quality/effort dispatch, adjacent effort helper, policies and fixture inputs. No managed launch.',
              'completed_fresh_predecessor': fresh['completed_scenarios'][0],
              'identity_boundary': 'Pack manifest/checksum/source identity changed. Old plans, receipts, feedback hashes, ownership inventories and timings remain old observations. Behavioral applicability does not replace fresh revised archive integrity, actual installed identity and owned-target reconciliation.',
              'required_fresh_evidence': ['revised archive integrity/provenance and installed pack identity/ownership',
                  'all original case-6 assertions against revised delivered runner',
                  'unfinished real published-predecessor brownfield conflict/recovery/customization',
                  '49 actual ordinary forms and lifecycle on each declared additional environment',
                  'complete final release replay and acceptance'],
              'excluded_claims': ['new package execution from old jobs', 'new timing/resource/environment observations',
                  'outer-client containment', 'native network isolation', 'whole-model efficiency', 'universal reliability']}
    destination = E / 'revised-behavior-reuse-proposal.json'
    data = (json.dumps(result, indent=2) + '\n').encode()
    if destination.exists():
        assert destination.read_bytes() == data
    else:
        destination.write_bytes(data)
    print(json.dumps({'status': result['status'], 'forms': len(forms), 'unchanged_dependency_members': len(unchanged), 'fresh_case_6_forms': 10}))


if __name__ == '__main__':
    main()
