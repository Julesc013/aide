"""Read-only original-consumer preflight; no fixture, allocation or generator."""
import ast
import base64
import gzip
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


record = {'state': 'started', 'jobs_requested': 0, 'consumer_tests_executed': False}
try:
    for path in (TASK / 'run_consumer.py', TASK / 'commit_and_consume.py', Path(__file__)):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    spec = importlib.util.spec_from_file_location('archive_consumer_preflight_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    checks = lite.validate_commit_message_text((EVIDENCE / 'consumer-message.txt').read_text(encoding='utf-8'))
    assert not [c for c in checks if c.severity == 'FAIL'], [(c.severity, c.message) for c in checks]
    config, _, working = workspace.load_config(ROOT / '.aide.local/lite-successor-qualification-execution.json')
    job = json.loads((EVIDENCE / 'consumer-job-template.json').read_bytes())
    assert 'canonical_outputs' not in job
    for index in range(8):
        candidate = dict(job, argv=[*job['argv'], str(index)], source_commit=git('rev-parse', 'HEAD'),
                         source_tree=git('rev-parse', 'HEAD^{tree}'))
        workspace.validate_job(candidate, working)
    original = ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/canaries'
    preserved = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(original.iterdir()) if p.is_file()}
    assert len(preserved) == 13
    for name, expected in preserved.items():
        data = subprocess.check_output(['git', 'show', 'ed4a90046eba12a717a9962f21523285667a669b:' + name], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == expected
    old_config = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/consumer-config.json'
    assert (EVIDENCE / 'consumer-config.json').read_bytes() == old_config.read_bytes()
    built = json.loads((EVIDENCE / 'build-result.json').read_bytes())
    assert built['status'] == 'PASS_BUILD_ONLY' and built['identity']['version'] == '1.2.0'
    assert all(sha(ROOT / name) == value['sha256'] for name, value in built['assets'].items())
    before = json.loads((EVIDENCE / 'release-before.json').read_bytes())
    assert all(sha(ROOT / name) == value['sha256'] and (ROOT / name).stat().st_size == value['size_bytes']
               for name, value in before.items())
    pack = json.loads((EVIDENCE / 'pack-subject.json').read_bytes())
    assert all(sha(ROOT / name) == expected for name, expected in pack.items())
    receipt = json.loads((EVIDENCE / 'build-job-result.json').read_bytes())
    assert receipt['phase'] == 'retired' and receipt['scratch_absent'] and receipt['reservation_released']
    assert receipt['result']['exit_code'] == 0 and receipt['result']['quiescent']
    for name, expected in receipt['collected_manifest'].items():
        assert workspace.content_digest(Path(receipt['retained']) / name) == expected
    bundle = json.loads((EVIDENCE / 'build-retained-evidence.json').read_bytes())
    compressed = base64.b64decode(bundle['data'], validate=True)
    assert hashlib.sha256(compressed).hexdigest() == bundle['gzip_sha256']
    raw = gzip.decompress(compressed)
    assert len(raw) == bundle['uncompressed_bytes'] and hashlib.sha256(raw).hexdigest() == bundle['sha256']
    retained = {p.relative_to(Path(receipt['retained'])).as_posix(): base64.b64encode(p.read_bytes()).decode('ascii')
                for p in sorted(Path(receipt['retained']).rglob('*')) if p.is_file()}
    assert json.loads(raw) == retained and len(retained) == bundle['files']
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    portable_files = set(lite.PORTABLE_SOURCE_FILES) | set(lite.PORTABLE_TEMPLATE_MAP)
    portable_dirs = tuple(path.rstrip('/') + '/' for path in lite.PORTABLE_SOURCE_DIRS)
    assert not [path for path in changed if path in portable_files or path.startswith(portable_dirs)]
    assert lite.pack_source_ancestor_has_unchanged_inputs(ROOT, built['identity']['source_commit'], git('rev-parse', 'HEAD'))
    git('diff', '--check')
    record.update(state='PASS_READ_ONLY_PREFLIGHT', source_head=git('rev-parse', 'HEAD'),
                  literal_shared_inputs=len(job['inputs']), original_canary_files=preserved,
                  old_probe_config_unchanged=True, build_job_retired=True, build_retained_files=len(retained),
                  stable_assets_preserved=8, release_preimages=len(before), pack_files=len(pack),
                  archive_assets=built['assets'], prepared_cases=list(range(8)),
                  worker_model_requests=0, whole_model_usage='unknown')
except BaseException as error:
    record.update(state='REFUSED', error_type=type(error).__name__, error=str(error))
    raise
finally:
    (EVIDENCE / 'consumer-prechecks.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
print(json.dumps({k: v for k, v in record.items() if k not in ('original_canary_files', 'archive_assets')}))
