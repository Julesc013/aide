"""Collect complete effect receipts through existing chunk/roundtrip owners."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
OLD = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    assert len(sys.argv) == 2 and sys.argv[1] in ('publication', 'consumer', 'closure')
    stage = sys.argv[1]
    helpers = load('effect_preserve', OLD / 'collect_hosted.py')
    verify = load('effect_restore', OLD / 'verify_profile_collection.py')
    helpers.E = verify.E = E
    files = {}
    operations = streams = 0

    def add(path, key):
        assert key not in files
        files[key] = path.read_bytes()

    checkpoint = E / (({'publication': 'recovery', 'consumer': 'consumer', 'closure': 'closure'}[stage]) + '-checkpoint-attempt-01.log')
    receipt = json.loads((checkpoint / 'result.json').read_bytes())
    assert receipt['status'] == 'PASS'
    for row in receipt['operations']:
        assert row['state'] == 'completed' and row['exit_code'] == 0
        operations += 1
        for name, expected in row['streams'].items():
            path = checkpoint / name
            assert path.stat().st_size == expected['bytes'] and helpers.sha(path) == expected['sha256']
            add(path, checkpoint.name + '/' + name)
            streams += 1
    add(checkpoint / 'result.json', checkpoint.name + '/result.json')
    if stage == 'publication':
        path = E / 'delivery-recovery-result.log'
        delivery = json.loads(path.read_bytes())
        assert delivery['status'] == 'PUBLISHED_ACQUIRED_CONSUMER_PENDING'
        assert delivery['published']['tag_name'] == 'aide-lite-v1.2.0' and not delivery['published']['draft']
        for row in delivery['operations']:
            assert row['status'] == 'COMPLETED' and row['exit_code'] == 0
            operations += 1
            for name, expected in row['streams'].items():
                path = E / name
                assert path.stat().st_size == expected['bytes'] and helpers.sha(path) == expected['sha256']
                add(path, name)
                streams += 1
        add(E / 'delivery-recovery-result.log', 'delivery-recovery-result.log')
        acquisition = ROOT / '.aide/release/acquired-aide-lite-v1.2.0.log/acquisition.json'
        assert helpers.sha(acquisition) == delivery['acquisition_receipt_sha256']
        add(acquisition, 'acquisition.json')
        helpers.h.save(E / 'published-acquired.json', {'state': delivery['status'],
            'release': delivery['published'], 'tag_commit': delivery['release_target'], 'execution_source': delivery['commit'], 'tag_object': delivery['tag_object'],
            'assets': delivery['acquired'], 'acquisition_receipt_sha256': delivery['acquisition_receipt_sha256'],
            'consumer_acceptance': 'pending', 'support_activation': delivery['support_activation']})
    if stage == 'consumer':
        path = E / 'acquired-execution.log'
        terminal = json.loads(path.read_bytes())
        assert terminal['state'] == 'acquired_original_consumer_pass'
        job = terminal['job_result']
        assert job['phase'] == 'retired' and job['scratch_absent'] and job['reservation_released']
        assert job['result']['quiescent'] and job['result']['exit_code'] == 0
        from core.execution import managed_workspace as workspace
        retained = Path(job['retained'])
        for name, expected in job['collected_manifest'].items():
            assert workspace.content_digest(retained / name) == expected
        for path in sorted(retained.rglob('*')):
            if path.is_file():
                add(path, 'retained/' + path.relative_to(retained).as_posix())
        add(E / 'acquired-execution.log', 'acquired-execution.log')
        helpers.h.save(E / 'acquired-job-retired.json', job)
    target = E / (stage + '-effects-retained.json')
    helpers.preserve(target, {name: base64.b64encode(raw).decode('ascii') for name, raw in files.items()})
    assert verify.restore(target) == files
    result = {'state': 'PASS_LOSSLESS_' + stage.upper(), 'operations': operations, 'streams': streams,
        'files': len(files), 'retained_sha256': helpers.sha(target), 'lossless_roundtrip_verified': True,
        'new_effects': 0, 'model_requests': 0}
    helpers.h.save(E / (stage + '-effects-verified.json'), result)
    print(json.dumps(result))


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT))
    main()
