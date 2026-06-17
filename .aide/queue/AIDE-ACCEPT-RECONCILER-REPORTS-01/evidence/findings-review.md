# Findings Review

Status: `PASS_WITH_WARNINGS`

Reviewed files:

- `.aide/reports/reconciler/findings.json`
- `.aide/reports/reconciler/findings.md`
- `.aide/reports/reconciler/reconciliation-report.json`
- `.aide/reports/reconciler-check/check-report.json`

The Reconciler reports four findings, all with severity `warning`:

1. `stale_context`: latest generated task packet still points to lifecycle fixture runner work.
2. `acceptance_gate_debt`: the queue intentionally carries many `needs_review` tasks.
3. `stale_generated_report`: OKF build reports still carry pre-acceptance next-task routing.
4. `source_hash_gap`: OKF source hashes lag the current queue index.

Each finding is `status: open`, `repair_authorized: false`, `mutates_source_truth: false`, and `report_only_disposition: reported_only_no_repair`.

Live-schema note: the prompt named generic per-finding fields such as `source`, `subject`, `message`, `recommended_action`, `auto_repair_available`, and `mutation_performed`. The implemented and checked live schema uses `source_refs`, `title`, `summary`, `recommended_follow_up`, `repair_authorized`, and `mutates_source_truth`, with report-level `mutation_performed: false`. This is accepted as the validated first-slice schema because the semantics are present, the build validation reports `finding_schema_valid: true`, and the independent check accepted the schema.

No finding contains secrets, raw prompts, provider keys, `.aide.local/` data, or external network data.
