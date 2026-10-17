"""Reuse the owned exporter and test actual portable defaults in disposable repos."""
import sys
sys.dont_write_bytecode = True
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tarfile
import unittest

ROOT = Path.cwd()
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
TMP = Path(os.environ['AIDE_JOB_TMP'])
assert Path(os.environ['TEMP']) == TMP
for key in list(os.environ):
    if key.startswith('GIT_'):
        os.environ.pop(key)
os.environ.update(GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL', GIT_TERMINAL_PROMPT='0')
EVIDENCE = ROOT / '.aide/queue/AIDE-GIT-DEFAULTS-01/evidence'
tools = json.loads((EVIDENCE / 'tool-identities.json').read_bytes())
git = Path(shutil.which('git')).resolve()
assert git == Path(tools['git_executable']).resolve()
assert hashlib.sha256(git.read_bytes()).hexdigest() == tools['git_executable_sha256']
assert not subprocess.check_output([str(git), 'status', '--porcelain'], cwd=ROOT).strip()


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_suite(label, suite):
    with (OUTPUT / (label + '.stderr')).open('x', encoding='utf8') as stderr:
        with (OUTPUT / (label + '.stdout')).open('x', encoding='utf8') as stdout:
            with contextlib.redirect_stdout(stdout):
                result = unittest.TextTestRunner(stream=stderr, verbosity=2).run(suite)
    record = {'tests_run': result.testsRun, 'failures': len(result.failures),
              'errors': len(result.errors), 'skips': len(result.skipped)}
    (OUTPUT / (label + '.json')).write_bytes((json.dumps(record, indent=2) + '\n').encode())
    assert result.wasSuccessful() and not result.skipped, label
    return record


assert sys.argv[1:] in ([], ['resume'])
resume = sys.argv[1:] == ['resume']
if not resume:
    q28 = load('git_defaults_q28', '.aide/scripts/tests/test_q28_git_workflow.py')
    repair = run_suite('affected-repair', unittest.TestSuite([
        q28.Q28GitWorkflowTests('test_git_detect_writes_report_with_mocked_git')]))
    assert repair['tests_run'] == 1

refresh = load('git_defaults_refresh', '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory_path = EVIDENCE / 'prior-pack-inventory.json'
inventory = json.loads(inventory_path.read_bytes())
predecessor = TMP / 'predecessor-pack'
if resume:
    # Reconstruct only the exact retained predecessor; do not reset the new pack.
    archive = subprocess.check_output([str(git), 'archive', '--format=tar',
                                       inventory['git_commit'], '--', refresh.PACK_REL], cwd=ROOT, timeout=30)
    assert len(archive) <= 8 * 1024 * 1024
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        for member in source:
            if member.isdir():
                continue
            assert member.isfile() and member.name.startswith(refresh.PACK_REL + '/')
            relative = member.name[len(refresh.PACK_REL) + 1:]
            assert relative in inventory['files'] and relative not in seen
            assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
            data = source.extractfile(member).read()
            assert hashlib.sha256(data).hexdigest() == inventory['files'][relative]['sha256']
            target = predecessor / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            seen.add(relative)
    assert seen == set(inventory['files'])
else:
    refresh.require_same(inventory)
    shutil.copytree(ROOT / refresh.PACK_REL, predecessor)
assert refresh.inventory_bytes(predecessor) == {
    name: entry['sha256'] for name, entry in inventory['files'].items()}
pack = ROOT / refresh.PACK_REL
if resume:
    expected = json.loads((EVIDENCE / 'refreshed-pack-sha256s.json').read_bytes())
    assert refresh.inventory_bytes(pack) == expected
    for command in ('doctor', 'validate', 'pack-status'):
        observed = refresh.invoke(command, [sys.executable, '-B',
                                            str(ROOT / '.aide/scripts/aide_lite.py'), command], OUTPUT)
        assert observed['exit_code'] == 0, command
else:
    sys.argv = [str(ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py'),
                'refresh', '--inventory', inventory_path.relative_to(ROOT).as_posix(),
                '--inventory-sha256', hashlib.sha256(inventory_path.read_bytes()).hexdigest()]
    refresh.main()
changelog = {}
for label, args in [
    ('changelog-preview', ['changelog', 'preview', '--range',
                          '6f2abc4cd69e0d94f86a00495cb8feeebe20398a..HEAD', '--limit', '100']),
    ('changelog-validate', ['changelog', 'validate']),
    ('changelog-status', ['changelog', 'status']),
]:
    observed = refresh.invoke(label, [sys.executable, '-B',
                                     str(ROOT / '.aide/scripts/aide_lite.py'), *args], OUTPUT)
    changelog[label] = observed
    (OUTPUT / 'changelog.json').write_bytes((json.dumps(changelog, indent=2) + '\n').encode())
    assert observed['exit_code'] == 0, label

q31 = load('git_defaults_q31', '.aide/scripts/tests/test_q31_export_pack_governance.py')
original = run_suite('original-q31', unittest.defaultTestLoader.loadTestsFromModule(q31))
assert original['tests_run'] == 6
aide = q31.aide_lite
result = {'status': 'INCOMPLETE', 'model_calls': 0, 'remote_effects': False,
          'predecessor': aide.import_pack_identity(predecessor),
          'current_pack': aide.import_pack_identity(pack), 'stages': {}}


def import_checked(source, target, predecessor_pack=None, resolutions=None):
    options = {'mode': 'safe', 'predecessor_pack': predecessor_pack, 'resolutions': resolutions}
    preview = aide.apply_import_pack(source, target, dry_run=True, **options)
    assert not preview['conflicts'], preview['conflicts']
    applied = aide.apply_import_pack(source, target, expected_plan_digest=preview['plan_digest'], **options)
    assert not applied['conflicts'] and applied['status'] in ('APPLIED', 'NO_CHANGES'), applied['status']
    return {'status': applied['status'], 'plan_digest': preview['plan_digest'],
            'written': len(applied['written'])}


def installed_choices(label, target):
    command = [sys.executable, '-I', '-B', str(target / '.aide/scripts/aide_lite.py'),
               '--repo-root', str(target), 'github', 'advisory']
    with (OUTPUT / (label + '.stdout')).open('xb') as stdout:
        with (OUTPUT / (label + '.stderr')).open('xb') as stderr:
            run = subprocess.run(command, cwd=target, stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr, timeout=30)
    assert run.returncode == 0, label
    report = json.loads((target / aide.GITHUB_PROTECTION_PLAN_JSON_PATH).read_bytes())
    assert not report['branch_protection_applied'] and not report['remote_protection_observed']
    assert not report['policy_issues']
    return {entry['branch']: entry['recommended'] for entry in report['branch_targets']}


try:
    with tempfile.TemporaryDirectory(dir=TMP, prefix='fresh-') as directory:
        target = Path(directory)
        q31.init_target_git(target)
        result['stages']['fresh_import'] = import_checked(pack, target)
        choices = installed_choices('fresh-advisory', target)
        assert choices['main'] is False and choices['dev'] is False
        assert 'local_short_lived_by_default' in (target / aide.GIT_WORKFLOW_POLICY_PATH).read_text(encoding='utf8')
        assert not (target / '.aide/queue/index.yaml').exists()
        result['stages']['fresh_choices'] = choices
    with tempfile.TemporaryDirectory(dir=TMP, prefix='custom-') as directory:
        target = Path(directory)
        q31.init_target_git(target)
        result['stages']['predecessor_import'] = import_checked(predecessor, target)
        relative = aide.BRANCH_PROTECTION_POLICY_PATH
        policy = target / relative
        policy.write_bytes(policy.read_bytes() + b'\n# Project-owned protection choice.\n')
        before = policy.read_bytes()
        preview = aide.apply_import_pack(pack, target, dry_run=True, mode='safe', predecessor_pack=predecessor)
        assert policy.read_bytes() == before
        assert preview['conflicts'] == [relative], preview['conflicts']
        preserved = refresh.inventory_bytes(target)
        refused = aide.apply_import_pack(pack, target, mode='safe', predecessor_pack=predecessor,
                                         expected_plan_digest=preview['plan_digest'])
        assert refused['status'] == 'CONFLICT' and not refused['written']
        assert refresh.inventory_bytes(target) == preserved
        result['stages']['unresolved_update'] = 'CONFLICT_without_changed_bytes'
        # Resolve against the new source explicitly, preserving the project's main opt-in.
        resolved = TMP / 'resolved-protection.yaml'
        new_text = (pack / aide.q31_pack_payload_path(relative)).read_text(encoding='utf8')
        assert '    protect: false' in new_text
        resolved.write_bytes((new_text.replace('    protect: false', '    protect: true', 1)
                              + '\n# Project-owned protection choice.\n').encode())
        result['stages']['initial_update_conflicts'] = preview['conflicts']
        result['stages']['custom_update'] = import_checked(pack, target, predecessor, {relative: resolved})
        assert policy.read_bytes() == resolved.read_bytes()
        choices = installed_choices('custom-advisory', target)
        assert choices['main'] is True and choices['dev'] is False
        result['stages']['custom_choices'] = choices
        receipt = aide.load_portable_import_receipt(target)
        assert receipt['managed'][relative]['local_overlay'] is True
        assert receipt['managed'][relative]['ownership'] == 'project_overlay_on_aide_managed'
        result['stages']['customization_receipt'] = receipt['managed'][relative]
    result['status'] = 'PASS'
finally:
    (OUTPUT / 'consumer.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
if resume:
    assert refresh.inventory_bytes(pack) == expected
print(json.dumps({'status': result['status'], 'affected_tests': 0 if resume else 1,
                  'original_q31_tests': 6, 'reused_passes': 42 if resume else 35,
                  'whole_task_usage': 'unknown'}))
