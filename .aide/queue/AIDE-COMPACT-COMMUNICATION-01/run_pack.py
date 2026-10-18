"""Qualify delivered communication and task briefs through the existing exporter."""
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
TASK = ROOT / '.aide/queue/AIDE-COMPACT-COMMUNICATION-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def invoke(label, command, cwd=ROOT, env=None):
    stdout, stderr = OUTPUT / (label + '.stdout'), OUTPUT / (label + '.stderr')
    receipt = OUTPUT / (label + '.invocation.json')
    record = {'command': command, 'cwd': str(cwd), 'state': 'started', 'exit_code': None}
    def save():
        receipt.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    save()
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, timeout=90, env=env)
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


refresh = load('communication_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', refresh.sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
added = {'files/.aide/scripts/tests/test_task_brief.py',
         'files/.aide/scripts/tests/test_compact_communication.py'}
changed = {'files/.aide/scripts/aide_lite.py',
           'files/.aide/scripts/tests/test_q27_commit_recovery.py',
           'files/.aide/policies/commit-messages.yaml', 'files/.aide/git/commit-template.md',
           'files/.aide/reports/aide-commit-message-standard.md',
           'files/docs/reference/commit-discipline.md', 'files/docs/reference/changelog-preview.md'}
assert set(after) == set(old) | added and not added.intersection(old)
assert len(after) == 869
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
assert 'files/.aide/controller/outcome-ledger.jsonl' not in after
for name in added | changed:
    assert refresh.sha(pack / name) == refresh.sha(ROOT / name.removeprefix('files/'))
for label, script, count in [('communication', TASK / 'run_checks.py', 71),
    ('brief', ROOT / '.aide/queue/AIDE-TASK-DEVELOPMENT-BRIEF-01/run_checks.py', 84)]:
    output = OUTPUT / label
    output.mkdir()
    invoke(label + '-delivered-tests', [sys.executable, '-B', str(script), str(pack / 'files')],
           env={**os.environ, 'AIDE_JOB_OUTPUT': str(output)})
    result = json.loads((output / 'delivered-tests.json').read_bytes())
    assert result['tests_run'] == count and not result['failures'] and not result['errors'] and not result['skips']

q31 = load('communication_q31', ROOT / '.aide/scripts/tests/test_q31_export_pack_governance.py')
aide = load('communication_delivered_cli', pack / 'files/.aide/scripts/aide_lite.py')
with tempfile.TemporaryDirectory(prefix='communication-consumer-') as directory:
    target = Path(directory)
    q31.init_target_git(target)
    (target / 'project-notes.txt').write_bytes(b'project customization\n')
    (target / 'AGENTS.md').write_bytes(b'Project-owned instructions.\n')
    preview = aide.apply_import_pack(pack, target, dry_run=True, mode='safe')
    assert not preview['conflicts'], preview['conflicts']
    installed = aide.apply_import_pack(pack, target, mode='safe', expected_plan_digest=preview['plan_digest'])
    assert not installed['conflicts'] and installed['status'] == 'APPLIED'
    assert not (target / 'core').exists()
    receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    assert receipt['mode'] == 'safe'
    for rel in ['.aide/scripts/aide_lite.py', '.aide/git/commit-template.md', '.aide/policies/commit-messages.yaml']:
        assert receipt['managed'][rel]['ownership'] == 'aide_portable_managed'
        assert receipt['managed'][rel]['installed_digest'] == refresh.sha(target / rel) == refresh.sha(ROOT / rel)
    assert not (target / aide.OUTCOME_LEDGER_PATH).exists(), 'source history leaked'
    assert not (target / '.aide/queue/AIDE-COMPACT-COMMUNICATION-01').exists()
    cli = [sys.executable, '-I', '-B', str(target / '.aide/scripts/aide_lite.py'), '--repo-root', str(target)]
    def write(relative, text):
        p = target / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8', newline='\n')
        return p
    message = ('fix(consumer): preserve the project result\n\n'
        'Keep the accepted project behavior discoverable across sessions.\n\n'
        'Validation: PASS - focused fixture\n NOT RUN - native device operation\n'
        'Changelog: Fixed: Preserve the accepted project result\n'
        'AIDE-Task: PROJECT-01\nAIDE-Format: compact-v1\n')
    message_path = write('message.txt', message)
    snapshot = refresh.inventory_bytes(target)
    checked = invoke('installed-message-check', cli + ['commit', 'check', '--message-file', 'message.txt'], target)
    template = invoke('installed-template', cli + ['commit', 'template'], target)
    assert b'result: PASS' in checked and b'AIDE-Format: compact-v1' in template and b'## Summary' not in template
    assert refresh.inventory_bytes(target) == snapshot
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=target, text=True, encoding='utf-8').strip()
    oids = []
    for index, msg in enumerate([aide.COMMIT_GOOD_EXAMPLE, message,
                                aide.COMMIT_GOOD_EXAMPLE.replace('- Added:', '- Unknown:')]):
        write('project-result.txt', str(index) + '\n')
        message_path.write_text(msg, encoding='utf-8', newline='\n')
        git('add', 'project-result.txt')
        git('commit', '-q', '-F', str(message_path))
        oids.append(git('rev-parse', 'HEAD'))
    installed_module = load('communication_installed_cli', target / '.aide/scripts/aide_lite.py')
    history = installed_module.make_changelog_preview(target, limit=3)
    assert history['commit_count'] == 3 and history['malformed_count'] == 1
    assert history['malformed_commits'][0]['commit_sha'] == oids[2]
    fixed = [x for x in history['categories']['Fixed'] if x['commit_sha'] == oids[1]]
    assert len(fixed) == 1 and 'NOT RUN - native device operation' in fixed[0]['validation']
    assert not history['release_publishing']
    (OUTPUT / 'installed-mixed-history.json').write_text(json.dumps(history, indent=2) + '\n', encoding='utf-8')

    # Target owns every task, quality and lesson fact; compare existing readers.
    task, source = 'PROJECT-BRIEF-01', 'src/repair.py'
    write('.aide/queue/' + task + '/task.yaml', f'id: {task}\ntitle: Repair the consumer\nowner: project-owner\n')
    write('.aide/queue/' + task + '/status.yaml', f'task_id: {task}\nstatus: running\nnext_action: review_candidate\n')
    write(source, 'project evidence\n')
    quality = {'schema_version': 'aide.file-quality-ledger.v0', 'source_commit': git('rev-parse', 'HEAD'),
        'records': [{'path': source, 'owner': 'project-module', 'kind': 'source', 'status': 'active',
        'quality_level': 'documented', 'recommended_next_action': 'inspect existing tests',
        'docs_refs': ['docs/contract.md'], 'test_refs': ['tests/test_consumer.py'],
        'dependency_refs': [], 'warnings': [], 'exemptions': []}]}
    quality_path = write(aide.FILE_QUALITY_LEDGER_JSON_PATH, json.dumps(quality))
    lesson = {'schema_version': 'aide.outcome-lesson.v1', 'id': 'project-oracle', 'revision': 1,
        'state': 'active', 'summary': 'Preserve the independent consumer check.', 'applies_to': [source],
        'supersedes': None, 'required_features': ['advisory_only', 'revision_chain', 'source_sha256'],
        'evidence': [{'path': source, 'sha256': refresh.sha(target / source)}]}
    ledger = write(aide.OUTCOME_LEDGER_PATH, json.dumps({'run_id': 'project-review', 'phase': 'review',
                   'source': 'project-owner', 'result': 'PASS', 'lesson': lesson}) + '\n')
    snapshot = refresh.inventory_bytes(target)
    brief = json.loads(invoke('installed-brief', cli + ['task', 'brief', '--task-id', task, '--path', source, '--json'], target))
    for field, args in [('continuation', ['task', 'resume-plan', '--task-id', task, '--json']),
                        ('quality', ['quality', 'explain-file', source, '--json']),
                        ('lessons', ['outcome', 'lessons', '--path', source, '--json'])]:
        assert brief[field] == json.loads(invoke('installed-' + field, cli + args, target))
    assert brief['result'] == 'OBSERVED' and brief['quality']['owner'] == 'project-module'
    assert brief['quality']['freshness'] == 'unverified' and not brief['execution_admitted'] and not brief['acceptance_verified']
    assert brief['lessons']['selected'][0]['lesson'] == lesson
    assert refresh.inventory_bytes(target) == snapshot
    # Missing/malformed auxiliary data stays explicit; inspect via installed reader.
    quality_path.unlink()
    missing = installed_module.build_task_development_brief(target, task, source)
    assert missing['result'] == 'PARTIAL' and missing['quality']['coverage'] == 'unindexed'
    quality_path.write_text('{broken', encoding='utf-8')
    snapshot = refresh.inventory_bytes(target)
    malformed = installed_module.build_task_development_brief(target, task, source)
    assert malformed['result'] == 'PARTIAL' and malformed['quality']['result'] == 'INVALID'
    assert len(malformed['lessons']['selected']) == 1
    assert refresh.inventory_bytes(target) == snapshot
    assert (target / 'project-notes.txt').read_bytes() == b'project customization\n'
    assert (target / 'AGENTS.md').read_bytes().startswith(b'Project-owned instructions.\n')
    consumer = {'status': 'PASS', 'core_absent': True, 'source_history_absent': True,
        'customization_preserved': True, 'read_only_commands_unchanged': True,
        'brief': brief, 'missing': missing, 'malformed': malformed,
        'message_check': checked.decode(), 'template': template.decode(), 'history_oids': oids}
    (OUTPUT / 'installed-consumer.json').write_text(json.dumps(consumer, indent=2) + '\n', encoding='utf-8')
assert refresh.inventory_bytes(pack) == after
(OUTPUT / 'delivered-result.json').write_text(json.dumps({'status': 'PASS',
    'communication_tests': 71, 'brief_tests': 84, 'ownership_tests': 6,
    'safe_installed_consumer': 'PASS', 'added': sorted(added), 'changed_payload': sorted(changed),
    'after_sha256s': after, 'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 155, 'safe_installed_consumer': 'PASS'}))



