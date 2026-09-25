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
- Synchronized `dev@c6fdc754844cf7d42302218ce08307a7e05dcb61`.
- Portable receipt and byte-boundary behavior from
  `AIDE-DELIVERED-PACK-SAFE-UPDATE-01`.
- Active Q46 uninstall policy remains authoritative and no-apply.

## Progress

- [x] Inspect current dev, lifecycle policy, specs, receipt owner, and tests.
- [x] Compile the broad intent and preserve its blocked split-required result.
- [x] Create an isolated task worktree from exact published dev.
- [x] Admit this bounded read-only child and record retained gates.
- [x] Add failing positive and adversarial planner tests.
- [x] Implement the smallest coherent portable planner and CLI surface.
- [x] Run focused tests and inspect the returned plan manually.
- [x] Add extracted ZIP and tar.gz planner regressions.
- [x] Synchronize current dev before artifact generation.
- [x] Regenerate and qualify exact delivered bytes.
- [x] Record evidence and publish the qualified task branch.
- [ ] Resolve the exact published commit-message disposition and integrate to dev.

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
- Treat the full target tree as an explicit preservation boundary, not an input
  to hash or inspect. Plan identity binds the receipt and every recorded managed
  target without reading unowned or potentially secret target bytes.
- Preserve published commit `486e81cd` and report its format failure; do not
  amend, rebase, force-push, or weaken strict checks for later commits.

## Surprises

- The commit checker requires bullets under every body heading and six trailers;
  the first published implementation checkpoint omitted those details even
  though its prose was detailed. Every later commit passes the exact checker.
- Post-artifact validation legitimately changes from `PASS` to
  `PASS_SOURCE_ANCESTOR`; the release-draft hashes therefore require one
  committed derivation-closure increment.

## Retrospective

The delivered CLI now turns a valid target-local receipt into a deterministic
read-only plan. Exact ZIP and tar.gz consumers each imported successfully,
classified 809 unchanged managed resources, and retained an identical target
tree digest before and after planning. Product qualification is complete for
this bounded no-apply slice. Dev integration is pending only the exact
historical message-conformance disposition, not a code or artifact failure.
