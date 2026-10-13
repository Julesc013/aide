"""Pinned native source qualification in owned scratch; target remains read-only."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import time
import zipfile

TASK = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    inputs = json.loads((TASK / 'evidence/native-fixture-inputs.json').read_text())
    preimages = json.loads((TASK / 'evidence/native-preimages.json').read_text())
    acquisition = json.loads((TASK / 'evidence/acquisition-result.json').read_text())
    scratch, output = map(Path, (os.environ['AIDE_JOB_TMP'], os.environ['AIDE_JOB_OUTPUT']))
    project, deps = scratch / 'native-project', scratch / 'native-dependencies'
    project.mkdir(); deps.mkdir()
    target = Path(inputs['target'])
    git = inputs['git_executable']
    assert sha(Path(git)) == inputs['git_executable_sha256']
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(deps),
                       GIT_CONFIG_GLOBAL='NUL', GIT_CONFIG_SYSTEM='NUL', GIT_TERMINAL_PROMPT='0')
    stages = []

    def invoke(label, argv, cwd, expected=0, timeout=120):
        out, err = output / (label + '.stdout'), output / (label + '.stderr')
        began = time.monotonic()
        write(output / 'active-stage.json', {'stage': label, 'status': 'INCOMPLETE'})
        with out.open('xb') as stdout, err.open('xb') as stderr:
            completed = subprocess.run(argv, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr, timeout=timeout)
        row = {'stage': label, 'exit_code': completed.returncode, 'elapsed_seconds': time.monotonic() - began,
               'stdout_bytes': out.stat().st_size, 'stdout_sha256': sha(out),
               'stderr_bytes': err.stat().st_size, 'stderr_sha256': sha(err)}
        stages.append(row); write(output / 'stages.json', stages)
        write(output / 'active-stage.json', {'stage': label, 'status': 'TERMINAL', 'exit_code': completed.returncode})
        print(json.dumps(row), flush=True)
        assert completed.returncode == expected, label + ': original full streams retained'
        return out.read_text(encoding='utf-8', errors='replace')

    # Exact original target reads only; refuse concurrent work instead of copying it.
    assert invoke('target-base', [git, '-C', str(target), 'rev-parse', 'HEAD'], target).strip() == inputs['base_revision']
    assert not invoke('target-clean', [git, '-C', str(target), 'status', '--porcelain'], target).strip()
    assert acquisition['status'] == 'PASS' and acquisition['collection_retirement_verified']
    assert sum(w['bytes'] for w in acquisition['wheels']) == 631366
    unpacked_bytes = 0
    for wheel in acquisition['wheels']:
        with zipfile.ZipFile(Path(acquisition['retained']) / 'output' / wheel['filename']) as archive:
            unpacked_bytes += sum(member.file_size for member in archive.infolist())
    assert unpacked_bytes == 2140864 and unpacked_bytes <= 8 * 1024 * 1024
    for wheel in acquisition['wheels']:
        path = Path(acquisition['retained']) / 'output' / wheel['filename']
        assert path.stat().st_size == wheel['bytes'] and sha(path) == wheel['sha256']
        # Fixture extraction only, not a generic installer: all pinned wheels have
        # ordinary package roots and no .data installation/entrypoint effects.
        with zipfile.ZipFile(path) as archive:
            seen = set()
            for member in archive.infolist():
                parts = PurePosixPath(member.filename).parts
                assert parts and not member.filename.startswith('/') and not stat.S_ISLNK(member.external_attr >> 16)
                assert all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.', '..') for p in parts)
                assert not any(p.endswith('.data') for p in parts)
                key = member.filename.casefold(); assert key not in seen; seen.add(key)
                destination = deps.joinpath(*parts)
                assert destination.resolve().is_relative_to(deps.resolve())
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with destination.open('xb') as stream:
                        stream.write(archive.read(member))
    assert sum(p.stat().st_size for p in deps.rglob('*') if p.is_file()) <= 8 * 1024 * 1024

    assert inputs['total_bytes'] <= inputs['maximum_fixture_bytes']
    for relative, expected in inputs['files'].items():
        parts = PurePosixPath(relative).parts
        assert parts and '..' not in parts and '.git' not in parts and not relative.startswith('/')
        source = target.joinpath(*parts)
        assert not source.is_symlink() and source.stat().st_nlink == 1
        data = source.read_bytes()
        assert len(data) == expected['bytes'] and hashlib.sha256(data).hexdigest() == expected['sha256']
        destination = project.joinpath(*parts); destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
    for relative, expected in preimages['proposed_paths'].items():
        source = TASK / 'native-proposed' / relative
        assert sha(source) == expected and sha(project / relative) == preimages['original_paths'][relative]
        (project / relative).write_bytes(source.read_bytes())
    stage_script = str(TASK / 'native_stage.py')

    def native(label, *arguments, expected=0):
        return invoke(label, [sys.executable, '-I', '-B', stage_script, str(deps), str(project),
                              str(output), *arguments], project, expected)

    native('native-index', 'cli', 'index')
    native('native-check', 'cli', 'check')
    native('native-tests', 'tests')
    counts = json.loads((output / 'native-test-counts.json').read_text())
    assert counts['tests_run'] == inputs['expected_test_count'] == 106
    assert not any(counts[k] for k in ('failures', 'errors'))
    # Preserve the native suite's existing environment skips, never weaken an
    # original assertion or hide an unexecuted check behind a full-pass claim.
    assert counts['skips'] <= 2
    for skipped in counts['skipped_cases']:
        assert skipped['test'].endswith(('.test_symlink_path_is_refused', '.test_bootstrap_refuses_symlink_root'))
        assert skipped['reason'].startswith('symlinks unavailable')
    native('native-manifest', 'cli', 'manifest')
    native('native-verify-manifest', 'cli', 'verify-manifest')
    # A real isolated Git fixture supplies the context's actual revision identity.
    hooks = scratch / 'empty-hooks'; hooks.mkdir()
    prefix = [git, '-c', 'core.hooksPath=' + str(hooks), '-c', 'core.autocrlf=false',
              '-c', 'commit.gpgSign=false', '-c', 'user.name=Native Fixture', '-c', 'user.email=fixture@invalid']
    invoke('fixture-git-init', prefix + ['init'], project)
    invoke('fixture-git-add', prefix + ['add', '--', '.'], project)
    invoke('fixture-git-baseline', prefix + ['commit', '-m', 'Owned native qualification baseline'], project)
    native('controlled-stop-after-completed-export', 'stop-after-export', expected=75)
    native('fresh-process-native-resume', 'resume')
    native('default-all-export', 'cli', 'aide-export', '--output', str(output / 'all-export'))
    selected = output / 'selected/DE-W000.json'
    all_files = sorted((output / 'all-export').glob('*.json'))
    assert len(all_files) > 1 and selected.read_bytes() == (output / 'all-export/DE-W000.json').read_bytes()
    for relative, expected in inputs['files'].items():
        assert sha(target / relative) == expected['sha256']
    assert not invoke('target-still-clean', [git, '-C', str(target), 'status', '--porcelain'], target).strip()
    write(output / 'qualification.json', {
        'schema': 'aide.native-consumer-source-qualification.v1',
        'status': 'PASS_WITH_ENVIRONMENT_SKIPS' if counts['skips'] else 'PASS',
        'native_work_id': 'DE-W000', 'native_base': inputs['base_revision'], 'counts': counts,
        'stages': stages, 'source_postimages': preimages['proposed_paths'],
        'original69_test_bodies_conserved': True, 'selected_bytes': selected.stat().st_size,
        'all_export_bytes': sum(p.stat().st_size for p in all_files), 'all_export_records': len(all_files),
        'target_mutated': False, 'global_installation': False, 'qualification_network': False,
        'arbitrary_interruption_qualified': False, 'outer_containment_qualified': False,
        'upstream_runtime_qualified': False, 'whole_task_usage': 'unknown', 'models_requested': 0})


if __name__ == '__main__':
    main()
