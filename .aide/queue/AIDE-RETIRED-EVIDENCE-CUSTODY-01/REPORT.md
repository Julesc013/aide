# Retired evidence custody development report

Date:2026-10-05 Australia/Sydney. The actual public custody workflow and 23
regressions pass through the restricted worker. Separately reviewed custody of
two real retired consumer jobs preserved complete evidence and original receipts,
verified lookup, retired redundant raw copies and released 7,921,599 managed
logical bytes. Later delivery source/projection/export qualification is now accepted in the
release WorkUnit; integration and stable certification remain unfinished. Exact maintenance sourcec8351859 received independent
ACCEPT_WITH_NOTES with all notes nonblocking/disposed. The bounded C4 child is
qualified; delivery work continues in the existing release WorkUnit. The outer
session remains unrestricted.

## What changed

The existing `job` command family now has custody plan/apply/recover/verify/read
operations. A finite ZIP preserves every collected log/output byte and empty
directory. Original owner/receipt files and their hashes remain at the same
locations. Archive and original collection digests are checked before raw-copy
retirement; unknown/changed evidence refuses. A pending operation uses the
preexisting active.json latch and admission.lock, so unchanged pinned owners
refuse additional allocation. Custody recovery resumes its exact operation;
ordinary job recovery returns the specific custody remedy.

Bounded evidence lookup resolves original member paths without extraction or
another checkout. Plan output is compact by default; full review evidence is
explicit. Source implementation is core/execution/retired_evidence.py and the
existing CLI. The24 executing owner dependencies are unchanged; worker-editable
source was not silently promoted into its own supervisor.

## Verified actual outcome

Exact sourcedca12298/treee5153a5a, independently accepted native effecte81f6f73,
ran once in job30c718369d6a46ebbb1648ae2f2a866f as CodexSandboxOffline. All23
tests passed without skips/errors/failures. Complete raw logs/output collection,
receipt and proof are verified. Scratch and fixtures retired, process quiescent,
no IO errors, reservation released. The source/native fixture used the current
7132 archive with24 unchanged pinned sources, read-only source, allocated TMP/
output, no canonical writes,2MiB scratch/1MiB logs/64KiB results/180s/2GiB memory/
32 processes and unchanged256MiB cooperative aggregate admission.

| Measurement | Actual observation |
| --- | --- |
| New retained evidence | 9959 logical bytes |
| Sampled workspace/log occupancy | 5483bytes;30s sampling can miss transients |
| Process memory peak | 246890496bytes |
| Known pools after native collection, before custody | scratch0 + control13694135 + retained219091093 =232785228logical bytes |
| Known pools after both live custody operations | scratch0 + control13694135 + retained211169494 =224863629logical bytes |
| Remaining cooperative aggregate capacity | 43571827bytes within unchanged256MiB limit |
| Live custody / reclaimed allocated space | Two transitions verified;7921599logical bytes saved; allocated disk recovery unmeasured |
| Original selected runtime configuration | a241 unchanged; held/stale original archive pin |
| Current stable candidate ZIP | 7132 unchanged; does not contain new custody source |
| Outer shell/editor/plugins and read isolation | Unrestricted / unqualified |
| Whole accepted-outcome efficiency | Unqualified; whole parent/review/retry accounting unknown |

See [result](evidence/native-fixture-result-v3.json),
[proof](evidence/native-fixture-proof-v3.json),
[exact revised effect](evidence/native-fixture-effect-v3.json) and
[effect admission](evidence/native-fixture-admission-v3.json).
Original receipt remains in the configured retained pool; full raw evidence
was not replaced with abbreviated model output.

## What the tests establish

Lossless binary/empty-directory roundtrip, unchanged receipts, equal raw/archive
bounded lookup, readonly lookup after unrelated execution config change,
interruption at intent staging/publication, archive/manifest/raw retirement,
idempotent recovery, exact archive reuse, stale/unknown/nonquiescent/hardlink
refusal, aggregate and canonical-artifact accounting, lock exclusion, changed
raw custody refusal, no new allocation while pending and specific public job
recovery refusal. These fixture results are not a live capacity-recovery proof.

The actual public CLI fixture additionally completes compact plan, raw read,
exact apply, complete verify and archived read with the unchanged pinned owner.
A source namespace gap was found by one real read-only plan after the genuine
22-test pass. Explicit source loading repaired it; a new exact23-test effect
was accepted and passed. Preserve22-test evidence and source rejection.

An earlier21-test native effect was REQUEST_CHANGES before dispatch. Reviewer
found assertion-dependent alias cleanup plus staged-intent and lock-view gaps.
The rejection stays preserved. At that stage, fixes received a new exact review
and only the corrected 22-test attempt ran. The later, separately reviewed
23-test attempt qualified the actual public CLI. No uncertain retry or relabelled
failure occurred.

## Separately reviewed live result

Frozen source8339181c/tree41f1fd1d and exact serial two-job effect1cbca7a2
received independent ACCEPT_WITH_NOTES; every note was explicitly nonblocking
and disposed. Each operation freshly checked its source/configuration, exact
plan and unchanged anchors before apply. Complete archive verification preceded
raw-copy retirement; bounded evidence lookup matched before and after.

| Original retired job | Complete original payload | Custody ZIP | Logical bytes saved |
| --- | ---: | ---: | ---: |
| dc069cd9c81f4ccf81c5959a14519685 | 3035803 | 301200 | 2723463 |
| eff8ab1f2afb4333b14690ee91007ffe | 5802413 | 571864 | 5198136 |

Original receipt hashes36c6ea3d/fc103deb and owner bytes are unchanged. Both
archives reconstruct the original log/output collection digests; no evidence
was truncated. Raw logs/output copies and pending active.json/.next state are
absent after success. The admin operations ran as BLACKGLASS-WIN1\Jules through
the source CLI; they did not expand worker write access. The separate native
fixture ran as CodexSandboxOffline. No model/provider invocation occurred.

[Complete live result](evidence/live-custody-result.json),
[postflight inventory](evidence/live-custody-postflight.json) and
[exact source/effect acceptance](evidence/live-custody-source-effect-acceptance.json)
retain identities and full verification references. Full preflight/apply/verify/
lookup logs remain in this evidence directory. Postflight enumerated only the
three configured pools:6201 entries, no fallback or whole-drive scan. Logical
savings affect cooperative admission; actual allocated disk recovery is unknown.

## Limits, compatibility and next useful work

At most16MiB of original evidence/4096 entries and1MiB intent/manifest JSON are
eligible. Worst-case staging and4MiB metadata reservation must fit the selected
aggregate budget and existing disk/memory headroom. A failed cleanup leaves
pending custody and stops allocation. These are cooperative ownership/admission
controls, not filesystem quotas, account/ACL isolation or whole-session control.

Plain old raw-file paths do not transparently decompress. The explicit custody
map/read interface must be used after a reviewed live transition; existing
receipts and their collection digests stay authentic historical records. Any
further live transition requires its own exact effect review. The two approved
operations used worst-case serial reservations7334555/10184109 within unchanged
256MiB; their measured success grants no authority over other jobs. Preserve
complete required evidence and all8 consumer cases/38 public forms/39 retained
outputs/12 job observations and delivered C1/replay acceptance.

The CLI edit initially made source capability/export projections stale. The
release WorkUnit subsequently passed67 fresh affected checks and fullvalidation
at eea174be, then one independently accepted pure clean export at cf234547
verified849 checksums and complete collection/retirement. See its current report.
Those are later delivery facts; no additional23 execution or new archive is
claimed by this maintenance slice. Packaging and integration remain open. Source
maintenance can continue; it must not claim this archive delivers custody.
Outer-client setup, ten historical dispositions, live model permission, matched
efficiency, stable ACCEPT/tag/publication/download/adoption and wider drive
cleanup remain distinct. FacMan product development remains paused.

## Files and checks

Changed source: retired_evidence.py, aide_lite.py, test_retired_evidence.py;
reference docs, this queue packet/evidence and existing root/generated indexes.

- `scripts/aide compile --write` and `scripts/aide validate`: PASS structural;
  149info/0warnings/0errors in preparation.
- Python AST, `git diff --check`, structured commit-message precheck: PASS.
- Compact task packet: actual CLI `verify_task_packet` PASS; all13 required
  sections, token estimate and context refs;3551bytes, zero warnings/errors.
  Independent review rejected the earlier f3 brief. A template-only comparison
  was narrower than the CLI contract; the actual verifier now establishes the
  fix. Native/live evidence is unchanged; no downstream effects occurred.
- The existing compact template now includes the missing estimate guidance
  under exact one-file scope admission; resulting sourcec8351859 is independently
  accepted, all notes nonblocking/disposed.
- Actual managed `job run` plus23 source tests: PASS; complete postflight and
  retirement verified. Full raw stderr contains23-test/OK result, no skips.
- `job custody plan/read/apply/verify/read` for the exact two jobs: PASS;
  complete digests, anchors, lookup, retirement and cleared pending state checked.
- Full source binding/export refresh, source integration and current-payload
  consumer/replay qualification: NOT RUN in this slice.
