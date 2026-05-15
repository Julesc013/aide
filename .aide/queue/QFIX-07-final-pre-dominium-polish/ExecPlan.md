# QFIX-07 ExecPlan: Final Pre-Dominium Polish

## Objective

Run a final AIDE-local remediation pass before Dominium handoff. Fix only
concrete, safe AIDE-side drift and record current validation.

## Scope

- Inspect queue status for failed, blocked, partial, or stale current-state
  records.
- Clean the Q46 stale `in_progress` marker while preserving its review gate.
- Refresh generated manifest if queue index changes make it stale.
- Rerun focused validation and no-publish/no-apply checks.
- Commit scoped metadata and evidence.

## Boundaries

- Do not mark Q36-Q48, QCHECK-04, or QFIX tasks as `passed`.
- Do not run Q49.
- Do not mutate Dominium, Eureka, branches, tags, GitHub, releases, uploads,
  providers, models, or network state.
- Do not run install/repair/upgrade/rollback/uninstall apply modes.

## Progress

- [x] Repo state inspected.
- [x] Queue status inspected.
- [x] Q46 current-state drift identified.
- [x] QFIX-07 packet created.
- [x] Safe metadata cleanup applied.
- [x] Generated manifest refreshed.
- [x] Validation rerun.
- [x] Evidence finalized.
- [ ] Commit created.
