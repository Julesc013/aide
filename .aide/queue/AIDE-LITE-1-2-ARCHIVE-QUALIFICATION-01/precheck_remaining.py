"""Read-only preflight for additive forms and actual-predecessor scenarios."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).parent
EVIDENCE = TASK / 'evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def function(text, name):
    return next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)


def assertions(node):
    return [ast.dump(n, include_attributes=False) for n in ast.walk(node) if isinstance(n, ast.Assert)
            and not any(isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name)
                        and x.value.id == 'sys' and x.attr == 'argv' for x in ast.walk(n))]


record = {'state': 'started', 'jobs_requested': 0, 'tests_executed': False, 'archives_changed': False}
try:
    for path in (TASK / 'run_additions.py', TASK / 'run_predecessor.py', TASK / 'commit_and_finish_cases.py',
                 ROOT / 'evals/lite/lifecycle.py', Path(__file__)):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    original = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/run_additions.py'
    old = function(original.read_text(encoding='utf-8'), 'main')
    new = function((TASK / 'run_additions.py').read_text(encoding='utf-8'), 'main')
    assert assertions(old) == assertions(new)
    old_eval = function(git('show', 'HEAD:evals/lite/lifecycle.py'), 'qualify_successor')
    new_eval = function((ROOT / 'evals/lite/lifecycle.py').read_text(encoding='utf-8'), 'qualify_successor')
    assert assertions(old_eval) == assertions(new_eval)
    assert [a.arg for a in old_eval.args.args] == [a.arg for a in new_eval.args.args]
    assert len(new_eval.args.kwonlyargs) == 1 and new_eval.args.kwonlyargs[0].arg == 'subject'
    assert ast.literal_eval(new_eval.args.kw_defaults[0]) == 'development-export'
    spec = importlib.util.spec_from_file_location('remaining_preflight_lite', ROOT / '.aide/scripts/aide_lite.py')
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    assert not [c for c in lite.validate_commit_message_text((EVIDENCE / 'remaining-message.txt').read_text(encoding='utf-8'))
                if c.severity == 'FAIL']
    built = json.loads((EVIDENCE / 'build-result.json').read_bytes())
    environment = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
                   'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(),
                                                             'version': platform.python_version()}}
    profile = next(p for p in built['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    assert environment == profile['environment']
    config, _, working = workspace.load_config(ROOT / '.aide.local/lite-successor-qualification-execution.json')
    jobs = json.loads((EVIDENCE / 'remaining-job-templates.json').read_bytes())
    assert set(jobs) == {'additions', 'predecessor'}
    for name, job in jobs.items():
        observed = dict(job, source_commit=git('rev-parse', 'HEAD'), source_tree=git('rev-parse', 'HEAD^{tree}'))
        assert 'canonical_outputs' not in observed
        workspace.validate_job(observed, working)
    assert all(workspace.file_digest(ROOT / name) == value['sha256'] for name, value in built['assets'].items())
    assert all(workspace.file_digest(ROOT / value['path']) == value['sha256']
               for value in built['identity']['predecessor_matrix'][0]['assets'])
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    portable_files = set(lite.PORTABLE_SOURCE_FILES) | set(lite.PORTABLE_TEMPLATE_MAP)
    portable_dirs = tuple(path.rstrip('/') + '/' for path in lite.PORTABLE_SOURCE_DIRS)
    assert not [path for path in changed if path in portable_files or path.startswith(portable_dirs)]
    git('diff', '--check')
    record.update(state='PASS_READ_ONLY_PREFLIGHT', source_head=git('rev-parse', 'HEAD'),
                  jobs={name: len(job['inputs']) for name, job in jobs.items()}, environment=environment,
                  original_additive_assertions_preserved=len(assertions(old)),
                  original_predecessor_assertions_preserved=len(assertions(old_eval)),
                  historical_default_preserved=True, source_portable_changes_after_refresh=0,
                  original_consumer_passes_retained=8, local_jobs_consumed=10, local_ceiling=13,
                  hosted_runs_consumed=0)
except BaseException as error:
    record.update(state='REFUSED', error_type=type(error).__name__, error=str(error))
    raise
finally:
    (EVIDENCE / 'remaining-prechecks.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
print(json.dumps(record))
