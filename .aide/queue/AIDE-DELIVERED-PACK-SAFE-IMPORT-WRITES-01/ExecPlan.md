# ExecPlan: safe delivered-pack importer writes

## Objective and scope

Close the importer parent-component race for exact, receipt-backed managed
payload writes. Keep the established import/update plan, target ownership,
intent/recovery, and delivered CLI semantics. Work only within the task
allowlist; use disposable targets for write tests.

## Dependencies and sequence

1. Start from remote-observed `dev@5dfa75e6`, clean separate worktree,
   `git plan`, and current importer implementation.
2. Add adversarial regressions for parent substitution and for an authored
   target leaf arriving or changing after preimage validation. Record the
   current failures before changing source.
3. Integrate the independently accepted pinned-parent/lifecycle-lock helper
   from the owned-repair stream. Adapt the importer to use a handle-bound
   publication path, or fail closed where that cannot be proved.
4. Run focused race, full import/update, affected release, and extracted-pack
   consumer tests. Review exact source; regenerate with the accepted generator,
   qualify artifacts and replay, then integrate only if accepted.

## Progress

- [x] Identified the path-check/write gap in current `apply_import_operation`.
- [x] Reproduce it with a deterministic disposable-parent substitution. The
  current importer wrote `compact-task.md` outside the target on Windows.
- [x] Reproduce a racing target leaf in both create and update operations.
  The current importer overwrote the concurrent bytes in both cases.
- [ ] Repair and qualify the source with the reviewed shared helper.
- [ ] Close independent review, provenance, and dev integration.

## Recovery and risks

Do not overwrite parent task branches or generated artifacts from an older
source. Preserve failed or skipped oracles honestly. A journal or no-clobber
leaf check does not by itself bind ancestor directories. Current import paths
for the supported platform need effect-time ownership and ancestor proof.
