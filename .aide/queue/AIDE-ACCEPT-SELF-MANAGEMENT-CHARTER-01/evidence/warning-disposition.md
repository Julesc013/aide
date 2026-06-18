# Warning Disposition

## WARNING-001: Queue Index CRLF Warning

- source: `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
- severity: warning
- accepted: true
- affected_paths:
  - `.aide/queue/index.yaml`
- rationale: Pre-existing/mixed-EOL formatting warning. It is not a charter
  authority failure and does not affect scope, evidence, or next-task routing.
- next_task: `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`

## WARNING-002: Prior Commit-Message Warning

- source: `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
- severity: warning
- accepted: true
- affected_paths:
  - `.git`
- rationale: The unrelated prior commit-message warning does not affect the
  charter or check commits. The checked charter commit and check commit passed
  validation.
- next_task: `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`

## WARNING-003: Future Track B Surfaces Deferred

- source: `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
- severity: warning
- accepted: true
- affected_paths:
  - `.aide/policies/self-management.yaml`
  - `docs/reference/aide-self-management.md`
  - `.aide/reports/self-management/object-backlog.md`
  - `.aide/reports/self-management/queue-sequence.md`
- rationale: This is an intentional boundary. Documentation truth, OKF drift,
  generated-output ledger, queue health, evidence lifecycle, schema lifecycle,
  tools/scripts, tests/fixtures/evals, and safety/secrets remain separate
  reviewed report-only tasks.
- next_task: `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
