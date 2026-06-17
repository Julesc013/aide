# Check Self-Management Charter

- task_id: AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01
- checked_task_id: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01
- checked_commit: bb64e63fdbdbd084a19c8f3f6d47b8229d497e68
- track: B
- result: PASS_WITH_WARNINGS
- recommended_next_task: AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01

## Summary

The self-management charter is ready for acceptance review with warnings. The
warnings do not affect authority, scope, evidence, or next-task selection.

This check establishes GovernanceFinding as a report convention only. It does
not implement a formal schema, helper library, CLI command, or reusable Python
object.

## Verified

- The self-management policy parses.
- The policy and reference document describe the same Track B doctrine.
- The charter report summarizes the task without claiming implementation.
- The object backlog lists future Track B objects without treating them as
  implemented.
- The queue sequence routes to `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01` and
  then `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`.
- The build task remains `needs_review` with complete evidence.
- The self-management loop is preserved.
- Protocol truth, evidence truth, generated reports, OKF explanation, queue
  truth, and local runtime state remain distinct.
- Generated outputs remain non-canonical.
- Cleanup by intuition remains forbidden.

## Governance Findings

| id | severity | surface | taxonomy | next_task |
| --- | --- | --- | --- | --- |
| FINDING-001 | info | self_management_charter | boundary_preserved | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-002 | info | self_management_charter | boundary_preserved | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-003 | info | structure_transactions | boundary_preserved | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-004 | info | evidence_lifecycle | evidence_complete | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-005 | info | generated_outputs | generated_truth_risk | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-006 | info | queue_health | next_task_routing | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-007 | info | dirty_state | dirty_state_classified | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-008 | warning | validation | pre_existing_warning | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-009 | warning | docs_truth | stale_claim | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-010 | info | self_management_charter | report_convention_established | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |
| FINDING-011 | warning | commit_state | pre_existing_warning | AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01 |

## Warnings

- `.aide/queue/index.yaml` has mixed/pre-existing line-ending warning state
  recorded by the build task. This is not a charter authority failure.
- Documentation truth, OKF drift, generated-output ledger, queue health,
  evidence lifecycle, schema lifecycle, tools/scripts, tests/fixtures/evals,
  and safety/secrets remain future report-only surfaces.
- The pre-check latest commit had a non-policy commit message. The checked
  charter commit is policy-valid, and this check commit passed post-commit
  validation.

## Non-Authorizations

This check does not authorize schemas, CLI commands, GovernanceFinding helper
or library implementation, OKF regeneration, generated-output ledger,
doc truth reconciler, file moves, renames, reference rewrites, migration apply,
runtime, provider/model/Gateway work, GitHub/network work, branch/worktree
automation, push, merge, release, or target-repo mutation.
