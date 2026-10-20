"""Preserve branch admission without replaying any Git effect."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path

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
    helpers = load('publication_preserve', OLD / 'collect_hosted.py')
    helpers.E = E
    verify = load('publication_restore', OLD / 'verify_profile_collection.py')
    verify.E = E
    record = json.loads((E / 'admission-execution.log').read_bytes())
    assert record['state'] == 'admitted_branch_created'
    assert record['base'] == '3fec7ac375da0e17f035336e080d75ebd26a9920'
    files = {'admission-execution.log': (E / 'admission-execution.log').read_bytes()}
    for row in record['operations']:
        assert row['state'] == 'completed' and row['exit_code'] == 0
        for name, identity in row['streams'].items():
            raw = (E / 'admission-streams.log' / name).read_bytes()
            assert len(raw) == identity['bytes'] and hashlib.sha256(raw).hexdigest() == identity['sha256']
            assert name not in files
            files[name] = raw
    assert len(record['operations']) == 20 and len(files) == 41
    target = E / 'admission-retained.json'
    helpers.preserve(target, {n: base64.b64encode(raw).decode('ascii') for n, raw in files.items()})
    assert verify.restore(target) == files
    summary = {'state': 'PASS_BRANCH_ADMISSION', 'base': record['base'],
        'task_branch': record['task_branch'], 'operations': 20, 'streams': 40,
        'receipt_sha256': helpers.sha(E / 'admission-execution.log'),
        'retained_sha256': helpers.sha(target), 'lossless_roundtrip_verified': True,
        'commit_push_tag_publication_download_job': 'none'}
    helpers.h.save(E / 'admission-verified.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
