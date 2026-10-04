# Retired evidence custody development report

Date:2026-10-05 Australia/Sydney. A bounded C4 source repair now passes22
meaningful regressions through the restricted managed worker. Live custody,
source integration and stable certification remain unfinished.

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

Exact source50c0ac2b/treea0752bc9, independently accepted native effectae629dc4,
ran once in jobc1ae2a93c1ca48c8941abea371a9bfa7 as CodexSandboxOffline. All22
tests passed without skips/errors/failures. Complete raw logs/output collection,
receipt and proof are verified. Scratch and fixtures retired, process quiescent,
no IO errors, reservation released. The source/native fixture used the current
7132 archive with24 unchanged pinned sources, read-only source, allocated TMP/
output, no canonical writes,2MiB scratch/1MiB logs/64KiB results/180s/2GiB memory/
32 processes and unchanged256MiB cooperative aggregate admission.

| Measurement | Actual observation |
| --- | --- |
| New retained evidence | 9620 logical bytes |
| Sampled workspace/log occupancy | 5311bytes;30s sampling can miss transients |
| Process memory peak | 246722560bytes |
| Known pools after collection | scratch0 + control13694135 + retained219081134 =232775269logical bytes |
| Live custody / reclaimed allocated space | No transition; no recovery measurement |
| Original selected runtime configuration | a241 unchanged; held/stale original archive pin |
| Current stable candidate ZIP | 7132 unchanged; does not contain new custody source |
| Outer shell/editor/plugins and read isolation | Unrestricted / unqualified |
| Whole accepted-outcome efficiency | Unqualified; whole parent/review/retry accounting unknown |

See [result](evidence/native-fixture-result-v2.json),
[proof](evidence/native-fixture-proof-v2.json),
[exact revised effect](evidence/native-fixture-effect-v2.json) and
[effect admission](evidence/native-fixture-admission-v2.json).
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

An earlier21-test native effect was REQUEST_CHANGES before dispatch. Reviewer
found assertion-dependent alias cleanup plus staged-intent and lock-view gaps.
The rejection stays preserved; fixes received a new exact review and only the
corrected22-test attempt ran. No uncertain retry or relabelled failure.

## Limits, compatibility and next useful work

At most16MiB of original evidence/4096 entries and1MiB intent/manifest JSON are
eligible. Worst-case staging and4MiB metadata reservation must fit the selected
aggregate budget and existing disk/memory headroom. A failed cleanup leaves
pending custody and stops allocation. These are cooperative ownership/admission
controls, not filesystem quotas, account/ACL isolation or whole-session control.

Plain old raw-file paths do not transparently decompress. The explicit custody
map/read interface must be used after a reviewed live transition; existing
receipts and their collection digests stay authentic historical records. Live
transition is separately gated. Two exact old consumer jobs are candidates;
metadata estimates confer no disposal authority or admitted space. Preserve
complete required evidence and all8 consumer cases/38 public forms/39 retained
outputs/12 job observations and delivered C1/replay acceptance.

The CLI edit makes affected source capability/export projections stale. Their
explicit refresh, packaging and source integration are later bounded effects;
no whole-source validation or new current archive is claimed here. Source
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
- Actual managed `job run` plus22 source tests: PASS; complete postflight and
  retirement verified. Full raw stderr contains22-test/OK result, no skips.
- Full source binding/export refresh, source integration, live custody and
  current-payload consumer/replay qualification: NOT RUN in this slice.
