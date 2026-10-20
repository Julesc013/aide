"""Regenerate frozen archive payloads in admitted scratch and verify current source."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import platform
import time

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'
TMP = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
OUT = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)


def main(*, deadline=None):
    assert deadline is not None and deadline > time.monotonic()
    def checkpoint(label):
        if time.monotonic() >= deadline:
            raise TimeoutError('replay active-work deadline: ' + label)
    assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
    spec = importlib.util.spec_from_file_location('replay_common', TASK / 'run_consumer.py')
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    lite = common.load('replay_source_lite', ROOT / '.aide/scripts/aide_lite.py')
    subject = json.loads((TASK / 'evidence/profile-build-result.json').read_text(encoding='utf-8'))
    frozen = json.loads((TASK / 'evidence/revised-pack-subject.json').read_text(encoding='utf-8'))
    pack = ROOT / '.aide/export/aide-lite-pack-v0'
    before = {p.relative_to(ROOT).as_posix(): common.sha(p)
              for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}
    assert all(common.sha(ROOT / p) == d for p, d in frozen.items())
    assert all(before[p] == v['sha256'] for p, v in subject['assets'].items())

    operations = {}
    for label, arguments in [('doctor', ['doctor']), ('validate', ['validate']),
                             ('stable-validate', ['release', 'stable-validate', '--version', '1.2.0']),
                             ('pack-status', ['pack-status'])]:
        if time.monotonic() >= deadline:
            raise TimeoutError('replay deadline before command admission')
        argv = [sys.executable, '-B', '.aide/scripts/aide_lite.py', *arguments]
        operations[label] = {'argv': argv, 'state': 'started', 'exit_code': None}
        common.write(OUT / 'operations.json', operations)
        streams = [OUT / (label + suffix) for suffix in ('.stdout', '.stderr')]
        try:
            with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
                process = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=min(120, max(0.001, deadline - time.monotonic())))
            operations[label].update(state='completed', exit_code=process.returncode)
        except BaseException as error:
            operations[label].update(state='exception', error_type=type(error).__name__, error=str(error))
            raise
        finally:
            operations[label]['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': common.sha(p)} for p in streams if p.exists()}
            common.write(OUT / 'operations.json', operations)
        assert process.returncode == 0, (label, process.returncode)

    fixture = TMP / 'case-archive-replay'
    fixture.mkdir()
    projected = fixture / lite.RELEASE_ARCHIVE_ROOT
    checkpoint('before projection')
    lite.build_release_pack_projection(pack, projected)
    checkpoint('after projection')
    lite.write_text_if_changed(projected / 'stable-release.json', lite.stable_json_text(subject['identity']))
    lite.write_text_if_changed(projected / 'checksums.json', lite.stable_json_text(lite.build_pack_checksums(projected)))
    okay, problems = lite.validate_pack_checksums(projected)
    assert okay, problems
    checkpoint('after metadata and checksums')
    replay = {}
    for suffix, writer in [('zip', lite.write_release_zip), ('tar.gz', lite.write_release_tar_gz)]:
        path = fixture / ('aide-lite-v1.2.0.' + suffix)
        checkpoint('before archive ' + suffix)
        writer(projected, path)
        checkpoint('after archive ' + suffix)
        relative = '.aide/release/stable/' + path.name
        observed = {'sha256': common.sha(path), 'size_bytes': path.stat().st_size}
        assert observed == subject['assets'][relative], suffix
        replay[relative] = observed

    # Fresh primary-profile identity/ownership evidence; old observations retain
    # their original package identities under the accepted applicability proof.
    profile = next(p for p in subject['identity']['profiles'] if p['profile_id'] == 'aide-lite-local-windows')
    actual = {'system': platform.system(), 'release': platform.release(), 'version': platform.version(),
              'machine': platform.machine(), 'runtime': {'implementation': platform.python_implementation(), 'version': platform.python_version()}}
    assert actual == profile['environment']
    helper = common.load('replay_identity_helpers', common.CAN / 'lifecycle_helper.py')
    transport = common.load('replay_identity_transport', ROOT / 'evals/lite/release.py')
    transport.DEADLINE = deadline
    checkpoint('before primary identity')
    rec = transport.recorder(helper, OUT)
    target = fixture / 'identity-target'
    target.mkdir()
    authored = b'# Existing project guidance\r\nPreserve it exactly.\r\n'
    project = {'README.md': b'# Existing project\n', 'tools/project.py': b"print('project tool')\n",
               '.aide/memory/project.md': b'Project-owned knowledge.\r\n'}
    (target / 'AGENTS.md').write_bytes(authored)
    for relative, raw in project.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    helper.install(rec, 'identity-install', projected, target)
    module = helper.load_delivered(projected)
    receipt = module.load_portable_import_receipt(target)
    assert receipt['pack'] == module.import_pack_identity(projected)
    assert common.sha(target / '.aide/scripts/aide_lite.py') == subject['delivered_cli_sha256']
    assert not (target / 'core').exists()
    actual_owned = {p: common.sha(target / p) for p in receipt['managed']}
    agents_after_removal = module.portable_agents_section_postimage((target / 'AGENTS.md').read_bytes(),
        receipt['managed']['AGENTS.md']['installed_digest'])
    assert agents_after_removal is not None and agents_after_removal.startswith(authored)
    for relative, entry in receipt['managed'].items():
        if relative != 'AGENTS.md':
            assert actual_owned[relative] == entry['installed_digest'], relative
    common.write(OUT / 'primary-revised-identity.json', {'environment': actual,
        'actual_pack': receipt['pack'], 'receipt': receipt, 'actual_owned_target_sha256s': actual_owned})
    plan = helper.plan_removal(rec, 'identity-removal-plan', target)
    assert plan['status'] == 'PLANNED' and set(plan['candidate_targets']) == set(receipt['managed'])
    removed = rec.installed('identity-removal', target, 'apply-removal', '--target', str(target),
                            '--expect-plan', plan['plan_digest'], '--json')
    assert json.loads(removed.stdout)['status'] == 'DETACHED'
    helper.assert_detached(target, set(receipt['managed']), module,
        {relative: hashlib.sha256(raw).hexdigest() for relative, raw in project.items()}, authored_agents=agents_after_removal)
    checkpoint('after primary identity and detach')

    after = {p.relative_to(ROOT).as_posix(): common.sha(p)
             for p in (ROOT / '.aide/release').rglob('*') if p.is_file()}
    assert after == before
    assert all(common.sha(ROOT / p) == d for p, d in frozen.items())
    checkpoint('before replay result')
    result = {'status': 'PASS', 'replay': replay, 'identity': subject['identity'],
              'recipe': 'existing release projection and archive writers; validated frozen identity',
              'preserved_release_files': len(before), 'preserved_pack_files': len(frozen),
              'operations': operations, 'model_calls': 0, 'publication': 'not performed',
              'fixture_retired': False}
    common.write(OUT / 'replay-result.json', result)
    worker = common.load('replay_retirement', common.ORIGINAL / 'worker.py')
    worker.retire_owned_fixture(fixture)
    checkpoint('after replay retirement')
    result['fixture_retired'] = True
    common.write(OUT / 'replay-result.json', result)
    print('PASS exact scratch archive replay and current source checks')


if __name__ == '__main__':
    main()
