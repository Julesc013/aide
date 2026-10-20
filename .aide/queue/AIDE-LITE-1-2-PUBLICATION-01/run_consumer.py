"""One original consumer on acquired release bytes through the existing runner."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    effect = E / 'acquired-effect.json'
    assert len(sys.argv) == 2 and sha(effect) == sys.argv[1]
    plan = json.loads(effect.read_bytes())
    assert plan['controller_sha256'] == sha(Path(__file__))
    review = json.loads((E / 'consumer-checkpoint-review.json').read_bytes())
    assert review['decision'] == 'ACCEPT' and not review['required_fixes']
    assert review['reviewer'] == '/root/review_disked_continuation'
    assert review['acquired_effect_sha256'] == sha(effect)
    assert review['acquired_controller_sha256'] == sha(Path(__file__))
    assert review['source_sha256'] == sha(E / 'consumer-checkpoint-source.json')
    assert review['effect_sha256'] == sha(E / 'consumer-checkpoint-effect.json')
    assert review['controller_sha256'] == sha(TASK / 'consumer_checkpoint.py')
    completed = json.loads((E / 'consumer-checkpoint-attempt-01.log/result.json').read_bytes())
    assert completed['status'] == 'PASS'
    assert len(completed['preview_sha256s']) == 6
    assert all(row['state'] == 'completed' and row['exit_code'] == 0 for row in completed['operations'])
    candidate, tree = completed['commit'], completed['tree']
    receipt = E / 'acquired-execution.log'
    with receipt.open('x', encoding='utf-8') as stream:
        stream.write('{}\n')
    result = {'state': 'started', 'effect_sha256': sha(effect), 'model_requests': 0,
        'source_commit': candidate, 'source_tree': tree, 'allocation_ceiling': 1}

    def save():
        receipt.write_bytes((json.dumps(result, indent=2) + '\n').encode('utf-8'))

    def inputs():
        assert sha(effect) == sys.argv[1]
        assert all(sha(ROOT / name) == value for name, value in plan['files'].items())
        assert git('rev-parse', 'HEAD') == candidate and git('rev-parse', 'HEAD^{tree}') == tree
        assert git('branch', '--show-current') == plan['task_branch']
        assert not git('status', '--porcelain')
        for ref in ('dev', 'main', 'origin/dev', 'origin/main'):
            assert git('rev-parse', ref) == candidate
        assert git('rev-parse', 'aide-lite-v1.2.0^{}') == plan['published_tag_target']
        assert workspace.dispatch_state(roots['control'])['mode'] == 'running'
        assert not (roots['control'] / 'active.json').exists()

    try:
        config, roots, working = workspace.load_config(ROOT / plan['qualification_config'])
        assert workspace.digest(config) == plan['qualification_config_digest']
        job = json.loads((E / 'acquired-job-template.json').read_bytes())
        assert sha(E / 'acquired-job-template.json') == plan['job_template_sha256']
        job.update(source_commit=candidate, source_tree=tree)
        with workspace.estate_lock(roots['control']), workspace.estate_lock(roots['control'], 'dispatch.lock'):
            inputs()
            workspace.validate_job(job, working)
            result.update(state='admission', job=job)
            save()
        terminal = workspace.run(ROOT / plan['qualification_config'], job)
        result.update(state='terminal', job_result=terminal)
        save()
        assert terminal['job'] == job and terminal['manifest_digest'] == workspace.digest(job)
        assert terminal['config_digest'] == plan['qualification_config_digest']
        assert terminal['phase'] == 'retired' and terminal['scratch_absent'] and terminal['reservation_released']
        assert terminal['result']['exit_code'] == 0 and terminal['result']['quiescent'] and not terminal['result']['io_errors']
        assert all(workspace.content_digest(Path(terminal['retained']) / name) == value for name, value in terminal['collected_manifest'].items())
        acquired = json.loads((Path(terminal['retained']) / 'output/acquired-consumer.json').read_bytes())
        assert acquired['status'] == 'PASS' and acquired['fixture_retired'] and acquired['original_assertions'] == 'unchanged'
        inputs()
        result['state'] = 'acquired_original_consumer_pass'
        save()
        print(json.dumps({'state': result['state'], 'job_id': terminal['job_id'], 'phase': terminal['phase']}), flush=True)
    except BaseException as error:
        result.update(state='stopped_reconcile', error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == '__main__':
    main()
