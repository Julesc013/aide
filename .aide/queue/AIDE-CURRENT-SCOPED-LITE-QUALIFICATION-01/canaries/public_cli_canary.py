"""Qualify opt-in public import explanation from frozen delivered ZIP bytes."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys


def sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


archive = Path(sys.argv[1]).resolve(strict=True)
expected_zip, expected_helper = sys.argv[2:]
helper_path = Path(__file__).with_name('lifecycle_helper.py')
if sha(archive) != expected_zip or sha(helper_path) != expected_helper:
    raise ValueError('archive or helper identity changed')
spec = importlib.util.spec_from_file_location('aide_public_cli_helper', helper_path)
helper = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = helper
spec.loader.exec_module(helper)
root = Path(os.environ['AIDE_JOB_TMP']) / 'public-cli'
root.mkdir()
retained = Path(os.environ['AIDE_JOB_OUTPUT'])
members = helper.extract_zip(archive, root / 'candidate')
pack = root / 'candidate' / helper.PACK_NAME
target = root / 'target'
target.mkdir()
owned = target / 'project-owned.txt'
owned.write_bytes(b'Preserve project-owned content.\r\n')
owned_digest = sha(owned)
rec = helper.Recorder(root)
helper.install(rec, 'fresh', pack, target)
if sha(owned) != owned_digest:
    raise AssertionError('import changed project-owned bytes')
source = target / '.aide/scripts/aide_lite.py'
source_digest = sha(source)
common = ('import-pack', '--pack', str(pack), '--target', str(target), '--mode', 'safe')
ordinary = rec.installed('ordinary-preview', target, *common, '--dry-run')
feedback = root / 'local-feedback.json'
if feedback.exists() or 'feedback_out:' in ordinary.stdout:
    raise AssertionError('feedback was created without opt-in')
requested = rec.installed('explicit-feedback', target, *common, '--dry-run',
                         '--explain', '--feedback-out', str(feedback))
for label in ('ordinary-preview', 'explicit-feedback'):
    shutil.copy2(root / f'{label}.json', retained / f'{label}.json')
shutil.copy2(feedback, retained / 'explicit-feedback-packet.json')
packet = json.loads(feedback.read_text(encoding='utf-8'))
if packet.get('sharing') != 'manual_only' or packet.get('network_calls') is not False:
    raise AssertionError('feedback sharing boundary changed')
explanations = packet.get('explanations', [])
if not explanations or not any(item.get('target') == '.aide/profile.yaml' for item in explanations):
    raise AssertionError('project profile explanation missing')
if any(item.get('project_rationale') != 'unknown' for item in explanations):
    raise AssertionError('unrecorded rationale invented')
if not all('observed_digest' in item and 'incoming_digest' in item for item in explanations):
    raise AssertionError('digest binding missing')
refused = rec.installed('feedback-without-preview', target, *common,
                       '--feedback-out', str(root / 'refused-feedback.json'),
                       exits=(1, 2, 3))
if refused.returncode == 0 or (root / 'refused-feedback.json').exists():
    raise AssertionError('feedback without dry run was accepted')
if sha(owned) != owned_digest or sha(source) != source_digest:
    raise AssertionError('delivered target bytes changed during preview')
validate = rec.installed('installed-validate', target, 'validate', exits=(0, 1, 2, 3))
shutil.copy2(root / 'installed-validate.json', retained / 'installed-validate.json')
before_inspection = helper.tree_hashes(target)
try:
    empty_status = rec.installed('empty-task-status', target, 'task', 'status', exits=(1,))
    empty_inspect = rec.installed('empty-task-inspect', target, 'task', 'inspect', exits=(1,))
finally:
    for label in ('empty-task-status', 'empty-task-inspect'):
        log = root / f'{label}.json'
        if log.is_file():
            shutil.copy2(log, retained / log.name)
if helper.tree_hashes(target) != before_inspection:
    raise AssertionError('empty task inspection mutated installed target')
if 'task_count: 0' not in empty_status.stdout or 'classification: missing' not in empty_inspect.stdout:
    raise AssertionError('empty task state not reported honestly')
task_id = 'LOCAL-PUBLIC-CLI-CANARY-01'
queue = target / '.aide/queue'
(queue / task_id / 'evidence').mkdir(parents=True)
(queue / 'index.yaml').write_text(
    'schema_version: aide.queue-index.v0\nitems:\n'
    f'  - id: {task_id}\n    status: running\n'
    f'    task: .aide/queue/{task_id}/task.yaml\n', encoding='utf-8')
(queue / task_id / 'task.yaml').write_text(
    f'schema_version: aide.queue-task.v0\nid: {task_id}\nstatus: running\n', encoding='utf-8')
(queue / task_id / 'status.yaml').write_text(
    'schema_version: aide.queue-status.v0\nstatus: running\n', encoding='utf-8')
before_inspection = helper.tree_hashes(target)
try:
    task_status = rec.installed('task-status', target, 'task', 'status')
    task_inspect = rec.installed('task-inspect', target, 'task', 'inspect', '--task-id', task_id)
finally:
    for label in ('task-status', 'task-inspect'):
        log = root / f'{label}.json'
        if log.is_file():
            shutil.copy2(log, retained / log.name)
if helper.tree_hashes(target) != before_inspection:
    raise AssertionError('populated task inspection mutated installed target')
if task_id not in task_status.stdout or 'classification: partial' not in task_inspect.stdout:
    raise AssertionError('populated task state missing')
summary = {'status': 'PASS' if validate.returncode == 0 else 'NEEDS_CLASSIFICATION',
           'zip_sha256': expected_zip, 'members': len(members),
           'installed_source_sha256': source_digest, 'project_owned_sha256': owned_digest,
           'feedback_sha256': sha(feedback), 'explanations': len(explanations),
           'ordinary_exit': ordinary.returncode, 'explicit_exit': requested.returncode,
           'refused_exit': refused.returncode, 'validate_exit': validate.returncode,
           'empty_status_exit': empty_status.returncode,
           'empty_inspect_exit': empty_inspect.returncode, 'task_status_exit': task_status.returncode,
           'task_inspect_exit': task_inspect.returncode, 'inspection_mutated': False,
           'commands': rec.commands}
(retained / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n', encoding='utf-8')
