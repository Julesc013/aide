"""Prepare one corrected fixture attempt; preserve the failed attempt and every original gate."""
import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
BASE = 'c25f16519c0991676c72c2ac41e77852e77b11ad'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('link_correction_preparation_helpers', TASK / 'prepare_link.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == BASE
    assert not h.git('diff', '--cached', '--name-only')
    failed = json.loads((E / 'link-initial-result.json').read_bytes())
    assert failed['local_jobs_consumed'] == 13 and not failed['export_refreshed']
    assert failed['scratch_absent'] and failed['reservation_released']
    assert failed['corrected_checks_run'] == 0
    source = 'core/execution/managed_workspace.py'
    assert (ROOT / source).read_bytes() == subprocess.check_output(['git', 'show', BASE + ':' + source])
    test_path = '.aide/scripts/tests/test_managed_workspace.py'
    old = ast.parse(subprocess.check_output(['git', 'show', BASE + ':' + test_path]))
    current = ast.parse((ROOT / test_path).read_bytes())
    old_methods = {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(old)
                   if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
    current_methods = {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(current)
                       if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
    assert old_methods == current_methods and len(old_methods) == 82
    old_helpers = h.nodes(subprocess.check_output(['git', 'show', BASE + ':' + test_path]))
    new_helpers = h.nodes((ROOT / test_path).read_bytes())
    assert set(old_helpers) == set(new_helpers) == {'ManagedWorkspaceTests'}
    ownership = h.load('link_corrected_export_ownership', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')
    ownership.require_same(json.loads((E / 'link-prior-export.json').read_bytes()))
    baseline = json.loads((E / 'link-baseline.json').read_bytes())
    assert all(h.sha(ROOT / name) == value for name, value in baseline['stable_assets'].items())
    previous = json.loads((E / 'link-effect.json').read_bytes())
    effect = dict(previous, base=BASE, local_jobs_already_consumed=13, total_local_ceiling=16,
                  controller_sha256=h.sha(TASK / 'commit_and_repair_scan_corrected.py'))
    effect['review_attestation'] = dict(effect['review_attestation'],
        path=(E / 'link-corrected-review.json').relative_to(ROOT).as_posix())
    effect['amendment'] = 'Thirteen consumed attempts remain counted; keep total ceiling16 and two exports total. One corrected regression/export attempt, one revised build, then one separately reviewed affected-consumer/replay group after hosted evidence. Every group retains600seconds; no retry or allowance reset.'
    effect['prior_failure'] = {'job_id': failed['job_id'], 'record': (E / 'link-initial-result.json').relative_to(ROOT).as_posix(),
                               'reason': 'The newly authored scandir fixture lacked the iterator protocol; no corrected-source checks or export ran.'}
    h.save(E / 'link-corrected-effect.json', effect)
    job = json.loads((E / 'link-job-template.json').read_bytes())
    job['inputs'] = {name: h.sha(ROOT / name) for name in job['inputs']}
    h.save(E / 'link-corrected-job-template.json', job)
    _, _, working = h.workspace.load_config(ROOT / effect['qualification_config'])
    h.workspace.validate_job(dict(job, source_commit=BASE, source_tree=h.git('rev-parse', BASE + '^{tree}')), working)
    owner = h.load('link_corrected_commit_validator', ROOT / '.aide/scripts/aide_lite.py')
    message = ('test(execution): correct the live-scan fixture iterator\n\n'
        '- Preserve the original failed probe and its complete retired collection; it reached no corrected checks or export.\n'
        '- Supply both scandir iteration and context protocols; retain all 82 test bodies and the unchanged production repair.\n'
        '- Prepare one exact corrected regression/export attempt, counting all 13 consumed allocations; rebuild and release gates remain separate.\n\n'
        'Validation: PASS - unchanged production bytes, 82 test bodies, owned export and stable assets, syntax and literal job preflight; runtime checks pending\n'
        'Changelog: Fixed: correct deterministic live-scan fixture iteration without changing production behavior\n'
        'Risk: No product pass follows from the original fixture error; further failure remains terminal.\n'
        'Follow-up: Original-source race demonstration and twenty corrected-source checks before one owned export.\n'
        'AIDE-Task: AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01\nAIDE-Format: compact-v1\n')
    failures = [c.message for c in owner.validate_commit_message_text(message) if c.severity == 'FAIL']
    assert not failures, failures
    path = E / 'link-corrected-message.txt'
    assert not path.exists()
    path.write_bytes(message.encode())
    h.save(E / 'link-corrected-prechecks.json', {'status': 'PASS_STRUCTURAL_CORRECTION', 'base': BASE,
        'production_bytes_unchanged': True, 'test_bodies_preserved': 82, 'fixture_change': 'iteration plus context-manager protocol',
        'original_failure_retained_files': failed['retained_files'], 'export_preimages': 879,
        'stable_assets_unchanged': 12, 'job_inputs': len(job['inputs']), 'job_preflight': 'PASS',
        'runtime_checks_run': 0, 'new_allocations': 0})
    source_path, verdict = E / 'link-corrected-source.json', E / 'link-corrected-review.json'
    excluded = {source_path.relative_to(ROOT).as_posix(), verdict.relative_to(ROOT).as_posix()}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: h.sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in files:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
    h.git('diff', '--check')
    h.save(source_path, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': BASE,
        'effect_sha256': h.sha(E / 'link-corrected-effect.json'), 'files': files,
        'qualification_state': 'Corrected fixture prepared; exact runtime and export effects pending.'})
    print(json.dumps({'source_sha256': h.sha(source_path), 'effect_sha256': h.sha(E / 'link-corrected-effect.json'),
                      'controller_sha256': effect['controller_sha256'], 'mapped_files': len(files), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
