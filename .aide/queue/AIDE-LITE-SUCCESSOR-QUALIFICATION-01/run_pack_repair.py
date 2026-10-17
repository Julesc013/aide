"""Refresh the owned development pack and verify its exact accounting projection."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
OUT = Path(os.environ['AIDE_JOB_OUTPUT'])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def release_inventory():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}

def main():
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    spec = importlib.util.spec_from_file_location('effort_pack_owner',
        ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
    refresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(refresh)
    inventory = TASK / 'evidence/pack-before-effort-repair.json'
    before = json.loads(inventory.read_text(encoding='utf-8'))
    release_before = release_inventory()
    sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
                '--inventory-sha256', sha(inventory)]
    refresh.main()
    pack = ROOT / refresh.PACK_REL
    after = refresh.inventory_bytes(pack)
    old = {name: value['sha256'] for name, value in before['files'].items()}
    added = {'files/.aide/scripts/aide_work_effort.py'}
    assert set(after) - set(old) == added and not set(old) - set(after)
    changed = {name for name in old if old[name] != after[name]} | added
    payload = added | {'files/.aide/scripts/aide_lite.py',
        'files/.aide/scripts/tests/test_work_effort.py',
        'files/.aide/scripts/tests/test_export_import.py',
        'files/.aide/scripts/tests/test_aide_lite.py',
        'files/docs/reference/aide-lite-test-runner.md'}
    assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
    for name in payload - added - {'files/.aide/scripts/aide_lite.py'}:
        assert sha(pack / name) == sha(ROOT / name.removeprefix('files/'))
    assert (pack / next(iter(added))).read_text(encoding='utf-8') == (
        ROOT / 'core/execution/work_effort.py').read_text(encoding='utf-8')
    delta = {'changed_paths': sorted(changed), 'after_sha256s': after,
             'release_before': release_before, 'delivered_tests': 'NOT_RUN'}
    (OUT / 'pack-repair-delta.json').write_text(json.dumps(delta, indent=2) + '\n', encoding='utf-8', newline='\n')
    # Run the same selected behavioral checks against delivered modules in a
    # separate process. Their export fixtures also exercise idempotent projection.
    bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; runpy.run_path(sys.argv[1],run_name='__main__')"
    with (OUT / 'delivered.stdout').open('xb') as out, (OUT / 'delivered.stderr').open('xb') as err:
        result = subprocess.run([sys.executable, '-B', '-c', bootstrap,
            str(TASK / 'run_effort_repair.py')], cwd=pack / 'files',
            stdin=subprocess.DEVNULL, stdout=out, stderr=err, timeout=360)
    delta['delivered_exit_code'] = result.returncode
    delta['release_unchanged'] = release_inventory() == release_before
    delta['pack_unchanged_during_tests'] = refresh.inventory_bytes(pack) == after
    delta['delivered_tests'] = 'PASS' if result.returncode == 0 else 'FAIL'
    (OUT / 'pack-repair-delta.json').write_text(json.dumps(delta, indent=2) + '\n', encoding='utf-8', newline='\n')
    assert result.returncode == 0 and delta['release_unchanged'] and delta['pack_unchanged_during_tests']
    print('PASS owned exporter, six payload changes, delivered21 and unchanged release assets')

if __name__ == '__main__':
    main()
