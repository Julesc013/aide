"""Read-only dev checkpoint preflight and task-local preview; no Git effects."""
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


record = {'state': 'started', 'jobs_requested': 0, 'git_effects': False, 'release_effects': False}
try:
    plan = json.loads((EVIDENCE / 'dev-effect.json').read_bytes())
    for path in (TASK / 'sync_dev.py', TASK / 'collect_consumers.py', Path(__file__)):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    lite = load('dev_preflight_lite', ROOT / '.aide/scripts/aide_lite.py')
    checks = lite.validate_commit_message_text((EVIDENCE / 'dev-message.txt').read_text(encoding='utf-8'))
    assert not [c for c in checks if c.severity == 'FAIL']
    assert all(sha(ROOT / name) == value for name, value in plan['stable_assets'].items())
    pins = json.loads((EVIDENCE / 'package-inputs.json').read_bytes())['files']
    assert all(sha(ROOT / name) == value for name, value in pins.items())
    config, roots, _ = workspace.load_config(ROOT / '.aide.local/execution.json')
    assert workspace.digest(config) == plan['control_config_digest']
    assert workspace.dispatch_state(roots['control'])['mode'] == 'running'
    assert not (roots['control'] / 'active.json').exists()
    assert git('rev-parse', 'HEAD') == plan['source_parent']
    assert git('branch', '--show-current') == plan['task_branch']
    assert git('rev-list', plan['base'] + '..HEAD').splitlines() == plan['source_commits']
    observed = dict(line.split()[::-1] for line in git('ls-remote', '--heads', 'origin', 'dev', 'main').splitlines())
    assert observed == {'refs/heads/dev': plan['base'], 'refs/heads/main': plan['base']}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    portable_files = set(lite.PORTABLE_SOURCE_FILES) | set(lite.PORTABLE_TEMPLATE_MAP)
    portable_dirs = tuple(path.rstrip('/') + '/' for path in lite.PORTABLE_SOURCE_DIRS)
    assert not [path for path in changed if path in portable_files or path.startswith(portable_dirs)]
    controller = load('dev_preflight_projection', TASK / 'sync_dev.py')
    record['preview_sha256s'] = controller.project_preview(lite, plan['base'], plan['source_parent'], 'preflight',
                                                         plan['canonical_preimages'], plan['source_commits'][1:])
    commands = []
    for args in [('doctor',), ('validate',), ('pack-status',),
                 ('commit', 'check', '--range', plan['base'] + '..' + plan['source_parent'])]:
        result = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *args], cwd=ROOT,
                                stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
        row = {'args': list(args), 'exit_code': result.returncode, 'streams': {},
               'tail': result.stdout.decode('utf-8', errors='replace').splitlines()[-5:]}
        for name in ('stdout', 'stderr'):
            raw = getattr(result, name)
            row['streams'][name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                                    'base64': base64.b64encode(raw).decode('ascii')}
        commands.append(row)
        record['commands'] = commands
        assert result.returncode == 0, row['tail']
    git('diff', '--check')
    record.update(state='PASS_READ_ONLY_PREFLIGHT', package_pins=len(pins), source_commits=3,
                  stable_assets=12, main_preserved=plan['base'], consumer_cases_passed=8,
                  source_portable_changes_after_refresh=0, task_branch_retained=True)
except BaseException as error:
    record.update(state='REFUSED', error_type=type(error).__name__, error=str(error))
    raise
finally:
    (EVIDENCE / 'dev-prechecks.json').write_bytes((json.dumps(record, indent=2) + '\n').encode())
print(json.dumps({k: v for k, v in record.items() if k not in ('commands', 'preview_sha256s')}))
