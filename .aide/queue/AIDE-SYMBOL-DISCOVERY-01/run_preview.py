"""Read-only verification of preserved attempts and the fixed final preview."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
TASK = ROOT / '.aide/queue/AIDE-SYMBOL-DISCOVERY-01'
from core.execution.managed_workspace import content_digest, load_config

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

owner = load('symbol_preview', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner.BASE = '118ab7829f300050394dc67a3af943963acfe218'
inventory = load('symbol_preview_inventory', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')

def verify_evidence():
    e = TASK / 'evidence'
    _, roots, _ = load_config(ROOT / '.aide.local/execution.json')
    for filename, expected_exit in [('source-attempt-01.json', 0), ('pack-attempt-02.json', 1), ('preview-attempt-03.json', 0)]:
        record = json.loads((e / filename).read_text(encoding='utf-8'))
        assert record['phase'] == 'retired' and record['result']['exit_code'] == expected_exit
        assert record['result']['quiescent'] and record['scratch_absent'] and record['reservation_released']
        assert not (roots['scratch'] / record['job_id']).exists()
        for name, digest in record['collected_manifest'].items():
            assert content_digest(Path(record['retained']) / name) == digest, name
    for filename in ['attempt-01-source-tests.json', 'attempt-03-delivered-tests.json']:
        checks = json.loads((e / filename).read_text(encoding='utf-8'))
        assert checks['tests_run'] == 44 and not any(checks[k] for k in ('errors','failures','skips'))
        subject = ROOT if checks['subject'] == 'source' else ROOT / '.aide/export/aide-lite-pack-v0/files'
        for p, digest in checks['inputs'].items():
            assert sha(subject / p) == digest, p
    delivered = json.loads((e / 'attempt-03-delivered-result.json').read_text(encoding='utf-8'))
    actual = {p: row['sha256'] for p, row in inventory.observe()['files'].items()}
    assert len(actual) == 872 and actual == delivered['pack_sha256s']
    for filename in ['attempt-03-installed-consumer.json']:
        row = json.loads((e / filename).read_text(encoding='utf-8'))
        assert row.get('status', row.get('result')) == 'PASS'
    release = json.loads((e / 'release-preimages.json').read_text(encoding='utf-8'))
    assert len(release) == 8 and all(sha(ROOT/p) == h for p,h in release.items())
    return {'source_tests':44,'delivered_tests':44,'pack_members':872,'release_assets_unchanged':8,
            'all_three_jobs_retired':True,'failed_export_attempt_preserved':True,'models_requested':0,'whole_outcome_usage':'unknown'}

def main():
    assert sys.argv[1:] == ['verify']
    evidence = verify_evidence()
    print(json.dumps({'result':'PASS', **evidence, 'preview':owner.verify()}, indent=2))


if __name__ == '__main__':
    main()
