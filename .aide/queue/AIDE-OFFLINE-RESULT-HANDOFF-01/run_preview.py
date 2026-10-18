"""Verify retained qualification and generate one fixed existing preview."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
TASK = ROOT / '.aide/queue/AIDE-OFFLINE-RESULT-HANDOFF-01'
from core.execution.managed_workspace import content_digest, load_config

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

owner = load('offline_preview', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner.BASE = '66c0b90b6aa0b68cd24659b6279f66b987cb585c'
inventory = load('offline_preview_inventory', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')

def verify_evidence():
    e = TASK / 'evidence'
    _, roots, _ = load_config(ROOT / '.aide.local/execution.json')
    for filename in ['source-attempt-01.json', 'pack-attempt-02.json']:
        record = json.loads((e / filename).read_text(encoding='utf-8'))
        assert record['phase'] == 'retired' and record['result']['exit_code'] == 0
        assert record['result']['quiescent'] and record['scratch_absent'] and record['reservation_released']
        assert not (roots['scratch'] / record['job_id']).exists()
        for name, digest in record['collected_manifest'].items():
            assert content_digest(Path(record['retained']) / name) == digest, name
    for filename in ['attempt-01-source-tests.json', 'attempt-02-delivered-tests.json']:
        checks = json.loads((e / filename).read_text(encoding='utf-8'))
        assert checks['tests_run'] == 97 and not any(checks[k] for k in ('errors','failures','skips'))
        subject = ROOT if checks['subject'] == 'source' else ROOT / '.aide/export/aide-lite-pack-v0/files'
        for p, digest in checks['inputs'].items():
            assert sha(subject / p) == digest, p
    delivered = json.loads((e / 'attempt-02-delivered-result.json').read_text(encoding='utf-8'))
    actual = {p: row['sha256'] for p, row in inventory.observe()['files'].items()}
    assert len(actual) == 870 and actual == delivered['pack_sha256s']
    for filename in ['attempt-02-installed-consumer.json', 'attempt-02-real-record-consumer.json']:
        row = json.loads((e / filename).read_text(encoding='utf-8'))
        assert row.get('status', row.get('result')) == 'PASS'
    release = json.loads((e / 'release-preimages.json').read_text(encoding='utf-8'))
    assert len(release) == 8 and all(sha(ROOT/p) == h for p,h in release.items())
    return {'source_tests':97,'delivered_tests':97,'pack_members':870,'release_assets_unchanged':8,
            'source_and_delivered_jobs_retired':True,'models_requested':0,'whole_outcome_usage':'unknown'}

def main():
    assert sys.argv[1:] in (['generate'], ['verify'])
    evidence = verify_evidence()
    if sys.argv[1:] == ['verify']:
        print(json.dumps({'result':'PASS',**evidence,'preview':owner.verify()},indent=2))
        return
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    for label, args in [('doctor',['doctor']),('validation',['validate']),('pack-status',['pack-status'])]:
        path = output / (label+'.log')
        with path.open('xb') as stream:
            result = subprocess.run([sys.executable,'-B','.aide/scripts/aide_lite.py',*args],
                stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
        assert result.returncode == 0,label
    owner.main()
    assert verify_evidence() == evidence
    (output/'qualification.json').write_text(json.dumps({'result':'PASS',**evidence,
        'preview':owner.verify()},indent=2)+'\n',encoding='utf-8',newline='\n')

if __name__ == '__main__':
    main()
