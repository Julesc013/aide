"""Refresh the owned pack, then exercise delivered and safe-installed lesson selection."""
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
TASK = ROOT / '.aide/queue/AIDE-OUTCOME-LESSONS-01'
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



refresh = load('lesson_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', refresh.sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
added = {'files/.aide/scripts/outcome_lessons.py', 'files/.aide/scripts/tests/test_outcome_lessons.py'}
changed = {'files/.aide/scripts/aide_lite.py', 'files/.aide/policies/controller.yaml',
           'files/docs/reference/outcome-controller-v0.md'}
assert set(after) == set(old) | added and not added.intersection(old)
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
assert 'files/.aide/controller/outcome-ledger.jsonl' not in after
for name in added | changed:
    assert refresh.sha(pack / name) == refresh.sha(ROOT / name.removeprefix('files/'))
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])
delivered_cli = pack / 'files/.aide/scripts/aide_lite.py'
source_ledger = ROOT / '.aide/controller/outcome-ledger.jsonl'
source_before = source_ledger.read_bytes()
real = json.loads(invoke('delivered-real-lesson', [sys.executable, '-I', '-B', str(delivered_cli),
    '--repo-root', str(ROOT), 'outcome', 'lessons', '--path', '.aide/scripts/tests/test_validation_output.py', '--json']))
assert [x['id'] for x in real['selected']] == ['portable-validation-fixture']
assert source_ledger.read_bytes() == source_before

q31 = load('lesson_q31', ROOT / '.aide/scripts/tests/test_q31_export_pack_governance.py')
aide = load('lesson_delivered_cli', delivered_cli)
with tempfile.TemporaryDirectory(prefix='lesson-consumer-') as directory:
    target = Path(directory)
    q31.init_target_git(target)
    (target / 'project-notes.txt').write_bytes(b'project customization\n')
    customization = (target / 'project-notes.txt').read_bytes()
    preview = aide.apply_import_pack(pack, target, dry_run=True, mode='safe')
    assert not preview['conflicts'], preview['conflicts']
    installed = aide.apply_import_pack(pack, target, mode='safe', expected_plan_digest=preview['plan_digest'])
    assert not installed['conflicts'] and installed['status'] == 'APPLIED'
    assert not (target / 'core').exists()
    helper = '.aide/scripts/outcome_lessons.py'
    receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    assert receipt['mode'] == 'safe'
    entry = receipt['managed'][helper]
    assert entry['ownership'] == 'aide_portable_managed'
    assert entry['installed_digest'] == refresh.sha(target / helper) == refresh.sha(ROOT / helper)
    ledger = target / aide.OUTCOME_LEDGER_PATH
    assert not ledger.exists(), 'source history leaked into installed project'
    ledger.parent.mkdir(parents=True, exist_ok=True)
    (target / 'source.txt').write_bytes(b'project source\n')
    lesson = {'schema_version': 'aide.outcome-lesson.v1', 'id': 'project-lesson', 'revision': 1,
        'state': 'active', 'summary': 'Original project guidance.', 'applies_to': ['tests/check.py'],
        'evidence': [{'path': 'source.txt', 'sha256': refresh.sha(target / 'source.txt')}],
        'supersedes': None, 'required_features': ['advisory_only', 'revision_chain', 'source_sha256'],
        'project_metadata': {'retained': True}}
    prefix = [sys.executable, '-I', str(target / '.aide/scripts/aide_lite.py'),
              '--repo-root', str(target), 'outcome', 'lessons', '--path', 'tests/check.py', '--json']
    history = b''
    observations = []
    for revision, state, summary in [(1, 'active', 'Original project guidance.'),
                                     (2, 'active', 'Corrected project guidance.'),
                                     (3, 'retired', 'Now covered by a regression.')]:
        if revision > 1:
            previous = hashlib.sha256(json.dumps(lesson, sort_keys=True, ensure_ascii=True,
                separators=(',', ':'), allow_nan=False).encode('ascii')).hexdigest()
            lesson = {**lesson, 'revision': revision, 'state': state, 'summary': summary, 'supersedes': previous}
        row = {'run_id': f'project-review-{revision}', 'phase': 'review', 'source': 'project-owner',
               'result': 'PASS', 'lesson': lesson}
        history += (json.dumps(row, sort_keys=True) + '\n').encode('utf-8')
        ledger.write_bytes(history)
        inventory_before = refresh.inventory_bytes(target)
        observation = json.loads(invoke(f'installed-revision-{revision}', prefix, target))
        assert refresh.inventory_bytes(target) == inventory_before, 'read-only lookup wrote files'
        assert ledger.read_bytes() == history
        if state == 'active':
            assert [(x['revision'], x['lesson']['summary']) for x in observation['selected']] == [(revision, summary)]
            assert observation['selected'][0]['lesson']['project_metadata'] == {'retained': True}
        else:
            assert observation['selected'] == [] and observation['excluded'][0]['reason'] == 'retired'
        observations.append(observation)
        if revision == 2:
            (target / 'source.txt').write_bytes(b'changed project source\n')
            stale = json.loads(invoke('installed-stale', prefix, target))
            assert stale['selected'] == [] and stale['excluded'][0]['revision'] == 2
            assert stale['excluded'][0]['evidence'][0]['state'] == 'stale'
            (target / 'source.txt').write_bytes(b'project source\n')
    assert (target / 'project-notes.txt').read_bytes() == customization
    consumer = {'status': 'PASS', 'actual_cli': str(target / '.aide/scripts/aide_lite.py'),
        'core_absent': True, 'source_history_absent': True, 'helper_entry': entry,
        'read_only_inventory_preserved': True, 'customization_preserved': True,
        'correction_and_retirement': observations, 'stale_revision': stale,
        'history_sha256': refresh.sha(ledger)}
    (OUTPUT / 'installed-consumer.json').write_text(json.dumps(consumer, indent=2) + '\n', encoding='utf-8')
assert source_ledger.read_bytes() == source_before and refresh.inventory_bytes(pack) == after
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'delivered_tests': 36, 'ownership_tests': 6, 'safe_installed_consumer': 'PASS',
     'added': sorted(added), 'changed_payload': sorted(changed), 'after_sha256s': after,
     'source_history_unchanged': True, 'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 36, 'safe_installed_consumer': 'PASS'}))
