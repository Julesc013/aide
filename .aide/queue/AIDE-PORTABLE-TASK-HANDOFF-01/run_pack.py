"""Refresh the owned pack, then exercise delivered and safe-installed handoff."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-PORTABLE-TASK-HANDOFF-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def invoke(label, command, cwd=ROOT):
    stdout, stderr = OUTPUT / (label + '.stdout'), OUTPUT / (label + '.stderr')
    receipt = OUTPUT / (label + '.invocation.json')
    record = {'command': command, 'cwd': str(cwd), 'state': 'started', 'exit_code': None}
    def save():
        receipt.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    save()
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, timeout=90)
        record.update(state='completed', exit_code=result.returncode)
    except (OSError, subprocess.SubprocessError) as error:
        record.update(state='exception', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record['streams'] = {p.name: {'bytes': p.stat().st_size,
                                     'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                             for p in (stdout, stderr) if p.exists()}
        save()
    assert result.returncode == 0, label + ' failed; original output retained'
    return stdout.read_bytes()


refresh = load('handoff_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', refresh.sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
added = {'files/.aide/scripts/task_handoff.py', 'files/.aide/scripts/tests/test_task_handoff.py'}
changed = {'files/.aide/scripts/aide_lite.py', 'files/docs/reference/task-os-report-only-commands.md'}
assert set(after) == set(old) | added and not added.intersection(old)
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
for name in added | changed:
    assert refresh.sha(pack / name) == refresh.sha(ROOT / name.removeprefix('files/'))
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])

# Actual completed WorkUnit contains a retained failed attempt and outstanding gates.
real_task = 'AIDE-CONTEXT-TASK-SELECTION-01'
records = [f'.aide/queue/{real_task}/{n}' for n in ('task.yaml', 'status.yaml', 'ExecPlan.md')]
real_before = {path: (ROOT / path).read_bytes() for path in records}
delivered_cli = pack / 'files/.aide/scripts/aide_lite.py'
raw = invoke('real-handoff', [sys.executable, '-I', '-B', str(delivered_cli), '--repo-root',
                             str(ROOT), 'task', 'handoff', 'export', '--task-id', real_task])
bundle = json.loads(raw)
assert bundle['task_id'] == real_task
for path in records:
    assert bundle['records'][path]['text'].encode('utf-8') == real_before[path]

q31 = load('handoff_q31', ROOT / '.aide/scripts/tests/test_q31_export_pack_governance.py')
aide = load('handoff_delivered_cli', delivered_cli)
with tempfile.TemporaryDirectory(prefix='handoff-consumer-') as directory:
    target = Path(directory)
    q31.init_target_git(target)
    preview = aide.apply_import_pack(pack, target, dry_run=True, mode='safe')
    assert not preview['conflicts'], preview['conflicts']
    installed = aide.apply_import_pack(pack, target, mode='safe', expected_plan_digest=preview['plan_digest'])
    assert not installed['conflicts'] and installed['status'] == 'APPLIED'
    assert not (target / 'core').exists()
    helper = '.aide/scripts/task_handoff.py'
    receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    assert receipt['mode'] == 'safe'
    entry = receipt['managed'][helper]
    assert entry['ownership'] == 'aide_portable_managed'
    assert entry['installed_digest'] == refresh.sha(target / helper) == refresh.sha(ROOT / helper)
    for path, data in real_before.items():
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    (target / 'handoff.json').write_bytes(raw)
    prefix = [sys.executable, '-I', str(target / '.aide/scripts/aide_lite.py'),
              '--repo-root', str(target), 'task', 'handoff']
    expected = refresh.inventory_bytes(target)
    observed = json.loads(invoke('installed-inspect', prefix + ['inspect', '--bundle', 'handoff.json',
                                  '--sha256', hashlib.sha256(raw).hexdigest(), '--json'], target))
    assert [x['comparison'] for x in observed['records']] == ['matching'] * 3
    assert observed['captured_observation'] == bundle and not observed['execution_admitted']
    exported = json.loads(invoke('installed-export', prefix + ['export', '--task-id', real_task], target))
    assert exported['records'] == bundle['records'] and exported['task_id'] == real_task
    assert refresh.inventory_bytes(target) == expected, 'installed read-only commands wrote files'
    (target / records[1]).write_bytes(b'status: interrupted\nremaining_obligations: reconcile_current_attempt\n')
    changed_observation = json.loads(invoke('installed-changed', prefix + ['inspect', '--bundle', 'handoff.json',
                                           '--sha256', hashlib.sha256(raw).hexdigest(), '--json'], target))
    assert [x['comparison'] for x in changed_observation['records']] == ['matching', 'changed', 'matching']
    consumer = {'status': 'PASS', 'actual_cli': str(target / '.aide/scripts/aide_lite.py'),
                'core_absent': True, 'receipt_sha256': refresh.sha(target / aide.PORTABLE_IMPORT_RECEIPT_PATH),
                'helper_entry': entry, 'source_task': real_task, 'bundle_sha256': hashlib.sha256(raw).hexdigest(),
                'original_record_sha256s': {p: hashlib.sha256(data).hexdigest() for p, data in real_before.items()},
                'read_only_inventory_preserved': True, 'changed_status_detected': True}
    (OUTPUT / 'installed-consumer.json').write_text(json.dumps(consumer, indent=2) + '\n', encoding='utf-8')
assert all((ROOT / p).read_bytes() == data for p, data in real_before.items())
assert refresh.inventory_bytes(pack) == after
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'delivered_tests': 79, 'ownership_tests': 6, 'safe_installed_consumer': 'PASS',
     'added': sorted(added), 'changed_payload': sorted(changed), 'after_sha256s': after,
     'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 79, 'safe_installed_consumer': 'PASS'}))
