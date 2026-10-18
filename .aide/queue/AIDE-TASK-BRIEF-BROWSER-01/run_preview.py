"""Reuse product evidence and verify the new observed rendering and fixed preview."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
TASK = ROOT / '.aide/queue/AIDE-TASK-BRIEF-BROWSER-01'
from core.execution.managed_workspace import content_digest, load_config

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

prior = load('browser_prior_qualification', ROOT / '.aide/queue/AIDE-TASK-BRIEF-SYMBOL-01/run_preview.py')
owner = load('browser_preview_owner', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner.BASE = 'ad1f67f1b0f4079038d6600752d3132b7714a692'

def verify_evidence(final=False):
    reused = prior.verify_evidence()
    e = TASK / 'evidence'
    _, roots, _ = load_config(ROOT / '.aide.local/execution.json')
    names = ['source-attempt-01.json'] + (['preview-attempt-02.json'] if final else [])
    for filename in names:
        row = json.loads((e / filename).read_bytes())
        assert row['phase'] == 'retired' and row['result']['exit_code'] == 0
        assert row['result']['quiescent'] and row['scratch_absent'] and row['reservation_released']
        assert not (roots['scratch'] / row['job_id']).exists()
        for name, digest in row['collected_manifest'].items():
            assert content_digest(Path(row['retained']) / name) == digest, name
    for attempt in (['01', '02'] if final else ['01']):
        for row in json.loads((e / ('attempt-' + attempt + '-projections.json')).read_bytes()):
            raw = Path(row['source']).read_bytes()
            projected = (ROOT / row['projection']).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row['raw_sha256']
            assert hashlib.sha256(projected).hexdigest() == row['projection_sha256']
            expected = raw if row['transformation'] == 'byte-identical' else raw.replace(b'\r\n', b'\n')
            assert projected == expected
    observed = json.loads((e / 'attempt-01-browser-result.json').read_bytes())
    assert observed['result'] == 'CAPTURE_AND_DOM_PASS_PENDING_VISUAL_REVIEW'
    assert observed['version'] == '155.0.4283.62' and len(observed['captures']) == 2
    assert observed['before']['files_verified'] == observed['after']['files_verified'] == 924
    original = ROOT / '.aide/queue/AIDE-TASK-BRIEF-SYMBOL-01/evidence/attempt-02-real-source-html.stdout'
    assert sha(original) == observed['page_sha256']
    visual = json.loads((e / 'visual-review.json').read_bytes())
    assert visual['result'] == 'PASS' and visual['independent_verdict'] == 'ACCEPT'
    assert sha(e / 'visual-review-independent.log') == visual['independent_review_sha256']
    for row, dimensions in zip(observed['captures'], [[1280, 1800], [480, 1800]], strict=True):
        assert row['dimensions'] == dimensions and row['complete_observation_equal']
        p = e / ('attempt-01-' + row['label'] + '.png')
        assert sha(p) == row['screenshot_sha256'] == visual['screenshots'][row['label']]['sha256']
    return {'result': 'PASS', 'reused_product_evidence': reused,
            'browser': observed['browser'], 'version': observed['version'],
            'capture_and_visual_review': 'PASS', 'captures': 2,
            'retired_jobs_verified': len(names), 'models_requested': 0,
            'whole_outcome_usage': 'unknown', 'accessibility': 'NOT_QUALIFIED'}

def main():
    assert sys.argv[1:] in (['generate'], ['verify'])
    final = sys.argv[1] == 'verify'
    evidence = verify_evidence(final)
    if final:
        print(json.dumps({'result': 'PASS', 'evidence': evidence, 'preview': owner.verify()}, indent=2))
    else:
        preimages = json.loads((TASK / 'evidence/preview-preimages.json').read_bytes())
        assert set(preimages) == owner.NAMES
        assert all(sha(ROOT / '.aide/changelog' / p) == h for p, h in preimages.items())
        owner.main()
        (Path(os.environ['AIDE_JOB_OUTPUT']) / 'evidence-verification.json').write_text(
            json.dumps(evidence, indent=2) + '\n', encoding='utf-8', newline='\n')

if __name__ == '__main__':
    main()
