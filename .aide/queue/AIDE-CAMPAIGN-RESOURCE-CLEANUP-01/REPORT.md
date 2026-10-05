# AIDE live scratch repair and delivery report — 2026-10-06

The live scratch scanner repair is independently qualified: all 60 workspace
tests passed, then one necessary partial-import recovery task completed through
the normal managed entry using the replacement supervisor. Complete results
were collected and scratch retired. Source integration and delivery of the
repaired payload retain their separate exact effect gates.

## Implemented behavior

A live scan may observe a regular file with zero links while its owner deletes
it. The scanner now reobserves only that regular, non-reparse case, at most twice
with 5 ms waits. Confirmed absence is omitted. Surviving fresh metadata goes
through the existing type, link, byte and file-count checks. Persistent zero
links, redirection, outside hardlinks and observation errors still refuse.
Strict quiescent collection does not retry or accept zero-link members.

Only the existing scanner and its regression module changed product behavior.
All 52 original test methods remain unchanged; eight regressions cover absence,
replacement size/growth, persistent zero links, strict collection, reparse,
observation errors and an outside hardlink. Three small queue helpers capture
complete raw results, prepare the qualified runtime and invoke the unchanged
original recovery canary. No runner rewrite, new checkout or storage layout.

## Actual qualification

| Execution | Actual outcome | Resource observations |
|---|---|---|
| Source job `68cacb7f651e4f70bdc3fb10b873ec4d` | Candidate 60 PASS, no skips. Old scanner's eight regression cases produced the expected four failures/three errors and one strict-case pass; this is expected regression evidence, not an old-suite PASS. | 47,634 B sampled scratch; 276,680,704 B Job memory; 35,863 B retained |
| Runtime builder `bc4e675bfb404899a8de17c595948e32` | Built/read back the exact 26-component execution ZIP; 25 components unchanged, qualified scanner the sole replacement. | 75,175 B sampled scratch; 35,385,344 B Job memory; 87,931 B retained |
| Normal task `78d7338f791849f89182c6bd82c7df50` | Original case03 passed all 10 public CLI checks, including refusal and exact recovery for fresh, predecessor and resolved updates; project-owned bytes preserved. | 22,480,659 B sampled scratch; 330,858,496 B Job memory; 152,621 B retained |

Every job observed `BLACKGLASS-WIN1\CodexSandboxOffline`, exited0 at the
worker and native parent, retained complete owner/receipt/log/output digests,
became quiescent, removed scratch and released reservations. These are separate
job peaks, not a whole-campaign total. Worker model calls were0; controller and
review usage remains unknown, so no matched total-cost saving is asserted.

[Source result](evidence/active-zero-link-source-result.log) and
[review](evidence/active-zero-link-source-result-and-runtime-build-review.log),
[runtime result](evidence/active-zero-link-runtime-build-result.log) and
[review](evidence/active-zero-link-runtime-result-and-normal-path-review.log),
[normal result](evidence/active-zero-link-normal-path-result.log) and
[final source/result review](evidence/active-zero-link-normal-result-and-source-review.log)
bind exact subjects. All review notes were explicitly nonblocking and disposed.

## Effective scope and lifecycle

The normal worker's source checkout was read-only. It could write only its
allocated tmp/cache/output under
`D:/Projects/AIDE/.aide.local/execution/scratch/78d7338f791849f89182c6bd82c7df50`.
Control/config writes were excluded; the exact active receipt was readable.
Python, Git and Codex toolchain roots were readable; network was disabled.
Results remain under the same UUID in the existing retained pool. No installed
execution profile was changed.

The selected runtime is a 69,803 B archive in this existing WorkUnit's evidence,
SHA256 `302688d665d2f1cd1b57d4539d1471ca9337f48dde385ec0f1faae5431ea2032`.
Its scanner SHA256 is
`bca3178f45667bdf326e549858de58469e0cb0153f104c03abfef9ad140a3d96`.
The old export supervisor was preserved. A direct source-root selection was
abandoned before use: the source contains157 Python core files and22 bytecode
files beyond the bounded accepted closure. No blanket cache removal or expanded
runtime limit was used. The existing archive route loads the exact26 directly.

The normal job kept a hard Windows Job memory cap of1 GiB,32 processes,
both4 GiB physical/commit reserves,32 MiB scratch,2 MiB results and900 s runtime.
Its shared locked admission observed218,755,890 B plus38,273,024 B reservations
against256 MiB. Placement is the exercised worker command sandbox. Disk growth
is sampled monitoring/cooperative admission, not a hard filesystem or global
quota. The actual run demonstrates normal deletion/retirement; it does not count
how many live zero-link observations occurred. Controlled regressions establish
that exact retry behavior.

An outer launch-wrapper variable error occurred after exact projection and
inspection0, before native submission. It was preserved and reconciled from
absent native streams/active owner; only the unsubmitted operation was resumed.
There was one actual normal job. No uncertain attempt, worker or copy was
replayed. [Reconciliation](evidence/active-zero-link-normal-path-wrapper-reconciliation.log)
and [numeric terminal](evidence/active-zero-link-normal-path-native-terminal.log)
preserve the distinction.

## Held package and release work

The held ZIP remains
`5cba4ff6658f8f74ea91ec44442e4d566eea20dac90f7f57c53eb903763587fe`:
854 members/851 checksums, including the preventive commit command and the
**old scanner**. None of its four assets changed in these runs. Its previous
98-test archive qualification and unchanged replay remain valid for those
bytes, not proof of delivery of this repair.

Its case0 passed in a retired job; cases1/2 produced actual PASS oracles inside
an overall failed job that exposed this deletion race; case03 now passed under
the qualified replacement supervisor. Cases4–7, current delivered41/full38-form
coverage and qualification of refreshed repaired assets remain unfinished.
The [release WorkUnit report](../AIDE-STABLE-LITE-RELEASE-EFFECT-01/REPORT.md)
owns those package/effect details and historical subjects.

Next authorized delivery sequence: finish exact guarded source/ref integration;
refresh only the changed export/payload closure under the pinned accepted
runtime; qualify affected delivered bytes, consumers, forms and replay; then
obtain the exact final release-effect acceptance and verify publication and
downloaded consumers when its independent prerequisites are satisfied.

## Remaining boundaries

The outer shell, editor/filesystem tools, plugins/integrations, other sessions
and unmanaged processes remain unrestricted. Worker read isolation is
unqualified. This is a qualified managed workflow, not whole-session containment.
The actual outer application/setup remains an external input; no machine ACL,
account, quota or permission mode was changed.

The eleven exact historical message decisions are still proposed, including the
already-published `66b66938` object; no message/history rewrite was performed.
The live nested Sol/medium permission, actual host/matched efficiency evidence,
final stable release acceptance/tag/publication/downloads and wider disk cleanup
remain separate. The reported500 GB machine sprawl was not measured or reclaimed
by this repair. FacMan product development remains paused. Broader codecs,
checkpoints, contributor conformance, invalidation and host support remain
bounded future work, not delivered features.

## Changed files and verification

[Qualification summary](evidence/active-zero-link-qualified-result.json)
preserves exact outcomes, component identities and the complete final independent
review. Full native originals remain in their configured local evidence/retained
roots; their hashes and custody are retained by that summary.

Product: `core/execution/managed_workspace.py` and
`.aide/scripts/tests/test_managed_workspace.py`. Supporting changes: this
WorkUnit's three qualification helpers, task/status/ExecPlan/report, intake
packet/draft, queue index, release task/status/plan/report, runner reference and
root plan/implementation/documentation indexes.

Executed through the existing `aide_lite.py job run` entry with separately
reviewed config/manifests: original baseline helper; full
`test_managed_workspace.py -v`; bounded runtime builder; unchanged
`partial_cli_canary.py` with exact held ZIP/TAR/CLI identities. Native inspection
returned0/writesfalse. Canonical `doctor` and `validate` then passed73 and60,169
checks respectively, with0 warnings/failures; complete raw outputs were retained
and both jobs retired scratch/released reservations. They exercised the exact
867-input/23-file closeout snapshot before these two link captions and actual
validation summary were updated. Source/test/helper bytes remain unchanged.
`git diff --check` and bounded link checks cover those final documentation edits.
The plain validators used the configured qualified Offline route without a new
principal observation. Exact subsequent commit/ref terminal evidence owns
integration; no future commit, export identity, tag or release is invented.
