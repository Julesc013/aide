"""Preserve the stopped attempt and prepare continuation of its exact existing draft."""
import ast
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
QE = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/evidence'
PRIOR = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode('utf-8'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replace(text, before, after):
    assert text.count(before) == 1, before[:100]
    return text.replace(before, after)


def main():
    original = json.loads((E / 'delivery-effect.json').read_bytes())
    stopped = json.loads((E / 'delivery-result.log').read_bytes())
    assert stopped['status'] == 'STOPPED_RECONCILE'
    assert stopped['failure'] == 'Draft creation needs exact ID reconciliation'
    base = stopped['commit']
    assert git('rev-parse', 'HEAD') == base and not git('diff', '--name-only')
    assert git('ls-files', '--others', '--exclude-standard').splitlines() == [(TASK / 'prepare_recovery.py').relative_to(ROOT).as_posix()]
    draft_list = json.loads((E / 'draft-reconciliation.log/api.stdout').read_bytes())
    draft = next(value for value in draft_list if value['id'] == 418708655)
    assert draft['draft'] and not draft['assets'] and draft['tag_name'] == 'aide-lite-v1.2.0'
    assert draft['target_commitish'] == base and draft['body'] == (TASK / 'release-notes.md').read_text(encoding='utf-8')
    save(E / 'recovery-draft-before.json', draft)
    h = load('recovery_preservation', QE.parent / 'collect_hosted.py')
    h.E = E
    verify = load('recovery_roundtrip', QE.parent / 'verify_profile_collection.py')
    verify.E = E
    files = {'delivery-result.log': (E / 'delivery-result.log').read_bytes()}
    checkpoints = []
    for folder in (E / 'publication-checkpoint-attempt-01.log',):
        record = json.loads((folder / 'result.json').read_bytes())
        assert record['status'] == 'PASS' and record['commit'] == base
        checkpoints.append((record, folder))
        files[folder.name + '/result.json'] = (folder / 'result.json').read_bytes()
    operations = streams = 0
    for record, folder in [(stopped, E), *checkpoints]:
        for row in record['operations']:
            assert row.get('status', row.get('state')).lower() == 'completed' and row['exit_code'] == 0
            operations += 1
            for name, identity in row['streams'].items():
                path = folder / name
                assert path.stat().st_size == identity['bytes'] and sha(path) == identity['sha256']
                key = (folder.name + '/' if folder != E else '') + name
                assert key not in files
                files[key] = path.read_bytes()
                streams += 1
    for path in sorted((E / 'draft-reconciliation.log').iterdir()):
        files['draft-reconciliation.log/' + path.name] = path.read_bytes()
    h.preserve(E / 'stopped-delivery-retained.json', {name: base64.b64encode(raw).decode('ascii') for name, raw in files.items()})
    assert verify.restore(E / 'stopped-delivery-retained.json') == files
    save(E / 'stopped-delivery-verified.json', {'state': 'STOPPED_AFTER_EXISTING_DRAFT_CREATION',
        'lossless_roundtrip_verified': True, 'operations': operations, 'streams': streams, 'files': len(files),
        'tag_target': base, 'tag_object': stopped['tag_object'], 'draft_id': draft['id'],
        'assets_uploaded': 0, 'published': False, 'consumer_allocations': 0,
        'interpretation': 'Immediate list returned only prior rows; fresh no-cache/alternate-page read plus CLI list identify the existing exact empty draft. Cache or consistency cause unproven; do not repeat creation.'})
    text = (PRIOR / 'resume_delivery.py').read_text(encoding='utf-8').replace('v1.1.0', 'v1.2.0').replace('AIDE Lite 1.1.0', 'AIDE Lite 1.2.0')
    text = replace(text, '    task_remote = plan["release_target"]', '    task_remote = None')
    text = replace(text, '        for name, value in original["preserved_local_refs"].items():\n            assert git(label + "-preserved-" + name.split("/")[-1], "rev-parse", name) == value',
        '        for number, (name, value) in enumerate(original["preserved_local_refs"].items()):\n            assert git(label + "-preserved-" + str(number), "rev-parse", name) == value')
    text = replace(text, 'assert git(label + "-" + name, "rev-parse", name) == plan["release_target"]', 'assert git(label + "-" + name, "rev-parse", name) == args.commit')
    text = text.replace('"refs/heads/dev": plan["release_target"]', '"refs/heads/dev": args.commit').replace('"refs/heads/main": plan["release_target"]', '"refs/heads/main": args.commit')
    text = replace(text, '        text = git(label + "-remote",', '        expected = {key: value for key, value in expected.items() if value is not None}\n        text = git(label + "-remote",')
    text = replace(text, 'spec_from_file_location("existing_release_projection", TASK / "update_presentation.py")',
        'spec_from_file_location("existing_release_projection", ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/update_presentation.py")')
    text = replace(text, '"X-GitHub-Api-Version: 2026-03-10", "repos/Julesc013/aide" + endpoint',
        '"X-GitHub-Api-Version: 2026-03-10", "-H", "Cache-Control: no-cache", "repos/Julesc013/aide" + endpoint')
    text = replace(text, 'assert isinstance(values, list) and len(values) == 2', 'assert isinstance(values, list) and len(values) < 100')
    a = text.index('        assert {row["id"] for row in values} ==')
    b = text.index('\n    endpoint = ', a)
    text = text[:a] + '''        assert {row['id'] for row in values} == {plan['release_id'], *[old['id'] for old in original['previous_releases']]}
        assert len({row['id'] for row in values}) == len(values)
        for old in original['previous_releases']:
            actual = next(row for row in values if row['id'] == old['id'])
            assert projection.projection(actual) == old

''' + text[b:]
    text = replace(text, 'values = api(label, "/releases?per_page=100")', 'values = api(label, "/releases?per_page=99")')
    text = replace(text, '            git("push-recovery-checkpoint", "push", "origin", args.commit + ":refs/heads/" + original["task_branch"])\n            task_remote = args.commit\n', '')
    anchor = '    assert sha(Path(__file__)) == plan["controller_sha256"]'
    text = replace(text, anchor, anchor + '''
    review = json.loads((EVIDENCE / 'recovery-checkpoint-review.json').read_bytes())
    assert review['decision'] == 'ACCEPT' and not review['required_fixes']
    assert review['reviewer'] == '/root/review_disked_continuation'
    assert review['recovery_effect_sha256'] == args.effect_sha256
    assert review['recovery_controller_sha256'] == sha(Path(__file__))
    assert review['support_activation'] == 'exact_four_declared_T3_L1_companion_profiles_only'
''')
    text = replace(text, 'record.update(status="PUBLISHED_ACQUIRED_CONSUMER_PENDING", published=published, acquired=identities,',
        'record.update(status="PUBLISHED_ACQUIRED_CONSUMER_PENDING", published=published, acquired=identities,\n                          support_activation="exact_four_declared_T3_L1_companion_profiles_only",')
    (TASK / 'resume_delivery.py').write_bytes(text.encode('utf-8'))
    (TASK / 'recovery_checkpoint.py').write_bytes((TASK / 'checkpoint.py').read_bytes().replace(b'publication-checkpoint', b'recovery-checkpoint').replace(b'publication-projection', b'recovery-projection'))
    plan = {'controller_sha256': sha(TASK / 'resume_delivery.py'), 'release_id': draft['id'], 'release_target': base,
        'tag_object': stopped['tag_object'], 'files': original['files'] | {(TASK / 'resume_delivery.py').relative_to(ROOT).as_posix(): sha(TASK / 'resume_delivery.py')},
        'effect': 'Resume only existing empty draft418708655: upload four original labelled assets, verify, publish and acquire. No creation, tag or asset replacement. New recovery source checkpoint may advance dev/main while immutable tag target stays ee36a934.',
        'maximum_seconds': 480, 'new_releases': 0, 'consumer_allocations': 0,
        'stopped_receipt_sha256': sha(E / 'delivery-result.log'), 'observed_draft_sha256': sha(E / 'recovery-draft-before.json')}
    save(E / 'recovery-effect.json', plan)
    # Record actual progress without claiming publication.
    status = TASK / 'status.yaml'
    status.write_bytes((status.read_text(encoding='utf-8') + 'tag_created: aide-lite-v1.2.0\ntag_target: ' + base + '\ndraft_id: 418708655\ndelivery_state: stopped_before_upload_existing_empty_draft_verified\n').encode())
    p = ROOT / 'IMPLEMENT.md'
    s = p.read_text(encoding='utf-8'); pos = s.index('\n\n') + 2
    p.write_bytes((s[:pos] + '### Existing Lite 1.2 draft reconciliation - 21 October 2026\n\nPre-tag checkpoint `ee36a934` reached local/remote dev/main. Annotated tag `d2accd1e` points there. Draft creation succeeded, but the immediate list omitted the new row, so the controller stopped before upload. A fresh read-only no-cache/alternate-page API observation and CLI list identify exact empty draft `418708655`; the cause of the earlier stale view is unproven. All completed operations and streams are losslessly retained. Recovery resumes that draft only; no duplicate creation, retag, rebuild or qualification restart.\n\n' + s[pos:]).encode())
    prior = json.loads((E / 'publication-checkpoint-effect.json').read_bytes())
    refs = {r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()}
    effect = dict(prior, base=base, main_base=base, source_parent=base, source_commits=[], all_refs=refs,
        controller_sha256=sha(TASK / 'recovery_checkpoint.py'), attempt_directory='recovery-checkpoint-attempt-01.log',
        effects=['One exact recovery evidence checkpoint and guarded dev/main FF/nonforce sync; tag and assets immutable.'])
    save(E / 'recovery-checkpoint-effect.json', effect)
    inputs = json.loads((E / 'publication-checkpoint-inputs.json').read_bytes())
    inputs['files'] = {name: sha(ROOT / name) for name in inputs['files']}
    save(E / 'recovery-checkpoint-inputs.json', inputs)
    message = ('fix(release): resume the verified existing Lite 1.2 draft\n\n'
        '- Preserve the stopped delivery, successful pre-tag sync and all raw operation streams.\n'
        '- Reconcile the existing empty draft by exact ID; retain the immutable tag and original assets.\n'
        '- Prepare bounded existing-owner upload/publication/acquisition without repeating creation.\n\n'
        'Validation: PASS - prior source checks and independent qualification retained; exact fresh draft/body/target and complete receipt roundtrip verified.\n'
        'Changelog: Fixed: recover a stopped release-list observation without duplicating a draft\n'
        'Risk: The immediate stale-list cause is unproven; uncertain effects still stop for reconciliation.\n'
        'Follow-up: Publish the existing draft, acquire exact assets, then run one original acquired-byte consumer.\n'
        'AIDE-Task: AIDE-LITE-1-2-PUBLICATION-01\nAIDE-Format: compact-v1\n')
    (E / 'recovery-checkpoint-message.txt').write_bytes(message.encode())
    lite = load('recovery_preparation_lite', ROOT / '.aide/scripts/aide_lite.py')
    assert not [c for c in lite.validate_commit_message_text(message) if c.severity == 'FAIL']
    source, review = E / 'recovery-checkpoint-source.json', E / 'recovery-checkpoint-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    for name in mapped:
        if name.endswith('.py'):
            ast.parse((ROOT / name).read_bytes(), filename=name)
        assert git('hash-object', '--no-filters', '--', name) == git('hash-object', '--path=' + name, '--', name), name
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': base,
        'effect_sha256': sha(E / 'recovery-checkpoint-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'recovery-checkpoint-effect.json'),
        'controller_sha256': sha(TASK / 'recovery_checkpoint.py'), 'recovery_effect_sha256': sha(E / 'recovery-effect.json'),
        'recovery_controller_sha256': sha(TASK / 'resume_delivery.py'), 'mapped_files': len(mapped), 'operations': operations, 'streams': streams}))


if __name__ == '__main__':
    main()
