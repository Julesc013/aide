"""Prepare a complete release preview while preserving unresolved historical failures."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01'
BASE = '0f293eb6a99dbd444bfa35016007b13451c49275'
LIMIT = 200


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify(common, lite):
    root = ROOT / '.aide/changelog'
    observed = json.loads((root / 'changelog.preview.json').read_text(encoding='utf-8'))
    endpoint = observed['source_head']
    scope = BASE + '..' + endpoint
    assert observed['source_range'] == scope and observed['preview_only'] is True
    subprocess.run(['git', 'merge-base', '--is-ancestor', endpoint, 'HEAD'], check=True)
    commits = subprocess.check_output(['git', 'rev-list', scope], text=True).splitlines()
    assert 0 < len(commits) <= LIMIT
    data = lite.make_changelog_preview(ROOT, revision_range=scope, limit=LIMIT)
    release = lite.make_release_notes_preview_data(data)
    expected = {
        'changelog.preview.json': lite.stable_json_text(data),
        'release-notes.preview.json': lite.stable_json_text(release),
        'CHANGELOG.preview.md': lite.render_changelog_preview(data),
        'RELEASE_NOTES.preview.md': lite.render_release_notes_preview(data, release),
        'malformed-commits.md': lite.render_malformed_commits_report(data),
        'latest-changelog-report.md': lite.render_changelog_report(data, release),
    }
    assert set(expected) == common.NAMES
    for name, value in expected.items():
        assert (root / name).read_bytes() == value.encode('utf-8'), name
    messages = lite.git_commit_messages_for_range(ROOT, scope, max_count=LIMIT)
    assert {row[0] for row in messages} == set(commits)
    known = json.loads((TASK / 'evidence/commit-format-records.json').read_text(encoding='utf-8'))['records']
    known = {row['commit']: row for row in known}
    assert len(known) == 3
    malformed = {row['commit_sha']: row for row in data['malformed_commits']}
    assert set(malformed) == set(known) and data['malformed_count'] == 3
    ignored, failures = [], {}
    for commit, subject, message in messages:
        parsed = lite.parse_commit_for_changelog(commit, subject, message)
        if parsed['ignored']:
            ignored.append({'commit_sha': commit, 'subject': subject})
        checks = lite.validate_commit_message_text(message)
        failed = [check.message for check in checks if check.severity == 'FAIL']
        if failed:
            failures[commit] = failed
        if commit in known:
            record = known[commit]
            assert lite.git_commit_object_facts(ROOT, commit) == {
                key: record[key] for key in ('commit', 'tree', 'parents')}
            assert lite.canonical_commit_message_sha256(message) == record['message_sha256']
            assert failed == record['failed_checks']
            assert malformed[commit]['reasons'] == record['changelog']['malformed_reasons']
    assert set(failures) == set(known)
    categorized = {row['commit_sha'] for row in data['entries']}
    assert categorized | set(malformed) | {row['commit_sha'] for row in ignored} == set(commits)
    assert data['commit_count'] == len(commits)
    assert '3 malformed or legacy commits require review' in release['warnings']
    return {
        'status': 'PASS_PREVIEW_WITH_UNRESOLVED_HISTORY',
        'source_head': endpoint, 'source_range': scope, 'commits': commits,
        'categorized_commits': sorted(categorized), 'malformed_commits': data['malformed_commits'],
        'ignored_merge_commits': ignored, 'malformed_count': 3,
        'strict_message_failures': failures, 'raw_range_result': 'FAIL',
        'owner_decision': 'pending', 'promotion_allowed': False, 'publication_performed': False,
        'sha256s': {name: common.sha(root / name) for name in sorted(common.NAMES)},
        'regeneration': 'read_only_exact_six_output_comparison',
    }


def main():
    assert sys.argv[1:] in (['generate'], ['verify'])
    common = load('existing_preview_inventory', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
    lite = load('fixed_preview_lite', ROOT / '.aide/scripts/aide_lite.py')
    if sys.argv[1:] == ['verify']:
        print(json.dumps(verify(common, lite), indent=2))
        return
    from core.execution.managed_workspace import root_path
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    root = root_path(str(ROOT / '.aide/changelog'))
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    endpoint = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    scope = BASE + '..' + endpoint
    count = int(subprocess.check_output(['git', 'rev-list', '--count', scope], text=True))
    assert 0 < count <= LIMIT
    before, directories = common.inventory(root)
    assert common.NAMES <= set(before)
    saved = output / 'prior-preview'
    saved.mkdir()
    for name in common.NAMES:
        (saved / name).write_bytes((root / name).read_bytes())
    registry = ROOT / '.aide/git/commit-message-dispositions.json'
    registry_digest = common.sha(registry)
    frozen_pack = json.loads((TASK / 'evidence/pack-subject-repaired.json').read_text(encoding='utf-8'))
    release_before = {path.relative_to(ROOT).as_posix(): common.sha(path)
                      for path in (ROOT / '.aide/release').rglob('*') if path.is_file()}
    assert len(release_before) == 53 and len(frozen_pack) == 863
    assert all(common.sha(ROOT / path) == digest for path, digest in frozen_pack.items())
    operations = {}
    for label, args, expected_exit in [
        ('preview', ['changelog', 'preview', '--range', scope, '--limit', str(LIMIT)], 0),
        ('validate', ['changelog', 'validate'], 0),
        ('status', ['changelog', 'status'], 0),
        ('raw-range', ['commit', 'check', '--range', scope, '--max-count', str(LIMIT), '--no-dispositions'], 1),
    ]:
        with (output / (label + '.log')).open('xb') as stream:
            process = subprocess.run([sys.executable, '-B', '.aide/scripts/aide_lite.py', *args],
                                     stdout=stream, stderr=subprocess.STDOUT, timeout=120)
        operations[label] = {'exit_code': process.returncode,
                             'log_sha256': common.sha(output / (label + '.log'))}
        (output / 'operations.json').write_text(json.dumps(operations, indent=2) + '\n', encoding='utf-8')
        assert process.returncode == expected_exit, label
    raw = (output / 'raw-range.log').read_text(encoding='utf-8')
    assert raw.splitlines()[1] == 'result: FAIL'
    assert set(re.findall(r'^- ([0-9a-f]{7}) FAIL ', raw, re.M)) == {'4bb6a4f', '651464a', 'ae26a1c'}
    after, after_directories = common.inventory(root)
    assert directories == after_directories and set(before) == set(after)
    assert all(after[name] == digest for name, digest in before.items() if name not in common.NAMES)
    assert common.sha(registry) == registry_digest
    assert release_before == {path.relative_to(ROOT).as_posix(): common.sha(path)
                              for path in (ROOT / '.aide/release').rglob('*') if path.is_file()}
    assert all(common.sha(ROOT / path) == digest for path, digest in frozen_pack.items())
    result = verify(common, lite)
    assert result['source_head'] == endpoint and len(result['commits']) == count
    current = output / 'generated-preview'
    current.mkdir()
    for name in common.NAMES:
        (current / name).write_bytes((root / name).read_bytes())
    result.update(operations=operations, unchanged_disposition_registry_sha256=registry_digest,
                  preserved_release_files=53, preserved_pack_files=863)
    (output / 'preview-result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'commits': count,
                      'malformed_count': 3, 'owner_decision': 'pending', 'promotion_allowed': False}))


if __name__ == '__main__':
    main()
