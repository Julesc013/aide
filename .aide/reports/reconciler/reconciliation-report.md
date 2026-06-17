# Reconciler Report

- task_id: AIDE-BUILD-RECONCILER-REPORTS-01
- capability_target: minimal_reconciler_reports
- status: PASS_WITH_WARNINGS
- validation_status: PASS_WITH_WARNINGS
- report_only: true
- detects_drift: true
- repair_implemented: false
- mutation_performed: false
- source_truth_mutation: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- github_mutation: false
- network_calls: false
- provider_or_model_calls: none
- Gateway calls: none
- findings_count: 4
- recommended_next_task: AIDE-CHECK-RECONCILER-REPORTS-01

## Findings By Category

- acceptance_gate_debt: 1
- source_hash_gap: 1
- stale_context: 1
- stale_generated_report: 1

## Reports Checked

- .aide/reports/okf/projection-report.json: PASS_WITH_WARNINGS
- .aide/reports/okf/validation.json: PASS_WITH_WARNINGS
- .aide/reports/okf/lint.json: PASS_WITH_WARNINGS
- .aide/reports/okf-accept/acceptance-report.json: ACCEPTED_WITH_WARNINGS
- .aide/reports/reference-id/reference-map.json: UNKNOWN
- .aide/reports/reference-id/validation.json: PASS_WITH_WARNINGS
- .aide/reports/event-record/event-family-index.json: PASS_WITH_WARNINGS
- .aide/reports/event-record/validation.json: PASS_WITH_WARNINGS

## Source Artifacts Checked

- .aide/context/latest-task-packet.md
- .aide/knowledge/okf/capabilities/minimal-contract-envelope.md
- .aide/knowledge/okf/capabilities/minimal-event-record-schema.md
- .aide/knowledge/okf/capabilities/minimal-evidence-packet.md
- .aide/knowledge/okf/capabilities/minimal-reference-id-scheme.md
- .aide/knowledge/okf/capabilities/minimal-testjob-schema.md
- .aide/knowledge/okf/capabilities/minimal-worker-run-schema.md
- .aide/knowledge/okf/capabilities/minimal-workunit-queue.md
- .aide/knowledge/okf/current-state/next-work.md
- .aide/knowledge/okf/current-state/queue.md
- .aide/knowledge/okf/current-state/review-gates.md
- .aide/knowledge/okf/current-state/stale-latest-task-packet.md
- .aide/knowledge/okf/decisions/okf-as-knowledge-plane.md
- .aide/knowledge/okf/decisions/protocol-vs-knowledge.md
- .aide/knowledge/okf/decisions/repo-contract-vs-runtime-state.md
- .aide/knowledge/okf/index.md
- .aide/knowledge/okf/log.md
- .aide/knowledge/okf/protocol/envelope.md
- .aide/knowledge/okf/protocol/event-record.md
- .aide/knowledge/okf/protocol/evidence-packet.md
- .aide/knowledge/okf/protocol/reference-id.md
- .aide/knowledge/okf/protocol/testjob.md
- .aide/knowledge/okf/protocol/worker-run.md
- .aide/knowledge/okf/protocol/workunit.md
- .aide/knowledge/okf/risks/acceptance-gate-debt.md
- .aide/knowledge/okf/risks/overclaiming.md
- .aide/knowledge/okf/risks/stale-latest-task-packet.md
- .aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/evidence/acceptance-summary.md
- .aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/evidence/next-task-prompt.md
- .aide/queue/AIDE-ACCEPT-OKF-KNOWLEDGE-BUNDLE-01/status.yaml
- .aide/queue/index.yaml
- .aide/reports/event-record/event-family-index.json
- .aide/reports/event-record/validation.json
- .aide/reports/okf/lint.json
- .aide/reports/okf/projection-report.json
- .aide/reports/okf/validation.json
- .aide/reports/okf-accept/acceptance-report.json
- .aide/reports/reference-id/reference-map.json
- .aide/reports/reference-id/validation.json
- core/knowledge/okf_bundle.py
- core/protocol/event_record.py
- core/protocol/reference_id.py
