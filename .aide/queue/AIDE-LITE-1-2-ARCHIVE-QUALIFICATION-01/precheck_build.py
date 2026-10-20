"""Read-only exact archive-build preflight, without a job or generator."""
import ast
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).parent
EVIDENCE = TASK / 'evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


record = {'state': 'started', 'job_requested': False, 'archives_built': False, 'export_refreshed': False}
try:
    for path in (TASK / 'run_build.py', TASK / 'commit_and_build.py', Path(__file__)):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    spec = importlib.util.spec_from_file_location('archive_build_preflight_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    checks = lite.validate_commit_message_text((EVIDENCE / 'build-message.txt').read_text(encoding='utf-8'))
    assert not [c for c in checks if c.severity == 'FAIL'], [(c.severity, c.message) for c in checks]
    qualification, _, working = workspace.load_config(ROOT / '.aide.local/lite-successor-qualification-execution.json')
    job = json.loads((EVIDENCE / 'build-job-template.json').read_bytes())
    job.update(source_commit=git('rev-parse', 'HEAD'), source_tree=git('rev-parse', 'HEAD^{tree}'))
    workspace.validate_job(job, working)
    workspace.canonical_roots(qualification, job, ROOT)
    assert set(job['canonical_outputs']) == {'.aide/release/stable'}
    pack = json.loads((EVIDENCE / 'pack-subject.json').read_bytes())
    actual_pack = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / lite.EXPORT_PACK_PATH).rglob('*')) if p.is_file()}
    assert actual_pack == pack and len(pack) == 879
    before = json.loads((EVIDENCE / 'release-before.json').read_bytes())
    actual_release = {p.relative_to(ROOT).as_posix(): {'sha256': sha(p), 'size_bytes': p.stat().st_size}
                      for p in sorted((ROOT / '.aide/release').rglob('*')) if p.is_file()}
    assert actual_release == before and len(before) == 58
    result = json.loads((EVIDENCE / 'canonical-job-result.json').read_bytes())
    assert result['phase'] == 'retired' and result['scratch_absent'] and result['reservation_released']
    assert result['result']['exit_code'] == 0 and result['result']['quiescent']
    for name, expected in result['collected_manifest'].items():
        assert workspace.content_digest(Path(result['retained']) / name) == expected
    tests = json.loads((EVIDENCE / 'canonical-tests.json').read_bytes())
    assert tests['passed'] and tests['tests_run'] == 12 and not tests['skips']
    scalars = lite.pack_manifest_scalars(ROOT / lite.EXPORT_PACK_PATH)
    assert scalars['source_commit'] == git('rev-parse', 'HEAD') and scalars['source_dirty_state'] == 'false'
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    portable_files = set(lite.PORTABLE_SOURCE_FILES) | set(lite.PORTABLE_TEMPLATE_MAP)
    portable_dirs = tuple(path.rstrip('/') + '/' for path in lite.PORTABLE_SOURCE_DIRS)
    portable_changes = sorted(path for path in changed if path in portable_files or path.startswith(portable_dirs))
    assert not portable_changes, portable_changes
    contract = lite.stable_release_contract(ROOT, '1.2.0')
    assert len(contract['profiles']) == 4 and len(contract['forms']) == 56
    commands = []
    for args in [('doctor',), ('validate',), ('pack-status',), ('commit', 'check', '--latest')]:
        process = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *args], cwd=ROOT,
                                 stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
        row = {'args': list(args), 'exit_code': process.returncode, 'streams': {}}
        for name in ('stdout', 'stderr'):
            raw = getattr(process, name)
            row['streams'][name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                                    'base64': base64.b64encode(raw).decode('ascii')}
        row['tail'] = process.stdout.decode('utf-8', errors='replace').splitlines()[-5:]
        commands.append(row)
        record['commands'] = commands
        assert process.returncode == 0, row['tail']
    git('diff', '--check')
    record.update(state='PASS_READ_ONLY_PREFLIGHT', source_head=git('rev-parse', 'HEAD'),
                  literal_job_inputs=len(job['inputs']), pack_files=len(pack), preserved_release_files=len(before),
                  profiles=4, public_forms=56, source_portable_changes_after_refresh=portable_changes,
                  canonical_tests_passed=12, canonical_job_retired=True,
                  config_digest=workspace.digest(qualification), future_commit_requires_same_portable_inputs=True)
except BaseException as error:
    record.update(state='REFUSED', error_type=type(error).__name__, error=str(error))
    raise
finally:
    (EVIDENCE / 'build-prechecks.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
print(json.dumps({k: v for k, v in record.items() if k != 'commands'}))
