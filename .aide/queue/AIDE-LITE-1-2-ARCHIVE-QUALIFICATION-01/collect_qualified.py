"""Preserve completed dev/main integration; never repeat its effects."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    h = load('qualified_integration_preservation', TASK / 'collect_hosted.py')
    verify = load('qualified_integration_roundtrip', TASK / 'verify_profile_collection.py')
    folder = E / 'qualified-integration-attempt-01.log'
    raw = (folder / 'result.json').read_bytes()
    result = json.loads(raw)
    assert result['status'] == 'PASS'
    assert result['commit'] == '3fec7ac375da0e17f035336e080d75ebd26a9920'
    assert result['tree'] == 'd6a066e80533a37a12ce15883889aded3e0caa8c'
    assert result['refs'] == {'dev': result['commit'], 'main': result['commit']}
    streams = {}
    for operation in result['operations']:
        assert operation['state'] == 'completed' and operation['exit_code'] == 0
        for name, expected in operation['streams'].items():
            data = (folder / name).read_bytes()
            assert len(data) == expected['bytes'] and hashlib.sha256(data).hexdigest() == expected['sha256']
            assert name not in streams
            streams[name] = base64.b64encode(data).decode()
    files = {p.name: base64.b64encode(p.read_bytes()).decode() for p in folder.iterdir() if p.is_file()}
    assert set(files) == set(streams) | {'result.json'}
    path = E / 'qualified-integration-retained.json'
    h.preserve(path, files)
    assert verify.restore(path) == {n: base64.b64decode(v) for n, v in files.items()}
    plan = json.loads((E / 'qualified-integration-effect.json').read_bytes())
    assert all(h.sha(ROOT / n) == value for n, value in plan['stable_assets'].items())
    assert all(h.sha(ROOT / n) == value for n, value in plan['canonical_preimages'].items())
    h.h.save(E / 'qualified-integration-completed.json', result)
    summary = {'status': 'PASS_VERIFIED_DEV_MAIN_SYNC', 'commit': result['commit'], 'tree': result['tree'],
        'refs': result['refs'], 'operations': len(result['operations']), 'streams': len(streams),
        'complete_receipt_sha256': hashlib.sha256(raw).hexdigest(), 'retained_sha256': h.sha(path),
        'lossless_roundtrip_verified': True, 'preview_sha256s': result['preview_sha256s'],
        'new_jobs': 0, 'model_requests': 0, 'scope': 'Accepted candidate and evidence integrated; support activation, publication and acquired-download acceptance remain separate.'}
    h.h.save(E / 'qualified-integration-verified.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
