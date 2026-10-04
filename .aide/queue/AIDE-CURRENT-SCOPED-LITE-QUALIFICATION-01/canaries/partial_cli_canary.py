"""Qualify delivered partial-import recovery through its public CLI."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys


source = Path(__file__).with_name('consumer_canary_base.py')
spec = importlib.util.spec_from_file_location('aide_partial_cli_fixture', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
zip_path, tar_path = (Path(value).resolve(strict=True) for value in sys.argv[1:3])
zip_hash, tar_hash, cli_hash = sys.argv[3:6]
if module.sha256_file(zip_path) != zip_hash or module.sha256_file(tar_path) != tar_hash:
    raise ValueError('frozen archive identity changed')
out = Path(os.environ['AIDE_JOB_TMP']) / 'partial-cli'
out.mkdir()
retained = Path(os.environ['AIDE_JOB_OUTPUT'])
rec = module.Recorder(out)
try:
    zip_members = module.extract_archive(zip_path, out / 'zip', 'zip')
    tar_members = module.extract_archive(tar_path, out / 'tar', 'tar')
    if zip_members != tar_members:
        raise AssertionError('archive member mismatch')
    pack = out / 'zip' / module.PACK_NAME
    if module.sha256_file(pack / 'files/.aide/scripts/aide_lite.py') != cli_hash:
        raise AssertionError('delivered CLI identity mismatch')
    delivered = module.delivered_module(pack)
    successor = module.make_synthetic_update(out / 'tar' / module.PACK_NAME,
                                              out / 'synthetic-v2', 2, delivered)
    target = out / 'target'
    target.mkdir()
    owned = target / 'project-owned.txt'
    owned.write_bytes(b'Project bytes survive recovery.\r\n')
    owned_hash = module.sha256_file(owned)

    def command(label: str, incoming: Path, predecessor: Path | None = None,
                *extra: str, expected: int = 0):
        args = ['import-pack', '--pack', str(incoming), '--target', str(target), '--mode', 'safe']
        if predecessor is not None:
            args.extend(['--from-pack', str(predecessor)])
        args.extend(extra)
        return rec.command(label, incoming, target, args, expected_exit=expected)

    fresh = delivered.apply_import_pack(pack, target, fail_after_writes=1)
    if fresh['status'] != 'INTERRUPTED' or fresh['recovery']['classification'] != 'partial':
        raise AssertionError('fresh fixture did not interrupt after a payload write')
    normal_fresh = command('fresh-ordinary-refusal', pack, None, expected=3)
    wrong_fresh = command('fresh-wrong-plan-refusal', pack, None,
                          '--recover-partial', '--expect-plan', '0' * 64, expected=3)
    exact_fresh = command('fresh-cli-recover', pack, None,
                          '--recover-partial', '--expect-plan', fresh['plan_digest'])
    if any('status: RECOVERY_REQUIRED' not in item.stdout for item in (normal_fresh, wrong_fresh)):
        raise AssertionError('fresh replay or wrong-plan guard failed')
    if 'status: RECOVERED' not in exact_fresh.stdout:
        raise AssertionError('fresh CLI recovery failed')

    feedback = out / 'update-feedback.json'
    if feedback.exists():
        raise AssertionError('feedback appeared without explicit request')
    preview_update = command('predecessor-feedback-preview', successor, pack,
                             '--dry-run', '--explain', '--feedback-out', str(feedback))
    packet = json.loads(feedback.read_text(encoding='utf-8'))
    if 'status: PLANNED' not in preview_update.stdout:
        raise AssertionError('predecessor feedback preview was not planned')
    if packet.get('sharing') != 'manual_only' or packet.get('network_calls') is not False:
        raise AssertionError('predecessor feedback sharing boundary changed')
    if not packet.get('explanations') or not all(
        'observed_digest' in item and 'incoming_digest' in item
        for item in packet['explanations']
    ):
        raise AssertionError('predecessor explanation lacks digest binding')
    if module.sha256_file(owned) != owned_hash:
        raise AssertionError('feedback preview changed project-owned bytes')

    update = delivered.apply_import_pack(successor, target, predecessor_pack=pack,
                                         fail_after_writes=1)
    if update['status'] != 'INTERRUPTED' or update['recovery']['classification'] != 'partial':
        raise AssertionError('update fixture did not interrupt after a payload write')
    normal_update = command('update-ordinary-refusal', successor, pack, expected=3)
    wrong_update = command('update-wrong-plan-refusal', successor, pack,
                           '--recover-partial', '--expect-plan', '0' * 64, expected=3)
    exact_update = command('update-cli-recover', successor, pack,
                           '--recover-partial', '--expect-plan', update['plan_digest'])
    if any('status: RECOVERY_REQUIRED' not in item.stdout for item in (normal_update, wrong_update)):
        raise AssertionError('update replay or wrong-plan guard failed')
    if 'status: RECOVERED' not in exact_update.stdout:
        raise AssertionError('predecessor-bound CLI recovery failed')
    if module.sha256_file(owned) != owned_hash:
        raise AssertionError('project-owned bytes changed')
    if (target / delivered.PORTABLE_IMPORT_INTENT_PATH).exists():
        raise AssertionError('successful CLI recovery retained active intent')
    if delivered.load_portable_import_receipt(target)['pack'] != delivered.import_pack_identity(successor):
        raise AssertionError('recovered receipt does not identify successor')

    third = module.make_synthetic_update(out / 'tar' / module.PACK_NAME,
                                         out / 'synthetic-v3', 3, delivered)
    edited = target / module.MANAGED
    edited.write_bytes(b'Project direct edit with unknown rationale.\n')
    selected = out / 'selected-resolution.txt'
    selected_bytes = b'Project selected V3 combination.\n'
    selected.write_bytes(selected_bytes)
    resolution = {module.MANAGED: selected}
    preview = delivered.apply_import_pack(third, target, dry_run=True,
                                          predecessor_pack=successor,
                                          resolutions=resolution)
    if preview['status'] != 'PLANNED':
        raise AssertionError('resolved V3 update did not plan')
    partial_resolution = delivered.apply_import_pack(
        third, target, predecessor_pack=successor, resolutions=resolution,
        expected_plan_digest=preview['plan_digest'], fail_after_writes=1)
    if partial_resolution['status'] != 'INTERRUPTED':
        raise AssertionError('resolved V3 update did not partially interrupt')
    resolution_args = ('--resolve', module.MANAGED, str(selected))
    ordinary_resolution = command('resolved-ordinary-refusal', third, successor,
                                  *resolution_args, expected=3)
    selected.write_bytes(b'Changed resolution input.\n')
    changed_resolution = command('resolved-changed-input-refusal', third, successor,
                                 *resolution_args, '--recover-partial', '--expect-plan',
                                 preview['plan_digest'], expected=3)
    selected.write_bytes(selected_bytes)
    exact_resolution = command('resolved-cli-recover', third, successor,
                               *resolution_args, '--recover-partial', '--expect-plan',
                               preview['plan_digest'])
    if any('status: RECOVERY_REQUIRED' not in item.stdout
           for item in (ordinary_resolution, changed_resolution)):
        raise AssertionError('resolved ordinary or changed-input guard failed')
    if 'status: RECOVERED' not in exact_resolution.stdout:
        raise AssertionError('resolved exact CLI recovery failed')
    if edited.read_bytes() != selected_bytes or selected.read_bytes() != selected_bytes:
        raise AssertionError('resolved recovery lost project-selected bytes')
    if (target / delivered.PORTABLE_IMPORT_INTENT_PATH).exists():
        raise AssertionError('resolved recovery retained active intent')
    if module.sha256_file(owned) != owned_hash:
        raise AssertionError('resolved recovery changed project-owned bytes')
    summary = {'status': 'PASS', 'zip_sha256': zip_hash, 'tar_sha256': tar_hash,
               'member_count': len(zip_members), 'cli_sha256': cli_hash,
               'fresh': ['INTERRUPTED', 'RECOVERY_REQUIRED', 'RECOVERY_REQUIRED', 'RECOVERED'],
               'update': ['INTERRUPTED', 'RECOVERY_REQUIRED', 'RECOVERY_REQUIRED', 'RECOVERED'],
               'resolved_update': ['INTERRUPTED', 'RECOVERY_REQUIRED',
                                   'RECOVERY_REQUIRED', 'RECOVERED'],
               'project_owned_sha256': owned_hash, 'synthetic_successor_is_published': False,
               'predecessor_feedback_sha256': module.sha256_file(feedback),
               'predecessor_explanations': len(packet['explanations']),
               'commands': rec.commands}
    (retained / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n', encoding='utf-8')
finally:
    for item in out.glob('*.json'):
        if item.name != 'summary.json':
            shutil.copy2(item, retained / item.name)
