# Lifecycle Fixture Uninstall Dry-Run Summary

- task_id: `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`
- result: `PASS_WITH_WARNINGS`
- mode: report-only/dry-run
- uninstall_scenarios_checked: 2
- generated_uninstall_plans_checked: 2
- expected_static_reports_present: 1
- missing_static_expected_report_refs: 1
- review_gate: `needs_review`

## Summary

`uninstall-manual-preserved` passes as static dry-run planning evidence with manual-preservation hash evidence, but it lacks a static expected report ref. `broad-delete-blocked` passes as blocked report-only evidence with `BLOCKED_BROAD_DELETE` in the generated plan and expected report.

No uninstall execution, rollback execution, lifecycle apply, scoped transaction fixture apply, fixture target mutation, active repo mutation, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, network calls, release publication, production-ready claim, or release-ready claim occurred.
