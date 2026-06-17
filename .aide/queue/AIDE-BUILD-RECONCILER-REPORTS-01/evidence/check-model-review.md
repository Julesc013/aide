# Check Model Review

The Reconciler model is deterministic and report-only.

Inputs checked:

- Queue index and accepted OKF task status/evidence/report references.
- Generated latest task packet.
- OKF projection, validation, lint, and acceptance reports.
- ReferenceID and EventRecord reports.
- OKF concept-page source hashes.

Output model:

- `reconciliation-report.json`
- `findings.json`
- `finding-taxonomy.json`
- `validation.json`
- matching Markdown summaries

The model classifies drift and records a recommended follow-up. It does not apply fixes.
