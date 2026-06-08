# Repair Dry-Run Design

## Purpose

This WorkUnit checks lifecycle fixture repair planning evidence without applying a repair. The lifecycle fixture repair surface is limited to generated repair plan review, generated plan report review, expected-state README evidence, marker defect evidence, path boundary checks, hash reference checks, drift context, scoped executor interlock, and no-apply proof.

## Inputs

- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-missing-marker.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-malformed-marker.plan.json`
- `.aide/reports/lifecycle-fixture-plans/repair-plan-missing-marker.plan-report.json`
- `.aide/reports/lifecycle-fixture-plans/repair-plan-malformed-marker.plan-report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-missing-marker/README.md`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-malformed-marker/README.md`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-drift-detection-checks.json`

## Boundaries

Allowed paths for writes are this task directory, `.aide/reports/lifecycle-fixture-repair-dry-run/**`, queue index, latest task packet, and deterministic status/validation reports. Generated repair plans, expected states, fixture targets, schemas, lifecycle apply code, scoped transaction executor code, and managed-section implementation remain read-only.

Forbidden operations include install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claims, and release-ready claims.

## Result

The repair dry-run check result is `PASS_WITH_WARNINGS`. Both repair scenarios are blocked exactly as expected. Static expected repair report refs are absent, so generated plan reports and expected-state README files are used as report evidence.
