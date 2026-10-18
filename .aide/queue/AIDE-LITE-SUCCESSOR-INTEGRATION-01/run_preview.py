"""Use the existing preview owner while retaining three known historical failures."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-INTEGRATION-01'
BASE = 'd8001eb81f934cda83e93ae0704f0c60aed675c7'
KNOWN = {'4bb6a4f990c5845a2141a20329168b582b37e8d8',
         '651464ae3e86b32b11080194d0d06beb88188dd4',
         'ae26a1ca80b10e87aaee2e4f68545df1c24c59ff'}
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], text=True, encoding='utf-8').strip()
owner = load('successor_preview_owner', ROOT / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner.BASE = BASE
def verify():
    lite = load('successor_preview_cli', ROOT / '.aide/scripts/aide_lite.py')
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
    commits = git('rev-list', scope).splitlines()
    malformed = {item['commit_sha'] for item in data['malformed_commits']}
    entries = {item['commit_sha'] for item in data['entries']}
    assert data['commit_count'] == len(commits) < 100
    assert data['malformed_count'] == 3 and malformed == KNOWN
    assert entries == set(commits) - KNOWN
    raw_failures = set()
    for commit, subject, message in lite.git_commit_messages_for_range(ROOT, scope, max_count=100):
        checks = lite.validate_commit_message_text(message)
        if lite.commit_message_result(checks) == 'FAIL':
            raw_failures.add(commit)
            assert lite.historical_message_is_presentation_only(message, checks)
            assert lite.commit_is_within_historical_boundary(ROOT, commit, lite.historical_presentation_boundary(ROOT))
    assert raw_failures == KNOWN
    return {'status': 'PASS', 'source_head': endpoint, 'source_range': scope,
        'commits': commits, 'malformed_count': 3, 'raw_failure_commits': sorted(raw_failures),
        'sha256s': {name: sha(root / name) for name in sorted(owner.NAMES)},
        'regeneration': 'read_only_exact_six_output_comparison',
        'historical_failures_preserved': True}
owner.verify = verify
pack = ROOT / '.aide/export/aide-lite-pack-v0'
qualified = json.loads((TASK / 'evidence/attempt-02-delivered-result.json').read_text(encoding='utf-8'))
expected_pack = qualified['after_sha256s']
def check_pack():
    actual = {p.relative_to(pack).as_posix(): sha(p) for p in pack.rglob('*') if p.is_file()}
    assert len(actual) == 870 and actual == expected_pack
check_pack()
owner.main()
check_pack()
if sys.argv[1:] == ['generate']:
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    endpoint = git('rev-parse', 'HEAD')
    for label, extra, code, result in [
            ('range-advisory', [], 0, 'PASS_WITH_WARNINGS'),
            ('range-raw', ['--no-dispositions'], 1, 'FAIL')]:
        command = [sys.executable, '-B', '.aide/scripts/aide_lite.py',
                   'commit', 'check', '--range', BASE + '..' + endpoint, *extra]
        with (output / (label + '.log')).open('xb') as stream:
            run = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=90)
        text = (output / (label + '.log')).read_text(encoding='utf-8')
        assert run.returncode == code and text.splitlines()[1] == 'result: ' + result
        lines = [line.split() for line in text.splitlines() if line.startswith('- ')]
        failures = {parts[1] for parts in lines if parts[2] != 'PASS'}
        assert failures == {commit[:7] for commit in KNOWN}
        expected_state = 'PRESENTATION_ADVISORY' if not extra else 'FAIL'
        assert all(parts[2] in {'PASS', expected_state} for parts in lines)
    print('PASS: fixed preview, three preserved raw failures and all 870 qualified pack hashes')
