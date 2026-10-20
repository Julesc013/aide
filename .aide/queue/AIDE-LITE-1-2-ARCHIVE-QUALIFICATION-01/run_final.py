"""Last local group; execution requires its exact source/effect acceptance."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import tempfile

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    assert not sys.argv[1:]
    hosted = json.loads((TASK / 'evidence/profile-coverage.json').read_bytes())
    assert hosted['behavioral_coverage_pass'] and len(hosted['profiles']) == 3
    assert hosted['fresh_primary_identity_required'] and not hosted['release_accepted']
    result = {'status': 'STARTED', 'phases': [], 'model_requests': 0, 'whole_model_usage': 'unknown'}

    def save():
        (OUT / 'final-group.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')

    save()
    deadline = time.monotonic() + 540
    for phase, filename, options, arguments, seconds in (
        ('managed', 'run_consumer.py', {'subject_name': 'profile-build-result.json'}, ['6'], 60),
        ('brownfield', 'run_predecessor.py', {'subject_name': 'profile-build-result.json', 'shapes': ('brownfield',)}, [], 240),
        ('replay', 'run_replay.py', {}, [], 210),
    ):
        record = {'phase': phase, 'state': 'STARTED', 'started_unix_ns': time.time_ns(), 'fixture_retired': False}
        result['phases'].append(record)
        save()
        before = dict(os.environ)
        argv = sys.argv
        temporary_cache = tempfile.tempdir
        try:
            if time.monotonic() >= deadline:
                raise TimeoutError('final group deadline before phase admission')
            phase_deadline = min(deadline, time.monotonic() + seconds)
            options['deadline'] = phase_deadline
            scratch, output = TMP / ('case-final-' + phase), OUT / phase
            scratch.mkdir()
            output.mkdir()
            # This owner binds TMP at import; bind it to the outer job root.
            worker = load('final_phase_retirement_' + phase, ROOT / '.aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py')
            os.environ.update(AIDE_JOB_TMP=str(scratch), AIDE_JOB_OUTPUT=str(output), TEMP=str(scratch), TMP=str(scratch), TMPDIR=str(scratch))
            sys.argv = [str(TASK / filename), *arguments]
            module = load('final_' + phase, TASK / filename)
            module.main(**options)
            # Retire only after successful original checks and inner retirement.
            worker.retire_owned_fixture(scratch)
            record['fixture_retired'] = True
            if time.monotonic() > phase_deadline:
                raise TimeoutError('phase completed beyond admitted active-work deadline')
            record['state'] = 'PASS'
        except BaseException as error:
            record.update(state='INCOMPLETE', error_type=type(error).__name__, error=str(error))
            result['status'] = 'INCOMPLETE'
            save()
            raise
        finally:
            sys.argv = argv
            tempfile.tempdir = temporary_cache
            os.environ.clear()
            os.environ.update(before)
            record['finished_unix_ns'] = time.time_ns()
            save()
    if time.monotonic() > deadline:
        result.update(status='INCOMPLETE', error_type='TimeoutError', error='shared deadline before final acceptance')
        save()
        raise TimeoutError(result['error'])
    result['status'] = 'PASS'
    save()
    print('PASS revised delivered managed forms, unfinished brownfield and exact release replay')


if __name__ == '__main__':
    main()
