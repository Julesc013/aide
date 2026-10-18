"""Refresh the combined development pack and test its real installed binding."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, unittest
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(name, data):
    (OUTPUT / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
def releases():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for p in (ROOT / '.aide/release/stable').iterdir() if p.is_file()}
refresh = load('combined_pack_owner', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
prior = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(prior.read_text(encoding='utf-8'))
release_before = releases()
dump('release-before.json', release_before)
sys.argv = [__file__, 'refresh', '--inventory', str(prior.relative_to(ROOT)),
            '--inventory-sha256', sha(prior)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: item['sha256'] for name, item in before['files'].items()}
added = {'files/.aide/scripts/aide_work_effort.py'}
changed = {'files/.aide/scripts/aide_lite.py', 'files/.aide/scripts/tests/test_work_effort.py',
    'files/.aide/scripts/tests/test_export_import.py', 'files/.aide/scripts/tests/test_aide_lite.py',
    'files/docs/reference/aide-lite-test-runner.md'}
assert len(after) == 870 and set(after) == set(old) | added and not added.intersection(old)
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
source = load('combined_source_cli', ROOT / '.aide/scripts/aide_lite.py')
assert (pack / 'files/.aide/scripts/aide_lite.py').read_text(encoding='utf-8') == source.portable_cli_text(
    (ROOT / '.aide/scripts/aide_lite.py').read_text(encoding='utf-8'))
assert (pack / next(iter(added))).read_bytes() == (ROOT / 'core/execution/work_effort.py').read_bytes()
for name in changed - {'files/.aide/scripts/aide_lite.py'}:
    assert sha(pack / name) == sha(ROOT / name.removeprefix('files/'))
dump('pack-delta.json', {'added': sorted(added), 'changed_payloads': sorted(changed),
                        'after_sha256s': after, 'all_newer_cli_source_preserved': True})
effort = load('combined_delivered_effort', pack / 'files/.aide/scripts/tests/test_work_effort.py')
compact = load('combined_delivered_compact', pack / 'files/.aide/scripts/tests/test_compact_communication.py')
methods = unittest.defaultTestLoader.getTestCaseNames(effort.WorkEffortTests)
source_only = {'test_safe_installed_effort_preserves_project_core_and_never_falls_back',
               'test_export_binding_drift_refuses_before_reset'}
assert source_only <= set(methods) and len(methods) == 17
suite = unittest.TestSuite(effort.WorkEffortTests(name) for name in methods if name not in source_only)
suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(compact))
def ids(tests):
    for item in tests:
        if isinstance(item, unittest.TestSuite):
            yield from ids(item)
        else:
            yield item.id()
expected = list(ids(suite))
assert len(expected) == 41
with (OUTPUT / 'delivered-tests.log').open('w', encoding='utf-8') as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
dump('delivered-tests.json', {'test_ids': expected, 'tests_run': result.testsRun,
    'failures': len(result.failures), 'errors': len(result.errors),
    'skips': [(t.id(), why) for t, why in result.skipped],
    'source_only_fixture_methods': sorted(source_only)})
assert result.wasSuccessful() and result.testsRun == 41 and not result.skipped
class InstalledPackEffort(effort.WorkEffortTests):
    def export_fixture(self):
        return pack / 'files', pack
method = 'test_safe_installed_effort_preserves_project_core_and_never_falls_back'
dump('installed-result.json', {'status': 'INCOMPLETE', 'test_method': method,
    'fixture': 'actual_owned_combined_development_pack', 'model_calls': 0})
with (OUTPUT / 'installed-tests.log').open('w', encoding='utf-8') as log:
    installed = unittest.TextTestRunner(stream=log, verbosity=2).run(
        unittest.TestSuite([InstalledPackEffort(method)]))
record = {'status': 'PASS' if installed.wasSuccessful() and not installed.skipped else 'FAIL',
          'tests_run': installed.testsRun, 'failures': len(installed.failures),
          'errors': len(installed.errors), 'skips': len(installed.skipped),
          'test_method': method, 'fixture': 'actual_owned_combined_development_pack'}
dump('installed-result.json', record)
assert record['status'] == 'PASS' and installed.testsRun == 1
assert refresh.inventory_bytes(pack) == after and releases() == release_before
dump('delivered-result.json', {'result': 'PASS', 'after_sha256s': after,
    'delivered_effort': 15, 'delivered_compact': 26, 'actual_installed_method': 1,
    'all_release_assets_unchanged': True, 'models_requested': 0, 'archive_qualification': False})
print('PASS: 870-member combined pack,41 delivered checks and actual installed effort consumer')
