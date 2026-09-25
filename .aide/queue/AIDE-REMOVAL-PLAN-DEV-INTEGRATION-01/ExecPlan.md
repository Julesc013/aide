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
- [ ] Reconcile and commit source with both histories.
- [ ] Qualify regenerated portable and local release bytes.
- [ ] Obtain independent integration verdict and observe qualified dev.

## Recovery

Stop on unrecognized conflicts or stale refs. Do not select an old archive over
the accepted generator. Resume from exact commits, merge state, this plan, and
external test handles. Reconcile uncertain remote effects before retrying a
push. Public release and actual removal remain separate campaign gates.
