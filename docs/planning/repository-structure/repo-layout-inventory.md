# Repo Layout Inventory

`AIDE-BUILD-REPO-LAYOUT-INVENTORY-01` records a report-only Track B inventory
of current `.aide` and `core` layout pressure.

## Result

The current layout is workable but has three pressure points:

1. `.aide/reports` is large, mixed, and heavily referenced by flat paths.
2. `.aide` and `core` intentionally duplicate domain names, which requires
   authority clarity rather than automatic consolidation.
3. Tiny `core/runtime`, `core/sdk`, and `core/control` stubs should not grow
   without explicit queue authority.

## Reports

- `.aide/reports/repo-layout/inventory.json`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.json`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`

## Decision

Do not generate a rationalization/apply prompt yet. The safe next gate is a
check of this inventory, followed by acceptance only if the design is considered
strong enough.

## Boundary

This inventory does not authorize file moves, file deletes, directory renames,
schema filename churn, reference rewrites, report restructuring, generated OKF
edits, generated-output source-truth changes, branch mutation, target-repo
mutation, provider/model calls, network calls, release work, or Track A
product-protocol implementation.
