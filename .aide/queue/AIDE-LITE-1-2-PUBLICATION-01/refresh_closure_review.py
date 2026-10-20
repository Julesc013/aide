"""Bind the required promotion summaries; preserve all completed qualification."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    source = E / 'closure-checkpoint-source.json'
    review = E / 'closure-checkpoint-review.json'
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    for n in mapped:
        if n.endswith('.py'):
            ast.parse((ROOT / n).read_bytes(), filename=n)
        assert git('hash-object', '--no-filters', '--', n) == git('hash-object', '--path=' + n, '--', n), n
    git('diff', '--check')
    effect = E / 'closure-checkpoint-effect.json'
    source.write_bytes((json.dumps({'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name,
        'base': git('rev-parse', 'HEAD'), 'effect_sha256': sha(effect), 'files': mapped}, indent=2) + '\n').encode())
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(effect),
        'controller_sha256': sha(TASK / 'closure_checkpoint.py'), 'mapped_files': len(mapped)}))


if __name__ == '__main__':
    main()
