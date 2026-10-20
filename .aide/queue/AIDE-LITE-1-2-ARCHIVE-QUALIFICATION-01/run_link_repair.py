"""Prove the legal link race, validate the shared owner, then refresh one owned export."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

ROOT = Path.cwd()
TASK = Path(__file__).parent
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

METHODS = (
    'test_stable_canonical_junction_refuses_without_touching_target',
    'test_canonical_junction_refuses_without_touching_target',
    'test_quick_canonical_overrun_fails_and_preserves_source_output',
    'test_live_usage_counts_transient_hardlink_but_collection_refuses_it',
    'test_live_usage_refuses_hardlink_to_outside_scratch',
    'test_live_link_retirement_rechecks_once_and_accepts_settled_member',
    'test_live_link_recheck_preserves_larger_first_observation',
    'test_live_link_recheck_refuses_persistent_outside_alias_with_bounded_diagnostic',
    'test_link_set_without_both_live_flags_refuses_without_recheck',
    'test_live_link_recheck_does_not_hide_growth_or_file_count',
    'test_live_link_recheck_does_not_hide_unavailable_metadata',
    'test_live_link_recheck_does_not_hide_redirection',
    'test_live_zero_link_member_confirmed_absent_is_not_retained',
    'test_live_zero_link_surviving_member_is_counted_from_fresh_metadata',
    'test_live_zero_link_replacement_cannot_hide_growth',
    'test_live_persistent_zero_link_member_is_refused_after_bounded_observation',
    'test_quiescent_zero_link_member_is_refused_without_retry',
    'test_live_zero_link_reobservation_rejects_reparse_metadata',
    'test_live_zero_link_reobservation_does_not_hide_observation_errors',
    'test_live_zero_link_replacement_cannot_alias_outside_scratch',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True) + '\n').encode())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def observations(result, stream):
    return {'tests_run': result.testsRun, 'successful': result.wasSuccessful(),
            'failures': [(case.id(), text) for case, text in result.failures],
            'errors': [(case.id(), text) for case, text in result.errors],
            'skips': [(case.id(), reason) for case, reason in result.skipped],
            'stream_sha256': sha(stream)}


def main():
    assert not sys.argv[1:]
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    os.environ['AIDE_RESOURCE_TEST_PARENT'] = str(TMP)
    baseline = json.loads((TASK / 'evidence/link-baseline.json').read_bytes())
    ownership = load('link_export_ownership', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')
    prior = json.loads((TASK / 'evidence/link-prior-export.json').read_bytes())
    save(OUT / 'export-before.json', ownership.require_same(prior))
    assert all(sha(ROOT / name) == digest for name, digest in baseline['stable_assets'].items())
    module = load('link_workspace_regressions', ROOT / '.aide/scripts/tests/test_managed_workspace.py')
    record = {'state': 'started', 'export_refreshed': False, 'methods': list(METHODS),
              'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'worker_model_requests': 0, 'whole_model_usage': 'unknown', 'support_claimed': False}
    try:
        raw = subprocess.check_output(['git', 'show', baseline['source_commit'] + ':core/execution/managed_workspace.py'])
        assert hashlib.sha256(raw).hexdigest() == baseline['workspace_sha256']
        old_node = next(node for node in ast.parse(raw).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'tree_usage')
        namespace = dict(workspace.__dict__)
        exec(compile(ast.Module(body=[old_node], type_ignores=[]), '<original-live-scan>', 'exec'), namespace)
        original_test = module.ManagedWorkspaceTests('test_live_link_retirement_rechecks_once_and_accepts_settled_member')
        path = OUT / 'original-legal-transition.txt'
        with path.open('x', encoding='utf-8', newline='\n') as stream, \
             mock.patch.object(workspace, 'tree_usage', namespace['tree_usage']):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.TestSuite([original_test]))
        before = observations(result, path)
        save(OUT / 'original-legal-transition.json', before)
        assert result.testsRun == 1 and not result.failures and not result.skipped and len(result.errors) == 1
        assert 'WorkspaceRefused: hardlink outside owned scratch or transient link set' in result.errors[0][1]
        record['original_legal_transition_rejected'] = True
        path = OUT / 'link-regressions.txt'
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
                unittest.TestSuite(module.ManagedWorkspaceTests(name) for name in METHODS))
        after = observations(result, path)
        save(OUT / 'link-regressions.json', after)
        record.update(state='regressions_completed', tests=after)
        save(OUT / 'link-result.json', record)
        assert result.wasSuccessful() and result.testsRun == len(METHODS) and not result.skipped
        assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
        ownership.require_same(prior)
        metadata = OUT / 'prior-metadata'
        metadata.mkdir()
        for name in sorted(ownership.EXCLUDED):
            (metadata / name).write_bytes((ROOT / ownership.PACK_REL / name).read_bytes())
        lite = load('link_export_owner', ROOT / '.aide/scripts/aide_lite.py')
        pack, report = lite.build_export_pack(ROOT)
        record.update(state='export_refreshed', export_refreshed=True, export=report)
        save(OUT / 'link-result.json', record)
        valid, problems = lite.validate_pack_checksums(pack)
        assert valid and not problems and not lite.validate_export_pack_boundary(pack)
        assert (pack / 'files/core/execution/managed_workspace.py').read_bytes() == (ROOT / 'core/execution/managed_workspace.py').read_bytes()
        members = {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob('*')) if p.is_file()}
        assert set(members) == set(prior['files'])
        changed = {name for name, digest in members.items() if digest != prior['files'][name]['sha256']}
        assert changed == {'files/core/execution/managed_workspace.py', 'checksums.json', 'manifest.yaml'}, changed
        assert all(sha(ROOT / name) == digest for name, digest in baseline['stable_assets'].items())
        save(OUT / 'export-after.json', {'source_commit': record['source_commit'], 'members': members,
                                       'changed_members': sorted(changed)})
        record.update(state='passed', stable_assets_unchanged=len(baseline['stable_assets']),
                      export_files=len(members), changed_members=sorted(changed))
    except BaseException as error:
        record.update(state='stopped', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        save(OUT / 'link-result.json', record)
    print('PASS original race demonstration, twenty shared-owner checks and one owned export refresh')


if __name__ == '__main__':
    main()
