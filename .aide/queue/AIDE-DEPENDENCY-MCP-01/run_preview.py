"""Existing promotion preview commands, plus read-only deterministic regeneration."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
BASE = '8f93cb7e021a5347e71d81a60aae4bd3f8d53602'
NAMES = {'CHANGELOG.preview.md', 'RELEASE_NOTES.preview.md', 'changelog.preview.json',
         'latest-changelog-report.md', 'malformed-commits.md', 'release-notes.preview.json'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    from core.execution.managed_workspace import ordinary
    files, directories, pending = {}, [], [root]
    while pending:
        directory = pending.pop()
        ordinary(directory, directory=True)
        directories.append(directory.relative_to(root).as_posix())
        for path in directory.iterdir():
            if path.is_dir():
                ordinary(path, directory=True)
                pending.append(path)
            else:
                ordinary(path)
                files[path.relative_to(root).as_posix()] = sha(path)
            if len(files) + len(directories) + len(pending) > 128:
                raise ValueError('changelog inventory exceeds bounded profile')
    return files, sorted(directories)


def verify():
    path = ROOT / '.aide/scripts/aide_lite.py'
    spec = importlib.util.spec_from_file_location('preview_readonly', path)
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    root = ROOT / '.aide/changelog'
    observed = json.loads((root / 'changelog.preview.json').read_text(encoding='utf-8'))
    endpoint = observed['source_head']
    scope = BASE + '..' + endpoint
    assert observed['source_range'] == scope and observed['preview_only'] is True
    subprocess.run(['git', 'merge-base', '--is-ancestor', endpoint, 'HEAD'], check=True)
    data = lite.make_changelog_preview(ROOT, revision_range=scope, limit=100)
    release = lite.make_release_notes_preview_data(data)
    expected = {'changelog.preview.json': lite.stable_json_text(data),
                'release-notes.preview.json': lite.stable_json_text(release),
                'CHANGELOG.preview.md': lite.render_changelog_preview(data),
                'RELEASE_NOTES.preview.md': lite.render_release_notes_preview(data, release),
                'malformed-commits.md': lite.render_malformed_commits_report(data),
                'latest-changelog-report.md': lite.render_changelog_report(data, release)}
    for name, value in expected.items():
        assert (root / name).read_bytes() == value.encode('utf-8'), name
    commits = subprocess.check_output(['git', 'rev-list', scope], text=True).splitlines()
    assert data['commit_count'] == len(commits) and data['malformed_count'] == 0
    assert {x['commit_sha'] for x in data['entries']} == set(commits)
    return {'status': 'PASS', 'source_head': endpoint, 'source_range': scope,
            'commits': commits, 'malformed_count': 0,
            'sha256s': {name: sha(root / name) for name in sorted(NAMES)},
            'regeneration': 'read_only_exact_six_output_comparison'}


def main():
    if sys.argv[1:] == ['verify']:
        print(json.dumps(verify(), indent=2))
        return
    assert sys.argv[1:] == ['generate']
    from core.execution.managed_workspace import root_path
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    root = root_path(str(ROOT / '.aide/changelog'))
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    before, directories = inventory(root)
    assert NAMES <= set(before)
    saved = output / 'prior-preview'; saved.mkdir()
    for name in NAMES:
        (saved / name).write_bytes((root / name).read_bytes())
    endpoint = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    operations = {}
    for label, args in [('preview', ['changelog', 'preview', '--range', BASE + '..' + endpoint, '--limit', '100']),
                        ('validate', ['changelog', 'validate']), ('status', ['changelog', 'status'])]:
        with (output / (label + '.log')).open('wb') as stream:
            result = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *args],
                                    stdout=stream, stderr=subprocess.STDOUT, timeout=120)
        operations[label] = {'exit_code': result.returncode, 'log_sha256': sha(output / (label + '.log'))}
        assert result.returncode == 0, label
    after, after_directories = inventory(root)
    assert directories == after_directories and set(before) == set(after)
    assert all(after[n] == h for n, h in before.items() if n not in NAMES)
    result = verify()
    assert result['source_head'] == endpoint
    result['operations'] = operations
    (output / 'preview-result.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps({'status': 'PASS', 'source_head': endpoint, 'commits': len(result['commits'])}))


if __name__ == '__main__':
    main()
