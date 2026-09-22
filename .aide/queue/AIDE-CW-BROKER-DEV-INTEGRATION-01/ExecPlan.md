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
- [x] Commit and publish the integration admission checkpoint.
- [x] Merge exact source with no commit and preserve both parents.
- [x] Resolve fourteen conflicts against current repository truth.
- [x] Verify current dev protected paths were not downgraded.
- [x] Run focused broker/runtime and packaging regressions.
- [x] Run canonical repository structural checks.
- [x] Run commit and range checks after the merge commit exists.
- [x] Publish the exact integration candidate.
- [x] Run the exact task-to-dev landing helper in dry-run mode.
- [x] Run the landing helper, merge to dev, validate, push, and observe refs.
- [ ] Refresh derived portable export and release artifacts from a clean post-landing source commit.
- [ ] Re-run canonical validation and close the integration task.

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

## Conflict Resolution

- Current `dev` won for four generated latest-intake projections and the three
  completed documentation-integration records.
- The broker source supplied its adopted integration-stage effect contract and
  navigation additions.
- Campaign, queue-index, `PLANS.md`, and `IMPLEMENT.md` records were combined
  so the broker/host/target history and the later delivered-pack slices remain.
- The queue index now contains 261 unique task ids, including all entries unique
  to either parent and the dedicated integration WorkUnit.
- No conflict occurred in `core/runtime/**` or the focused test modules.

## Candidate Validation

- Continuous-worker, broker, provider, GitHub, host, image, PE, and security
  discovery ran 312 cases: 311 passed and one Windows symlink-creation case was
  skipped because the current process lacks that privilege.
- Portable export/import and ownership-aware update discovery passed 25 cases.
- Release-bundle discovery passed 10 cases, including extracted-archive import.
- `aide_lite.py doctor` and `aide_lite.py validate` both returned `PASS`.
- The helper correctly refused to produce a clean-tree landing plan while the
  merge was uncommitted; a fresh plan is required after candidate publication.
- The published two-parent candidate is
  `091382e81f08b6e7363380cd3190c7483234d9ab`, tree
  `4f75f5a9d1686a9fc5cfce9a484477237d9fbc2c`.
- Its latest-commit policy check passes. The complete incoming range check also
  reports historical message-format failures already present in published
  ancestry; those are retained as evidence and are not rewritten or presented
  as passing.
- The post-publication landing helper returned `ready_dry_run` for a no-ff merge
  of this task branch into `dev`, followed by `git push origin dev`.
- `dev` landed the task through two-parent commit
  `bed5a57aed4f7686de4b9137dbb3afc8e7995436`. Local `dev`, `origin/dev`, and
  the observed remote ref matched that identity, and the requested source
  `75da33108995ba63fc7148c6b4137349d7013798` is its ancestor.
- The first validation after the landing commit correctly failed portable-pack
  provenance because its manifest still names pre-integration source
  `31bd91bd10ed57e98e658380cd9372e074867f63`. The integration is preserved;
  refresh derived export and release artifacts from a clean post-landing commit
  before marking this WorkUnit complete.
