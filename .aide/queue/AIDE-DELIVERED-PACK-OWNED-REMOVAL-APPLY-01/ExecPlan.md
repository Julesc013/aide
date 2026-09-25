# ExecPlan: receipt-owned portable removal apply

## Objective and scope

Close the real removal gap left by the read-only planner for the supported
portable pack. Act only on exact receipt-owned bytes in a disposable target.
Preserve target-authored and unknown state, including surrounding `AGENTS.md`
content, and leave a clear recovery state across interruptions.

## Dependencies and sequence

1. Start from remote-observed `dev@5dfa75e6`, the integrated planner, and a
   separate clean task worktree. Inspect receipt, planner, import intent, and
   target path rules before effect code.
2. Add adversarial tests for stale plan/receipt, changed or missing bytes,
   three-way update residue, parent junctions, racing leaves, interruption,
   repeat invocation, and authored `AGENTS.md` preservation.
3. Implement a bounded CLI apply mode with exact plan acknowledgement and a
   target-local recoverable intent. Use the qualified shared lifecycle lock
   and anchored path operations; do not replace reviewed primitives with
   path-only checks. Keep source and generated outputs distinct.
4. Run focused and full importer/lifecycle tests, extracted ZIP/tar consumer
   checks, canonical validation, and independent source review. Reconcile
   source with current dev, regenerate current artifacts, replay and review
   the integrated candidate before a dev effect.

## Progress

- [x] Observed the current planner's explicit `apply_allowed: false` boundary.
- [x] Admitted a bounded task and isolated worktree from the observed dev.
- [x] Characterized receipt, planner, exact-preview, import-intent, and target-path rules.
- [x] Implemented and provisionally tested a bounded Windows owned-file removal
  slice with exact plan, same-handle digest/delete, recoverable intent, and
  target-root pinning. The AGENTS managed section and receipt remain; result
  is explicitly `PARTIAL_REMOVAL`.
- [ ] Reconcile the shared lifecycle lock and pinned-directory helper from the
  separately reviewed repair stream. Run tests on actual combined source.
- [x] Add anchored whole-file removal only for the exact new-project
  `AGENTS.md` scaffold with a receipt-matching managed block. Delete the
  runner last and retire the receipt only after all recorded managed paths
  were removed in this operation. Retain the receipt and runner when a path
  was already absent; test interruption and creation at the former
  receipt-retirement boundary.
- [x] Repair independent source review findings on `d13894ba`: bind every
  managed-file intent preimage to the receipt, revalidate the exact generated
  whole-file AGENTS shape on resume, and reject older intents whose absent
  paths were permitted to retire the receipt. Twelve focused tests pass with
  frozen helper injection. Independent rereview is pending.
- [ ] Implement anchored managed-section removal inside authored brownfield
  `AGENTS.md`; preserve that file, the runner, and receipt meanwhile.
- [ ] Run combined-source and extracted consumer qualification, independent
  review, and integration after the shared helper dependency is accepted.

## Recovery and risks

## Artifact guidance repair after independent review

The combined source and first extracted consumers passed behavior checks, but
independent artifact review rejected the frozen `00966855` guides: both generated
install notes still described removal as planning only. Supersede that source by
editing the two guide generators and a focused guide regression within this
WorkUnit, record the reason in `IMPLEMENT.md`, then freeze a clean source commit.
Regenerate the export and release outputs from that commit, repeat affected tests
and disposable consumers, obtain independent review of changed source and exact
artifact bytes, and only then consider a dev effect. Preserve the rejected
archive bytes externally for comparison; never publish or integrate them.

## Recovery and risks

The planner alone is not deletion authority. An exact receipt and effect-time
bytes must both agree before each removal. A partial run must remain
classifiable; never discard the last ownership record before reconciliation.
Do not mutate real targets. The separate repair and importer-safety streams
are dependencies for final integrated acceptance, so generated artifacts
must come from their combined accepted source rather than this old base.
The six apply regressions pass only with a temporary in-process import of one
frozen repair-helper snapshot; this does not constitute combined-source
acceptance. The partial result retains the portable CLI runner so a target can
still inspect and reconcile its receipt or intent after the file effects.
The conditional-detach source candidate retains an exact target-local intent
through receipt retirement; after the runner is deleted, recovery must use
the extracted pack CLI. An already-absent managed path now prevents receipt
retirement because its absence cannot be guarded against creation at the
terminal boundary. It does not remove authored content or claim general
rollback. The separate validation record identifies current tests and the
stale generated-pack provenance in this source branch.
