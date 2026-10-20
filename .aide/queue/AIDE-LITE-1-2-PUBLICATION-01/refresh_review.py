"""Verify the focused publication-race correction and rebind preserved preparation."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode('utf-8'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    delivery = json.loads((E / 'delivery-effect.json').read_bytes())
    previous = json.loads((E / 'next-preparation.log/releases.json').read_bytes())
    tree = ast.parse((TASK / 'deliver.py').read_bytes())
    main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
    functions = [node for node in main.body if isinstance(node, ast.FunctionDef) and node.name in ('projection', 'release_list')]
    assert len(functions) == 2
    namespace = {'plan': delivery}
    exec(compile(ast.Module(body=functions, type_ignores=[]), 'actual_release_guard', 'exec'), namespace)
    outcomes = {}
    for name, values, candidate, expected in [
        ('preserved_only', previous, None, True),
        ('candidate_draft', previous + [{'id': 999999999, 'tag_name': 'aide-lite-v1.2.0'}], 999999999, True),
        ('unexpected_concurrent', previous + [{'id': 999999998, 'tag_name': 'newer-product'}], None, False),
        ('unexpected_before_latest', previous + [{'id': 999999999, 'tag_name': 'aide-lite-v1.2.0'}, {'id': 999999998, 'tag_name': 'newer-product'}], 999999999, False),
        ('duplicate_id', previous + [previous[0]], None, False),
        ('missing_predecessor', previous[:1], None, False),
    ]:
        namespace['TAG'] = 'aide-lite-v1.2.0'
        namespace['api'] = lambda label, path, response=values: copy.deepcopy(response)
        try:
            namespace['release_list'](name, candidate)
            actual = True
        except AssertionError:
            actual = False
        assert actual is expected, name
        outcomes[name] = {'accepted': actual, 'expected': expected, 'pass': True}
    save(E / 'release-guard-fixtures.json', {'state': 'PASS', 'cases': outcomes,
        'method': 'Compile the actual nested projection/release_list AST; deterministic API responses, no network effects or jobs.',
        'controller_sha256': sha(TASK / 'deliver.py'), 'original_rejection_preserved': True})
    delivery['controller_sha256'] = sha(TASK / 'deliver.py')
    delivery['files'] = {name: sha(ROOT / name) for name in delivery['files']}
    save(E / 'delivery-effect.json', delivery)
    inputs = json.loads((E / 'publication-checkpoint-inputs.json').read_bytes())
    inputs['files'] = {name: sha(ROOT / name) for name in inputs['files']}
    save(E / 'publication-checkpoint-inputs.json', inputs)
    source = E / 'publication-checkpoint-source.json'
    review = E / 'publication-checkpoint-review.json'
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    mapped = {name: sha(ROOT / name) for name in sorted(changed - excluded)}
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    effect = E / 'publication-checkpoint-effect.json'
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name,
        'base': delivery['base'], 'effect_sha256': sha(effect), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(effect),
        'controller_sha256': sha(TASK / 'checkpoint.py'), 'delivery_effect_sha256': sha(E / 'delivery-effect.json'),
        'delivery_controller_sha256': sha(TASK / 'deliver.py'), 'mapped_files': len(mapped), 'guard_fixtures': len(outcomes)}))


if __name__ == '__main__':
    main()
