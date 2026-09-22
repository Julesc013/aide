# ExecPlan: Broker Runtime Dev Integration

## Objective

Create a reviewable two-parent merge that preserves the complete published
broker/runtime line and current dev, then qualify that combined source for dev.

## Facts

- Source: `75da33108995ba63fc7148c6b4137349d7013798`.
- Target: `13fc9a6a0aa02bd4c2343c640e8b83a95d89c6ab`.
- Merge base: `bfb86c12b9e6d2970024d29c57ba629994ec43cc`.
- Neither parent is an ancestor of the other.
- The source has fourteen unique runtime commits after the merge base.
- Net source-to-target comparison covers 535 paths: 432 under `.aide/queue`,
  32 under `core/runtime`, 17 under `.aide/scripts`, and smaller documentation,
  specification, and generated-evidence sets.
- A synthetic merge reports fourteen conflicts, all in current-state intake,
  queue coordination, root logs, or specification navigation.

## Progress

- [x] Verify exact local and remote source and target refs.
- [x] Compare ancestry, unique commits, path groups, and net tree delta.
- [x] Run a synthetic merge and enumerate conflict classes.
- [x] Create an isolated integration worktree from current dev.
- [x] Admit this exact owner-prioritized integration WorkUnit.
- [ ] Commit and publish the integration admission checkpoint.
- [ ] Merge exact source with no commit and preserve both parents.
- [ ] Resolve fourteen conflicts against current repository truth.
- [ ] Verify current dev protected paths were not downgraded.
- [ ] Run focused broker/runtime and packaging regressions.
- [ ] Run canonical repository and commit-range checks.
- [ ] Publish the exact integration candidate.
- [ ] Run the landing helper, merge to dev, validate, push, and observe refs.

## Conflict Policy

- Keep current dev latest-intake outputs; they are replaceable current-state
  projections, not broker source identity.
- Preserve completed documentation integration records from current dev.
- Reconcile campaign status and root logs by retaining both completed product
  work and the unfinished broker route.
- Reconcile the queue index by task id, retaining every current dev entry and
  every unique broker/host/target entry.
- Preserve current specification navigation while ensuring the adopted broker
  effect contract and broker reference page remain linked.
- Never choose an older generated release or portable importer output over the
  current qualified dev artifact.

## Test Strategy

Run the focused broker/provider/host suites from the combined tree, then the
portable importer/release regressions that protect current dev. Follow with
canonical `test`, `validate`, pack/release read-only checks, and incoming
commit-message validation. Record skips, especially the Windows symlink case,
without converting them to passes.

## Recovery

Until the merge commit is published, aborting the merge returns this isolated
branch to its admission commit without touching either parent. After
publication, fix forward. Never rewrite the published source or target refs.

