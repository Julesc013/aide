# Findings Review

Status: `PASS_WITH_WARNINGS`

Reviewed file: `.aide/reports/reconciler/findings.json`

The build reports four warning findings:

1. `stale_context`: `.aide/context/latest-task-packet.md` points to unrelated lifecycle fixture runner work.
2. `acceptance_gate_debt`: the queue contains existing `needs_review` debt.
3. `stale_generated_report`: OKF generated reports still recommend an older OKF check route while accepted OKF routing points to Reconciler.
4. `source_hash_gap`: OKF source hashes for the queue index are stale.

All findings are warning-class, report-only, and marked without repair authorization. No finding was hidden or escalated into unauthorized mutation.
