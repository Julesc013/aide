"""Read-only source/manifest preflight; no fixtures, allocation or generator."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def methods(text):
    tree = ast.parse(text)
    owner = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'ManagedWorkspaceTests')
    return {n.name: ast.dump(n, include_attributes=False) for n in owner.body
            if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}


record = {'state': 'started', 'tests_executed': False, 'allocation_requested': False,
          'export_refreshed': False, 'production_assets_created': False}
try:
    parsed = []
    for relative in ['core/execution/managed_workspace.py', '.aide/scripts/aide_lite.py',
                     '.aide/scripts/tests/test_managed_workspace.py'] + [
                         p.relative_to(ROOT).as_posix() for p in sorted(TASK.glob('*.py'))]:
        ast.parse((ROOT / relative).read_text(encoding='utf-8'), filename=relative)
        parsed.append(relative)
    relative = '.aide/scripts/tests/test_managed_workspace.py'
    previous = methods(git('show', 'HEAD:' + relative))
    current = methods((ROOT / relative).read_text(encoding='utf-8'))
    assert len(previous) == 71 and all(current.get(k) == v for k, v in previous.items())
    assert len(current) == 75
    worker_tree = ast.parse((TASK / 'run_canonical.py').read_text(encoding='utf-8'))
    names = ast.literal_eval(next(n.value for n in worker_tree.body if isinstance(n, ast.Assign)
                                 and any(isinstance(t, ast.Name) and t.id == 'METHODS' for t in n.targets)))
    assert len(names) == 12 and len(set(names)) == 12 and set(names).issubset(current)
    lite = load('canonical_source_preflight_lite', ROOT / '.aide/scripts/aide_lite.py')
    checks = lite.validate_commit_message_text((TASK / 'evidence/source-message.txt').read_text(encoding='utf-8'))
    assert not [c for c in checks if c.severity == 'FAIL'], [(c.severity, c.message) for c in checks]
    config, _, working = workspace.load_config(ROOT / '.aide.local/lite-successor-qualification-execution.json')
    job = json.loads((TASK / 'evidence/local-job-template.json').read_bytes())
    job.update(source_commit=git('rev-parse', 'HEAD'), source_tree=git('rev-parse', 'HEAD^{tree}'))
    workspace.validate_job(job, working)
    roots = workspace.canonical_roots(config, job, ROOT)
    assert set(job['canonical_outputs']) == {'.aide/export/aide-lite-pack-v0'}
    ownership = load('canonical_source_preflight_ownership', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py')
    observed = ownership.require_same(json.loads((TASK / 'evidence/prior-export-inventory.json').read_bytes()))
    baseline = json.loads((TASK / 'evidence/baseline.json').read_bytes())['stable_assets']
    assert len(baseline) == 8 and all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h
                                      for p, h in baseline.items())
    assert set(p.relative_to(ROOT).as_posix() for p in (ROOT / '.aide/release/stable').iterdir()) == set(baseline)
    git('diff', '--check')
    record.update(state='PASS_READ_ONLY_PREFLIGHT', source_head=git('rev-parse', 'HEAD'),
                  syntax=parsed, original_methods_unchanged=len(previous), new_methods=sorted(set(current)-set(previous)),
                  selected_methods=list(names), literal_job_inputs=len(job['inputs']),
                  observed_commit_tree_substituted_only_in_preflight_copy=True,
                  config_digest=workspace.digest(config), canonical_destinations=sorted(job['canonical_outputs']),
                  recoverable_export_files=observed['file_count'], stable_assets_unchanged=len(baseline),
                  commit_message_checks=[{'severity': c.severity, 'message': c.message} for c in checks])
except BaseException as error:
    record.update(state='REFUSED', error_type=type(error).__name__, error=str(error))
    raise
finally:
    (TASK / 'evidence/source-prechecks.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
print(json.dumps({k: v for k, v in record.items() if k not in ('syntax', 'selected_methods', 'commit_message_checks')}))
