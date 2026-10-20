"""Map current immutable command witnesses; historical selectors provide no current verdict."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
EVIDENCE = TASK / 'evidence'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unpack(path):
    value = json.loads(path.read_bytes())
    compressed = base64.b64decode(value['data'], validate=True)
    assert sha(compressed) == value['gzip_sha256']
    raw = gzip.decompress(compressed)
    assert sha(raw) == value['sha256'] and len(raw) == value['uncompressed_bytes']
    files = json.loads(raw)
    assert len(files) == value['files']
    return {name: base64.b64decode(data, validate=True) for name, data in files.items()}


def command_parts(tokens):
    parts = {'positionals': []}
    key = 'positionals'
    for token in tokens:
        if token.startswith('--'):
            assert token not in parts or token == '--stream', ('duplicate option', token)
            key = token
            parts.setdefault(key, [])
        else:
            parts[key].append(token)
    return parts


def main():
    selectors = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/replacement-cli-coverage.json'
    recipes = json.loads(selectors.read_bytes())['forms']
    built = json.loads((EVIDENCE / 'build-result.json').read_bytes())
    profile = next(p for p in built['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    consumers = json.loads((EVIDENCE / 'consumer-results.json').read_bytes())
    remaining = json.loads((EVIDENCE / 'remaining-results.json').read_bytes())
    sources = {}
    for row in consumers['cases']:
        assert row['result']['status'] == 'PASS' and row['result']['fixture_retired']
        case = f"case-{row['case']:02d}"
        path = EVIDENCE / f"consumer-{case}-retained.json"
        sources[case] = (row['job_id'], path, unpack(path), consumers['subject'])
    additions = next(row for row in remaining['cases'] if row['case'] == 'additions')
    assert additions['state'] == 'PASS_ALL_EIGHTEEN_ADDITIVE_FORMS'
    path = EVIDENCE / 'remaining-additions-retained.json'
    sources['additions'] = (additions['job_id'], path, unpack(path), remaining['subject'])
    rows = []
    partial = {'job usage --attempt-set <attempt-roster-json>',
               'job effort --work-set <path>', 'job effort --work-set <path> --json'}
    for recipe in recipes:
        # The old case/path pair is a lookup recipe only. No old job, digest, argv or verdict is copied.
        form, selector = recipe['form'], recipe['evidence']
        job, path, files, subject = sources[selector['case']]
        name = 'output/' + selector['retained_output']
        raw = files[name]
        witness = json.loads(raw)
        argv = witness['argv']
        tail = argv[argv.index('--repo-root') + 2:]
        expected, actual_parts = command_parts(form.split()), command_parts(tail)
        # CLI option order is immaterial; an explicit JSON rendering may supplement the public form.
        if '--json' not in expected and actual_parts.get('--json') == []:
            del actual_parts['--json']
        assert set(expected) == set(actual_parts), (form, tail)
        for key, patterns in expected.items():
            if key == '--stream' and len(patterns) == 1:
                patterns = patterns * len(actual_parts[key])
            assert len(patterns) == len(actual_parts[key]), (form, key, tail)
            for pattern, actual in zip(patterns, actual_parts[key]):
                if pattern.startswith('<') and pattern.endswith('>'):
                    assert actual and not actual.startswith('--'), (form, pattern, actual)
                    if pattern == '<digest>':
                        assert re.fullmatch('[0-9a-f]{64}', actual)
                else:
                    assert pattern == actual, (form, pattern, actual)
        expected_exit = 2 if form in partial else (1 if form == 'task inspect' else 0)
        assert witness['exit_code'] == expected_exit, (form, witness['exit_code'])
        assert job == json.loads(files['receipt.json'])['job_id']
        rows.append({'form': form, 'status': 'OBSERVED_WITH_PRESERVED_ORIGINAL_ASSERTIONS',
                     'evidence': {'job_id': job, 'subject': subject,
                                  'bundle': path.relative_to(ROOT).as_posix(), 'bundle_sha256': sha(path.read_bytes()),
                                  'member': name, 'member_sha256': sha(raw), 'argv_tail': tail,
                                  'exit_code': witness['exit_code']},
                     'scope': 'Command observation plus preserved original semantic assertions; no universal correctness or whole-session containment claim.'})
    assert len(rows) == 56 and len({r['form'] for r in rows}) == 56
    assert {r['form'] for r in rows} == set(profile['supported_cli_forms'])
    result = {'status': 'PASS_56_CURRENT_FORM_MAPPING', 'profile': profile,
              'subject_assets': built['assets'], 'forms': rows,
              'selector_provenance': {'path': selectors.relative_to(ROOT).as_posix(), 'sha256': sha(selectors.read_bytes()),
                                      'role': 'case/path lookup only; all evidence identities and observations come from current retained bundles'},
              'remaining': 'Actual predecessor brownfield scenario, additional hosted profiles and release replay remain incomplete.'}
    destination = EVIDENCE / 'current-cli-coverage.json'
    data = (json.dumps(result, indent=2) + '\n').encode()
    if destination.exists():
        assert destination.read_bytes() == data
    else:
        destination.write_bytes(data)
    print(json.dumps({'status': result['status'], 'forms': len(rows), 'jobs': len(sources), 'support_activated': False}))


if __name__ == '__main__':
    main()
