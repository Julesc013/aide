"""Verify and preserve the completed dev synchronization without repeating effects."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path

TASK = Path(__file__).parent
E = TASK / 'evidence'
ROOT = TASK.parents[2]
spec = importlib.util.spec_from_file_location('sync_collection', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
folder = E / 'revised-dev-attempt-01.log'
raw = (folder / 'result.json').read_bytes()
result = json.loads(raw)
assert result['status'] == 'PASS'
assert result['commit'] == '03929beb3c7278975f9c0b3b1378712aeca2ac91'
assert result['tree'] == 'e03bc5ef66394dd91d09725acd841e7bc57b4d92'
assert result['refs'] == {'dev': result['commit'], 'main': 'ed4a90046eba12a717a9962f21523285667a669b'}
streams = {}
for operation in result['operations']:
    assert operation['state'] == 'completed' and operation['exit_code'] == 0
    for name, expected in operation['streams'].items():
        data = (folder / name).read_bytes()
        assert len(data) == expected['bytes'] and hashlib.sha256(data).hexdigest() == expected['sha256']
        assert name not in streams
        streams[name] = base64.b64encode(data).decode('ascii')
files = {p.name: base64.b64encode(p.read_bytes()).decode('ascii') for p in folder.iterdir() if p.is_file()}
assert set(files) == set(streams) | {'result.json'}
h.save(E / 'revised-dev-retained.json', h.bundle(json.dumps(files, sort_keys=True, separators=(',', ':')).encode(), files=len(files)))
h.save(E / 'revised-dev-completed.json', result)
summary = {'status': 'PASS_VERIFIED_DEV_SYNC', 'commit': result['commit'], 'tree': result['tree'],
           'refs': result['refs'], 'operations': len(result['operations']), 'streams': len(streams),
           'complete_receipt_sha256': hashlib.sha256(raw).hexdigest(),
           'preview_sha256s': result['preview_sha256s'], 'model_requests': 0,
           'scope': 'Dev checkpoint only; revised consumer/profile/replay, main promotion and publication remain open.'}
h.save(E / 'revised-dev-verified.json', summary)
print(json.dumps(summary))
