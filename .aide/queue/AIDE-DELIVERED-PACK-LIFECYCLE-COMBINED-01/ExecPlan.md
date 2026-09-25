# ExecPlan: combined delivered-pack lifecycle acceptance

## Objective and scope

Integrate the independently accepted rollback source with the reviewed
authored-`AGENTS.md` removal source against current `dev`. Add the missing
pending-removal rollback gate, preserve both source histories and the current
release generator, and qualify the resulting delivered ZIP/tar bytes before a
normal `dev` integration effect. This WorkUnit does not promote `main`, publish
a release, or mutate a real target repository.

Allowed paths: `.aide/scripts/aide_lite.py`, its export/import tests,
`docs/reference/cross-repo-pack-export-import.md`, the two contributing child
WorkUnits, this WorkUnit, campaign evidence, `.aide/queue/index.yaml`,
`PLANS.md`, `IMPLEMENT.md`, and deterministic `.aide/export/**`,
`.aide/release/**`, and `.aide/changelog/**` outputs.

## Dependencies and current facts

- `dev@ea53e319bd066efcdd0dc5ded38acd4f2d38c990` was clean, observed
  locally and at `origin/dev`, before this worktree was created.
- Rollback source `33824b369b844b1c7a4304844838bcb424806131` has an
  independent source ACCEPT. It lacks an early pending-removal-intent guard.
- Authored-section removal source `d5b44626d6f9efc6f90c8b8eda1e990e5864b5af`
  passed its author tests; independent exact source review is still running.
- Prior generated artifacts on `dev` belong to the current repaired generator.
  Source merges must not restore older generated outputs.

## Sequence

1. Freeze exact candidate identities, verify clean worktrees, Git plan and
   actual refs. Create this isolated task branch from current `dev`.
2. Merge accepted rollback source, preserving queue/planning history. Add the
   pending-removal-intent guard and regressions for valid, retired-receipt,
   malformed, and stale-preview cases.
3. Only after independent removal acceptance, merge its frozen or superseding
   source. Resolve actual conflicts without dropping either history or the
   current generator. Obtain independent review of changed combined scope.
4. Run affected tests and canonical validation, regenerate current pack and
   release outputs once, run full importer/release tests and extracted fresh
   and brownfield lifecycle consumers. Preserve logs, exit codes and hashes.
5. Converge release metadata, replay the generator with zero tracked change,
   inspect staged paths and exact ancestry, obtain independent artifact and
   dev-effect acceptance, then normal fast-forward/push and observe remote.
6. Record the compact mandatory-profile matrix and update task/campaign
   evidence. Keep remaining update conflict, native/hosted and release gates
   open until their own qualification.

## Recovery and effect boundary

One integration writer owns shared Git refs/metadata and generated state.
Pending import, repair or removal intents are never reinterpreted as a fresh
rollback. An uncertain target effect must be reconciled before replay. No
unreviewed source or artifact candidate may advance `dev`.

## Progress

- [x] Observed clean primary/removal/rollback worktrees and remote `dev`.
- [x] Ran dry-run `git plan`; it reported ready with no blocker.
- [x] Created this integration worktree from `dev@ea53e319`.
- [x] Merge reviewed rollback source with both parents and all queue/planning
      additions preserved (`03f4b0a1`).
- [x] Reproduce the pending-removal rollback diagnostic defect, add an early
      validated-intent gate and pass the exact Windows regression. Wider
      combined tests remain open.
- [x] Receive independent authored-section source verdict: `d5b44626` was
      rejected for orphaned backup recovery; superseding `2c4c9089` received
      ACCEPT_WITH_NOTES for source combination. Merge it only after this
      rollback guard is checkpointed.
- [x] Merge accepted removal repair `2c4c9089` into source `723322cf` with
      both parent histories intact. Independent combined-source review returned
      `ACCEPT_WITH_NOTES` for the source only.
- [x] Run 9 focused combined importer cases; regenerate the current export,
      changelog and local release/draft outputs from clean source `723322cf`.
      Canonical validation, pack status, and 202 Q27-Q48 fixture tests pass.
- [x] Repair the authored-CRLF rollback defect found by the extracted-artifact
      canary; red/green exact regression and 8 focused rollback tests pass.
      Preserve the rejected candidate's exact report and ZIP/tar bytes.
- [x] Freeze superseding source `9a0843c3`; independent delta review ACCEPT.
      Regenerate local ZIP/tar/guide, pass Q31/Q34/Q47/Q48 and canonical
      checks. Independent extracted consumer review ACCEPT_WITH_NOTES after
      49 delivered CLI commands on the exact new bytes.
- [x] Full exact-source importer suite passes 85/85 with a hashed external log.
- [ ] Artifact projection/metadata convergence and zero-diff replay, exact
      dev-effect review and observed `dev` ref.
