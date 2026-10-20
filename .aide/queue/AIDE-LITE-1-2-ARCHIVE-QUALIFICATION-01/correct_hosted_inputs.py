"""Preserve the rejected packet and remove its sole checkout-unavailable pin."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
spec = importlib.util.spec_from_file_location('hosted_correction_helpers', TASK / 'collect_remaining.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    initial_source = E / 'hosted-source.json'
    initial_effect = E / 'hosted-effect.json'
    source = json.loads(initial_source.read_bytes())
    effect = json.loads(initial_effect.read_bytes())
    assert sha(initial_source) == 'ec02482b3234ff107b91db43b7201f64259bdc93f404fa8a41fc12c5d767e2ee'
    assert sha(initial_effect) == '4dc00349656bcc2157ac96dcd446a5c682ab489558c1a84c347e90d9612a5214'
    verdict = json.loads((E / 'hosted-initial-review.json').read_bytes())
    assert verdict['decision'] == 'REJECT' and verdict['source_sha256'] == sha(initial_source)
    assert verdict['effect_sha256'] == sha(initial_effect)
    assert git('rev-parse', 'HEAD') == source['base'] == effect['checkpoint_parent']
    assert not git('diff', '--cached', '--name-only')
    # Preserve every exact uncommitted candidate byte, not only its hash table.
    candidate = {name: base64.b64encode((ROOT / name).read_bytes()).decode('ascii') for name in source['files']}
    assert all(sha(ROOT / name) == digest for name, digest in source['files'].items())
    candidate[initial_source.relative_to(ROOT).as_posix()] = base64.b64encode(initial_source.read_bytes()).decode('ascii')
    h.save(E / 'hosted-initial-candidate.json', h.bundle(json.dumps(candidate, sort_keys=True, separators=(',', ':')).encode(), files=len(candidate)))
    for name in ('source', 'effect', 'inputs'):
        path = E / ('hosted-' + name + '.json')
        destination = E / ('hosted-initial-' + name + '.json')
        assert not destination.exists()
        path.rename(destination)
    pins = json.loads((E / 'hosted-initial-inputs.json').read_bytes())
    local = '.aide.local/lite-successor-qualification-execution.json'
    assert pins['files'][local] == 'b73f055a31c0b62ed66e9f1ad2dcd3dae4b6f443296ac80fb7cce301e09d8815'
    del pins['files'][local]
    tracked = set(git('ls-files').splitlines())
    missing = set(pins['files']) - tracked - set(source['files'])
    assert not missing, sorted(missing)
    assert all(sha(ROOT / name) == value for name, value in pins['files'].items())
    h.save(E / 'hosted-inputs.json', pins)
    checks = json.loads((E / 'hosted-prechecks.json').read_bytes())
    for row in checks['commands']:
        assert row['exit_code'] == 0
        for name, expected in row['streams'].items():
            path = E / 'hosted-prechecks.log' / name
            assert path.stat().st_size == expected['bytes'] and sha(path) == expected['sha256']
    correction = {'state': 'PASS_HOSTED_CHECKOUT_AVAILABILITY_PREPARATION', 'excluded_local_pin': local,
        'local_pin_sha256': 'b73f055a31c0b62ed66e9f1ad2dcd3dae4b6f443296ac80fb7cce301e09d8815',
        'hosted_input_files': len(pins['files']), 'availability': 'Every hosted pin is tracked or an exact mapped checkpoint candidate.',
        'source_prechecks_reused': {'path': 'evidence/hosted-prechecks.json', 'sha256': sha(E / 'hosted-prechecks.json'),
            'reason': 'No evaluator, portable source, archive, original assertion, workflow or controller bytes changed.'},
        'jobs_run': 0, 'effect': 'Local-only control configuration stays local; all original bounded effect and qualification obligations remain.'}
    h.save(E / 'hosted-correction-checks.json', correction)
    effect['package_inputs_sha256'] = sha(E / 'hosted-inputs.json')
    effect['initial_rejected_effect_sha256'] = sha(E / 'hosted-initial-effect.json')
    effect['checkout_availability_sha256'] = sha(E / 'hosted-correction-checks.json')
    h.save(E / 'hosted-effect.json', effect)
    excluded = {(E / name).relative_to(ROOT).as_posix() for name in ('hosted-source.json', 'hosted-review.json')}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    files = {name: sha(ROOT / name) for name in sorted(changed - excluded)}
    git('diff', '--check')
    h.save(E / 'hosted-source.json', {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name,
        'base': source['base'], 'effect_sha256': sha(E / 'hosted-effect.json'), 'files': files})
    print(json.dumps({'source_sha256': sha(E / 'hosted-source.json'), 'effect_sha256': sha(E / 'hosted-effect.json'),
                      'controller_sha256': sha(TASK / 'checkpoint_and_host.py'), 'mapped_files': len(files),
                      'hosted_pins': len(pins['files']), 'new_jobs': 0}))


if __name__ == '__main__':
    main()
