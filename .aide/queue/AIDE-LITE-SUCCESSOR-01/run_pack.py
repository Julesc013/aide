"""Existing exporter plus exact payload delta and the first delivered partition."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

root = Path.cwd()
task = root / '.aide/queue/AIDE-LITE-SUCCESSOR-01'
output = Path(os.environ['AIDE_JOB_OUTPUT'])
assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
path = root / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'
spec = importlib.util.spec_from_file_location('successor_pack_owner', path)
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)
inventory = task / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(root)),
            '--inventory-sha256', hashlib.sha256(inventory.read_bytes()).hexdigest()]
refresh.main()

after = refresh.inventory_bytes(root / refresh.PACK_REL)
old = {name: value['sha256'] for name, value in before['files'].items()}
added = {'files/.aide/scripts/tests/test_stable_successor.py'}
assert set(after) - set(old) == added and not set(old) - set(after)
changed = {name for name in old if old[name] != after[name]} | added
payload = added | {'files/.aide/scripts/aide_lite.py', 'files/.aide/policies/release-versioning.yaml',
                   'files/docs/reference/aide-lite-release-bundle.md'}
assert changed - {'manifest.yaml', 'checksums.json', 'export-report.md'} == payload, sorted(changed)
for name in payload:
    assert refresh.sha(root / refresh.PACK_REL / name) == refresh.sha(root / name.removeprefix('files/'))

# Read the actual maintainer declaration and historical pins. This is not an
# install/update consumer, a publication observation or a support qualification.
spec = importlib.util.spec_from_file_location('successor_contract_owner', root / '.aide/scripts/aide_lite.py')
lite = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lite
spec.loader.exec_module(lite)
contract = lite.stable_release_contract(root, '1.1.0')
assert len(contract['forms']) == 56 and contract['predecessors'][0]['version'] == '1.0.0'
assert len(contract['preserved']) == 4
(output / 'source-contract.json').write_text(json.dumps({
    'result': 'DECLARATION_RESOLVED', 'forms': contract['forms'],
    'contract_sha256': contract['digest'], 'predecessor': contract['predecessors'],
    'upgrade_qualified': False}, indent=2) + '\n', encoding='utf-8', newline='\n')

bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
subprocess.run([sys.executable, '-B', '-c', bootstrap, str(task / 'run_checks.py'),
                'delivered_a', str(root / refresh.PACK_REL / 'files')], check=True, timeout=120)
assert refresh.inventory_bytes(root / refresh.PACK_REL) == after
(output / 'pack-delta.json').write_text(json.dumps({'changed_paths': sorted(changed),
    'after_sha256s': after}, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS exporter, declaration resolution, delivered18 and exact four-file payload delta')
