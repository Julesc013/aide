"""Exercise all 18 additive forms from the actual installed successor ZIP."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location('successor_common', TASK / 'run_consumer.py')
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    subject = json.loads((TASK / 'evidence/build-result.json').read_text())
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    for name, value in subject['assets'].items():
        assert common.sha(ROOT / name) == value['sha256']
    helper = common.load('additions_lifecycle_helper', common.CAN / 'lifecycle_helper.py')
    fixture = TMP / 'case-additions'
    fixture.mkdir()
    helper.extract_zip(ROOT / '.aide/release/stable/aide-lite-v1.1.0.zip', fixture / 'archive')
    pack = fixture / 'archive' / helper.PACK_NAME
    target = fixture / 'target'
    target.mkdir()
    capture = common.load('additions_capture', ROOT / '.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/delivered_additions.py')

    def invoke(label, argv, cwd):
        record = {'argv': argv, 'cwd': str(cwd), 'exit_code': None}
        path = OUT / (label + '.json')
        stdout, stderr = OUT / (label + '.stdout'), OUT / (label + '.stderr')
        common.write(path, record)
        try:
            result = capture.capture_streams(argv, cwd=cwd, env=dict(os.environ),
                stdout_path=stdout, stderr_path=stderr, timeout=180)
            record['exit_code'] = result.returncode
        except BaseException as exc:
            record['exception'] = repr(exc)
            raise
        finally:
            for key, stream in (('stdout', stdout), ('stderr', stderr)):
                record[key] = stream.read_text(encoding='utf-8', errors='replace') if stream.exists() else ''
                record[key + '_sha256'] = common.sha(stream) if stream.exists() else None
            common.write(path, record)
        return subprocess.CompletedProcess(argv, result.returncode, record['stdout'], record['stderr'])

    class Recorder(helper.Recorder):
        def run(self, label, script, root, *parts, exits=(0,), offline_text=False):
            argv = [sys.executable, '-I', '-B', str(script), '--repo-root', str(root), *parts]
            result = invoke(label, argv, root)
            self.commands.append({'label': label, 'path': str(OUT / (label + '.json')),
                                  'sha256': common.sha(OUT / (label + '.json')), 'exit_code': result.returncode})
            assert result.returncode in exits, (label, result.returncode)
            if offline_text:
                assert 'network_calls: none' in result.stdout
            return result

    rec = Recorder(OUT)
    helper.install(rec, 'install', pack, target)
    assert common.sha(target / '.aide/scripts/aide_lite.py') == subject['delivered_cli_sha256']
    module = helper.load_delivered(pack)
    forms = {}

    def write(relative, text):
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def command(label, *args, form=None, exits=(0,), writes=()):
        before = helper.tree_hashes(target)
        result = rec.installed(label, target, *args, exits=exits)
        after = helper.tree_hashes(target)
        changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
        assert changed <= set(writes), (label, sorted(changed - set(writes)))
        if form:
            assert form not in forms
            forms[form] = {'command': label, 'exit_code': result.returncode,
                           'allowed_report_writes': list(writes)}
        return result.stdout

    task_id = 'DELIVERED-ADDITIONS-01'
    task_path = '.aide/queue/' + task_id
    write('.aide/queue/index.yaml', f'items:\n  - id: {task_id}\n    status: interrupted\n')
    write('.aide/context/latest-task-packet.md', f'# Consumer task\ntask_id: {task_id}\n')
    write(task_path + '/task.yaml', f'id: {task_id}\ntitle: Preserve an interrupted fixture\n')
    receipt = write(task_path + '/evidence/completed.json', '{"effect":"first","result":"completed"}\n')
    write(task_path + '/status.yaml', f'task_id: {task_id}\nstatus: interrupted\nresult: INCOMPLETE\n'
          'owner: consumer_team\nnext_action: inspect_uncertain_effect\n'
          'remaining_obligations:\n  - second_effect\ncompleted_ref: evidence/completed.json\n'
          'completed_sha256: ' + common.sha(receipt) + '\n')
    for action in ('current', 'resume-plan'):
        for explicit in (False, True):
            for machine in (False, True):
                args = ['task', action] + (['--task-id', task_id] if explicit else []) + (['--json'] if machine else [])
                form = 'task ' + action + (' --task-id <ID>' if explicit else '') + (' --json' if machine else '')
                report_writes = [module.TASK_OS_RESUME_PLAN_REPORT_PATH] if action == 'resume-plan' and not machine else []
                text = command(f'{action}-{explicit}-{machine}', *args, form=form, writes=report_writes)
                if machine:
                    data = json.loads(text)
                    view = data if action == 'current' else data['task']
                    assert view['task_id'] == task_id and view['status'] == 'interrupted'
                    assert view['remaining_obligations'] == ['second_effect']
                    assert view['acceptance_verified'] is False
                    assert view['evidence'][0]['digest_verified'] is True
                    assert view['evidence'][0]['applicability'] == 'unverified'
                    if action == 'resume-plan':
                        assert data['execution_admitted'] is False and data['safe_to_resume'] is None
                        assert data['recommendation'] == 'reconcile_attempt'
                elif action == 'current':
                    assert f'task_id: {task_id}' in text and 'status: interrupted' in text
                else:
                    assert 'safe_to_resume: unknown' in text
                    assert task_path in (target / module.TASK_OS_RESUME_PLAN_REPORT_PATH).read_text()
    for action in ('current', 'resume-plan'):
        refused = json.loads(command(action + '-escape', 'task', action, '--task-id', '../../outside', '--json', exits=(1,)))
        assert (refused if action == 'current' else refused['task'])['task_id'] == ''
    write('.aide/context/latest-task-packet.md', 'task_id: ../../outside\n')
    for action in ('current', 'resume-plan'):
        command(action + '-broken-default', 'task', action, '--json', exits=(1,))
        text = command(action + '-explicit-survives', 'task', action, '--task-id', task_id, '--json')
        assert task_id in text
    write('.aide/context/latest-task-packet.md', f'# Consumer task\ntask_id: {task_id}\n')

    # A real disposable Git repository; no remote or live repository mutation.
    hooks = fixture / 'empty-hooks'
    hooks.mkdir()
    for label, args in (('fixture-init', ['init', '-b', 'main']),
                        ('fixture-commit', ['-c', 'user.name=Consumer Fixture', '-c',
                         'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
                         '-c', 'core.hooksPath=' + str(hooks),
                         'commit', '--allow-empty', '-m', 'Fixture base'])):
        result = invoke(label, ['git', '-C', str(target), *args], target)
        assert result.returncode == 0, result.stderr
    workflow = target / '.aide/policies/git-workflow.yaml'
    workflow_text = workflow.read_text()
    for expected in ('main_hosting_protection: optional_project_choice',
                     'dev_hosting_protection: normally_disabled_project_may_override',
                     'task_branches: local_short_lived_by_default',
                     'publish_task_when: collaboration important_checkpoint or blocked_continuity warrants sharing',
                     'remote_cleanup: exact_reviewed_closed_inactive_contained_task_refs_only'):
        assert expected in workflow_text, expected
    assert 'non_mutating: true' in command('git-policy', 'git', 'policy', form='git policy')
    detected = command('git-detect', 'git', 'detect', form='git detect')
    assert 'current_branch: main' in detected and 'non_mutating: true' in detected
    plan = command('git-plan', 'git', 'plan', form='git plan')
    assert 'dry_run: true' in plan and 'remote_mutation: false' in plan
    override = workflow_text.replace('main_hosting_protection: optional_project_choice',
                                     'main_hosting_protection: project_requires_protection')
    write('.aide/policies/git-workflow.yaml', override)
    command('git-project-override', 'git', 'policy')
    assert workflow.read_text() == override

    command('review-pack', 'review-pack', form='review-pack', writes=[module.REVIEW_PACKET_PATH])
    review = (target / module.REVIEW_PACKET_PATH).read_text()
    assert '.aide/prompts/evidence-review.md' in review
    assert '.aide/verification/review-decision-policy.yaml' in review

    write('app/main.py', 'from app import helper\n\ndef run():\n    return helper.VALUE\n')
    write('app/helper.py', 'VALUE = 1\n\ndef shared_helper():\n    return VALUE\n')
    write('lib/other_helper.py', 'def shared_helper():\n    return 2\n')
    write('app/tests/test_main.py', 'from app import main\n\ndef test_run():\n    assert main.run() == 1\n')
    write('docs/consumer-guide.md', '# Guide\nSee [main](app/main.py).\n')
    # Existing delivered inventory owner supplies the input to actual CLI ledger.
    module.write_repo_intelligence_outputs(target, module.build_repo_intelligence(target))
    command('quality-ledger', 'quality', 'ledger', form='quality ledger', writes=module.Q38_GENERATED_OUTPUT_FILES)
    command('quality-reuse', 'quality', 'reuse', form='quality reuse')
    text = command('quality-human', 'quality', 'explain-file', 'app/main.py', form='quality explain-file <path>')
    assert 'app/tests/test_main.py' in text and 'freshness: unverified' in text
    data = json.loads(command('quality-json', 'quality', 'explain-file', 'app/helper.py', '--json', form='quality explain-file <path> --json'))
    assert data['coverage'] == 'heuristic_incomplete' and data['freshness'] == 'unverified'
    assert any('lib/other_helper.py' in item['peers']['items'] for item in data['reuse']['items'])
    assert any('does not prove shared semantics' in item for item in data['caveats'])
    missing = json.loads(command('quality-unindexed', 'quality', 'explain-file', 'unknown.py', '--json', exits=(1,)))
    assert missing['coverage'] == 'unindexed'
    write('app/helper.py', 'raise RuntimeError("changed after inventory")\n')
    assert json.loads(command('quality-stale', 'quality', 'explain-file', 'app/helper.py', '--json')) == data

    # Explicit synthetic receipts test accounting behavior, not actual model cost.
    work = {'schema': 'aide.work-effort-set.v1', 'work_id': 'consumer-work', 'receipts': [], 'usage_roster': None}
    for index, code in enumerate((0, 1)):
        job = {'schema': 'aide.maintainer-job.v1', 'workunit': 'consumer-work', 'source_commit': 'b' * 40, 'source_tree': 'c' * 40}
        job_id = ('a' if index == 0 else 'e') * 32
        value = {'job_id': job_id, 'job': job,
                 'manifest_digest': hashlib.sha256(json.dumps(job, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
                 'phase': 'retired', 'scratch_absent': True, 'reservation_released': True,
                 'result': {'job_id': job_id, 'reason': 'exited', 'exit_code': code, 'quiescent': True},
                 'peaks': {'memory_bytes': 100 - index, 'scratch_bytes': 200 + index},
                 'collected_manifest': {'output': 'd' * 64}}
        path = write(f'fixture-receipt-{index}.json', json.dumps(value) + '\n')
        work['receipts'].append({'path': path.name, 'sha256': common.sha(path), 'phase': 'tests'})
    work['receipts'].append(dict(work['receipts'][0]))
    write('fixture-work.json', json.dumps(work) + '\n')
    human = command('effort-human', 'job', 'effort', '--work-set', 'fixture-work.json', exits=(2,), form='job effort --work-set <path>')
    assert '1 failed' in human and 'accounting unknown' in human
    data = json.loads(command('effort-json', 'job', 'effort', '--work-set', 'fixture-work.json', '--json', exits=(2,), form='job effort --work-set <path> --json'))
    assert data['attempt_count'] == 2 and data['duplicate_observations_excluded'] == 1
    assert data['execution_outcomes']['FAILED'] == 1 and data['execution_outcomes']['SUCCEEDED'] == 1
    assert data['whole_work_cost'] is None and data['model_usage'] is None
    refused = json.loads(command('effort-escape', 'job', 'effort', '--work-set', '../fixture-work.json', '--json', exits=(1,)))
    assert refused['status'] == 'REFUSED'
    work['receipts'][0]['sha256'] = '0' * 64
    write('fixture-work.json', json.dumps(work) + '\n')
    refused = json.loads(command('effort-changed-input', 'job', 'effort', '--work-set', 'fixture-work.json', '--json', exits=(1,)))
    assert refused['status'] == 'REFUSED'

    required = json.loads((ROOT / '.aide/release/successor-candidate.json').read_text())['additional_cli_forms']
    assert set(forms) == set(required) and len(forms) == 18
    for name, value in subject['assets'].items():
        assert common.sha(ROOT / name) == value['sha256']
    summary = {'status': 'PASS', 'forms': forms, 'commands': rec.commands,
               'assets': subject['assets'], 'installed_cli_sha256': subject['delivered_cli_sha256'],
               'usage_fixture': 'synthetic', 'whole_task_cost': None, 'model_calls': 0,
               'release_qualification': 'other gates pending', 'fixture_retired': False}
    common.write(OUT / 'summary.json', summary)
    worker = common.load('additions_retirement', common.ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(fixture)
    summary['fixture_retired'] = True
    common.write(OUT / 'summary.json', summary)
    print('PASS all 18 additive delivered CLI forms; refusal and unchanged-state checks retained')


if __name__ == '__main__':
    main()
