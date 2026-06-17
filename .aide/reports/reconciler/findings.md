# Reconciler Findings

- task_id: AIDE-BUILD-RECONCILER-REPORTS-01
- status: PASS_WITH_WARNINGS
- findings_count: 4
- report_only: true
- repair_authorized: false
- mutation_performed: false

## reconciler-001-stale_context

- category: stale_context
- severity: warning
- title: Latest task packet lags accepted OKF queue routing
- expected: Latest context packet mentions `AIDE-BUILD-RECONCILER-REPORTS-01` or is regenerated after OKF acceptance.
- observed: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit - Current Truth And Root Authority Audit
- repair_authorized: false
- mutates_source_truth: false

## reconciler-002-acceptance_gate_debt

- category: acceptance_gate_debt
- severity: warning
- title: Queue contains review-gated accepted or implemented work
- expected: Review-gated work remains explicit until a review task accepts, rejects, or supersedes it.
- observed: needs_review_count=86; task_count=141
- repair_authorized: false
- mutates_source_truth: false

## reconciler-003-stale_generated_report

- category: stale_generated_report
- severity: warning
- title: OKF build reports retain pre-acceptance next-task routing
- expected: Accepted queue routing recommends `AIDE-BUILD-RECONCILER-REPORTS-01`.
- observed: .aide/reports/okf/projection-report.json: recommended_next_task=AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01; .aide/reports/okf/validation.json: recommended_next_task=AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01
- repair_authorized: false
- mutates_source_truth: false

## reconciler-004-source_hash_gap

- category: source_hash_gap
- severity: warning
- title: OKF source hashes lag current source files
- expected: Generated OKF source_hashes match current source artifacts or are marked stale by a Reconciler report.
- observed: stale_hash_count=10; sample=.aide/knowledge/okf/current-state/next-work.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/queue.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/review-gates.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/stale-latest-task-packet.md -> .aide/queue/index.yaml; .aide/knowledge/okf/decisions/okf-as-knowledge-plane.md -> .aide/queue/index.yaml
- repair_authorized: false
- mutates_source_truth: false
