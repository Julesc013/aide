from pathlib import Path
import hashlib, json, subprocess, sys, time

ROOT = Path(r'D:\Projects\AIDE\aide')
AE = ROOT / '.aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence'
EXPECTED_HEAD = '2a44f17eb7232757133df549ac6fc519d535e71b'
EXPECTED_REVIEW = '3d0c862b7c0de04eeafed2a1173335b88de250293716511d88a1f3cbb081a683'
EXPECTED_EFFECT = 'd4a49c0683ae1903611e0350d0edbc4f9c4708f05363bda88cf5eaf71f741ab4'
EXPECTED_MANIFEST = '84d5621e634989b7bf2ad62ed3472c6989b2d9b4a9b44acfd1e465319991a1a6'
REQUEST = 'ceaa759a8344465fa4d5b1340dfb4eed'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    with path.open('xb') as stream:
        stream.write((json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8'))

def main():
    review_path = AE / 'h2-resource-root-effect-review.json'
    effect_path = AE / 'h2-resource-effect-manifest.json'
    manifest_path = AE / 'h2-resource-source-manifest.json'
    assert digest(review_path) == EXPECTED_REVIEW
    assert digest(effect_path) == EXPECTED_EFFECT
    assert digest(manifest_path) == EXPECTED_MANIFEST
    review = json.loads(review_path.read_bytes())
    effect = json.loads(effect_path.read_bytes())
    manifest = json.loads(manifest_path.read_bytes())
    assert review['result'] == 'PASS_EXACT_FINITE_EFFECT_REVIEW'
    assert review['request_id'] == effect['plan']['request_id'] == REQUEST
    assert review['effect_sha256'] == EXPECTED_EFFECT
    pins = manifest['files'] | manifest['unchanged_dependencies']
    for name, expected in pins.items():
        assert digest(ROOT / name) == expected, name
    assert digest(Path(effect['interpreter']['path'])) == effect['interpreter']['sha256']
    identity = subprocess.check_output(['whoami'], text=True).strip()
    assert identity.casefold() == r'BLACKGLASS-WIN1\Jules'.casefold(), identity
    head = subprocess.check_output(['git', '-c', 'safe.directory=D:/Projects/AIDE/aide', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    assert head == EXPECTED_HEAD
    parent = Path(effect['output_parent']['path'])
    output = parent / ('system-resource-' + REQUEST)
    journal = parent / ('system-resource-' + REQUEST + '.intent.jsonl')
    assert not output.exists() and not journal.exists()
    assert time.time() < effect['plan']['expires_at']
    stdout_path = AE / 'h2-resource-actual-controller-stdout.txt'
    stderr_path = AE / 'h2-resource-actual-controller-stderr.txt'
    command = [effect['interpreter']['path'], '-I', '-S', '-B', str(AE / 'h2_system_resource_controller.py'), '--run', str(effect_path), EXPECTED_EFFECT]
    invocation = {'schema': 'aide.host.resource-actual-invocation.v1', 'head': head,
        'identity': identity, 'review_sha256': EXPECTED_REVIEW, 'effect_sha256': EXPECTED_EFFECT,
        'request_id': REQUEST, 'source_pins': pins, 'command': command,
        'driver_sha256': digest(Path(__file__)), 'started_at': time.time(),
        'expires_at': effect['plan']['expires_at'], 'automatic_retry': False,
        'outer_watchdog_seconds': 120, 'source_effect_scope': 'exact approved ordinary two-API resource feasibility probe'}
    save(AE / 'h2-resource-actual-invocation.json', invocation)
    started = time.perf_counter()
    outcome = {'schema': 'aide.host.resource-actual-execution.v1', 'request_id': REQUEST,
        'invocation_sha256': digest(AE / 'h2-resource-actual-invocation.json')}
    try:
        with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
            completed = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=120, check=False)
            outcome['controller_exit_code'] = completed.returncode
    except BaseException as error:
        outcome['orchestration_error_type'] = type(error).__name__
    outcome.update({'ended_at': time.time(), 'elapsed_seconds': time.perf_counter() - started,
        'automatic_retry': False, 'native_effect_replayed': False, 'source_pins_unchanged': all(digest(ROOT / name) == expected for name, expected in pins.items()),
        'review_unchanged': digest(review_path) == EXPECTED_REVIEW, 'effect_unchanged': digest(effect_path) == EXPECTED_EFFECT})
    artifacts = [stdout_path, stderr_path, journal, output / 'stdin', output / 'stdout', output / 'stderr']
    outcome['artifacts'] = {str(path): {'bytes': path.stat().st_size, 'sha256': digest(path)} for path in artifacts if path.is_file()}
    outcome['output_directory_entries'] = sorted(path.name for path in output.iterdir()) if output.is_dir() else []
    save(AE / 'h2-resource-actual-execution.json', outcome)
    print(json.dumps(outcome, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
