# ExecPlan: AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01

## Objective

Run static report-only and dry-run checks against generated install lifecycle fixture plans. The checks compare generated install plan intent with fixture metadata, generated plan reports, static expected reports where present, expected states, path boundaries, managed-section expectations, hash references, no-apply flags, scoped executor interlock, and capability labels.

## Scope

Allowed writes are limited to this task directory, `.aide/reports/lifecycle-fixture-install-dry-run/**`, queue index, latest task packet, and deterministic status/validation report refreshes. Generated install plans, static fixtures, source-pack files, expected states, expected report examples, lifecycle schemas, scoped executor source, and active apply surfaces are read-only.

## Check Model

The check model simulates install planning by static analysis only. It may parse JSON, compare fixture metadata and report records, compute SHA-256 hashes for referenced static files, and compare managed-section before/after content. It must not run install apply, lifecycle apply, scoped transaction apply, active repo apply, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, GitHub mutation, network calls, release publication, or broad active-repo apply.

## Install Scenarios

- `install-clean`
- `install-existing-manual-preserved`
- `install-managed-section`
- `protected-path-blocked`
- `traversal-blocked`

Upgrade, repair, rollback, uninstall, fixture apply, active repo apply, and target repo adoption are deferred.

## Result

Result is `PASS_WITH_WARNINGS`. All five install scenarios were checked with no repair defects. Two scenarios, `install-clean` and `install-existing-manual-preserved`, do not have static `expected_report_ref` values; generated plan reports were used as report evidence for those scenarios.

## Review Gate

Stop at `needs_review`.
