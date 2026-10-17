"""Close the affected development pack through the existing owned exporter."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LOCAL-DEPENDENCY-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
TMP = Path(os.environ['AIDE_JOB_TMP'])
assert TMP.parent == OUTPUT.parent and Path(os.environ['TEMP']) == TMP
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip()


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


refresh = load('dependency_pack_refresh', '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()

pack = ROOT / refresh.PACK_REL
payload = pack / 'files'
state_rel = Path('core/runtime/continuous_worker/state.py')
assert (payload / state_rel).read_bytes() == (ROOT / state_rel).read_bytes()
for relative in ('.aide/scripts/tests/test_dependency_requests.py',
                 '.aide/scripts/tests/test_continuous_worker_requests.py',
                 'core/runtime/continuous_worker/requests.py',
                 'core/runtime/continuous_worker/__main__.py'):
    assert not (payload / relative).exists(), relative

# A fresh isolated interpreter must import actual delivered bytes, never source.
consumer = TMP / 'delivered_state_check.py'
consumer.write_text('''import sqlite3, sys
from pathlib import Path
payload, root = map(Path, sys.argv[1:])
sys.path.insert(0, str(payload))
from core.runtime.continuous_worker import state
assert Path(state.__file__).resolve() == (payload / "core/runtime/continuous_worker/state.py").resolve()
writer = state.State(root)
try:
    writer.bind({"tasks": [{"id": "consumer", "depends_on": []}]})
    before = writer.status()
finally:
    writer.close()
reader = state.State(root, read_only=True)
try:
    assert reader.status() == before
    try:
        reader.event(None, "forbidden", {})
    except sqlite3.OperationalError:
        pass
    else:
        raise AssertionError("read-only delivered State allowed mutation")
finally:
    reader.close()
writer = state.State(root)
try:
    assert writer.status() == before
    assert writer.claim(1)["task"] == "consumer"
finally:
    writer.close()
print("PASS delivered State initialization, read-only refusal, reopening and claim")
''', encoding='utf-8')
result = {'status': 'INCOMPLETE', 'source_only_exclusion': 'PASS',
          'exported_state_sha256': refresh.sha(payload / state_rel),
          'live_deliveries': 0, 'model_calls': 0, 'operations': {}}
changelog = ROOT / '.aide/changelog'
generated = {'CHANGELOG.preview.md', 'RELEASE_NOTES.preview.md', 'changelog.preview.json',
             'latest-changelog-report.md', 'malformed-commits.md', 'release-notes.preview.json'}
before = refresh.inventory_bytes(changelog)
try:
    commands = [('delivered-state', [sys.executable, '-I', '-B', str(consumer), str(payload), str(TMP / 'state')])]
    for label, args in (
        ('changelog-preview', ['changelog', 'preview', '--range',
                              '9605d8e333a1da8f113a2a1b44f88427511fbba2..HEAD', '--limit', '100']),
        ('changelog-validate', ['changelog', 'validate']),
        ('changelog-status', ['changelog', 'status']),
    ):
        commands.append((label, [sys.executable, '-B', str(ROOT / '.aide/scripts/aide_lite.py'), *args]))
    for label, command in commands:
        observed = refresh.invoke(label, command, OUTPUT)
        result['operations'][label] = observed
        assert observed['exit_code'] == 0, label
    after = refresh.inventory_bytes(changelog)
    assert set(after) == set(before)
    assert all(after[name] == value for name, value in before.items() if name not in generated)
    result['status'] = 'PASS'
finally:
    (OUTPUT / 'closure.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps({'status': result['status'], 'scope': 'development pack closure'}), flush=True)
