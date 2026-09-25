# ExecPlan: removal planner dev integration

## Objective and scope

Preserve the delivered-pack removal planner's receipt-bound source and tests in
current dev without replacing later customization, host, historical-policy, or
release-generator work. Operate only within this WorkUnit's allowlist. No
removal apply, deletion, live target effect, or public release.

## Dependencies and sequence

1. Verify clean dev `1c75abf1`, source `d1362f91`, merge base, helper plan,
   one Git writer, and exact accepted historical disposition B.
2. Merge with both parents. Resolve source/test, queue, root-log, and generated
   conflicts; preserve current dev derived bytes during source reconciliation.
3. Commit source merge, export first from clean committed combined source, then
   refresh changelog/local bundle/draft with the current generator.
4. Run affected tests, extracted archive canaries, canonical/range checks,
   checksum/provenance checks, and full post-commit replay.
5. Obtain independent exact integrated candidate review. Repair findings and
   seek focused rereview when required. Fast-forward dev only after acceptance
   and fresh remote ancestry/one-writer checks; observe resulting identities.

## Progress

- [x] Read-only preflight identified stale old artifacts and direct-merge
  conflicts; exact B historical disposition is accepted in current dev.
- [x] Merge both histories without an automatic commit. Preserve current dev
  generated export/release/changelog bytes and intake reports. Retain both
  customization and planner tests plus both root execution logs.
- [x] Validate reconciled source with 32 import, 18 release, 11 draft, 11
  changelog, and 6 governance tests; canonical validate and doctor pass.
- [x] Commit reconciled source `1a25e33e` with both parents.
- [x] Qualify regenerated portable and local release bytes at `2819385a`;
  replay changed zero of 44 tracked release files.
- [x] Obtain independent `ACCEPT_WITH_NOTES` for the exact combined candidate.
- [ ] Observe qualified dev after fresh remote ancestry and single-writer checks.

## Recovery

Stop on unrecognized conflicts or stale refs. Do not select an old archive over
the accepted generator. Resume from exact commits, merge state, this plan, and
external test handles. Reconcile uncertain remote effects before retrying a
push. Public release and actual removal remain separate campaign gates.
