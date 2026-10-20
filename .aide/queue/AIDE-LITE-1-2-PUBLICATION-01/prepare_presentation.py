"""Reconcile current release views; preserve frozen package and historical evidence."""
import json
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
E = TASK / 'evidence'
QUAL = ROOT / '.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01'


def write(path, text):
    path.write_bytes(text.encode('utf-8'))


def replace(path, before, after):
    text = path.read_text(encoding='utf-8')
    if before not in text and after in text:
        return
    assert text.count(before) == 1, (str(path), before[:80])
    write(path, text.replace(before, after))


def main():
    # Narrow current-state policy amendment accompanies the pre-tag docs review.
    replace(TASK / 'task.yaml', '    - docs/reference/portability-and-build-profiles.md\n',
        '    - docs/reference/portability-and-build-profiles.md\n    - governance/release-policy.md\n')
    for name in ('task.yaml', 'status.yaml'):
        replace(TASK / name, 'status: prepared\n', 'status: running\n')
    replace(TASK / 'status.yaml', 'bounded_publication_preparation_admission_pending', 'branch_admitted_pre_tag_preparation')
    replace(TASK / 'status.yaml', 'Independently review exact branch/checkpoint admission; prepare pre-tag documentation and frozen publication effect.',
        'Review exact documentation checkpoint, publication/acquisition controller and effect; then verify actual acquired-byte consumer.')
    replace(TASK / 'ExecPlan.md', '**Current:** preparation only. No admission checkpoint/branch, tag, new release, download or consumer allocation in this task has occurred.',
        '**Current:** branch-only admission completed at `3fec7ac3`; all 20 operations/40 streams are losslessly retained and verified. No checkpoint, tag, new release, download or consumer allocation has occurred. Pre-tag reconciliation includes the narrow current-state paragraph in `governance/release-policy.md`; its release rules are unchanged.')
    p = ROOT / '.aide/queue/index.yaml'
    text = p.read_text(encoding='utf-8')
    pos = text.find('AIDE-LITE-1-2-PUBLICATION-01')
    assert pos >= 0
    tail = text[pos:]
    assert 'status: prepared' in tail
    write(p, text[:pos] + tail.replace('status: prepared', 'status: running', 1))
    for name in ('README.md', 'ROADMAP.md', 'DOCUMENTATION.md', 'IMPLEMENT.md'):
        p = ROOT / name
        text = p.read_text(encoding='utf-8')
        # Headings only: prose and historical records retain their meaning.
        text = '\n'.join(('### ' + line[2:] if line.startswith('# ') else '### ' + line[3:] if line.startswith('## ') else line) for line in text.split('\n'))
        write(p, text)
    p = ROOT / 'README.md'
    text = p.read_text(encoding='utf-8')
    paragraphs = text.split('\n\n')
    for i, paragraph in enumerate(paragraphs):
        if paragraph.startswith('**Current portability work:**'):
            paragraphs[i] = '**Current portability work:** [Lite 1.2 archive qualification](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md) is independently accepted and integrated into `dev`/`main` at `3fec7ac3`. Four exact modern companion profiles are qualified: 56 forms on Windows 10 and 49 ordinary forms each on Windows Server, Linux and macOS. Retained evidence keeps its original subjects and applicability proofs. Publication and acquired-download acceptance remain separate.'
        elif paragraph.startswith('**AIDE Lite 1.2.0 is the next planned release**'):
            paragraphs[i] = '**AIDE Lite 1.2.0 is prepared for publication.** Its shared Python 3 implementation uses explicit filesystem/platform bindings; optional PowerShell adapters require Core 7+. Legacy native ports remain staged. Future Extension 1.0 uses shared contracts with distinct IDE adapters/packages. The [portability and build plan](docs/reference/portability-and-build-profiles.md) distinguishes maintained source, exact supported profiles, native targets and future product releases.'
    write(p, '\n\n'.join(paragraphs))
    p = ROOT / 'ROADMAP.md'
    text = p.read_text(encoding='utf-8').replace('Current direction - 19 October 2026', 'Current direction - 21 October 2026')
    a = text.index('Compatible multi-profile metadata')
    b = text.index('AIDE Extension 1.0 is', a)
    text = text[:a] + ('The exact Lite 1.2 candidate is independently qualified and integrated into local/remote `dev` and `main` at `3fec7ac3`. The [qualification report](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md) preserves original failures and subjects, bounded retained evidence, final byte-exact replay and four exact modern profiles. The [publication WorkUnit](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/ExecPlan.md) owns the remaining tag, labelled downloads, publication and original acquired-byte consumer; Lite 1.1 remains the published release until that effect completes.\n\n'
        'One maintained source tree and shared semantic owners remain the design rule. Windows 9x, older Windows NT, MS-DOS/FreeDOS, OS/2, BSD, Unix, Solaris/SunOS and future native ports are staged across later releases. Controller runtime, build host, target ABI and IDE package are separate profiles; modern Python 3 or optional PowerShell Core 7+ is not imposed on every legacy target. [Portability and exit](docs/reference/portability-and-build-profiles.md) defines adoption, customization, coexistence, replacement and removal obligations.\n\n') + text[b:]
    write(p, text)
    p = ROOT / 'TODO.md'
    replace(p, '- [ ] Qualify exact modern Lite 1.2 profiles, portable ordinary CLI and actual 1.1.0 predecessor/customization/conflict/recovery evidence.',
        '- [x] Qualify exact modern Lite 1.2 profiles, portable ordinary CLI and actual 1.1.0 predecessor/customization/conflict/recovery evidence; preserve exact subjects and reviewed applicability.')
    replace(p, '- [ ] Qualify platform participation beyond Windows: bounded Linux/macOS profiles, then evidence-driven BSD/Solaris/Unix adaptations and DOS/OS/2/vintage native or offline-companion paths.',
        '- [ ] Extend qualified modern companion participation into evidence-driven BSD/Solaris/Unix adaptations and DOS/OS/2/vintage native or offline-companion paths.')
    p = ROOT / 'DOCUMENTATION.md'
    text = p.read_text(encoding='utf-8')
    a, b = text.index('**Actual archive phase:**'), text.index('### Shared lifecycle documentation')
    text = text[:a] + ('**Current release boundary:** [Lite 1.2 qualification](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md) is independently accepted and integrated at `3fec7ac3`; [publication and acquired-download acceptance](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/ExecPlan.md) remain. The [portability reference](docs/reference/portability-and-build-profiles.md) records shared source, exact modern profiles, staged native legacy ports, project-owned customization/exit and independently versioned future products. Lite 1.1 remains published. Earlier dated progress notes below retain their historical scope.\n\n'
        '**Release-profile format:** [Lite profiles](docs/reference/lite-release-profiles.md) defines compatible v2 declarations/markers, exact environment and command dispositions and preserved historical identities. Frozen preparation wording is superseded by current qualification evidence; archives are not rebuilt to rewrite their history.\n\n') + text[b:]
    write(p, text)
    p = ROOT / 'docs/reference/portability-and-build-profiles.md'
    text = p.read_text(encoding='utf-8')
    text = text.replace('it does not qualify a versioned 1.2 archive or every managed execution backend.',
        'versioned 1.2 archive qualification is now independently accepted in the [release report](../../.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md). This does not qualify every managed execution backend.')
    text = text.replace('Exact 1.2 profiles and Python minor-version floors must be selected and tested before freezing its release contract; there is no 1.2 candidate archive, date or support expansion yet.',
        'The frozen 1.2 candidate now has accepted T3/L1 companion profiles on Windows 10/19045 AMD64 (56 forms), Windows Server 2025/26100 AMD64, Linux 7.0.0-1017-azure x86_64 and Darwin 24.6.0 arm64 (49 ordinary forms each), all on CPython 3.14.8. Full environment tuples, retained macOS applicability, limitations and original results are linked in the release report. Seven managed-job forms remain unqualified on each additional profile. Publication and acquired-byte acceptance remain separate.')
    text = text.replace('Lite 1.2 must qualify these behaviors against actual published 1.1.0 and exact new profiles.',
        'Lite 1.2 qualification covers these behaviors against actual published 1.1.0 and the exact declared profiles, with original subjects and bounded applicability retained in the release report.')
    write(p, text)
    p = ROOT / 'governance/release-policy.md'
    text = p.read_text(encoding='utf-8')
    a, b = text.index('**Current product state:**'), text.index('\n\n', text.index('**Current product state:**'))
    text = text[:a] + '**Current product state:** Lite 1.1.0 is published, acquired and consumer-verified; 1.0.0 remains preserved. Lite 1.2.0 exact archive/profile qualification is independently accepted and integrated at `3fec7ac3`; its separately admitted [publication WorkUnit](../.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/ExecPlan.md) owns tag, publication and acquired-byte acceptance. Legacy native ports and future products remain staged. The [changelog](../CHANGELOG.md) and [current campaign](../.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/CURRENT.md) distinguish these states.' + text[b:]
    write(p, text)
    for name, heading, content in [
        ('IMPLEMENT.md', '### Lite 1.2 publication preparation - 21 October 2026', 'Qualified integration at `3fec7ac3` is verified across all 165 operations/330 streams. The separately admitted publication branch preserves its 20 operations/40 streams. Pre-tag reconciliation fixes stale current-state descriptions, including the release-policy paragraph, without changing release rules, product code, exports or frozen assets. The first admission collection attempted the prior verifier\'s old evidence directory; task-local binding was corrected and all 41 files roundtrip exactly. Publication, downloads and the one new acquired-byte consumer remain gated.'),
        ('PLANS.md', '### Lite 1.2 publication execution', 'The branch-only admission is complete and losslessly verified. Pre-tag documentation now reflects accepted archive qualification and `dev`/`main@3fec7ac3`. Reuse the existing guarded checkpoint/delivery/acquisition owners; publish four immutable labelled assets, then run one original case0 consumer on public downloads. No archive/export regeneration or repeat of exhausted qualification is admitted. [WorkUnit](.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/ExecPlan.md).')]:
        p = ROOT / name
        text = p.read_text(encoding='utf-8')
        first = text.index('\n\n') + 2
        write(p, text[:first] + heading + '\n\n' + content + '\n\n' + text[first:])
    p = ROOT / 'CHANGELOG.md'
    text = p.read_text(encoding='utf-8')
    pos = text.index('#### AIDE Lite 1.1.0')
    entry = ('#### AIDE Lite 1.2.0 - prepared for publication\n\n'
        '- **Added:** shared Linux/macOS lifecycle bindings and explicit per-environment release profiles from one maintained source tree.\n'
        '- **Qualified:** T3/L1 companion profiles on Windows 10/19045 AMD64 (56 public forms), Windows Server 2025/26100 AMD64, Linux 7.0.0-1017-azure x86_64 and Darwin 24.6.0 arm64 (49 ordinary forms each), all CPython 3.14.8.\n'
        '- **Lifecycle:** fresh/brownfield adoption, project-owned customization, actual published 1.1.0 upgrade/conflict/recovery and owned repair/removal; exact original subjects and retained applicability remain explicit.\n'
        '- **Fixed:** live filesystem re-observation at the existing ownership boundary; false refusal regression and exact release replay passed.\n'
        '- **Limits:** cooperative POSIX ownership; seven managed forms remain unqualified on each additional profile. Outer-client isolation, live-model outcomes and legacy native/IDE parity are outside this release. Changed-path rollback and customized-overlay downgrade retain manual-recovery limits.\n'
        '- **Delivery:** exact archive qualification and dev/main integration passed; publication and acquired-download acceptance pending. [Evidence](.aide/queue/AIDE-LITE-1-2-ARCHIVE-QUALIFICATION-01/REPORT.md).\n\n')
    write(p, text[:pos] + entry + text[pos:])
    # Do not reset historical allocations or relabel companion execution as native-port completion.
    p = ROOT / '.aide/queue/AIDE-LITE-1-2-PORTABILITY-01/release-plan.json'
    plan = json.loads(p.read_bytes())
    plan['state'] = 'exact_archives_qualified_integrated_publication_pending'
    plan['active_increment'] = TASK.name
    plan['current_archive_qualification'] = {'workunit': QUAL.name, 'integration': '3fec7ac375da0e17f035336e080d75ebd26a9920',
        'independent_acceptance': True, 'publication': False, 'acquired_consumer': False,
        'allocations_consumed': 17, 'exports_consumed': 2, 'hosted_runs_consumed': 2, 'hosted_jobs_consumed': 5}
    for profile in plan['candidate_profiles']:
        profile['archive_qualified'] = True
        profile['support_mode'] = 'companion'
        if profile['environment']['system'] == 'Linux':
            profile['environment'].update(release='7.0.0-1017-azure', version='#17~24.04.1-Ubuntu SMP PREEMPT Thu Sep 24 18:46:57 UTC 2026')
    plan['claims']['cross_platform_qualified'] = 'exact_declared_companion_profiles_only_unpublished'
    plan['archive_qualification_allowance']['historical_planning_record'] = True
    plan['archive_qualification_allowance']['current_disposition'] = 'Superseded by owning qualification task amendments; all17local/twoexports/twohosted/fivejobs consumed, no retry allowance.'
    write(p, json.dumps(plan, indent=2) + '\n')
    p = ROOT / '.aide/queue/AIDE-LITE-1-2-PORTABILITY-01/status.yaml'
    text = p.read_text(encoding='utf-8').replace('planning_delivered_development_lifecycle_accepted_release_contract_delivered_archives_in_preparation', 'planning_delivered_exact_archives_qualified_integrated_publication_pending')
    text = text.replace('Continue admitted actual 1.2 archive/public-profile qualification; publication and staged native legacy/IDE products remain separate.',
        'Complete separately admitted Lite 1.2 publication/acquired-byte acceptance; staged legacy native/IDE products and daily-use workflow remain separate.')
    write(p, text)
    print('PASS: pre-tag current-state reconciliation; no product/export/asset changes')


if __name__ == '__main__':
    main()
