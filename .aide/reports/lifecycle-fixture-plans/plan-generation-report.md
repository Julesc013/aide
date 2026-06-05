# Lifecycle Fixture Plan Generation Report

Result: `PASS_WITH_WARNINGS`

- Task: `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- Plans generated: `13`
- Plan index: `.aide/examples/apply/lifecycle-fixtures/generated-plans/plan-index.json`
- Generator command implemented: `false`
- Lifecycle apply implemented: `false`
- Lifecycle apply executed: `false`
- Scoped transaction apply executed: `false`
- Target files mutated: `false`
- Rollback execution implemented: `false`
- Review gate: `needs_review`

## Scenarios

| Scenario | Phase | Mode | Expected status | Expected blocker | Plan |
| --- | --- | --- | --- | --- | --- |
| `install-clean` | `install` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-clean.plan.json` |
| `install-existing-manual-preserved` | `install` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-existing-manual-preserved.plan.json` |
| `install-managed-section` | `install` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json` |
| `upgrade-v2` | `upgrade` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-v2.plan.json` |
| `upgrade-manual-preserved` | `upgrade` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-manual-preserved.plan.json` |
| `drift-detected` | `upgrade` | `report` | `BLOCKED` | `BLOCKED_DRIFT_DETECTED` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/drift-detected.plan.json` |
| `repair-plan-missing-marker` | `repair` | `report` | `BLOCKED` | `BLOCKED_MARKER_MISSING` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-missing-marker.plan.json` |
| `repair-plan-malformed-marker` | `repair` | `report` | `BLOCKED` | `BLOCKED_MARKER_MALFORMED` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-malformed-marker.plan.json` |
| `rollback-record-generated` | `rollback` | `report` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/rollback-record-generated.plan.json` |
| `uninstall-manual-preserved` | `uninstall` | `dry-run` | `PASS_WITH_WARNINGS` | `` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/uninstall-manual-preserved.plan.json` |
| `protected-path-blocked` | `install` | `report` | `BLOCKED` | `BLOCKED_PROTECTED_PATH` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/protected-path-blocked.plan.json` |
| `traversal-blocked` | `install` | `report` | `BLOCKED` | `BLOCKED_PATH_TRAVERSAL` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/traversal-blocked.plan.json` |
| `broad-delete-blocked` | `uninstall` | `report` | `BLOCKED` | `BLOCKED_BROAD_DELETE` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/broad-delete-blocked.plan.json` |

## Warnings

- Report-only generated artifacts; no generator CLI command implemented in this task.
- Global task next-plan selector may still lag task-local next batch.
