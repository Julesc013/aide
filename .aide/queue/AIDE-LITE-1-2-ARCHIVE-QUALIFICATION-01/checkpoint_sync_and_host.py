"""One reviewed checkpoint, guarded dev synchronization and targeted hosted run."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.apply.managed_commit import create_commit
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source, effect = E / 'profile-hosted-source.json', E / 'profile-hosted-effect.json'
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped, plan = (json.loads(p.read_bytes()) for p in (source, effect))
    assert mapped['effect_sha256'] == sha(effect)
    verdict_path = E / 'profile-hosted-review.json'
    verdict = json.loads(verdict_path.read_bytes())
    assert verdict['decision'] == 'ACCEPT' and not verdict['required_fixes']
    assert verdict['reviewer'] == '/root/review_disked_continuation'
    assert [verdict['source_sha256'], verdict['effect_sha256'], verdict['controller_sha256']] == [sha(source), sha(effect), sha(Path(__file__))]
    allowed = set(mapped['files']) | {p.relative_to(ROOT).as_posix() for p in (source, verdict_path)}
    logs = E / 'profile-hosted-checkpoint-streams.log'
    logs.mkdir()
    receipt = E / 'profile-hosted-checkpoint.log'
    assert not receipt.exists()
    result = {'state': 'started', 'source_sha256': sha(source), 'effect_sha256': sha(effect), 'operations': []}

    def save():
        receipt.write_bytes((json.dumps(result, indent=2) + '\n').encode())

    def run(label, argv):
        row = {'label': label, 'argv': argv, 'state': 'started'}
        result['operations'].append(row)
        save()
        streams = [logs / (label + ending) for ending in ('.stdout', '.stderr')]
        try:
            with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
                value = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=90)
            row.update(state='completed', exit_code=value.returncode)
        except BaseException as error:
            row.update(state='exception', error_type=type(error).__name__, error=str(error))
            raise
        finally:
            row['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in streams if p.exists()}
            save()
        assert value.returncode == 0, label
        return streams[0].read_text(encoding='utf-8').strip()

    def git(label, *args):
        return run(label, ['git', *args])

    def inputs():
        assert sha(source) == sys.argv[1] and sha(effect) == sys.argv[2]
        assert all(sha(ROOT / name) == value for name, value in mapped['files'].items())
        assert all(sha(ROOT / name) == value for name, value in plan['stable_assets'].items())
        inputs = json.loads((E / 'profile-hosted-inputs.json').read_bytes())
        assert sha(E / 'profile-hosted-inputs.json') == plan['package_inputs_sha256']
        assert all(sha(ROOT / name) == value for name, value in inputs['files'].items())
        assert workspace.dispatch_state(roots['control'])['mode'] == 'running'
        assert not (roots['control'] / 'active.json').exists()

    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == plan['control_config_digest']
    spec = importlib.util.spec_from_file_location('archive_hosted_checkpoint_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    try:
        with workspace.estate_lock(roots['control']), workspace.estate_lock(roots['control'], 'dispatch.lock'):
            inputs()
            assert git('branch', 'branch', '--show-current') == plan['task_branch']
            assert git('head', 'rev-parse', 'HEAD') == plan['checkpoint_parent']
            for ref in ('dev', 'origin/dev'):
                assert git('ref-' + ref.replace('/', '-'), 'rev-parse', ref) == plan['dev_preimage']
            for ref in ('main', 'origin/main'):
                assert git('ref-' + ref.replace('/', '-'), 'rev-parse', ref) == plan['main_base']
            refs = {line.split()[1]: line.split()[0] for line in git('refs', 'show-ref').splitlines()}
            assert refs == plan['all_refs']
            assert not git('index', 'diff', '--cached', '--name-only')
            changed = set(git('changed', 'diff', '--name-only').splitlines()) | set(git('untracked', 'ls-files', '--others', '--exclude-standard').splitlines())
            assert changed == allowed, sorted(changed ^ allowed)
            for flags, label in ((('--all',), 'fetch-url'), (('--push', '--all'), 'push-url')):
                assert git(label, 'remote', 'get-url', *flags, 'origin') == plan['origin_url']
            remote = {r.split()[1]: r.split()[0] for r in git('remote', 'ls-remote', '--heads', 'origin', 'dev', 'main').splitlines()}
            assert remote == {'refs/heads/dev': plan['dev_preimage'], 'refs/heads/main': plan['main_base']}
            helper = lite.make_git_helper_plan(ROOT, 'plan', dry_run=True)
            result['helper_plan'] = helper
            save()
            assert helper['status'] == 'blocked' and helper['blockers'] == ['dirty_tree_requires_classification']
            git('diff-check', 'diff', '--check')
            run('message', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check', '--message-file', str(E / 'profile-hosted-message.txt')])
            git('stage', 'add', '--', *sorted(allowed))
            assert set(git('staged', 'diff', '--cached', '--name-only').splitlines()) == allowed
            inputs()
            for index, name in enumerate(sorted(allowed)):
                assert git('raw-' + str(index), 'hash-object', '--no-filters', '--', name) == git('blob-' + str(index), 'rev-parse', ':' + name)
            tree = git('tree', 'write-tree')
            message = E / 'profile-hosted-message.txt'
            commit = create_commit(ROOT, message=message.read_bytes(), expected_message_sha256=sha(message),
                expected_ref='refs/heads/' + plan['task_branch'], expected_head=plan['checkpoint_parent'],
                expected_tree=tree, allowed_paths=sorted(allowed), apply=True,
                validator=lambda body: [c.message for c in lite.validate_commit_message_text(body) if c.severity == 'FAIL'])
            result.update(state='checkpointed', commit=commit)
            save()
            assert commit['status'] == 'COMMITTED' and not git('clean', 'status', '--porcelain')
            run('commit-check', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check', '--latest'])
            candidate = commit['candidate_commit']
            # The existing preview owner writes only this task's ignored outputs.
            projection_spec = importlib.util.spec_from_file_location('profile_dev_preview_owner', TASK / 'sync_revised_dev.py')
            projection = importlib.util.module_from_spec(projection_spec)
            projection_spec.loader.exec_module(projection)
            projection.EVIDENCE = E / 'profile-hosted-preview.log'
            projection.EVIDENCE.mkdir()
            preview = projection.project_preview(lite, plan['dev_preimage'], candidate, 'local', plan['canonical_preimages'], plan['source_commits'])
            result['preview_sha256s'] = preview
            save()
            validation = run('validate-before-dev', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'validate'])
            lines = validation.splitlines()
            assert lines.count('status: PASS') == 1
            summaries = [line for line in lines if line.startswith('checks:')]
            assert len(summaries) == 1
            counts = re.fullmatch(r'checks: (\d+); PASS: (\d+); WARN: (\d+); FAIL: (\d+); OTHER: (\d+)', summaries[0])
            assert counts and tuple(map(int, counts.groups()[2:])) == (1, 0, 0)
            assert int(counts[1]) == int(counts[2]) + 1
            assert [line for line in lines if line.startswith('- ') and not line.startswith('- PASS ')] == [
                '- WARN review packet review ref missing: .aide/prompts/evidence-review.md']
            run('range-before-dev', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check', '--range', plan['dev_preimage'] + '..' + candidate])
            assert not git('clean-before-dev', 'status', '--porcelain')
            ready = lite.make_git_helper_plan(ROOT, 'plan', dry_run=True)
            result['ready_dev_plan'] = ready
            save()
            assert ready['status'] != 'blocked' and not ready['blockers']
            assert workspace.dispatch_state(roots['control'])['mode'] == 'running' and not (roots['control'] / 'active.json').exists()
            inputs()
            current_remote = {r.split()[1]: r.split()[0] for r in git('remote-before-dev', 'ls-remote', '--heads', 'origin', 'dev', 'main').splitlines()}
            assert current_remote == {'refs/heads/dev': plan['dev_preimage'], 'refs/heads/main': plan['main_base']}
            git('dev-ancestor', 'merge-base', '--is-ancestor', plan['dev_preimage'], candidate)
            git('dev-local', 'update-ref', 'refs/heads/dev', candidate, plan['dev_preimage'])
            for flags, label in ((('--all',), 'dev-fetch-url'), (('--push', '--all'), 'dev-push-url')):
                assert git(label, 'remote', 'get-url', *flags, 'origin') == plan['origin_url']
            git('push-dev', 'push', '--no-follow-tags', 'origin', candidate + ':refs/heads/dev')
            git('fetch-dev', 'fetch', '--no-tags', 'origin', 'refs/heads/dev:refs/remotes/origin/dev')
            remote_after = {r.split()[1]: r.split()[0] for r in git('remote-after-dev', 'ls-remote', '--heads', 'origin', 'dev', 'main').splitlines()}
            assert remote_after == {'refs/heads/dev': candidate, 'refs/heads/main': plan['main_base']}
            assert preview == projection.project_preview(lite, plan['dev_preimage'], candidate, 'dev', plan['canonical_preimages'], plan['source_commits'])
            assert git('dev-tracking', 'rev-parse', 'origin/dev') == git('dev-final', 'rev-parse', 'dev') == candidate
            expected_refs = dict(plan['all_refs'])
            for ref in ('refs/heads/' + plan['task_branch'], 'refs/heads/dev', 'refs/remotes/origin/dev'):
                expected_refs[ref] = candidate
            for ref, target in plan['symbolic_refs'].items():
                assert git('symbolic-' + ref.replace('/', '-'), 'symbolic-ref', ref) == target
                expected_refs[ref] = expected_refs[target]
            observed_refs = {r.split()[1]: r.split()[0] for r in git('refs-after-dev', 'show-ref').splitlines()}
            assert observed_refs == expected_refs
            assert not git('clean-after-dev', 'status', '--porcelain')
            result['dev_synced'] = candidate
            save()
        # The reused observer owns its finite wait and complete stream collection.
        subprocess.run([sys.executable, '-B', str(TASK / 'observe_profile_hosted.py'), sha(source), sha(effect)],
                       cwd=ROOT, check=True, stdin=subprocess.DEVNULL)
        result['state'] = 'hosted_observed'
        save()
    except BaseException as error:
        result.update(state='stopped', error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == '__main__':
    main()
