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
