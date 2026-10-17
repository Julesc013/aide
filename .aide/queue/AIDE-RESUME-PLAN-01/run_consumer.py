"""Disposable CLI continuation exercise, not a runtime cancellation claim."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
cli = source / '.aide/scripts/aide_lite.py'
output = Path(os.environ['AIDE_JOB_OUTPUT'])
with tempfile.TemporaryDirectory(prefix='resume-consumer-') as temporary:
    root = Path(temporary)
    task_id = 'CONSUMER-CONTINUATION-01'
    task = root / '.aide/queue' / task_id
    task.mkdir(parents=True)
    (root / '.aide/context').mkdir()
    (task / 'task.yaml').write_text(f'id: {task_id}\ntitle: Complete two bounded fixture effects\n', encoding='utf-8')
    (root / '.aide/context/latest-task-packet.md').write_text('task_id: ANOTHER-TASK\n', encoding='utf-8')
    first = task / 'first-effect.txt'
    # A separate fixture process exits abruptly after one durable effect/receipt.
    producer = """import hashlib,os,sys
from pathlib import Path
p=Path(sys.argv[1]); data=b'first fixture effect completed\\n'
(p/'first-effect.txt').write_bytes(data)
(p/'receipt.json').write_text('{"effect":"first","result":"completed"}\\n',encoding='utf-8')
sha=hashlib.sha256((p/'receipt.json').read_bytes()).hexdigest()
(p/'status.yaml').write_text('task_id: CONSUMER-CONTINUATION-01\\nstatus: interrupted\\nresult: INCOMPLETE\\ncompleted_ref: receipt.json\\ncompleted_sha256: '+sha+'\\nremaining_obligations:\\n  - second_fixture_effect\\n',encoding='utf-8')
os._exit(7)
"""
    result = subprocess.run([sys.executable, '-B', '-c', producer, str(task)], timeout=10)
    assert result.returncode == 7
    preserved = {p.name: p.read_bytes() for p in (first, task / 'receipt.json', task / 'status.yaml')}
    records = []
    def inspect(expected):
        before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, '-B', str(cli), '--repo-root', str(root),
                                 'task', 'resume-plan', '--task-id', task_id, '--json'],
                                capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data['task']['task_id'] == task_id and data['recommendation'] == expected
        assert data['safe_to_resume'] is None and data['execution_admitted'] is False
        assert before == {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        assert first.read_bytes() == preserved['first-effect.txt']
        assert (task / 'receipt.json').read_bytes() == preserved['receipt.json']
        records.append(data)
        return data
    partial = inspect('reconcile_attempt')
    assert partial['task']['remaining_obligations'] == ['second_fixture_effect']
    assert partial['task']['evidence'][0]['digest_verified'] is True
    assert partial['task']['evidence'][0]['applicability'] == 'unverified'
    # An explicitly owned fixture transition, not an automatic action by the CLI.
    (task / 'original-incomplete.yaml').write_bytes(preserved['status.yaml'])
    (task / 'second-effect.txt').write_text('second fixture effect completed\n', encoding='utf-8')
    (task / 'status.yaml').write_text(
        f'task_id: {task_id}\nstatus: passed\nresult: PASS_FIXTURE\n'
        'original_ref: original-incomplete.yaml\ncompleted_ref: receipt.json\n'
        'remaining_obligations:\n  - actual_host_recovery_unqualified\n', encoding='utf-8')
    complete = inspect('inspect_completed_evidence')
    assert complete['task']['result'] == 'PASS_FIXTURE'
    assert complete['task']['remaining_obligations'] == ['actual_host_recovery_unqualified']
    assert (task / 'original-incomplete.yaml').read_bytes() == preserved['status.yaml']
    (output / ('consumer-delivered.json' if 'export' in source.parts else 'consumer-source.json')).write_text(
        json.dumps({'status': 'PASS', 'producer_exit': 7, 'inspections': records,
                    'completed_effect_sha256': hashlib.sha256(first.read_bytes()).hexdigest(),
                    'actual_host_recovery': 'unqualified'}, indent=2) + '\n', encoding='utf-8')
print('PASS fresh-process continuation advice, original incomplete result and completed effect preserved')
