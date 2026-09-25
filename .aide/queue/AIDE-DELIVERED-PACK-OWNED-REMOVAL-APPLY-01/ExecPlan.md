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
- [ ] Complete anchored managed-section removal, receipt retirement, consumer
  qualification, independent review, and integration.

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
