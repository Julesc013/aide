"""Check declared command syntax against the real parser; no handlers/fixtures."""
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
POLICY = ROOT/'.aide/policies/release-versioning.yaml'
SCRIPT = ROOT/'.aide/scripts/aide_lite.py'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def state():
    return subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain=v1'],
                          capture_output=True, check=True, timeout=15).stdout.decode()

before = state()
spec = importlib.util.spec_from_file_location('contract_cli_check', SCRIPT)
lite = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lite
spec.loader.exec_module(lite)
parser = lite.build_parser(ROOT)
section = POLICY.read_text(encoding='utf-8').split('  candidate_public_cli:\n', 1)[1].split('  cli_scope_rule:', 1)[0]
forms = [line[6:] for line in section.splitlines() if line.startswith('    - ')]
replacements = {'<task>': 'AIDE-STABLE-RELEASE-CONTRACT-01', '<task-id>': 'AIDE-STABLE-RELEASE-CONTRACT-01',
                '<evidence-path>': '.aide/queue/AIDE-STABLE-RELEASE-CONTRACT-01/evidence',
                '<new-pack>': 'new-pack', '<old-pack>': 'old-pack', '<target>': 'target',
                '<target-path>': '.aide/prompts/compact-task.md', '<resolution-file>': 'merged-file',
                '<local-packet>': 'feedback.json', '<digest>': 'a'*64,
                '<current-pack>': 'current-pack', '<previous-pack>': 'previous-pack',
                '<owned-path>': '.aide/scripts/aide_lite.py', '<pack>': 'pack'}
rows = []
for form in forms:
    text = form
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    error = io.StringIO()
    try:
        if re.search(r'<[^>]+>', text):
            raise ValueError('undeclared placeholder')
        with contextlib.redirect_stderr(error):
            parsed = parser.parse_args(shlex.split(text))
        if not callable(getattr(parsed, 'handler', None)):
            raise ValueError('missing callable handler')
        rows.append({'form': form, 'result': 'PASS', 'handler': parsed.handler.__name__})
    except (SystemExit, ValueError) as failure:
        rows.append({'form': form, 'result': 'FAIL', 'detail': error.getvalue().splitlines()[-1:] or [str(failure)]})
after = state()
assert before == after, 'parser/import rewrote Git state'
result = {'source_commit': subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, check=True).stdout.decode().strip(),
          'code_sha256': sha(SCRIPT), 'policy_sha256': sha(POLICY),
          'validation_scope': 'argument parser only; no handler, native effect, lifecycle or archive qualification',
          'forms': rows, 'non_mutating': True, 'handlers_invoked': 0,
          'metadata_schemas': [lite.PROJECT_CUSTOMIZATIONS_SCHEMA, lite.PROJECT_CUSTOMIZATIONS_SCHEMA_V2],
          'optional_features': lite.PORTABLE_OPTIONAL_FEATURES}
(Path(__file__).parent/'candidate-cli-check.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'forms': len(rows), 'passed': sum(r['result']=='PASS' for r in rows),
                  'failures': [r for r in rows if r['result']=='FAIL'], 'non_mutating': True}))
raise SystemExit(0 if all(r['result']=='PASS' for r in rows) else 1)
