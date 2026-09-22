# ExecPlan: Delivered Pack Removal Plan

## Objective

Turn the target-local portable import receipt into an exact, deterministic,
preservation-first removal plan from the delivered CLI without applying any
removal or changing target state.

## Scope

- Reuse the portable receipt validator and target-path boundary.
- Classify unchanged recorded managed files as removal candidates.
- Classify changed, missing, malformed, unknown, and target-owned state
  conservatively.
- Treat the portable `AGENTS.md` block separately from authored bytes.
- Bind the plan to exact receipt and current-state observations.
- Exercise the command through both extracted release archive formats.

## Non-Goals

- No file deletion, directory pruning, managed-section removal, repair,
  rollback, uninstall apply, policy amendment, or live target operation.
- No main promotion, tag, upload, GitHub Release, or publication.
- No adoption of all lifecycle draft requirements.

## Dependencies

- `dev@13fc9a6a0aa02bd4c2343c640e8b83a95d89c6ab`.
- Portable receipt and byte-boundary behavior from
  `AIDE-DELIVERED-PACK-SAFE-UPDATE-01`.
- Active Q46 uninstall policy remains authoritative and no-apply.

## Progress

- [x] Inspect current dev, lifecycle policy, specs, receipt owner, and tests.
- [x] Compile the broad intent and preserve its blocked split-required result.
- [x] Create an isolated task worktree from exact published dev.
- [x] Admit this bounded read-only child and record retained gates.
- [ ] Add failing positive and adversarial planner tests.
- [ ] Implement the smallest coherent portable planner and CLI surface.
- [ ] Run focused tests and inspect the returned plan manually.
- [ ] Add extracted ZIP and tar.gz planner regressions.
- [ ] Regenerate and qualify exact delivered bytes.
- [ ] Record evidence, publish, and prepare exact task-to-dev integration.

## Test Oracle

A valid plan requires a digest-valid portable receipt and exact observation of
each recorded target. Only unchanged AIDE-managed bytes may be classified as a
future removal candidate. Locally edited or unknown bytes are conflicts or
preservations; target-owned artifacts and authored `AGENTS.md` bytes are never
removal candidates. Planning must leave a complete before/after target-tree
digest unchanged.

## Recovery

The command is read-only and writes no target journal. Rerun from the current
receipt and target bytes. The task branch is independently recoverable through
frequent commits; shared history is never rewritten after publication.

## Decisions

- Extend the portable CLI owner rather than convert source-generated Q46 plans
  into target truth.
- Use receipt-backed exact bytes as the first ownership oracle.
- Name apply as a retained future gate; do not hide it behind a fixture flag.

