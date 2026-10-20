"""One reviewed checkpoint and final existing-runner qualification group."""
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
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
    source, effect = E / 'final-source.json', E / 'final-effect.json'
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped, plan = (json.loads(p.read_bytes()) for p in (source, effect))
    assert mapped['effect_sha256'] == sha(effect)
    verdict_path = E / 'final-review.json'
    verdict = json.loads(verdict_path.read_bytes())
    assert verdict['decision'] == 'ACCEPT' and not verdict['required_fixes']
    assert verdict['reviewer'] == '/root/review_disked_continuation'
    assert [verdict['source_sha256'], verdict['effect_sha256'], verdict['controller_sha256']] == [sha(source), sha(effect), sha(Path(__file__))]
    allowed = set(mapped['files']) | {p.relative_to(ROOT).as_posix() for p in (source, verdict_path)}
    logs = E / 'final-checkpoint-streams.log'
    logs.mkdir()
    receipt = E / 'final-checkpoint.log'
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
        inputs = json.loads((E / 'final-inputs.json').read_bytes())
        assert sha(E / 'final-inputs.json') == plan['package_inputs_sha256']
        assert all(sha(ROOT / name) == value for name, value in inputs['files'].items())
        assert workspace.dispatch_state(roots['control'])['mode'] == 'running'
        assert not (roots['control'] / 'active.json').exists()

    actual_environment = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(), 'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(), 'version': platform.python_version()}}
    assert actual_environment == plan['profile_environment']
    coverage = json.loads((E / 'profile-coverage.json').read_bytes())
    assert coverage['behavioral_coverage_pass'] and coverage['fresh_primary_identity_required'] and not coverage['release_accepted']
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
            run('message', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check', '--message-file', str(E / 'final-message.txt')])
            git('stage', 'add', '--', *sorted(allowed))
            assert set(git('staged', 'diff', '--cached', '--name-only').splitlines()) == allowed
            inputs()
            for index, name in enumerate(sorted(allowed)):
                assert git('raw-' + str(index), 'hash-object', '--no-filters', '--', name) == git('blob-' + str(index), 'rev-parse', ':' + name)
            tree = git('tree', 'write-tree')
            message = E / 'final-message.txt'
            commit = create_commit(ROOT, message=message.read_bytes(), expected_message_sha256=sha(message),
                expected_ref='refs/heads/' + plan['task_branch'], expected_head=plan['checkpoint_parent'],
                expected_tree=tree, allowed_paths=sorted(allowed), apply=True,
                validator=lambda body: [c.message for c in lite.validate_commit_message_text(body) if c.severity == 'FAIL'])
            result.update(state='checkpointed', commit=commit)
            save()
            assert commit['status'] == 'COMMITTED' and not git('clean', 'status', '--porcelain')
            run('commit-check', [sys.executable, '-B', '.aide/scripts/aide_lite.py', 'commit', 'check', '--latest'])
            candidate = commit['candidate_commit']
        candidate = commit['candidate_commit']
        subject_tree = commit['expected_tree']
        assert git('job-head', 'rev-parse', 'HEAD') == candidate
        assert git('job-tree', 'rev-parse', 'HEAD^{tree}') == subject_tree
        assert not git('job-clean', 'status', '--porcelain')
        inputs()
        qualification, _, _ = workspace.load_config(ROOT / plan['qualification_config'])
        assert workspace.digest(qualification) == plan['qualification_config_digest']
        job = json.loads((E / 'final-job-template.json').read_bytes())
        job.update(source_commit=candidate, source_tree=subject_tree)
        result.update(state='local_admission', job=job)
        save()
        terminal = workspace.run(ROOT / plan['qualification_config'], job)
        result.update(state='local_terminal', job_result=terminal)
        save()
        assert terminal['job'] == job and terminal['manifest_digest'] == workspace.digest(job)
        assert terminal['config_digest'] == plan['qualification_config_digest']
        assert terminal['phase'] == 'retired' and terminal['scratch_absent'] and terminal['reservation_released']
        assert terminal['result']['exit_code'] == 0 and terminal['result']['quiescent'] and not terminal['result']['io_errors']
        assert git('final-head', 'rev-parse', 'HEAD') == candidate
        assert git('final-tree', 'rev-parse', 'HEAD^{tree}') == subject_tree
        assert not git('final-clean', 'status', '--porcelain')
        inputs()
        result['state'] = 'final_qualification_terminal_pass'
        save()
        print(json.dumps({'state':result['state'],'job_id':terminal['job_id'],'phase':terminal['phase']}), flush=True)
    except BaseException as error:
        result.update(state='stopped', error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == '__main__':
    main()
