"""Qualify the two changed portable payloads using existing exporter/import owners."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-HISTORICAL-PRESENTATION-BOUNDARY-02'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def invoke(label, command, cwd=ROOT, env=None, expected=0):
    record = {'command': command, 'cwd': str(cwd), 'state': 'started'}
    receipt = OUTPUT / (label + '.json')
    def save():
        receipt.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    save()
    try:
        with (OUTPUT / (label + '.log')).open('xb') as stream:
            r = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, timeout=90)
        record.update(state='completed', exit_code=r.returncode)
        assert r.returncode == expected, label
    except BaseException as error:
        record.update(state='exception', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        save()
    return (OUTPUT / (label + '.log')).read_text(encoding='utf-8')
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
refresh = load('history_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', refresh.sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
changed = {'files/.aide/policies/commit-messages.yaml', 'files/docs/reference/commit-discipline.md'}
assert set(after) == set(old) and len(after) == 869
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
for name in changed:
    assert refresh.sha(pack / name) == refresh.sha(ROOT / name.removeprefix('files/'))
output = OUTPUT / 'delivered'
output.mkdir()
invoke('delivered-regressions', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')],
       env={**os.environ, 'AIDE_JOB_OUTPUT': str(output)})
q31 = load('history_q31', ROOT / '.aide/scripts/tests/test_q31_export_pack_governance.py')
aide = load('history_pack_cli', pack / 'files/.aide/scripts/aide_lite.py')
with tempfile.TemporaryDirectory(prefix='history-policy-consumer-') as directory:
    target = Path(directory)
    q31.init_target_git(target)
    (target / 'project-notes.txt').write_bytes(b'project customization\n')
    (target / 'AGENTS.md').write_bytes(b'Project-owned instructions.\n')
    preview = aide.apply_import_pack(pack, target, dry_run=True, mode='safe')
    assert not preview['conflicts']
    installed = aide.apply_import_pack(pack, target, mode='safe', expected_plan_digest=preview['plan_digest'])
    assert not installed['conflicts'] and installed['status'] == 'APPLIED'
    installed_agents = (target / 'AGENTS.md').read_bytes()
    assert installed_agents.startswith(b'Project-owned instructions.\n')
    assert not (target / 'core').exists()
    receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    for rel in ['.aide/scripts/aide_lite.py', '.aide/policies/commit-messages.yaml']:
        assert receipt['managed'][rel]['ownership'] == 'aide_portable_managed'
        assert receipt['managed'][rel]['installed_digest'] == refresh.sha(target / rel) == refresh.sha(ROOT / rel)
    assert not (target / '.aide/queue/AIDE-HISTORICAL-PRESENTATION-BOUNDARY-02').exists()
    assert not (target / aide.OUTCOME_LEDGER_PATH).exists()
    assert aide.historical_presentation_boundary(target) == '', 'source object must not transfer authority'
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=target, text=True, encoding='utf-8').strip()
    original = git('rev-parse', 'HEAD')
    bad = subprocess.check_output(['git', 'show', '-s', '--format=%B',
        '4bb6a4f990c5845a2141a20329168b582b37e8d8'], cwd=ROOT, text=True, encoding='utf-8')
    subprocess.run(['git', '-c', 'core.hooksPath=', 'commit', '--quiet', '--allow-empty', '-F', '-'],
                   cwd=target, input=bad, text=True, encoding='utf-8', check=True)
    malformed = git('rev-parse', 'HEAD')
    cli = [sys.executable, '-I', '-B', str(target / '.aide/scripts/aide_lite.py'), '--repo-root', str(target)]
    scope = original + '..' + malformed
    text = invoke('installed-source-boundary-refused', cli + ['commit', 'check', '--range', scope],
                  target, expected=1)
    assert 'result: FAIL' in text and 'PRESENTATION_ADVISORY' not in text
    good = (TASK / 'evidence/source-message.txt').read_text(encoding='utf-8')
    (target / 'message.txt').write_text(good, encoding='utf-8')
    text = invoke('installed-compact-check', cli + ['commit', 'check', '--message-file', 'message.txt'], target)
    assert 'result: PASS' in text
    policy = target / '.aide/policies/commit-messages.yaml'
    boundary = json.loads((TASK / 'evidence/history-before.json').read_text(encoding='utf-8'))['boundary']
    policy.write_text(policy.read_text(encoding='utf-8').replace(boundary, malformed), encoding='utf-8')
    assert aide.historical_presentation_boundary(target) == malformed
    text = invoke('installed-local-adoption', cli + ['commit', 'check', '--range', scope], target)
    assert 'result: PASS_WITH_WARNINGS' in text and 'PRESENTATION_ADVISORY' in text and 'original_failure:' in text
    invoke('installed-raw-failure', cli + ['commit', 'check', '--range', scope, '--no-dispositions'],
           target, expected=1)
    invoke('installed-latest-strict', cli + ['commit', 'check', '--latest'], target, expected=1)
    assert git('rev-parse', 'HEAD') == malformed
    assert git('show', '-s', '--format=%B', malformed).strip() == bad.strip()
    assert (target / 'AGENTS.md').read_bytes() == installed_agents
    assert (target / 'project-notes.txt').read_bytes() == b'project customization\n'
    consumer = {'installed_receipt_owned': True, 'source_history_absent': True,
                'missing_source_boundary_strict': True, 'project_adopts_own_boundary': True,
                'raw_and_latest_strict': True, 'compact_message_pass': True,
                'history_and_project_content_preserved': True}
result = {'result': 'PASS', 'after_sha256s': after, 'changed_payloads': sorted(changed),
          'consumer': consumer, 'delivered_tests': 45, 'models_requested': 0}
(OUTPUT / 'delivered-result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print('PASS: owned export, 45 delivered regressions and safe-installed historical policy')
