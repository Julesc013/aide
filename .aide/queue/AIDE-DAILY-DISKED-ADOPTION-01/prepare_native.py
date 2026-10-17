"""Prepare exact native adoption postimages in owned scratch; never edit DiskEd."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import time
import zipfile

TASK = Path(__file__).resolve().parent
ORIGINAL = TASK.parent / 'AIDE-DAILY-DISKED-EXPORT-01'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def ordinary(path, *, expected_links=1):
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        assert not stat.S_ISLNK(info.st_mode)
        assert not getattr(info, 'st_file_attributes', 0) & 0x400
    assert path.is_file() and path.stat().st_nlink == expected_links


def main():
    began = time.monotonic()
    inputs = read(ORIGINAL / 'evidence/native-fixture-inputs.json')
    plan = read(TASK / 'evidence/preparation-inputs.json')
    acquisition = read(ORIGINAL / 'evidence/acquisition-result.json')
    prior = read(ORIGINAL / 'evidence/native-first-attempt-result.json')
    target = Path(plan['target'])
    scratch, output = map(Path, (os.environ['AIDE_JOB_TMP'], os.environ['AIDE_JOB_OUTPUT']))
    project, deps = scratch / 'native-project', scratch / 'native-dependencies'
    project.mkdir(); deps.mkdir()
    git = Path(inputs['git_executable'])
    # This pinned installed Git binary has two installer-created hard links.
    # Source, dependency and evidence inputs retain the single-link requirement.
    ordinary(git, expected_links=2)
    assert sha(git) == inputs['git_executable_sha256']
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL', GIT_TERMINAL_PROMPT='0')

    def check_target():
        def observe(*args):
            return subprocess.check_output([str(git), '-C', str(target), *args],
                                           env=env, text=True, timeout=20).strip()
        assert observe('rev-parse', 'HEAD') == plan['base_revision']
        assert not observe('status', '--porcelain')
        for relative, expected in inputs['files'].items():
            path = target / relative
            ordinary(path)
            assert path.stat().st_size == expected['bytes'] and sha(path) == expected['sha256'], relative

    check_target()
    assert acquisition['status'] == 'PASS' and acquisition['collection_retirement_verified']
    assert sha(Path(acquisition['retained']) / 'receipt.json') == acquisition['receipt_sha256']
    expanded = 0
    for wheel in acquisition['wheels']:
        path = Path(acquisition['retained']) / 'output' / wheel['filename']
        ordinary(path)
        assert sha(path) == wheel['sha256'] and path.stat().st_size == wheel['bytes']
        with zipfile.ZipFile(path) as archive:
            seen = set()
            for member in archive.infolist():
                parts = PurePosixPath(member.filename).parts
                assert parts and not member.filename.startswith('/')
                assert all(p not in ('.', '..') and ':' not in p and '\\' not in p for p in parts)
                assert not stat.S_ISLNK(member.external_attr >> 16)
                assert not any(p.endswith('.data') for p in parts)
                assert member.filename.casefold() not in seen
                seen.add(member.filename.casefold())
                expanded += member.file_size
                assert expanded <= 8 * 1024 * 1024
                destination = deps.joinpath(*parts)
                assert destination.resolve().is_relative_to(deps.resolve())
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with destination.open('xb') as stream:
                        stream.write(archive.read(member))
    assert expanded == 2140864
    assert inputs['total_bytes'] <= inputs['maximum_fixture_bytes']
    for relative, expected in inputs['files'].items():
        data = (target / relative).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected['sha256']
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
    for folder, entries in ((ORIGINAL / 'native-proposed', plan['source_postimages']),
                            (TASK / 'native-proposed', plan['metadata_postimages'])):
        for relative, expected in entries.items():
            source = folder / relative
            ordinary(source); assert sha(source) == expected
            destination = project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())

    # Reuse the native owner and pinned dependency closure, not a parallel schema.
    sys.path.insert(0, str(deps))
    sys.path.insert(0, str(project / 'spec/tools'))
    for name in ('yaml', 'jsonschema', 'attrs', 'referencing', 'rpds', 'typing_extensions'):
        module = importlib.import_module(name)
        assert Path(module.__file__).resolve().is_relative_to(deps.resolve())
    for wheel in acquisition['wheels']:
        distribution = importlib.metadata.distribution(wheel['name'])
        assert distribution.version == wheel['version']
        assert Path(distribution.locate_file('')).resolve() == deps.resolve()
    import specctl
    assert Path(specctl.__file__).resolve() == project / 'spec/tools/specctl.py'
    native = specctl.Bundle(project / 'spec')
    grant = read(project / 'spec/work/grants.json')['records'][-1]
    handoff = read(project / '.aide/handoffs/DE-W000-aide-selected-export-2026-10-17.json')
    native.validate(specctl.SCHEMA_PREFIX + 'grant:1', grant)
    native.validate(specctl.SCHEMA_PREFIX + 'handoff:1', handoff)
    assert grant['work_id'] == handoff['work_id'] == 'DE-W000'
    assert grant['base_revision'] == handoff['base_revision'] == plan['base_revision']
    assert handoff['files_changed'] == [] and all(t['status'] == 'not_run' for t in handoff['tests'])
    index = native.index()
    assert set(index['changed']) <= {'generated/index.json'}
    checks = native.check()
    write(output / 'native-check.json', checks)
    assert checks['status'] == 'PASS'
    manifest = native.manifest()
    assert native.manifest(True)['status'] == 'PASS'

    # The unchanged code, test bodies and exact original streams retain their
    # earlier scoped result. Metadata validation does not rerun or relabel them.
    assert prior['source_postimages'] == plan['source_postimages']
    assert prior['python_executable_sha256'] == sha(Path(sys.executable))
    assert prior['collection_retirement_verified'] and prior['all_collection_hashes_verified']
    assert sha(Path(prior['retained']) / 'receipt.json') == prior['receipt_sha256']
    counts = prior['completed_native_tests']
    assert counts['tests_run'] == 160 and counts['failures'] == counts['errors'] == 0 and counts['skips'] == 2
    assert counts['dependency_versions'] == {w['name']: w['version'] for w in acquisition['wheels']}
    prior_output = Path(prior['retained']) / 'output'
    assert sha(prior_output / 'native-tests.stderr') == prior['completed_native_test_stderr_sha256']
    assert read(prior_output / 'native-test-counts.json') == counts

    before = {p: row['sha256'] for p, row in inputs['files'].items()}
    after = {p.relative_to(project).as_posix(): sha(p) for p in project.rglob('*') if p.is_file()}
    changed = sorted(p for p in after if after[p] != before.get(p))
    expected_changes = set(plan['source_postimages']) | set(plan['metadata_postimages']) | set(plan['fixed_generated_paths'])
    assert set(changed) == expected_changes, changed
    total = 0
    for relative in changed:
        data = (project / relative).read_bytes(); total += len(data)
        assert total <= plan['maximum_prepared_bytes']
        destination = output / 'postimages' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
    check_target()
    write(output / 'preparation-result.json', {
        'schema': 'aide.native-adoption-preparation.v1', 'status': 'PASS',
        'native_work_id': 'DE-W000', 'native_base': plan['base_revision'],
        'preimages': {p: before.get(p) for p in changed},
        'postimages': {p: after[p] for p in changed}, 'postimage_bytes': total,
        'native_index': index, 'native_manifest': manifest, 'native_metadata_validation': 'PASS',
        'reused_test_job': prior['job_id'], 'reused_test_counts': counts,
        'native_tests_reexecuted': False, 'target_mutated': False,
        'grant_activated': False, 'writer_ownership': 'pending',
        'arbitrary_interruption_qualified': False, 'whole_task_usage': 'unknown',
        'model_calls': 0, 'network_calls': 0, 'elapsed_seconds': time.monotonic() - began})
    print('PASS: exact native metadata/postimages prepared; target unchanged; ownership/effect held.', flush=True)


if __name__ == '__main__':
    main()
