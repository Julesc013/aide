"""Existing exporter ownership checks, exact payload delta and delivered consumer."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

root = Path.cwd()
task = root / '.aide/queue/AIDE-RESUME-PLAN-01'
output = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
path = root / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'
spec = importlib.util.spec_from_file_location('resume_pack_owner', path)
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)
inventory = task / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(root)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()
after = refresh.inventory_bytes(root / refresh.PACK_REL)
old = {name: value['sha256'] for name, value in before['files'].items()}
added = {'files/.aide/scripts/tests/test_resume_plan.py'}
assert set(after) - set(old) == added and not set(old) - set(after)
changed = {name for name in old if old[name] != after[name]} | added
payload = added | {'files/.aide/scripts/aide_lite.py', 'files/docs/reference/task-os-report-only-commands.md'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(root / refresh.PACK_REL / name) == refresh.sha(root / name.removeprefix('files/'))
bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
subprocess.run([sys.executable, '-B', '-c', bootstrap, str(task / 'run_checks.py'),
                str(root / refresh.PACK_REL / 'files')], check=True, timeout=90)
assert refresh.inventory_bytes(root / refresh.PACK_REL) == after
(output / 'pack-delta.json').write_text(json.dumps({'changed_paths': sorted(changed),
    'after_sha256s': after}, indent=2) + '\n', encoding='utf-8')
print('PASS actual delivered checks and consumer; exact three-file payload delta')
