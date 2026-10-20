"""Rebind the focused dependency and successful-checkpoint recovery preconditions."""
import ast
import importlib.util
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
spec = importlib.util.spec_from_file_location('recovery_refresh_helpers', TASK / 'prepare_recovery.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    path = E / 'recovery-effect.json'
    effect = json.loads(path.read_bytes())
    for p in (E / 'delivery-effect.json', ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/update_presentation.py'):
        effect['files'][p.relative_to(ROOT).as_posix()] = h.sha(p)
    effect['controller_sha256'] = h.sha(TASK / 'resume_delivery.py')
    effect['files'] = {name: h.sha(ROOT / name) for name in effect['files']}
    path.write_bytes((json.dumps(effect, indent=2) + '\n').encode())
    path = E / 'recovery-checkpoint-inputs.json'
    pins = json.loads(path.read_bytes())
    pins['files'] = {name: h.sha(ROOT / name) for name in pins['files']}
    path.write_bytes((json.dumps(pins, indent=2) + '\n').encode())
    source, review = E / 'recovery-checkpoint-source.json', E / 'recovery-checkpoint-review.json'
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    mapped = {name: h.sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert h.git('hash-object', '--no-filters', '--', name) == h.git('hash-object', '--path=' + name, '--', name), name
    h.git('diff', '--check')
    checkpoint_effect = E / 'recovery-checkpoint-effect.json'
    source.write_bytes((json.dumps({'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name,
        'base': h.git('rev-parse', 'HEAD'), 'effect_sha256': h.sha(checkpoint_effect), 'files': mapped}, indent=2) + '\n').encode())
    print(json.dumps({'source_sha256': h.sha(source), 'effect_sha256': h.sha(checkpoint_effect),
        'controller_sha256': h.sha(TASK / 'recovery_checkpoint.py'), 'recovery_effect_sha256': h.sha(E / 'recovery-effect.json'),
        'recovery_controller_sha256': h.sha(TASK / 'resume_delivery.py'), 'mapped_files': len(mapped)}))


if __name__ == '__main__':
    main()
