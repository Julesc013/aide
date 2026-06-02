# Remaining Risks

## Review Gate

AIDE-APPLY-01 ends at `needs_review`. The implementation is not accepted until a follow-up review task validates scope, evidence, and no-apply boundaries.

## Fixture-Only Limit

The patcher is intentionally limited to in-memory and fixture-owned writes. It does not yet provide a reviewed active repository apply path.

## Generated State Churn

Full eval and validation regenerated existing task-os, capability, transaction, golden-run, and export-pack reports. This is expected generated state, not new policy authority.

## Export Provenance

`pack-status` reports `DIRTY_SOURCE_RECORDED` because the pack was built from the in-progress source tree before the AIDE-APPLY-01 commit existed.

## Separate Gitignore Commit

`.gitignore` was handled as a separate direct user request in commit `2204d99`. It is not part of the AIDE-APPLY-01 change set.

## Deferred Work

Real managed-section apply, transaction execution, target-repo mutation, install/repair/upgrade/rollback/uninstall apply, branch mutation, push, release, and GitHub mutation remain deferred.
