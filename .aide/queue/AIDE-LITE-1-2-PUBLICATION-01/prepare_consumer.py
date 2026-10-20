"""Prepare one acquired-byte consumer; no allocation or repeated qualification."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
QE = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/evidence'
sys.path.insert(0, str(ROOT))
from core.execution import managed_workspace as workspace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    delivery = json.loads((E / 'delivery-recovery-result.log').read_bytes())
    assert delivery['status'] == 'PUBLISHED_ACQUIRED_CONSUMER_PENDING'
    base = delivery['commit']
    assert git('rev-parse', 'HEAD') == base and not git('diff', '--cached', '--name-only')
    for name in ('collect_effects.py', 'run_consumer.py'):
        path = TASK / name
        body = (E / 'next-preparation.log' / name).read_bytes()
        if path.exists():
            assert path.read_bytes() == body
        else:
            path.write_bytes(body)
    if not (E / 'publication-effects-verified.json').exists():
        subprocess.run([sys.executable, '-B', str(TASK / 'collect_effects.py'), 'publication'], cwd=ROOT, check=True, timeout=90)
    pub = json.loads((E / 'published-acquired.json').read_bytes())
    assert pub['release']['id'] == 418708655 and pub['tag_commit'] == 'ee36a9342e17a4c13378bd9ac034c506056f6de2'
    source = (TASK / 'checkpoint.py').read_bytes().replace(b'publication-checkpoint', b'consumer-checkpoint').replace(b'publication-projection', b'consumer-projection')
    (TASK / 'consumer_checkpoint.py').write_bytes(source)
    # Current public state is factual; the consumer remains pending.
    p = ROOT / 'README.md'
    paragraphs = p.read_text(encoding='utf-8').split('\n\n')
    for i, text in enumerate(paragraphs):
        if text.startswith('AIDE Lite **1.1.0 is published**'):
            paragraphs[i] = 'AIDE Lite **1.2.0 is published** as [`aide-lite-v1.2.0`](https://github.com/Julesc013/aide/releases/tag/aide-lite-v1.2.0). Four exact T3/L1 companion profiles use CPython 3.14.8: Windows 10/19045 AMD64 (56 forms), Windows Server 2025/26100 AMD64, Linux 7.0.0-1017-azure x86_64 and Darwin 24.6.0 arm64 (49 ordinary forms each). All four public downloads match the frozen identities; original acquired-byte adoption/recovery acceptance is pending. [Publication and hashes](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-acquired.json)'
        elif text.startswith('**Release identities:**'):
            paragraphs[i] = '**Release identities:** the tag records reviewed checkpoint `ee36a934`; the manifest records frozen payload source `158a5cdc`. Install a labelled portable package; GitHub automatic source archives are repository snapshots. Lite 1.0.0 and 1.1.0 tags, assets and original evidence remain preserved.'
        elif text.startswith('**Lite 1.2 progress:**'):
            paragraphs[i] = '**Lite 1.2 evidence:** original archive consumers, exact profile forms, published-predecessor scenarios and final replay are independently accepted. Retained macOS behavior keeps its original subjects and applicability proof. POSIX ownership is cooperative; seven managed forms remain unqualified on each additional profile. [Qualification and limitations](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md)'
        elif text.startswith('**AIDE Lite 1.2.0 is prepared for publication.**'):
            paragraphs[i] = '**AIDE Lite 1.2.0 is published.** One maintained Python 3 source tree uses explicit platform bindings; optional PowerShell adapters require Core 7+. Legacy native ports remain staged. Future Extension 1.0 shares contracts through distinct IDE adapters/packages. [Portability, exit and independent products](docs/reference/portability-and-build-profiles.md).'
    p.write_bytes('\n\n'.join(paragraphs).encode())
    p = TASK / 'status.yaml'
    text = p.read_text(encoding='utf-8').replace('published: false', 'published: true').replace('delivery_state: stopped_before_upload_existing_empty_draft_verified', 'delivery_state: published_acquired_consumer_pending')
    p.write_bytes(text.encode())
    p = TASK / 'ExecPlan.md'
    text = p.read_text(encoding='utf-8')
    pos = text.index('**Current:**')
    text = text[:pos] + '**Current:** release `418708655` is published and all four public downloads match their frozen hashes/sizes. The tag remains at `ee36a934`; the recovery execution checkpoint is `' + base + '`. Stopped/rejected attempts remain preserved. One acquired-byte original consumer remains; no new allocation has occurred.\n'
    p.write_bytes(text.encode())
    p = ROOT / 'IMPLEMENT.md'
    text = p.read_text(encoding='utf-8'); pos = text.index('\n\n') + 2
    if '### Lite 1.2 published and acquired - 21 October 2026' not in text:
        p.write_bytes((text[:pos] + '### Lite 1.2 published and acquired - 21 October 2026\n\nExisting draft `418708655` was published with four exact labelled assets. The annotated tag remains at `ee36a934`; execution source `' + base + '` is separate. All public downloads match immutable hashes/sizes, and the original stopped draft observation remains losslessly preserved. One original acquired-byte adoption/recovery consumer is prepared through the existing600-second runner; qualification allowances remain exhausted and no model requests are admitted.\n\n' + text[pos:]).encode())
    acquired = ROOT / '.aide/release/acquired-aide-lite-v1.2.0.log'
    receipt = json.loads((acquired / 'acquisition.json').read_bytes())
    assert receipt['status'] == 'PASS'
    template = json.loads((QE / 'final-job-template.json').read_bytes())
    names = set(template['inputs']) | {p.relative_to(ROOT).as_posix() for p in (TASK / 'run_acquired_consumer.py', TASK / 'run_consumer.py')}
    names |= {(acquired / n).relative_to(ROOT).as_posix() for n in [*pub['assets'], 'acquisition.json']}
    job = dict(template, owner=TASK.name, workunit=TASK.name,
        argv=[sys.executable, (TASK / 'run_acquired_consumer.py').relative_to(ROOT).as_posix()], canonical_outputs={})
    job['inputs'] = {n: sha(ROOT / n) for n in sorted(names)}
    cfg_path = '.aide.local/lite-successor-qualification-execution.json'
    config, _, working = workspace.load_config(ROOT / cfg_path)
    assert workspace.digest(config) == 'fca2e5c311d117eed49b7f07a33b3cd434801cf46a987db47ff3cc14a4460f33'
    workspace.validate_job(dict(job, source_commit=base, source_tree=git('rev-parse', 'HEAD^{tree}')), working)
    save(E / 'acquired-job-template.json', job)
    plan = {'controller_sha256': sha(TASK / 'run_consumer.py'), 'task_branch': git('branch', '--show-current'),
        'published_tag_target': pub['tag_commit'], 'qualification_config': cfg_path,
        'qualification_config_digest': workspace.digest(config), 'job_template_sha256': sha(E / 'acquired-job-template.json'),
        'files': job['inputs'], 'maximum_local_allocations': 1, 'inner_deadline_seconds': 540,
        'outer_deadline_seconds': 600, 'model_requests': 0,
        'effects': ['Run only original case0 with every fresh/brownfield and partial-recovery assertion on actual acquired ZIP/TAR; collect and retire through existing runner.',
            'The exact accepted consumer checkpoint fills source_commit/tree; no archive/export or exhausted qualification restart. Stop once on failed admission or uncertain outcome.']}
    save(E / 'acquired-effect.json', plan)
    previous = json.loads((E / 'recovery-checkpoint-effect.json').read_bytes())
    effect = dict(previous, base=base, main_base=base, source_parent=base, source_commits=[],
        controller_sha256=sha(TASK / 'consumer_checkpoint.py'), attempt_directory='consumer-checkpoint-attempt-01.log',
        all_refs={r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()},
        effects=['One exact consumer preparation/docs/evidence checkpoint and guarded dev/main synchronization; no job from this checkpoint alone.'])
    save(E / 'consumer-checkpoint-effect.json', effect)
    inputs = json.loads((E / 'recovery-checkpoint-inputs.json').read_bytes())
    inputs['files'] = {n: sha(ROOT / n) for n in inputs['files']}
    save(E / 'consumer-checkpoint-inputs.json', inputs)
    message = ('test(lite): bind the original consumer to public 1.2 downloads\n\n'
        '- Preserve successful publication, exact labelled downloads and complete recovery receipts.\n'
        '- Update current release state while keeping acquired-byte consumer acceptance pending.\n'
        '- Prepare one original case0 through existing resource admission, collection and retirement.\n\n'
        'Validation: PASS - all four public hashes/sizes, successful publication and lossless controller collection; exact runner/config/input validation and structural checks.\n'
        'Changelog: Changed: bind Lite 1.2 public acquisition and original consumer acceptance\n'
        'Risk: The new consumer has not run; full AIDE daily-use, host containment and staged native ports remain open.\n'
        'Follow-up: Execute one independently accepted original acquired-byte consumer and close evidence.\n'
        'AIDE-Task: AIDE-LITE-1-2-PUBLICATION-01\nAIDE-Format: compact-v1\n')
    (E / 'consumer-checkpoint-message.txt').write_bytes(message.encode())
    source, review = E / 'consumer-checkpoint-source.json', E / 'consumer-checkpoint-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    for n in mapped:
        if n.endswith('.py'):
            ast.parse((ROOT / n).read_bytes(), filename=n)
        assert git('hash-object', '--no-filters', '--', n) == git('hash-object', '--path=' + n, '--', n), n
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': base,
        'effect_sha256': sha(E / 'consumer-checkpoint-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'consumer-checkpoint-effect.json'),
        'controller_sha256': sha(TASK / 'consumer_checkpoint.py'), 'acquired_effect_sha256': sha(E / 'acquired-effect.json'),
        'acquired_controller_sha256': sha(TASK / 'run_consumer.py'), 'mapped_files': len(mapped), 'job_input_files': len(job['inputs'])}))


if __name__ == '__main__':
    main()
