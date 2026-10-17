"""Reuse the owned exporter and test actual portable defaults in disposable repos."""
import sys
sys.dont_write_bytecode = True
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

ROOT = Path.cwd()
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])
TMP = Path(os.environ['AIDE_JOB_TMP'])
assert Path(os.environ['TEMP']) == TMP
for key in list(os.environ):
    if key.startswith('GIT_'):
        os.environ.pop(key)
os.environ.update(GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL', GIT_TERMINAL_PROMPT='0')
EVIDENCE = ROOT / '.aide/queue/AIDE-INSTALLED-CHANGELOG-GUARD-01/evidence'
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


refresh = load('installed_guard_refresh', '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
# Keep the earlier pre-default predecessor to exercise an actual policy conflict.
old_inventory_path = ROOT / '.aide/queue/AIDE-GIT-DEFAULTS-01/evidence/prior-pack-inventory.json'
inventory = json.loads(old_inventory_path.read_bytes())
predecessor = TMP / 'predecessor-pack'
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
assert sys.argv[1:] == ['resume'], 'only the separately admitted remaining stages'
pack = ROOT / refresh.PACK_REL
expected_pack = json.loads((EVIDENCE / 'refreshed-pack-sha256s.json').read_bytes())
assert refresh.inventory_bytes(pack) == expected_pack
for command in ('doctor', 'validate', 'pack-status'):
    observed = refresh.invoke(command, [sys.executable, '-B',
                                       str(ROOT / '.aide/scripts/aide_lite.py'), command], OUTPUT)
    assert observed['exit_code'] == 0, command
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
# Five unaffected Q31 passes plus the repaired original consumer are conserved.
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
    assert not (target / '.aide/queue/index.yaml').exists()
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
    queue = target / '.aide/queue/index.yaml'
    queue.parent.mkdir(parents=True, exist_ok=True)
    queue.write_bytes(b'items: []\n')
    command = [sys.executable, '-I', '-B', str(target / '.aide/scripts/aide_lite.py'),
               '--repo-root', str(target), 'changelog', 'preview', '--range', 'HEAD']
    with (OUTPUT / (label + '-changelog.stdout')).open('xb') as stdout:
        with (OUTPUT / (label + '-changelog.stderr')).open('xb') as stderr:
            observed = subprocess.run(command, cwd=target, stdin=subprocess.DEVNULL,
                                      stdout=stdout, stderr=stderr, timeout=30)
    assert observed.returncode == 0, label + '-installed-changelog'
    return {entry['branch']: entry['recommended'] for entry in report['branch_targets']}


try:
    with tempfile.TemporaryDirectory(dir=TMP, prefix='fresh-') as directory:
        target = Path(directory)
        q31.init_target_git(target)
        result['stages']['fresh_import'] = import_checked(pack, target)
        choices = installed_choices('fresh-advisory', target)
        assert choices['main'] is False and choices['dev'] is False
        assert 'local_short_lived_by_default' in (target / aide.GIT_WORKFLOW_POLICY_PATH).read_text(encoding='utf8')
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
assert refresh.inventory_bytes(pack) == expected_pack
print(json.dumps({'status': result['status'], 'q31_methods_reused': 6, 'whole_task_usage': 'unknown'}))
