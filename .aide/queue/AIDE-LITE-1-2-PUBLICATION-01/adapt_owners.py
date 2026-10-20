"""Adapt the accepted prior release owners; no new runtime or scheduler."""
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
QUAL = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
PRIOR = ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01'


def replace(text, before, after):
    assert text.count(before) == 1, before[:100]
    return text.replace(before, after)


def write(name, text):
    path = TASK / name
    assert not path.exists(), path
    path.write_bytes(text.encode('utf-8'))


def main():
    text = (QUAL / 'sync_qualified.py').read_text(encoding='utf-8')
    text = text.replace('qualified-integration', 'publication-checkpoint').replace('qualified-projection', 'publication-projection')
    text = replace(text, 'EVIDENCE = TASK / "evidence"', 'EVIDENCE = TASK / "evidence"\nQE = ROOT / ".aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/evidence"')
    for name in ('qualification-closure-review.json', 'qualification-closure-proposal.json', 'final-qualified.json', 'profile-build-result.json'):
        text = text.replace("EVIDENCE / '" + name + "'", "QE / '" + name + "'")
    text = replace(text, "assert proof['subject']['commit'] == plan['source_parent']", "assert proof['subject']['commit'] == plan['qualification_source']")
    write('checkpoint.py', text)
    text = (PRIOR / 'acquire.py').read_text(encoding='utf-8').replace('v1.1.0', 'v1.2.0')
    text = replace(text, "receipt_path.write_text(json.dumps(receipt, indent=2) + '\\n', encoding='utf-8')", "receipt_path.write_bytes((json.dumps(receipt, indent=2) + '\\n').encode('utf-8'))")
    write('acquire.py', text)
    text = (PRIOR / 'run_acquired_consumer.py').read_text(encoding='utf-8')
    text = text.replace('AIDE-LITE-SUCCESSOR-PUBLICATION-01', TASK.name).replace('v1.1.0', 'v1.2.0')
    text = replace(text, 'AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/build-result-repaired.json', 'AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/evidence/profile-build-result.json')
    text = replace(text, 'timeout=600)', 'timeout=540)')
    text = replace(text, "path.write_text(json.dumps(value, indent=2) + '\\n', encoding='utf-8')", "path.write_bytes((json.dumps(value, indent=2) + '\\n').encode('utf-8'))")
    write('run_acquired_consumer.py', text)
    text = (PRIOR / 'deliver.py').read_text(encoding='utf-8').replace('v1.1.0', 'v1.2.0').replace('AIDE Lite 1.1.0', 'AIDE Lite 1.2.0')
    text = replace(text, 'state = {"dev": plan["base"], "main": plan["base"],', 'state = {"dev": args.commit, "main": args.commit,')
    start = text.index('        refs = git(label, "ls-remote"')
    end = text.index('        observed = ', start)
    text = text[:start] + ('        refs = git(label, "ls-remote", "--heads", "--tags", "origin",\n'
        '                   "refs/heads/dev", "refs/heads/main", "refs/heads/" + plan["task_branch"],\n'
        '                   *plan["preserved_remote_refs"], "refs/tags/" + TAG, "refs/tags/" + TAG + "^{}")\n') + text[end:]
    text = replace(text, '        if "tag_object" in record:', '        expected = {key: value for key, value in expected.items() if value is not None}\n        if "tag_object" in record:')
    start = text.index('    def release_list(')
    end = text.index('    try:\n        with workspace.estate_lock', start)
    text = text[:start] + '''    def projection(release):
        keys = ['id', 'tag_name', 'name', 'body', 'draft', 'prerelease', 'published_at', 'target_commitish', 'immutable']
        asset_keys = ['id', 'name', 'label', 'size', 'digest', 'state', 'browser_download_url']
        return {**{key: release.get(key) for key in keys}, 'assets': sorted(
            [{key: item.get(key) for key in asset_keys} for item in release['assets']], key=lambda item: item['id'])}

    def release_list(label, candidate=None):
        values = api(label, '/releases?per_page=100')
        assert isinstance(values, list) and len(values) < 100, 'Incomplete release enumeration'
        by_id = {value['id']: value for value in values}
        assert len(by_id) == len(values)
        expected_ids = {previous['id'] for previous in plan['previous_releases']}
        if candidate is not None:
            expected_ids.add(candidate)
        assert set(by_id) == expected_ids, 'Release set changed; reconcile before publication'
        for previous in plan['previous_releases']:
            assert projection(by_id[previous['id']]) == previous, 'Historical release changed'
        matches = [value for value in values if value['tag_name'] == TAG]
        assert [value['id'] for value in matches] == ([] if candidate is None else [candidate])
        return values

''' + text[end:]
    start = text.index('            for branch in ("dev", "main"):\n                guards("pre-"')
    end = text.index('            guards("pre-tag")', start)
    text = text[:start] + ('            checkpoint = json.loads((EVIDENCE / "publication-checkpoint-attempt-01.log/result.json").read_bytes())\n'
        '            assert checkpoint["status"] == "PASS" and checkpoint["commit"] == args.commit\n'
        '            assert checkpoint["tree"] == args.tree and checkpoint["refs"] == state | {"task_remote": None} if False else checkpoint["refs"] == {"dev": args.commit, "main": args.commit}\n'
        '            record["checkpoint_preview_sha256s"] = checkpoint["preview_sha256s"]\n'
        '            save()\n') + text[end:]
    # Exact verdict is part of the committed reviewed packet, not inferred from delegation.
    anchor = '    assert sha(Path(__file__)) == plan["controller_sha256"]'
    text = replace(text, anchor, anchor + '''
    verdict = json.loads((EVIDENCE / 'publication-checkpoint-review.json').read_bytes())
    assert verdict['decision'] == 'ACCEPT' and not verdict['required_fixes']
    assert verdict['reviewer'] == '/root/review_disked_continuation'
    assert verdict['delivery_effect_sha256'] == args.effect_sha256
    assert verdict['delivery_controller_sha256'] == sha(Path(__file__))
    assert verdict['support_activation'] == 'exact_four_declared_T3_L1_companion_profiles_only'
''')
    text = replace(text, '            assert lite("validate-before", "validate").splitlines()[1] == "status: PASS"',
        '            spec = importlib.util.spec_from_file_location("publication_checkpoint_owner", TASK / "checkpoint.py")\n'
        '            owner = importlib.util.module_from_spec(spec)\n            spec.loader.exec_module(owner)\n'
        '            owner.validate_source_output(lite("validate-before", "validate"))')
    text = replace(text, 'git("push-tag", "push", "origin",', 'git("push-tag", "push", "--no-follow-tags", "origin",')
    text = replace(text, '        for path, expected in plan["files"].items():',
        '        for flags in (("--all",), ("--push", "--all")):\n'
        '            assert git(label + "-url-" + str(len(flags)), "remote", "get-url", *flags, "origin") == plan["remote_url"]\n'
        '        for path, expected in plan["files"].items():')
    text = replace(text, '            assert checkpoint["tree"] == args.tree and checkpoint["refs"] == state | {"task_remote": None} if False else checkpoint["refs"] == {"dev": args.commit, "main": args.commit}',
        '            assert checkpoint["tree"] == args.tree and checkpoint["refs"] == {"dev": args.commit, "main": args.commit}')
    write('deliver.py', text)
    print('PASS: adapted existing checkpoint, publication, acquisition and original consumer owners')


if __name__ == '__main__':
    main()
