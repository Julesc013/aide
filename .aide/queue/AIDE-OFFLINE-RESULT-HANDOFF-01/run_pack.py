"""Owned pack refresh and a real installed offline request/result exchange."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile
from pathlib import Path

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-OFFLINE-RESULT-HANDOFF-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def invoke(label, command, cwd=ROOT, expected=0):
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
        record['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                             for p in (stdout, stderr) if p.exists()}
        save()
    assert result.returncode == expected, label + ' failed; original output retained'
    return stdout.read_bytes()

assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
release_before = json.loads((TASK / 'evidence/release-preimages.json').read_text(encoding='utf-8'))
assert all(sha(ROOT / p) == h for p, h in release_before.items())
refresh = load('offline_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
changed = {'files/.aide/scripts/aide_lite.py', 'files/.aide/scripts/task_handoff.py',
           'files/.aide/scripts/tests/test_task_handoff.py',
           'files/docs/reference/task-os-report-only-commands.md'}
assert set(after) == set(old)
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
source_cli = load('offline_source_projection', ROOT / '.aide/scripts/aide_lite.py')
for name in changed:
    source = ROOT / name.removeprefix('files/')
    expected = (source_cli.portable_cli_text(source.read_text(encoding='utf-8')).encode('utf-8')
                if name == 'files/.aide/scripts/aide_lite.py' else source.read_bytes())
    assert (pack / name).read_bytes() == expected
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])
q31 = load('offline_q31', ROOT / '.aide/scripts/tests/test_q31_export_pack_governance.py')
aide = load('offline_delivered_cli', pack / 'files/.aide/scripts/aide_lite.py')
codec = aide.task_handoff_codec()
with tempfile.TemporaryDirectory(prefix='offline-consumer-') as directory:
    outer = Path(directory)
    sender, receiver = outer / 'sender', outer / 'receiver'
    sender.mkdir(); receiver.mkdir()
    q31.init_target_git(sender)
    (sender / 'AGENTS.md').write_text('Project-owned working rules; preserve.\n', encoding='utf-8')
    (sender / 'notes.txt').write_bytes(b'Project customization remains.\r\n')
    manual = {p: (sender / p).read_bytes() for p in ['AGENTS.md', 'notes.txt']}
    preview = aide.apply_import_pack(pack, sender, dry_run=True, mode='safe')
    assert not preview['conflicts']
    installed = aide.apply_import_pack(pack, sender, mode='safe', expected_plan_digest=preview['plan_digest'])
    assert installed['status'] == 'APPLIED' and not installed['conflicts']
    assert not (sender / 'core').exists()
    for name, raw in manual.items():
        assert raw in (sender / name).read_bytes()
    receipt = json.loads((sender / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    helper = '.aide/scripts/task_handoff.py'
    assert receipt['managed'][helper]['installed_digest'] == sha(sender / helper) == sha(ROOT / helper)
    assert receipt['managed'][helper]['ownership'] == 'aide_portable_managed'
    identity = 'OFFLINE-CONSUMER-01'
    task_dir = sender / '.aide/queue' / identity
    task_dir.mkdir(parents=True)
    (task_dir / 'task.yaml').write_text('id: ' + identity + '\ntitle: Repair arithmetic\n', encoding='utf-8')
    (task_dir / 'status.yaml').write_text('status: interrupted\nresult: INCOMPLETE\n', encoding='utf-8')
    (task_dir / 'ExecPlan.md').write_text('Preserve failed work; verify before accepting.\n', encoding='utf-8')
    (sender / 'arithmetic.py').write_bytes(b'def add(a, b):\n    return a - b\n')
    cli = sender / '.aide/scripts/aide_lite.py'
    prefix = [sys.executable, '-I', str(cli)]
    def handoff(label, target, args, expected=0):
        return invoke(label, prefix + ['--repo-root', str(target), 'task', 'handoff', *args],
                      target, expected)
    request = handoff('installed-request', sender, ['export', '--task-id', identity,
                                                   '--input', 'arithmetic.py', '--input', 'notes.txt'])
    request_sha = hashlib.sha256(request).hexdigest()
    decoded = codec.decode(request, request_sha)
    (sender / 'request.json').write_bytes(request)
    (receiver / 'request.json').write_bytes(request)
    # This fixture copies only its known input, not arbitrary archive paths.
    (receiver / 'arithmetic.py').write_bytes(decoded['inputs']['arithmetic.py']['text'].encode('utf-8'))
    repaired = b'def add(a, b):\n    return a + b\n'
    (receiver / 'arithmetic.py').write_bytes(repaired)
    (receiver / 'report.txt').write_text('Repair written; interrupted before independent checks.\n', encoding='utf-8')
    (receiver / 'candidate.patch').write_bytes(b'-    return a - b\n+    return a + b\n')
    first = handoff('installed-partial', receiver, ['result-export', '--request', 'request.json',
        '--request-sha256', request_sha, '--attempt-id', 'attempt-1', '--outcome', 'interrupted',
        '--report', 'report.txt', '--patch', 'candidate.patch'])
    (sender / 'partial.json').write_bytes(first)
    def inspect(label, result_name, data, expected=0):
        return handoff(label, sender, ['result-inspect', '--request', 'request.json',
            '--request-sha256', request_sha, '--result', result_name,
            '--result-sha256', hashlib.sha256(data).hexdigest(), '--json'], expected)
    initial = json.loads(inspect('installed-partial-inspect', 'partial.json', first))
    assert initial['recorded_outcome'] == 'interrupted' and not initial['accepted']
    assert initial['selected_input_state'] == 'matching'
    before_resume = sha(receiver / 'arithmetic.py')
    oracle = "from arithmetic import add\nassert add(2,3)==5\nassert add(-4,1)==-3\nassert add(0,0)==0\n"
    (receiver / 'check.py').write_text(oracle, encoding='utf-8')
    invoke('independent-repair-check', [sys.executable, '-B', str(receiver / 'check.py')], receiver)
    assert sha(receiver / 'arithmetic.py') == before_resume
    (receiver / 'checks.json').write_text('{"result":"PASS","cases":3,"scope":"selected arithmetic behavior"}\n', encoding='utf-8')
    (receiver / 'report.txt').write_text('Existing repair verified; no repeated edit. Candidate only.\n', encoding='utf-8')
    second = handoff('installed-complete', receiver, ['result-export', '--request', 'request.json',
        '--request-sha256', request_sha, '--attempt-id', 'attempt-2', '--outcome', 'submitted',
        '--report', 'report.txt', '--patch', 'candidate.patch', '--checks', 'checks.json'])
    (sender / 'result.json').write_bytes(second)
    stable = refresh.inventory_bytes(sender)
    accepted = json.loads(inspect('installed-result-inspect', 'result.json', second))
    replay = json.loads(inspect('installed-result-replay', 'result.json', second))
    assert accepted == replay and accepted['selected_input_state'] == 'matching'
    assert accepted['recorded_outcome'] == 'submitted' and not accepted['accepted']
    assert refresh.inventory_bytes(sender) == stable
    assert (sender / 'partial.json').read_bytes() == first
    assert (sender / 'arithmetic.py').read_bytes() != repaired
    original = (sender / 'arithmetic.py').read_bytes()
    (sender / 'arithmetic.py').write_bytes(b'concurrent sender change\n')
    stale = json.loads(inspect('installed-stale-base', 'result.json', second))
    assert stale['selected_input_state'] == 'changed' and stale['safe_to_apply'] is None
    (sender / 'truncated.json').write_bytes(second[:-8])
    inspect('installed-truncated', 'truncated.json', second, expected=1)
    (sender / 'arithmetic.py').write_bytes(original)
    for name, raw in manual.items():
        assert raw in (sender / name).read_bytes()
    consumer = {'status':'PASS','source_task':identity,'request_sha256':request_sha,
        'partial_result_sha256':hashlib.sha256(first).hexdigest(),
        'result_sha256':hashlib.sha256(second).hexdigest(),'source_repair_tests':3,
        'partial_preserved':True,'continuation_without_repeated_edit':True,
        'read_only_replay':True,'changed_base_detected':True,'truncation_refused':True,
        'customization_preserved':True,'core_absent':True,'auto_apply_or_accept':False,
        'helper_receipt':receipt['managed'][helper]}
    (OUTPUT / 'installed-consumer.json').write_text(json.dumps(consumer,indent=2)+'\n',encoding='utf-8')

    real_task = 'AIDE-MINI-WORKER-01'
    source_paths = [f'.aide/queue/{real_task}/{name}' for name in ['task.yaml','status.yaml','ExecPlan.md','REPORT.md']]
    source_paths += [f'.aide/queue/{real_task}/evidence/attempt-03-fixture-result.json','docs/reference/mini-worker.md']
    real_before = {p:sha(ROOT/p) for p in source_paths}
    real_request = handoff('real-request', ROOT, ['export','--task-id',real_task,'--input','docs/reference/mini-worker.md'])
    (receiver/'real-request.json').write_bytes(real_request)
    (receiver/'real-report.txt').write_bytes((ROOT/source_paths[3]).read_bytes())
    (receiver/'real-checks.json').write_bytes((ROOT/source_paths[4]).read_bytes())
    real_sha = hashlib.sha256(real_request).hexdigest()
    real_result = handoff('real-result',receiver,['result-export','--request','real-request.json',
        '--request-sha256',real_sha,'--attempt-id','fixture-record-transfer-1','--outcome','submitted',
        '--report','real-report.txt','--checks','real-checks.json'])
    (sender/'real-request.json').write_bytes(real_request)
    (sender/'real-result.json').write_bytes(real_result)
    for p in source_paths[:3]+['docs/reference/mini-worker.md']:
        dest=sender/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/p).read_bytes())
    real_observed=json.loads(handoff('real-inspect',sender,['result-inspect','--request','real-request.json',
        '--request-sha256',real_sha,'--result','real-result.json',
        '--result-sha256',hashlib.sha256(real_result).hexdigest(),'--json']))
    assert real_observed['selected_input_state']=='matching' and not real_observed['accepted']
    assert real_observed['captured_result']['artifacts']['report']['text'].encode('utf-8')==(ROOT/source_paths[3]).read_bytes()
    assert all(sha(ROOT/p)==h for p,h in real_before.items())
    assert not (sender / 'core').exists()
    (OUTPUT/'real-record-consumer.json').write_text(json.dumps({'result':'PASS','task':real_task,
        'source_sha256s':real_before,'source_records_unchanged':True,
        'request_sha256':real_sha,'result_sha256':hashlib.sha256(real_result).hexdigest(),
        'existing_evidence_transferred_not_requalified':True},indent=2)+'\n',encoding='utf-8')
assert all(sha(ROOT / p) == h for p, h in release_before.items())
assert refresh.inventory_bytes(pack)==after
(OUTPUT/'delivered-result.json').write_text(json.dumps({'status':'PASS','delivered_tests':97,
    'safe_installed_consumer':'PASS','real_record_consumer':'PASS','changed_payload':sorted(changed),
    'pack_members':len(after),'pack_sha256s':after,'models_requested':0},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','delivered_tests':97,'safe_installed_consumer':'PASS'}))
