# ExecPlan: AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01

## Objective

Run static report-only and dry-run checks against generated upgrade lifecycle fixture plans. The checks compare generated upgrade plan intent with fixture metadata, generated plan reports, static expected reports where present, expected states, drift detection expectations, path boundaries, managed-section expectations, preimage and postimage hash references, no-apply flags, scoped transaction executor v0 limitations, and capability labels.

## Scope

Allowed writes are limited to this task directory, `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`, queue index, latest task packet, and deterministic status/validation report refreshes. Generated upgrade plans, static fixtures, source-pack files, expected states, expected report examples, lifecycle schemas, scoped executor source, and active apply surfaces are read-only.

## Check Model

The check model simulates upgrade planning by static analysis only. It may parse JSON, compare fixture metadata and report records, compute SHA-256 hashes for referenced static files, and compare managed-section before/after content. It must not run install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, GitHub mutation, network calls, release publication, or broad active-repo apply.

## Upgrade Scenarios

- `upgrade-v2`
- `upgrade-manual-preserved`
- `drift-detected`

Install, repair, rollback, uninstall, fixture apply, active repo apply, and target repo adoption are deferred.

## Result

Result is `PASS_WITH_WARNINGS`. All three upgrade scenarios were checked with no repair defects. `upgrade-manual-preserved` does not have a static `expected_report_ref`; generated plan report evidence exists and the static fixture hash, managed-section, path boundary, and no-apply checks pass.

## Review Gate

Stop at `needs_review`.
