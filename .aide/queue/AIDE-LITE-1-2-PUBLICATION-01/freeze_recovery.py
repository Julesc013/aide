"""Finish the retained preparation after correcting its source-only import helper."""
import ast
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
spec = importlib.util.spec_from_file_location('recovery_freezer', TASK / 'prepare_recovery.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def main():
    assert h.git('rev-parse', 'HEAD') == 'ee36a9342e17a4c13378bd9ac034c506056f6de2'
    lite = h.load('recovery_freeze_lite', ROOT / '.aide/scripts/aide_lite.py')
    message = (E / 'recovery-checkpoint-message.txt').read_text(encoding='utf-8')
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    inputs_path = E / 'recovery-checkpoint-inputs.json'
    inputs = json.loads(inputs_path.read_bytes())
    inputs['files'] = {n: h.sha(ROOT / n) for n in inputs['files']}
    inputs_path.write_bytes((json.dumps(inputs, indent=2) + '\n').encode())
    source, review = E / 'recovery-checkpoint-source.json', E / 'recovery-checkpoint-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    changed = set(h.git('diff', '--name-only').splitlines()) | set(h.git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: h.sha(ROOT / n) for n in sorted(changed - excluded)}
    for n in mapped:
        if n.endswith('.py'):
            ast.parse((ROOT / n).read_bytes(), filename=n)
        assert h.git('hash-object', '--no-filters', '--', n) == h.git('hash-object', '--path=' + n, '--', n), n
    h.git('diff', '--check')
    effect = E / 'recovery-checkpoint-effect.json'
    h.save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name,
        'base': h.git('rev-parse', 'HEAD'), 'effect_sha256': h.sha(effect), 'files': mapped})
    print(json.dumps({'source_sha256': h.sha(source), 'effect_sha256': h.sha(effect),
        'controller_sha256': h.sha(TASK / 'recovery_checkpoint.py'), 'recovery_effect_sha256': h.sha(E / 'recovery-effect.json'),
        'recovery_controller_sha256': h.sha(TASK / 'resume_delivery.py'), 'mapped_files': len(mapped)}))


if __name__ == '__main__':
    main()
