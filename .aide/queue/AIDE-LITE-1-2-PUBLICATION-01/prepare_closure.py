"""Close actual release/consumer evidence and prepare one final guarded sync."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=30).strip()


def write(path, text):
    for before, after in [('Lite1.2', 'Lite 1.2'), ('Lite1.1', 'Lite 1.1'), ('Lite1.0', 'Lite 1.0'),
        ('Extension1.0', 'Extension 1.0'), ('CPython3.14.8', 'CPython 3.14.8'),
        ('21October2026', '21 October 2026'), ('Observed21', 'Observed 21'),
        ('October2026', 'October 2026'), ('56primary', '56 primary'), ('49ordinary', '49 ordinary'), ('17local', '17 local')]:
        text = text.replace(before, after)
    path.write_bytes(text.encode('utf-8'))


def paragraphs(path, changes):
    parts = path.read_text(encoding='utf-8').split('\n\n')
    for i, text in enumerate(parts):
        for prefix, replacement in changes.items():
            if text.startswith(prefix):
                parts[i] = replacement
                break
    write(path, '\n\n'.join(parts))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    terminal = json.loads((E / 'acquired-execution.log').read_bytes())
    assert terminal['state'] == 'acquired_original_consumer_pass'
    job = terminal['job_result']
    base = terminal['source_commit']
    assert git('rev-parse', 'HEAD') == base
    subprocess.run([sys.executable, '-B', str(TASK / 'collect_effects.py'), 'consumer'], check=True, timeout=90)
    publication = json.loads((E / 'published-acquired.json').read_bytes())
    original = json.loads((E / 'delivery-effect.json').read_bytes())
    projection = load('final_release_projection', ROOT / '.aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01/update_presentation.py')
    logs = E / 'closure-readback.log'
    logs.mkdir()
    observed = {}
    for label, endpoint in [('release', '/releases/418708655'), ('releases', '/releases?per_page=99')]:
        argv = [original['gh_executable'], 'api', '-H', 'X-GitHub-Api-Version: 2026-03-10', '-H', 'Cache-Control: no-cache', 'repos/Julesc013/aide' + endpoint]
        out, err = logs / (label + '.stdout'), logs / (label + '.stderr')
        with out.open('xb') as stdout, err.open('xb') as stderr:
            result = subprocess.run(argv, stdout=stdout, stderr=stderr, stdin=subprocess.DEVNULL, timeout=60)
        assert result.returncode == 0
        observed[label] = {'argv': argv, 'exit_code': result.returncode, 'stdout_sha256': sha(out), 'stderr_sha256': sha(err), 'value': json.loads(out.read_bytes())}
    release = projection.projection(observed['release']['value'])
    assert release == projection.projection(publication['release'])
    values = observed['releases']['value']
    assert {v['id'] for v in values} == {418708655, 416392381, 406882845} and len(values) == 3
    for old in original['previous_releases']:
        assert projection.projection(next(v for v in values if v['id'] == old['id'])) == old
    save(E / 'final-publication-readback.json', observed)
    proof = {'state': 'PUBLISHED_ACQUIRED_ORIGINAL_CONSUMER_PASS', 'version': '1.2.0',
        'release': release, 'tag_object': publication['tag_object'], 'tag_commit': publication['tag_commit'],
        'payload_source': '158a5cdcac7afecbc180a6324ea02e46617d1bc9', 'assets': publication['assets'],
        'acquisition_receipt_sha256': publication['acquisition_receipt_sha256'],
        'consumer': {'job_id': job['job_id'], 'source_commit': base, 'source_tree': terminal['source_tree'],
            'manifest_digest': job['manifest_digest'], 'config_digest': job['config_digest'], 'original_assertions': 'unchanged',
            'case': 0, 'partial_recovery': 'PASS', 'exit_code': job['result']['exit_code'],
            'quiescent': job['result']['quiescent'], 'scratch_absent': job['scratch_absent'], 'reservation_released': job['reservation_released']},
        'qualification_review_sha256': sha(QE / 'qualification-closure-review.json'),
        'publication_collection_sha256': sha(E / 'publication-effects-verified.json'),
        'consumer_collection_sha256': sha(E / 'consumer-effects-verified.json'),
        'support_scope': 'Four exact T3/L1 companion profiles; CPython3.14.8,56primary/49ordinary per additional profile. Retained macOS applicability and original subjects remain explicit.',
        'full_platform_complete': False, 'legacy_native_ports_complete': False, 'worker_model_requests': 0,
        'controller_review_usage': 'unknown', 'whole_outcome_efficiency': 'unqualified'}
    save(E / 'published-lite-1.2.0-qualified.json', proof)
    paragraphs(ROOT / 'README.md', {'AIDE Lite **1.2.0 is published**':
        'AIDE Lite **1.2.0 is published** as [`aide-lite-v1.2.0`](https://github.com/Julesc013/aide/releases/tag/aide-lite-v1.2.0). Four exact T3/L1 companion profiles use CPython 3.14.8: Windows 10/19045 AMD64 (56 forms), Windows Server 2025/26100 AMD64, Linux 7.0.0-1017-azure x86_64 and Darwin 24.6.0 arm64 (49 ordinary forms each). All four public downloads match frozen hashes/sizes; the original acquired-byte fresh/brownfield and partial-import recovery consumer passed and retired. [Delivery proof](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json)',
        '**Current portability work:**': '**Current portability work:** Lite 1.2 archive/profile qualification, publication and acquired-byte acceptance are complete for the exact declared profiles. Original failures and retained behavioral applicability remain preserved. [Qualification](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md), [delivery](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json). Broader managed backends, native legacy ports and future products retain separate acceptance requirements.'})
    paragraphs(ROOT / 'ROADMAP.md', {'**Released:**': '**Released:** AIDE Lite 1.2.0 for four exact modern T3/L1 companion profiles:56 public forms on primary Windows and49 ordinary forms on Windows Server/Linux/macOS. Actual published1.1 predecessor/customization/conflict/recovery, immutable package replay, public download identities and the original acquired-byte adoption/recovery consumer are accepted. Historical releases and original evidence remain preserved.',
        'The exact Lite 1.2 candidate is independently qualified': 'Lite 1.2 qualification and public delivery are complete for the exact declared profiles. The [release evidence](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json) preserves tag/payload/execution identities, original failures and retained applicability. Next is the existing daily-use/downstream milestone, with real host delivery, useful accepted work, recovery and complete available effort accounting.'})
    p = ROOT / 'CHANGELOG.md'
    text = p.read_text(encoding='utf-8')
    parts = text.split('\n\n')
    stale = ('- **Qualification candidate:**', '- **Added, development:** compatible multi-profile', '- **Added, development:** shared Linux/macOS')
    parts = [part for part in parts if not part.startswith(stale)]
    text = '\n\n'.join(parts).replace('#### AIDE Lite 1.2.0 - prepared for publication', '#### AIDE Lite 1.2.0 - 21 October 2026')
    text = text.replace('Lite 1.2 modern profile qualification, staged native legacy ports', 'Staged native legacy ports')
    text = text.replace('exact archive qualification and dev/main integration passed; publication and acquired-download acceptance pending.', 'published with four labelled downloads; every public hash/size and original acquired-byte adoption/recovery consumer passed. The job is retired, scratch absent and reservation released.')
    write(p, text)
    p = ROOT / 'TODO.md'
    text = p.read_text(encoding='utf-8').replace('- [ ] Complete Lite 1.2 publication and acquired-byte acceptance.', '- [x] Complete Lite 1.2 publication and acquired-byte acceptance; preserve the one retired original consumer and exact public assets.')
    text = text.replace('- [ ] Review publication and acquired-byte consumers after archive/profile acceptance.', '- [x] Independently review publication and acquired-byte consumer inputs/effects; close exact release evidence.')
    write(p, text)
    paragraphs(ROOT / 'DOCUMENTATION.md', {'**Current release boundary:**': '**Current release boundary:** [AIDE Lite 1.2 delivery](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json) includes exact archive/profile qualification, published labelled assets, verified public downloads and original acquired-byte adoption/recovery acceptance. [Portability and build profiles](docs/reference/portability-and-build-profiles.md) preserves the shared-source design, staged legacy native goals, customization/exit and independently versioned future products. Earlier dated progress notes retain their historical scope.'})
    paragraphs(ROOT / 'governance/release-policy.md', {'**Current product state:**': '**Current product state:** Lite 1.2.0 is published, acquired and original-consumer verified for four exact modern T3/L1 companion profiles. [Delivery evidence](../.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json) preserves immutable assets, actual subjects, retained applicability and retirement. Lite1.0/1.1 remain preserved. Legacy native ports, host products and full daily-use workflow remain staged under their own evidence gates.'})
    p = ROOT / 'docs/reference/portability-and-build-profiles.md'
    text = p.read_text(encoding='utf-8').replace('**Current evidence:** Lite 1.1.0 is published for the exact T3 Windows 10 build 19045/Python 3.14.8 local CLI profile.', '**Current evidence:** Lite 1.2.0 is published and acquired-consumer verified for the four exact T3/L1 modern companion profiles below; historical Lite1.1/1.0 profiles remain preserved.')
    text = text.replace('Publication and acquired-byte acceptance remain separate.', 'Publication and the original acquired-byte consumer are now complete; [delivery evidence](../../.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json) records exact identities and retirement.')
    write(p, text)
    parent = ROOT / '.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01'
    current = ('### Current campaign: useful daily operation remains the finish line\n\n'
        '**Observed21October2026.** [AIDE Lite1.2.0](https://github.com/Julesc013/aide/releases/tag/aide-lite-v1.2.0) is published, acquired and original-consumer verified. This view projects existing queue/evidence records and grants no new authority.\n\n'
        '**Delivered:** four exact T3/L1 companion profiles, CPython3.14.8;56primary Windows forms and49ordinary forms each on Windows Server/Linux/macOS. Four labelled assets match frozen identities. Tag checkpoint `ee36a934`, payload source `158a5cdc` and subsequent execution checkpoints remain distinct. The acquired-byte case0 and partial recovery passed; the one job retired with absent scratch/released reservation. [Proof](../AIDE-LITE-1-2-PUBLICATION-01/evidence/published-lite-1.2.0-qualified.json).\n\n'
        '**Preserved:** Lite1.0/1.1 assets, all failed/interrupted attempts, original evidence subjects and bounded retained macOS applicability. Qualification consumed17local allocations, two exports and two hosted runs/five jobs; publication used one distinct acquired-byte allocation. No allowance is reset. Worker model requests were zero; controller/review usage and whole-outcome efficiency remain unknown.\n\n'
        '**Remaining useful outcome:** complete and repeat real work in AIDE and one downstream project, preserving customization, useful results, interruption recovery, exclusive mutation ownership and complete available effort accounting. Full AIDE is unfinished.\n\n'
        '| Next work | Required condition / existing owner |\n| --- | --- |\n'
        '| Host delivery/editing/cancellation | Host owner supplies the supported endpoint/session/workspace or explicit cooperative binding; qualify the actual route and boundaries. |\n'
        '| DiskEd adoption | Local checkout is idle per user; another machine contributes. Refresh actual source/preimages and admit a finite native target phase, preserving DE-W000/tools and exhausted prior allowances. |\n'
        '| FacMan-to-Setup dependency | Current request accepted by both project owners; returned exact result and requester adoption. No unofficial clone or second writer. |\n'
        '| Better decisions and learning | Existing reuse/context/lesson owners; evaluate actual usefulness, correction and invalidation before routing changes or model adaptation. |\n'
        '| Mini and efficiency | Pinned optional worker/approved route and finite live-model budget; matched accepted outcomes, complete known costs and explicit unknowns. |\n'
        '| Legacy/native and Extension1.0 | Existing staged native/host lanes; shared semantics and separate toolchains/packages; companion participation is not native-port completion. |\n\n'
        'The unqualified readability checkpoint `8cd2236f` remains on its local task branch with zero jobs. Independent work can proceed when its own prerequisites are ready; unchanged blockers do not restart observers or model turns. [Roadmap](../../../ROADMAP.md), [TODO](../../../TODO.md), [portability/exit](../../../docs/reference/portability-and-build-profiles.md).\n')
    write(parent / 'CURRENT.md', current)
    p = parent / 'status.yaml'
    lines = p.read_text(encoding='utf-8').splitlines()
    values = {'observed_source_checkpoint': base, 'next_action': 'Continue existing useful daily-use and downstream workflow through its exact host/source/owner gates; Lite1.2 publication is complete.',
        'published_lite': '1.2.0 exact four modern T3/L1 companion profiles;1.1.0 and1.0.0 preserved', 'qualified_unpublished_lite': 'none;1.2.0 published and acquired-consumer verified',
        'published_profile_ref': (E / 'published-lite-1.2.0-qualified.json').relative_to(ROOT).as_posix(), 'current_state_sha256': sha(parent / 'CURRENT.md')}
    write(p, '\n'.join(next((key + ': ' + value for key, value in values.items() if line.startswith(key + ':')), line) for line in lines) + '\n')
    portability = ROOT / '.aide/queue/AIDE-LITE-1-2-PORTABILITY-01'
    p = portability / 'release-plan.json'; plan = json.loads(p.read_bytes())
    plan['state'] = 'exact_modern_profiles_published_acquired_original_consumer_verified'
    plan['current_archive_qualification'].update(publication=True, acquired_consumer=True)
    plan['claims']['cross_platform_qualified'] = 'exact_declared_companion_profiles_only_published'
    write(p, json.dumps(plan, indent=2) + '\n')
    p = portability / 'status.yaml'; text = p.read_text(encoding='utf-8').replace('planning_delivered_exact_archives_qualified_integrated_publication_pending', 'planning_delivered_modern_release_published_acquired_consumer_pass')
    text = text.replace('Complete separately admitted Lite 1.2 publication/acquired-byte acceptance; staged legacy native/IDE products and daily-use workflow remain separate.', 'Lite1.2 exact modern release is complete; continue existing daily-use/downstream and staged legacy native/IDE work through their own gates.')
    write(p, text)
    p = TASK / 'status.yaml'; text = p.read_text(encoding='utf-8').replace('status: running', 'status: passed').replace('result: PENDING', 'result: PASS').replace('product_qualified: false', 'product_qualified: true').replace('local_jobs_consumed: 0', 'local_jobs_consumed: 1').replace('planning_state: published_acquired_original_consumer_preparation', 'planning_state: published_acquired_original_consumer_pass').replace('delivery_state: published_acquired_consumer_pending', 'delivery_state: published_acquired_consumer_pass')
    text = '\n'.join('next_action: Continue the existing daily-use/downstream campaign; no new release or allocation from this completed task.' if line.startswith('next_action:') else line for line in text.splitlines()) + '\nacceptance_scope: Exact Lite1.2 package and four declared companion profiles; full AIDE/native legacy/host products remain unfinished.\n'
    write(p, text)
    p = TASK / 'task.yaml'; write(p, p.read_text(encoding='utf-8').replace('status: running', 'status: passed'))
    p = ROOT / '.aide/queue/index.yaml'; text = p.read_text(encoding='utf-8'); pos = text.index('- id: AIDE-LITE-1-2-PUBLICATION-01')
    write(p, text[:pos] + text[pos:].replace('status: running', 'status: passed', 1))
    p = TASK / 'ExecPlan.md'; text = p.read_text(encoding='utf-8'); pos = text.index('**Current:**')
    write(p, text[:pos] + '**Current:** publication, all four acquired hashes/sizes and original case0/partial-import recovery passed. The one acquired-byte allocation is retired; scratch absent, reservation released and lossless collection verified. Final source/effect review and guarded closeout integration preserve tag/payload identities and retire only this owned local task branch. Actual final refs remain in the operation receipt; this plan does not invent a future commit hash.\n')
    report = ('### AIDE Lite1.2 delivery\n\n**Published:** release418708655, `aide-lite-v1.2.0`, four labelled immutable assets. Tag object `' + publication['tag_object'] + '` targets `' + publication['tag_commit'] + '`; payload source remains `158a5cdc`. Public acquisition and original fresh/brownfield plus partial-import recovery passed. Job `' + job['job_id'] + '` is retired, quiescent, scratch absent and reservation released.\n\n'
        '**Evidence:** [qualified outcome](evidence/published-lite-1.2.0-qualified.json), [consumer collection](evidence/consumer-effects-verified.json), [publication collection](evidence/publication-effects-verified.json), [original stop](evidence/stopped-delivery-verified.json). Raw/chunked receipts preserve every recorded outcome; no qualification allowance or failed attempt was reset.\n\n'
        '**Limits:** exact T3/L1 companion profiles on CPython3.14.8;56primary/49ordinary per additional profile. POSIX ownership remains cooperative; seven managed forms on additional profiles, outer-client isolation, whole-task efficiency, legacy native ports and future host/service products remain outside this claim. Original rollback/custom-overlay recovery limits remain.\n\n'
        '**Integration:** the separately reviewed final checkpoint uses existing guarded dev/main synchronization and retires only its owned local task branch after ancestry/preservation checks. Its own post-commit receipt stays task-local runtime evidence at `evidence/closure-checkpoint-attempt-01.log/result.json`; final Git refs identify the actual checkpoint, avoiding another evidence-only commit cycle. No new tag or asset mutation occurs.\n')
    write(TASK / 'REPORT.md', report)
    for name, heading in [('PLANS.md', '### Lite1.2 delivered - 21 October2026'), ('IMPLEMENT.md', '### Lite1.2 acquired consumer and closure - 21 October2026')]:
        p = ROOT / name; text = p.read_text(encoding='utf-8'); pos = text.index('\n\n') + 2
        write(p, text[:pos] + heading + '\n\nLite1.2 is published and all four public hashes/sizes match. The original acquired-byte adoption/recovery consumer passed in one retired job; complete receipts roundtrip. Historical/rejected/stopped results and tag/payload identities remain preserved. The source-only preparer originally validated prospective placeholder IDs; its corrected copy check did not allocate or run a test. Final reviewed closeout updates current docs and safely syncs dev/main, with its own operation receipt retained as runtime evidence. [Delivery report](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/REPORT.md). Full daily-use/downstream, host and staged native/Extension work remain open.\n\n' + text[pos:])
    controller = (TASK / 'checkpoint.py').read_text(encoding='utf-8').replace('publication-checkpoint', 'closure-checkpoint').replace('publication-projection', 'closure-projection')
    anchor = '            remote("remote-final")\n            record.update(status="PASS", refs=state)'
    assert controller.count(anchor) == 1
    controller = controller.replace(anchor, '            remote("remote-final")\n            git("switch-owned-dev", "switch", "dev")\n            assert git("retirement-head", "rev-parse", "HEAD") == commit\n            git("owned-ancestor", "merge-base", "--is-ancestor", plan["task_branch"], "dev")\n            git("retire-owned-local-task", "branch", "-d", plan["task_branch"])\n            record["task_branch_retired"] = True\n            inputs()\n            assert not git("retirement-clean", "status", "--porcelain")\n            record.update(status="PASS", refs=state)')
    write(TASK / 'closure_checkpoint.py', controller)
    previous = json.loads((E / 'consumer-checkpoint-effect.json').read_bytes())
    effect = dict(previous, base=base, main_base=base, source_parent=base, source_commits=[], all_refs={r.split()[1]: r.split()[0] for r in git('show-ref').splitlines()},
        controller_sha256=sha(TASK / 'closure_checkpoint.py'), attempt_directory='closure-checkpoint-attempt-01.log',
        effects=['One exact final evidence/docs checkpoint, guarded dev/main FF/nonforce sync, matching task-local previews and retirement of only owned local task/aide-lite-1-2-publication-01 after ancestry/preservation checks. No publication, tag, asset, export or job effect.'])
    save(E / 'closure-checkpoint-effect.json', effect)
    pins = json.loads((E / 'consumer-checkpoint-inputs.json').read_bytes())
    pins['files'] = {n: sha(ROOT / n) for n in pins['files']}
    save(E / 'closure-checkpoint-inputs.json', pins)
    message = ('docs(lite): close published 1.2 acceptance and current roadmap\n\n'
        '- Preserve exact publication, public download and original consumer pass with lossless receipts and retired ownership.\n'
        '- Reconcile README, docs, TODO, plans, roadmap, changelog and release/portability state without changing frozen bytes.\n'
        '- Preserve full-platform blockers and prepare final guarded dev/main sync and owned local branch retirement.\n\n'
        'Validation: PASS - original acquired-byte case0 and partial recovery; exact four assets and fresh public readback; complete receipt roundtrip, quiescence and retirement.\n'
        'Changelog: Changed: publish Lite1.2 exact modern profiles and close acquired-package acceptance\n'
        'Risk: Outer containment, whole-outcome efficiency, actual daily-use/downstream and staged native/host products remain unfinished.\n'
        'Follow-up: Continue existing campaign through dependency-ready host/source/owner gates; no qualification or publication restart.\n'
        'AIDE-Task: AIDE-LITE-1-2-PUBLICATION-01\nAIDE-Format: compact-v1\n')
    write(E / 'closure-checkpoint-message.txt', message)
    source, review = E / 'closure-checkpoint-source.json', E / 'closure-checkpoint-review.json'
    excluded = {p.relative_to(ROOT).as_posix() for p in (source, review)}
    changed = set(git('diff', '--name-only').splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
    mapped = {n: sha(ROOT / n) for n in sorted(changed - excluded)}
    for n in mapped:
        if n.endswith('.py'):
            ast.parse((ROOT / n).read_bytes(), filename=n)
        assert git('hash-object', '--no-filters', '--', n) == git('hash-object', '--path=' + n, '--', n), n
    git('diff', '--check')
    save(source, {'schema': 'aide.exact-source-map.v1', 'workunit': TASK.name, 'base': base, 'effect_sha256': sha(E / 'closure-checkpoint-effect.json'), 'files': mapped})
    print(json.dumps({'source_sha256': sha(source), 'effect_sha256': sha(E / 'closure-checkpoint-effect.json'), 'controller_sha256': sha(TASK / 'closure_checkpoint.py'), 'mapped_files': len(mapped), 'job_id': job['job_id']}))


if __name__ == '__main__':
    main()
