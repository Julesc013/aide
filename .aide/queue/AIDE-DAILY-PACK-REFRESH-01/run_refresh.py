"""Reviewed task-local exporter/validator orchestration; no new resource owner."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import unittest

from pack_inventory import REPO, PACK_REL, EXCLUDED, require_same


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory_bytes(root):
    return {path.relative_to(root).as_posix(): sha(path)
            for path in sorted(root.rglob('*')) if path.is_file()}


def invoke(label, command, output):
    stdout, stderr = output / (label + '.stdout'), output / (label + '.stderr')
    with stdout.open('xb') as out, stderr.open('xb') as err:
        result = subprocess.run(command, cwd=REPO, stdin=subprocess.DEVNULL,
                                stdout=out, stderr=err, timeout=120)
    record = {'exit_code': result.returncode,
              'stdout_bytes': stdout.stat().st_size, 'stdout_sha256': sha(stdout),
              'stderr_bytes': stderr.stat().st_size, 'stderr_sha256': sha(stderr)}
    print(json.dumps({'stage': label, **record}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('phase', choices=('refresh', 'replay'))
    parser.add_argument('--inventory', required=True)
    parser.add_argument('--inventory-sha256', required=True)
    args = parser.parse_args()
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    import test_pack_inventory
    tests = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(test_pack_inventory))
    test_record = {'tests_run': tests.testsRun, 'failures': len(tests.failures),
                   'errors': len(tests.errors), 'skips': len(tests.skipped)}
    (output / 'ownership-tests.json').write_text(json.dumps(test_record, sort_keys=True) + '\n', encoding='utf-8')
    if tests.testsRun != 6 or not tests.wasSuccessful() or tests.skipped:
        raise AssertionError('six ownership checks must pass before any export reset')
    expected_path = REPO / args.inventory
    if sha(expected_path) != args.inventory_sha256:
        raise ValueError('reviewed ownership inventory changed')
    expected = json.loads(expected_path.read_text(encoding='utf-8'))
    observed = require_same(expected)
    root = Path(observed['root'])
    before = {name: value['sha256'] for name, value in observed['files'].items()}
    release_root = REPO / '.aide/release/stable'
    release_names = ['aide-lite-v1.0.0.zip', 'aide-lite-v1.0.0.tar.gz',
                     'aide-lite-v1.0.0.manifest.json', 'aide-lite-v1.0.0.SHA256SUMS.txt']
    prior_release = {name: sha(release_root / name) for name in release_names}
    preservation = output / 'prior-metadata'
    preservation.mkdir()
    for name in sorted(EXCLUDED):
        (preservation / name).write_bytes((root / name).read_bytes())
    record = {'schema': 'aide.derived-export-qualification.v1', 'phase': args.phase,
              'job_id': os.environ['AIDE_JOB_ID'], 'status': 'INCOMPLETE',
              'before_files': len(before), 'before_metadata': {name: before[name] for name in EXCLUDED},
              'prior_git_commit': observed['git_commit'], 'models_requested': 0,
              'archives_changed': None, 'filesystem_containment_claimed': False,
              'operations': {}}
    record['ownership_tests'] = test_record
    record['published_release_before'] = prior_release
    result_path = output / 'qualification.json'
    try:
        # Recheck complete ownership immediately before unchanged reset/export.
        # Coordination is trusted; this is not a malicious-writer isolation claim.
        require_same(expected)
        for command in ('export-pack', 'doctor', 'validate', 'pack-status'):
            result = invoke(command, [sys.executable, '-B', str(REPO / '.aide/scripts/aide_lite.py'), command], output)
            record['operations'][command] = result
            if result['exit_code']:
                raise AssertionError(command + ' failed; original full output retained')
        after = inventory_bytes(root)
        record['after_files'] = len(after)
        record['after_bytes'] = sum(path.stat().st_size for path in root.rglob('*') if path.is_file())
        record['after_sha256s'] = after
        record['byte_equality'] = before == after
        record['published_release_after'] = {name: sha(release_root / name) for name in release_names}
        record['archives_changed'] = record['published_release_after'] != prior_release
        if record['archives_changed']:
            raise AssertionError('published release bytes changed outside this effect')
        if args.phase == 'replay' and not record['byte_equality']:
            raise AssertionError('frozen clean export replay changed bytes')
        record['status'] = 'PASS'
    except Exception as error:
        record['status'] = 'FAIL_PRESERVED'
        record['error'] = {'type': type(error).__name__, 'message': str(error)}
        raise
    finally:
        if 'published_release_after' not in record:
            try:
                record['published_release_after'] = {name: sha(release_root / name) for name in release_names}
                record['archives_changed'] = record['published_release_after'] != prior_release
            except Exception as comparison_error:
                record['archives_changed'] = None
                record['release_comparison_error'] = {
                    'type': type(comparison_error).__name__, 'message': str(comparison_error)}
                # Keep the original operation failure, including its traceback.
        result_path.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n',
                               encoding='utf-8', newline='\n')
        print(json.dumps({key: record.get(key) for key in ('status', 'phase', 'byte_equality')}), flush=True)


if __name__ == '__main__':
    main()
