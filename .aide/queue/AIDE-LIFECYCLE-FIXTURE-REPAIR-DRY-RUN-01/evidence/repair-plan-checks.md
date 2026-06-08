# Repair Plan Checks

Report: `.aide/reports/lifecycle-fixture-repair-dry-run/repair-plan-checks.json`

Result: `PASS_WITH_WARNINGS`

Plans checked:

- `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-missing-marker.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-malformed-marker.plan.json`

Both generated repair plans are fixture-only and report-only. Each plan has exactly one blocked `validate` operation against `manual/with-managed-section.md`, a `needs_review` review gate, explicit allowed roots, protected roots, stop conditions, prohibited operation checks, and no-mutation fields.

Scenario outcomes:

- `repair-plan-missing-marker`: expected status `BLOCKED`, expected blocker `BLOCKED_MARKER_MISSING`, check state `PASS_WITH_WARNINGS`.
- `repair-plan-malformed-marker`: expected status `BLOCKED`, expected blocker `BLOCKED_MARKER_MALFORMED`, check state `PASS_WITH_WARNINGS`.

Warning:

- Both generated repair plans have an empty static expected repair report ref. Generated plan reports and expected-state README files are used as report evidence.
