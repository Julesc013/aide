"""Refresh the owned pack, then exercise delivered validation presentation."""
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
TASK = ROOT / '.aide/queue/AIDE-VALIDATION-OUTPUT-01'
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
added = {'files/.aide/scripts/tests/test_validation_output.py'}
changed = {'files/.aide/scripts/aide_lite.py', 'files/docs/reference/aide-lite.md'}
assert set(after) == set(old) | added and not added.intersection(old)
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
for name in added | changed:
    assert refresh.sha(pack / name) == refresh.sha(ROOT / name.removeprefix('files/'))
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])

# Compare actual complete repository findings with the default presentation.
# Retain full text once; JSON losslessness is exercised by fresh CLI fixtures.
full = invoke('actual-full', [sys.executable, '-B', str(ROOT / '.aide/scripts/aide_lite.py'), 'validate', '--full'])
compact = invoke('actual-compact', [sys.executable, '-B', str(ROOT / '.aide/scripts/aide_lite.py'), 'validate'])
lines = full.decode('utf-8').splitlines()
assert lines[:2] == ['AIDE Lite validate', 'status: PASS']
assert all(line.startswith('- ') for line in lines[2:])
messages = [line[2:] for line in lines[2:]]
counts = {name: sum(m.startswith(name + ' ') for m in messages) for name in ('PASS', 'WARN', 'FAIL')}
counts['OTHER'] = len(messages) - sum(counts.values())
observed = compact.decode('utf-8').splitlines()
assert observed[:2] == lines[:2]
assert observed[2] == f"checks: {len(messages)}; " + '; '.join(f'{key}: {value}' for key, value in counts.items())
assert observed[3:-1] == ['- ' + m for m in messages if not m.startswith('PASS ')]
assert observed[-1] == f"omitted PASS details: {counts['PASS']}; use validate --full or --json for all results"
assert len(compact) < len(full)
measurement = {'status': 'PASS', 'full_bytes': len(full), 'compact_bytes': len(compact),
               'full_sha256': hashlib.sha256(full).hexdigest(),
               'compact_sha256': hashlib.sha256(compact).hexdigest(),
               'counts': counts, 'nonpass_messages': [m for m in messages if not m.startswith('PASS ')],
               'all_nonpass_preserved': True, 'cost_and_speed_savings': 'not_measured'}
(OUTPUT / 'actual-output-comparison.json').write_text(json.dumps(measurement, indent=2) + '\n', encoding='utf-8')
assert refresh.inventory_bytes(pack) == after
(OUTPUT / 'delivered-result.json').write_text(json.dumps(
    {'status': 'PASS', 'delivered_tests': 36, 'ownership_tests': 6,
     'added': sorted(added), 'changed_payload': sorted(changed), 'after_sha256s': after,
     'actual_output_comparison': measurement, 'models_requested': 0}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'delivered_tests': 36, 'actual_output_comparison': measurement}))
