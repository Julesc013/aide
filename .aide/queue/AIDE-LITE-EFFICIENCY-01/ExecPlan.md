# AIDE Lite execution efficiency

## Purpose and scope

Add the smallest portable mechanism that stops model polling during an AIDE
job and returns a bounded, truthful outcome. The existing Windows maintainer
runner remains the sole process, reservation and cleanup owner. This WorkUnit
adopts the owner's 2026-09-28 efficiency priority; the attached amendment is
an implementation brief, while the owner's direct request supplies priority.

## Current facts

- Parent branch base `190d3f5c` preserves reviewed post-Lite lifecycle work.
- Remote `dev@76e17a4c` holds an earlier accepted local Lite release candidate;
  ten exact historical-message owner decisions still gate main promotion.
- `job run` already blocks inside deterministic code and retains a detailed
  receipt, but its CLI prints the entire receipt. The runner is source-only.
- The portable `.aide/scripts/aide_lite.py` is exported to Lite; the first
  observer must work without importing the source-only runner.

## Milestones and verification

1. Implement `job wait` as read-only attach to an exact existing job ID and
   manifest digest. Check current control and retained state with bounded
   reads, wait without emitting healthy ticks, then return one compact view.
   Include actual observer reads/unchanged observations and identify host model
   usage as unknown. Never submit, cancel, clean or acknowledge a job.
2. Tiny synthetic tests: unchanged healthy wait, terminal recovery on repeated
   read, stale/mismatched attempt, missing/malformed/oversized evidence, timeout,
   and path redirection. No large fixture or new workspace.
3. Exercise an actual necessary AIDE validation through the configured D job
   owner and the new observer. Record exact source, job, resource and result
   identities; preserve full evidence outside the compact view.
4. Qualify the exported Lite CLI in a disposable consumer without importing
   the source checkout. Obtain independent exact source/effect review, then
   reconcile the minimum efficiency contract into the next release candidate.

## Recovery and limits

The observer has no write ownership. An observation timeout is pending, not a
terminal job result; reattach to the same exact identity. A missing or corrupt
receipt must never be reported as PASS. No CLI path can claim control of
unmediated Codex turns or internal inference. Later increments must add
pause-aware dispatch, supported host binding and actual usage normalization
before broader efficiency claims. FacMan product development stays paused.

## Progress

- [x] Owner priority and current runner/export boundaries characterized.
- [x] Portable observer and bounded view implemented at frozen source `f30bbad2`; exact independent source integration/local-effect ACCEPT.
- [x] First source candidate `54b83760` adds portable read-only attachment;
  six D-managed synthetic tests passed on that exact source, and a copied Lite
  CLI ran without a source checkout. The superseding `f30bbad2` makes compact
  `job run` output the default and retains explicit `--full` compatibility.
- [x] Six synthetic cases and one actual export-inclusion job passed under the configured D runner; receipts and resource bounds are in `evidence/first-slice-qualification-2026-09-29.md`.
- [ ] Qualify the actual exported Lite archive and host binding. The copied CLI fixture passed without source checkout, but is narrower than full archive qualification.
- [x] A generated export-pack fixture was archived, extracted and used as an isolated Lite consumer at test-only `45c143de`; exact D job PASS and a preceding false-test failure are recorded in `evidence/export-consumer-qualification-2026-09-29.md`. Canonical release bytes remain unfrozen.
- [ ] Continue pause-aware dispatch, usage/outcome accounting and release qualification in bounded increments.

## Next bounded increment: portable Codex usage import

Add a read-only `job usage` view for up to eight ordinary, bounded Codex
`exec --json` streams. Count each completed turn once, preserve failed or
missing-usage coverage as unknown, and report input, cached input, output and
reasoning output separately. Reject changed/malformed or oversized input;
never echo raw model messages or start a model. Exercise duplicate, cumulative,
failed and malformed synthetic streams under the D runner. This is a host
usage-import boundary, not permission to dispatch or a claim that every Codex
or Work request passes through AIDE. Exact source review and an actual supported
host binding remain gates.

Source `728e61a2` passed its first tests but received independent
REQUEST_CHANGES for missing turn-start accounting. Superseding `fe8bca8b`
passed 11 focused cases and one extracted-pack case under the D runner;
independent delta review returned ACCEPT. Exact receipts and limits are in
`evidence/codex-usage-import-qualification-2026-09-29.md`. Next obtain a real
host stream and bind pause-aware dispatch before claiming host-level savings.

The reviewed post-Lite source candidate `28492e00` fast-forwarded local and
remote `dev` on 2026-09-29. The exact integration review and observed refs are
in `evidence/dev-source-integration-2026-09-29.md`. Release acceptance remains
bound to older frozen bytes; qualify a new tree and its delivered consumers.

## Next bounded increment: deliver the existing job owner in Lite

Export the existing Windows managed-workspace owner and only its direct Python
dependencies as payload files. Do not fork its allocator or supervisor. Keep
safe import from copying broad `core/**` paths into a target repository; the
operator runs the extracted Lite CLI against an explicit, disposable Git
consumer. Preserve source-checkout admission for maintainer tests while an
unconfigured extracted pack can still run its portable no-model selftest.

Add one extracted-ZIP consumer test: configure tiny finite local roots under the
test's admitted D scratch, inspect and run a source-bound Python job through the
delivered CLI, verify the compact result and retired scratch. No Codex request,
canonical release rebuild, target-owned rollout or alternative storage pool.
Review the exact source delta before dev integration. A real host dispatch
binding, usage coverage and final release bytes remain separate gates.

Source `b117f0f8` passed the first extracted-ZIP consumer case, but independent
review found a missing-index admission bypass. Superseding `26f343b7` passed
both the delivered job and missing-index refusal tests in a D-managed job;
independent review returned ACCEPT for dev source integration. The exact
receipts and limits are in `evidence/portable-job-owner-qualification-2026-09-29.md`.
Local and remote `dev` then fast-forwarded to evidence closeout `b9aad160`.
The real host binding and final canonical release bytes remain open.

A no-model installed-Codex context preflight measured 45639 visible text
UTF-8 bytes for a fresh debugger input with a 44-byte probe message. This
does not count tokens or prove an actual worker turn. Exact version, executable
hash and coverage limits are in `evidence/codex-context-preflight-2026-09-29.md`.

## Next bounded increment: make the context observation repeatable in Lite

Add a read-only `job context` parser for one bounded Codex `debug prompt-input`
JSON stream on stdin. Count text per role without retaining or printing raw
prompt material; label tool definitions, effective tokens, internal inference
and actual model calls unknown. Reject malformed and oversized streams. Test
synthetic privacy/boundary cases and one installed-host no-model stream under
the configured D runner. This parser does not launch Codex or qualify the
pause-aware worker; those gates remain open.

The superseding `b4f250f7` source passed 3/3 synthetic and installed-host
cases under the D runner after two retained failed attempts exposed the real
`input_text` schema. Independent source review returned ACCEPT for dev
integration. The next extracted-pack qualification must assert `job context`
from delivered bytes. Exact receipts and limits are in
`evidence/codex-context-parser-qualification-2026-09-29.md`.

The extracted-ZIP fixture consumer now asserts `job context` from delivered
bytes and passed 1/1 in D-managed job `680c0a88`. Its scratch was retired and
the reservation released. This closes the fixture proof; final canonical
release bytes and a live mediated host binding remain separate gates.

## 2026-09-29 delivered wait attachment qualification

Objective: extend the existing extracted-ZIP consumer to attach to the actual
job it just ran, using the returned exact job ID and manifest digest. Check the
retained terminal receipt, zero observer-started model requests, and refusal
of a changed manifest digest. Use the current D-managed test owner, preserve the
exact committed test source and receipt, and review this test-only increment
before dev integration. No Codex invocation or canonical release rebuild is
part of this slice. The real host binding and final release bytes remain open.

The committed test-only candidate `3796ad33` passed the exact extracted-pack
consumer test 1/1 under the D owner. It reattached to the real completed job,
rejected a changed digest, and retired scratch. The exact receipt and limits
are in `evidence/delivered-wait-attachment-2026-09-29.md`. Independent review
remains before dev integration; this is not a live Codex or final asset proof.

Independent `/root/stable_effect_review` then **ACCEPTED dev test/evidence
integration** of the exact test commit and evidence-only closeout. The reviewer
rehashed the retained receipt and checked the delivered attachment and refusal;
see `evidence/delivered-wait-attachment-review-3796ad33.md`. No test rerun or
live model effect was claimed.

## 2026-09-29 usage JSON ambiguity repair

Objective: make the existing portable `job usage` importer reject duplicate
JSON object keys in Codex event lines, including nested token counters. Python's
default parser otherwise keeps the last value and can report a misleading
complete usage total. Scope: the existing Lite importer, its focused tests and
this WorkUnit's evidence. Reproduce with a conflicting duplicate counter and
event type, repair without adding a parser dependency, run the focused suite
through the configured D owner, then obtain exact source review before dev.
This does not launch a model or replace the pending real-host qualification.

The exact source candidate `8a12605d` passed 15/15 focused cases in a
D-managed job, including conflicting duplicate counter and event type
regressions. Scratch retired and the reservation was released. Independent
`/root/stable_effect_review` ACCEPTed dev source integration. Receipt, review
and limits are in `evidence/codex-usage-duplicate-key-2026-09-29.md`.

## 2026-09-29 one-turn Codex host binding

Objective: admit a single explicit Codex `exec` job through the existing
managed-workspace Windows Job, reservation, log and retirement owner. The
current runner admits Python only, so Lite cannot yet demonstrate a supported
host-applied model path. Extend that owner's job schema with a distinct
`codex_exec` adapter and bound task-packet/schema inputs; keep ordinary Python
behavior unchanged. Build a literal, read-only, ephemeral one-turn CLI command
with explicit ChatGPT account method, model and effort; disable nested agents,
apps, hooks, remote plugins and web search. Launch in the admitted D scratch,
send only the bounded packet on stdin and retain bounded JSONL output locally.
No arbitrary argv, API fallback, global settings change or automatic replay.

First prove refusal of malformed/missing/escaping inputs and capture the exact
command with a synthetic host under the existing D runner. Then qualify the
installed host path and a real model turn only when account allowance and
effect scope are established. Obtain independent source/security review before
dev integration. Export and downloaded-byte qualification remain later gates.
This amendment uses the owner's campaign delegation to extend the existing
owner for the explicit efficiency priority; it does not add a scheduler.

The initial reviewed host subject `12ac93c9` received REQUEST_CHANGES for
permission/budget, retained prompt reservation and executable parent identity.
The intermediate `33151c5e` received REQUEST_CHANGES for ambiguous local JSON
permission. Final source `67e1d572` passed 46/46 synthetic Windows managed-job
tests in D: job `5e5972bf`; scratch retired and reservation released.
Independent `/root/native_os_build_review` ACCEPTed that exact tree for dev
source integration. Its source verdict does not qualify a live model turn,
Codex JSONL result, actual usage, extracted Lite or final release bytes. The
exact review and test receipt are recorded in
`evidence/codex-host-binding-qualification-2026-09-29.md`.

## Next delivered boundary: current extracted Lite Codex admission

Objective: extend the existing extracted-ZIP fixture consumer to prove that the
new Codex adapter is present in delivered Lite and refuses a model turn without
the separate local permission. Keep the same disposable consumer and D-managed
runner, without launching a model or generating the canonical release pack.
Record the exact fixture source and receipt, then seek focused test review.
This closes delivered admission/refusal only; a live turn and JSONL verdict
remain separate qualification gates.

Frozen `1bacae3a` passed the extracted fixture but independent review
REQUESTED_CHANGES because it exercised `job inspect`. Superseding `8b0cba06`
exercises delivered `job run`, passed 1/1 in the D-managed job `dabd6ae6`,
retired scratch, and received independent ACCEPT for dev test integration.
The exact receipts and review scope are in
`evidence/codex-delivered-admission-2026-09-29.md`.

## 2026-09-29 known usage subtotal integrity

Objective: prevent the portable `job usage` result from presenting missing
token categories as zero, and from counting a stream with conflicting terminal
events as a known subtotal. Scope: the existing importer in
`.aide/scripts/aide_lite.py`, its focused regression file and this WorkUnit.
First assert the current wrong subtotal on synthetic one-turn JSONL, then
repair the calculation without introducing a parser or storage service. Run
the affected tests through the approved D owner, obtain narrow independent
source review and integrate only accepted source. Rebuild exact Lite assets
later as one coherent changed-source projection; the accepted `42672db9`
release subject and its local effect remain historical evidence, not a test
result for changed code. No live Codex request or new workspace is needed.

The red D-managed run failed exactly the two new usage integrity regressions.
After the parser repair, all 17 focused cases passed in one D-managed job;
both attempts retired scratch and released reservations. Freeze the source
with the small receipt record, then request independent review of this delta.
Independent review ACCEPTED exact source `46c51f71` for dev integration. The
review did not rerun tests or extend acceptance to previously built assets.
Next: preserve this verdict, integrate source into dev, then refresh the
current-source release projection and qualify its exact delivered bytes.

## 2026-09-29 turn-boundary subtotal correction

Objective: keep a valid independent session's known usage subtotal when a
different stream has an ambiguous turn boundary. Scope is the existing usage
importer, its focused regression test, and this WorkUnit's evidence. First
prove the failure with a synthetic two-session stream through the configured
D-managed runner, then exclude only the ambiguous record from the subtotal.
Retain the global same-session ambiguity guard and unknown full totals. Run the
focused suite, request exact-source review, and defer changed-byte release
projection until the next coherent release refresh. No live model call or new
workspace is needed.

The D-managed red run `bdfa68a4` failed only the new regression (17 other
cases passed). The repaired source passed all 18 cases in job `6da5799b`;
both jobs retired scratch and released reservations. Independent source review
and changed-byte release qualification remain pending.

## 2026-09-29 bounded attempt attribution

Objective: add a read-only attempt roster to the existing portable `job usage`
importer so a completed work outcome can distinguish parent, child, review,
retry, repair and overhead streams. Use a bounded JSON file with unique attempt
IDs, explicit parent links and exact stream digests. A missing stream remains
an explicit gap; supplied roster completeness and internal host requests stay
unverified. No model call, tariff, billing claim or new storage service.

Scope: `.aide/scripts/aide_lite.py`, focused efficiency regressions, the
existing Lite runner guide and this WorkUnit. First test missing, duplicate,
cross-session and role accounting
cases with synthetic streams; implement against the existing parser and run
the focused suite through the approved D runner. Obtain independent exact
source review before dev integration. Refresh release bytes once after the
coherent efficiency source slice; do not repeat the just-qualified consumer
matrix for each internal edit. The separate live host permission remains a
real qualification boundary.

Four new attribution cases produced the expected red result in D-managed job
`3b4489de` while the earlier 18 cases passed. The implemented importer passed
all 22 cases in D-managed job `1f2be7e7`; scratch retired and reservation was
released. Exact source review, dev integration and changed-byte release
qualification remain pending. Full work usage and live host requests remain
unknown.

Independent exact-source review requested changes to `cec72cb6`: malformed
parent IDs and deeply nested JSON could crash the CLI rather than produce
`REFUSED`. Two new cases reproduced the defects in D-managed job `80d5b71e`.
The repair validates all parent IDs before traversing links and converts JSON
recursion failure to bounded refusal. The 24-case suite passed in job
`2f84b44b`. The superseding source needs its own scoped review; this does not
change the live-model or delivered-byte gates.
