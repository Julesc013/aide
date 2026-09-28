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
