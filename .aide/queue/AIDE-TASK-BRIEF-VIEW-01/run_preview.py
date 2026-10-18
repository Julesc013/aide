"""Verify exact retained qualification and generate the existing fixed preview."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
TASK = ROOT / '.aide/queue/AIDE-TASK-BRIEF-VIEW-01'
from core.execution.managed_workspace import content_digest, load_config

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

owner = load('brief_view_preview', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner.BASE = '4b4b735ef3f31af4e0d16d622453f814365ef437'
inventory = load('brief_view_inventory', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')

def verify_evidence(final=False):
    e = TASK / 'evidence'
    _, roots, _ = load_config(ROOT / '.aide.local/execution.json')
    names = ['source-attempt-01.json', 'pack-attempt-02.json']
    if final:
        names.append('preview-attempt-03.json')
    for filename in names:
        row = json.loads((e / filename).read_text(encoding='utf-8'))
        assert row['phase'] == 'retired' and row['result']['exit_code'] == 0
        assert row['result']['quiescent'] and row['scratch_absent'] and row['reservation_released']
        assert not (roots['scratch'] / row['job_id']).exists()
        for name, digest in row['collected_manifest'].items():
            assert content_digest(Path(row['retained']) / name) == digest, name
    for attempt in ('01','02'):
        for row in json.loads((e / ('attempt-'+attempt+'-projections.json')).read_bytes()):
            raw = Path(row['source']).read_bytes()
            projected = (ROOT / row['projection']).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row['raw_sha256']
            assert hashlib.sha256(projected).hexdigest() == row['projection_sha256']
            assert projected == raw.replace(b'\r\n', b'\n')
    for filename in ['attempt-01-source-tests.json', 'attempt-02-delivered-tests.json']:
        checks = json.loads((e / filename).read_bytes())
        assert checks['tests_run'] == 104 and not any(checks[k] for k in ('errors','failures','skips'))
        subject = ROOT if checks['subject'] == 'source' else ROOT / '.aide/export/aide-lite-pack-v0/files'
        for p, digest in checks['inputs'].items():
            assert sha(subject / p) == digest, p
    delivered = json.loads((e / 'attempt-02-delivered-result.json').read_bytes())
    actual = {p: row['sha256'] for p, row in inventory.observe()['files'].items()}
    assert len(actual) == 874 and actual == delivered['pack_sha256s']
    ownership = json.loads((e / 'attempt-02-ownership-tests.json').read_bytes())
    assert ownership == {'tests_run':6, 'failures':0, 'errors':0, 'skips':0}
    installed = json.loads((e / 'attempt-02-installed-consumer.json').read_bytes())
    assert installed['result'] == 'PASS'
    assert installed['core_absent'] and installed['customization_preserved']
    assert installed['fresh_process_read_only'] and installed['independent_projection_binding_oracle']
    assert installed['browser_render'] == 'NOT_RUN' and not installed['execution_authority']
    for row in installed['observations'].values():
        assert row['complete_json_equal'] and row['inactive_markup'] and not row['execution_admitted']
    assert installed['observations']['real-source']['state'] == 'PARTIAL'
    source = json.loads((e / 'attempt-01-actual-consumer.json').read_bytes())
    assert source['result'] == 'PASS' and source['source_records_unchanged']
    assert source['canonical_observation_sha256'] == installed['observations']['real-source']['observation_sha256']
    release = json.loads((e / 'release-preimages.json').read_bytes())
    assert len(release) == 8 and all(sha(ROOT/p) == h for p,h in release.items())
    return {'source_tests':104, 'delivered_tests':104, 'ownership_tests':6, 'pack_members':874,
            'actual_source_and_installed_consumers':'PASS', 'retired_jobs_verified':len(names),
            'release_assets_unchanged':8, 'browser_render':'NOT_RUN',
            'models_requested':0, 'whole_outcome_usage':'unknown'}

def main():
    assert sys.argv[1:] in (['generate'], ['verify'])
    final = sys.argv[1] == 'verify'
    evidence = verify_evidence(final=final)
    if final:
        print(json.dumps({'result':'PASS', **evidence, 'preview':owner.verify()}, indent=2))
    else:
        preimages = json.loads((TASK/'evidence/preview-preimages.json').read_bytes())
        assert set(preimages) == owner.NAMES
        assert all(sha(ROOT/'.aide/changelog'/p) == h for p,h in preimages.items())
        owner.main()
        (Path(os.environ['AIDE_JOB_OUTPUT'])/'evidence-verification.json').write_text(
            json.dumps({'result':'PASS', **evidence}, indent=2)+'\n', encoding='utf-8', newline='\n')

if __name__ == '__main__':
    main()
