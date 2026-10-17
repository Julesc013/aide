"""Actual published-predecessor upgrade and recovery in owned disposable targets."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
POLICY = '.aide/policies/git-workflow.yaml'
OPTIONAL = '.aide.local.example/README.md'


def main():
    assert sys.argv[1:] in (['upgrade'], ['recovery'])
    mode = sys.argv[1]
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    spec = importlib.util.spec_from_file_location('predecessor_common', TASK / 'run_consumer.py')
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    helper = common.load('predecessor_helper', common.CAN / 'lifecycle_helper.py')
    capture = common.load('predecessor_capture', ROOT / '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py')
    subject = json.loads((TASK / 'evidence/build-result-repaired.json').read_text(encoding='utf-8'))
    historical = json.loads((TASK / 'evidence/release-before-rebuild.json').read_text(encoding='utf-8'))
    predecessor = {p: v for p, v in historical.items() if p.startswith('.aide/release/stable/aide-lite-v1.0.0.')}
    assert len(predecessor) == 4
    assets = {**predecessor, **subject['assets']}
    assert all(common.sha(ROOT / p) == v['sha256'] for p, v in assets.items())
    fixture = TMP / ('case-predecessor-' + mode)
    fixture.mkdir()
    stable = ROOT / '.aide/release/stable'
    helper.extract_zip(stable / 'aide-lite-v1.0.0.zip', fixture / 'old')
    helper.extract_zip(stable / 'aide-lite-v1.1.0.zip', fixture / 'new')
    old = fixture / 'old' / helper.PACK_NAME
    new = fixture / 'new' / helper.PACK_NAME
    delivered = helper.load_delivered(new)
    assert common.sha(new / 'files/.aide/scripts/aide_lite.py') == subject['delivered_cli_sha256']
    old_policy, new_policy = (old / 'files' / POLICY).read_bytes(), (new / 'files' / POLICY).read_bytes()
    assert old_policy != new_policy
    checks = []

    class Recorder(helper.Recorder):
        def run(self, label, script, root, *parts, exits=(0,), offline_text=False):
            argv = [sys.executable, '-I', '-B', str(script), '--repo-root', str(root), *parts]
            record = {'argv': argv, 'exit_code': None}
            stdout, stderr = OUT / (label + '.stdout'), OUT / (label + '.stderr')
            common.write(OUT / (label + '.json'), record)
            try:
                result = capture.capture_streams(argv, cwd=root, env=dict(os.environ),
                    stdout_path=stdout, stderr_path=stderr, timeout=180)
                record['exit_code'] = result.returncode
            except BaseException as exc:
                record['exception'] = repr(exc)
                raise
            finally:
                for key, path in [('stdout', stdout), ('stderr', stderr)]:
                    record[key + '_sha256'] = common.sha(path) if path.exists() else None
                common.write(OUT / (label + '.json'), record)
            text, errors = stdout.read_text(encoding='utf-8'), stderr.read_text(encoding='utf-8')
            assert result.returncode in exits, (label, result.returncode)
            if offline_text:
                assert 'network_calls: none' in text
            self.commands.append({'label': label, 'exit_code': result.returncode,
                                  'record_sha256': common.sha(OUT / (label + '.json'))})
            return subprocess.CompletedProcess(argv, result.returncode, text, errors)

    rec = Recorder(OUT)

    def command(label, target, *extra, exits=(0,)):
        return rec.pack(label, new, 'import-pack', '--pack', str(new), '--from-pack', str(old),
                        '--target', str(target), '--mode', 'safe', *extra, exits=exits, offline_text=True)

    def preserve(target, files, authored):
        assert all((target / p).read_bytes() == content for p, content in files.items())
        assert (target / 'AGENTS.md').read_bytes().startswith(authored)

    if mode == 'upgrade':
        fresh = fixture / 'fresh'
        fresh.mkdir()
        helper.install(rec, 'fresh-old-install', old, fresh)
        helper.update(rec, 'fresh-actual-update', new, old, fresh)
        assert delivered.load_portable_import_receipt(fresh)['pack'] == delivered.import_pack_identity(new)
        assert (fresh / POLICY).read_bytes() == new_policy
        assert common.sha(fresh / '.aide/scripts/aide_lite.py') == subject['delivered_cli_sha256']
        checks.append('fresh_published_predecessor_update')

        brown = fixture / 'brown'
        brown.mkdir()
        authored = b'# Project guidance\r\nPreserve this authored prefix.\r\n'
        (brown / 'AGENTS.md').write_bytes(authored)
        project = {'README.md': b'# Existing project\r\n', 'tools/project-check.py': b'print("project check")\r\n'}
        for relative, content in project.items():
            path = brown / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        helper.install(rec, 'brown-old-install', old, brown)
        preserve(brown, project, authored)
        optional_before = (old / 'files' / OPTIONAL).read_bytes()
        assert (new / 'files' / OPTIONAL).read_bytes() == optional_before
        assert (brown / OPTIONAL).read_bytes() == optional_before
        old_brown_receipt = delivered.load_portable_import_receipt(brown)
        assert OPTIONAL in old_brown_receipt['managed']
        assert old_brown_receipt['managed'][OPTIONAL]['installed_digest'] == helper.sha(optional_before)
        controls = {'schema_version': 'aide.project-customizations.v2', 'entries': {},
                    'disabled_features': [{'feature_id': 'local_state_examples',
                                           'rationale': 'Project owns its local examples.'}]}
        control_bytes = (json.dumps(controls, indent=2) + '\n').encode()
        (brown / delivered.PROJECT_CUSTOMIZATIONS_PATH).write_bytes(control_bytes)
        project[delivered.PROJECT_CUSTOMIZATIONS_PATH] = control_bytes
        (brown / OPTIONAL).write_bytes(b'Project-maintained optional example.\r\n')
        project[OPTIONAL] = (brown / OPTIONAL).read_bytes()
        local = old_policy + b'\n# Project decision: retain this local explanation.\n'
        (brown / POLICY).write_bytes(local)
        before = helper.tree_hashes(brown)
        preview = command('brown-conflict-preview', brown, '--dry-run', '--explain', exits=(2,))
        assert helper.field(preview.stdout, 'status') == 'PLANNED_CONFLICT'
        assert POLICY in preview.stdout and helper.tree_hashes(brown) == before
        refused = command('brown-conflict-apply', brown, '--expect-plan',
                          helper.field(preview.stdout, 'plan_digest'), exits=(2,))
        assert helper.field(refused.stdout, 'status') == 'CONFLICT'
        assert helper.tree_hashes(brown) == before
        checks.append('real_changed_upstream_conflict_refuses_without_writes')

        selected = fixture / 'resolved-git-policy.yaml'
        merged = new_policy + b'\n# Project decision: retain this local explanation.\n'
        selected.write_bytes(merged)
        resolution = ('--resolve', POLICY, str(selected))
        preview = command('brown-resolved-preview', brown, *resolution, '--dry-run', '--explain')
        assert helper.field(preview.stdout, 'status') == 'PLANNED'
        assert helper.tree_hashes(brown) == before
        partial = delivered.apply_import_pack(new, brown, predecessor_pack=old,
            resolutions={POLICY: selected}, expected_plan_digest=helper.field(preview.stdout, 'plan_digest'),
            fail_after_writes=1)
        common.write(OUT / 'resolved-update-interruption.json', partial)
        assert partial['status'] == 'INTERRUPTED' and partial['recovery']['classification'] == 'partial'
        partial_state = helper.tree_hashes(brown)
        for label, args in [('ordinary', ()), ('wrong-plan', ('--recover-partial', '--expect-plan', '0' * 64))]:
            refused = command('resolved-' + label, brown, *resolution, *args, exits=(3,))
            assert helper.field(refused.stdout, 'status') == 'RECOVERY_REQUIRED'
            assert helper.tree_hashes(brown) == partial_state
        selected.write_bytes(merged + b'# Changed after interrupted attempt.\n')
        changed = command('resolved-changed-input', brown, *resolution, '--recover-partial',
                          '--expect-plan', partial['plan_digest'], exits=(3,))
        assert helper.field(changed.stdout, 'status') == 'RECOVERY_REQUIRED'
        assert helper.tree_hashes(brown) == partial_state
        selected.write_bytes(merged)
        applied = command('brown-resolved-recovery', brown, *resolution,
                          '--recover-partial', '--expect-plan', partial['plan_digest'])
        assert helper.field(applied.stdout, 'status') == 'RECOVERED'
        assert not (brown / delivered.PORTABLE_IMPORT_INTENT_PATH).exists()
        preserve(brown, project, authored)
        assert (brown / POLICY).read_bytes() == merged
        receipt = delivered.load_portable_import_receipt(brown)
        entry = receipt['managed'][POLICY]
        assert receipt['pack'] == delivered.import_pack_identity(new)
        assert receipt['disabled_features'] == ['local_state_examples'] and OPTIONAL not in receipt['managed']
        assert entry['local_overlay'] and entry['ownership'] == 'project_overlay_on_aide_managed'
        assert entry['installed_digest'] == helper.sha(merged) and entry['source_digest'] == helper.sha(new_policy)
        common.write(OUT / 'resolved-overlay.json', {'path': POLICY, 'entry': entry,
                     'controls_sha256': helper.sha(control_bytes),
                     'preserved_project_files': {p: helper.sha(v) for p, v in project.items()},
                     'authored_prefix_sha256': helper.sha(authored)})
        checks.append('explicit_combined_resolution_and_project_controls_preserved')
        checks.append('actual_resolved_interruption_wrong_input_refusal_and_exact_recovery')
        customized_state = helper.tree_hashes(brown)
        removal = helper.plan_removal(rec, 'customized-removal-boundary', brown)
        row = next(row for row in removal['operations'] if row['target'] == POLICY)
        assert row['action'] == 'preserve_project_overlay' and row['removal_candidate'] is False
        assert helper.tree_hashes(brown) == customized_state
        preserve(brown, project, authored)
        common.write(OUT / 'customized-recovery-limitation.json', {
            'state': 'resolved_overlay_and_disabled_optional_features',
            'automatic_downgrade': 'unsupported; preserve for manual reconciliation',
            'removal_apply_performed': False, 'protected_policy_operation': row})
        checks.append('customized_overlay_preserved_without_detach_or_receipt_deletion')
    else:
        target = fixture / 'recovery'
        target.mkdir()
        authored = b'# Recovery project guidance\r\n'
        (target / 'AGENTS.md').write_bytes(authored)
        project = {'project-owned.txt': b'Preserve across interruption and rollback.\r\n'}
        (target / 'project-owned.txt').write_bytes(project['project-owned.txt'])
        helper.install(rec, 'recovery-old-install', old, target)
        old_receipt = delivered.load_portable_import_receipt(target)
        original_owned = {p: common.sha(target / p) for p in old_receipt['managed'] if p != 'AGENTS.md'}
        old_block_digest = old_receipt['managed']['AGENTS.md']['installed_digest']
        partial = delivered.apply_import_pack(new, target, predecessor_pack=old, fail_after_writes=1)
        common.write(OUT / 'actual-update-interruption.json', partial)
        assert partial['status'] == 'INTERRUPTED' and partial['recovery']['classification'] == 'partial'
        partial_state = helper.tree_hashes(target)
        for label, args in [('ordinary', ()), ('wrong-plan', ('--recover-partial', '--expect-plan', '0' * 64))]:
            result = command('recovery-' + label, target, *args, exits=(3,))
            assert helper.field(result.stdout, 'status') == 'RECOVERY_REQUIRED'
            assert helper.tree_hashes(target) == partial_state
        recovered = command('recovery-exact', target, '--recover-partial', '--expect-plan', partial['plan_digest'])
        assert helper.field(recovered.stdout, 'status') == 'RECOVERED'
        assert not (target / delivered.PORTABLE_IMPORT_INTENT_PATH).exists()
        preserve(target, project, authored)
        current_receipt = delivered.load_portable_import_receipt(target)
        assert current_receipt['pack'] == delivered.import_pack_identity(new)
        assert (target / POLICY).read_bytes() == new_policy
        checks.append('actual_interrupted_upgrade_refusal_and_exact_cli_recovery')

        before = helper.tree_hashes(target)
        args = ('rollback-pack', '--current-pack', str(new), '--previous-pack', str(old),
                '--target', str(target), '--json')
        for label, tail in [('preview', ('--dry-run',)), ('apply', ('--expect-plan', '0' * 64))]:
            refused = rec.installed('actual-path-change-rollback-' + label, target, *args, *tail, exits=(1,))
            assert 'rollback payload paths differ; ownership-aware path changes require separate recovery' in refused.stderr
            assert helper.tree_hashes(target) == before
        checks.append('actual_cross_version_rollback_refusal_preserves_target')
        new_targets = set(current_receipt['managed'])
        old_targets = set(old_receipt['managed'])
        assert old_targets < new_targets and len(new_targets - old_targets) == 8
        assert '.aide/scripts/aide_work_effort.py' in new_targets - old_targets
        # This target has no recorded overlay or disabled managed feature.
        assert not current_receipt['disabled_features']
        assert all(not row['local_overlay'] for row in current_receipt['managed'].values())
        agents_before = (target / 'AGENTS.md').read_bytes()
        begin = b'<!-- AIDE-PORTABLE:BEGIN section=aide-lite-pack-v0'
        end = b'<!-- AIDE-PORTABLE:END section=aide-lite-pack-v0 -->'
        assert agents_before.count(begin) == agents_before.count(end) == 1
        start = agents_before.index(begin)
        finish = agents_before.index(end, start) + len(end)
        assert helper.sha(agents_before[start:finish]) == current_receipt['managed']['AGENTS.md']['installed_digest']
        authored_outside = agents_before[:start] + agents_before[finish:]
        plan = helper.plan_removal(rec, 'downgrade-detach-preview', target)
        assert plan['status'] == 'PLANNED' and set(plan['candidate_targets']) == new_targets
        wrong = rec.installed('downgrade-detach-wrong-plan', target, 'apply-removal',
                              '--target', str(target), '--expect-plan', '0' * 64, '--json', exits=(3,))
        assert json.loads(wrong.stdout)['status'] == 'STALE_PLAN' and helper.tree_hashes(target) == before
        detached = rec.installed('downgrade-detach-exact', target, 'apply-removal',
                                '--target', str(target), '--expect-plan', plan['plan_digest'], '--json')
        detached_record = json.loads(detached.stdout)
        assert detached_record['status'] == 'DETACHED' and detached_record['receipt_retained'] is False
        helper.assert_detached(target, new_targets, delivered,
                               {p: helper.sha(v) for p, v in project.items()}, authored_agents=authored_outside)
        helper.install(rec, 'downgrade-published-reinstall', old, target)
        restored = delivered.load_portable_import_receipt(target)
        assert restored['pack'] == delivered.import_pack_identity(old)
        assert restored['managed']['AGENTS.md']['installed_digest'] == old_block_digest
        assert all(common.sha(target / p) == digest for p, digest in original_owned.items())
        assert all(not (target / p).exists() for p in new_targets - old_targets)
        preserve(target, project, authored)
        assert (target / 'AGENTS.md').read_bytes().startswith(authored_outside)
        common.write(OUT / 'separate-recovery.json', {
            'route': 'explicit complete detach then published predecessor safe reinstall',
            'automatic_rollback': False, 'old_safe_targets': len(old_targets),
            'new_safe_targets': len(new_targets), 'added_paths_removed': sorted(new_targets - old_targets),
            'project_preserved': {p: helper.sha(v) for p, v in project.items()},
            'authored_outside_sha256': helper.sha(authored_outside),
            'restored_pack': restored['pack']})
        checks.append('supported_unchanged_target_detach_and_published_reinstall_recovery')

    assert all(common.sha(ROOT / p) == v['sha256'] for p, v in assets.items())
    summary = {'status': 'PASS', 'mode': mode, 'checks': checks, 'assets': assets,
               'published_predecessor': '1.0.0', 'candidate': '1.1.0',
               'old_policy_sha256': helper.sha(old_policy), 'new_policy_sha256': helper.sha(new_policy),
               'commands': rec.commands, 'model_calls': 0, 'fixture_retired': False}
    common.write(OUT / 'summary.json', summary)
    worker = common.load('predecessor_retirement', common.ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(fixture)
    summary['fixture_retired'] = True
    common.write(OUT / 'summary.json', summary)
    print('PASS actual published-predecessor ' + mode)


if __name__ == '__main__':
    main()
