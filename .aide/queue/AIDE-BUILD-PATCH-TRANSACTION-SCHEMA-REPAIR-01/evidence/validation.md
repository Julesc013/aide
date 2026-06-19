# Validation

Validation performed for this repair includes:

- Python compile checks for the repaired helper and focused tests.
- Focused PatchTransaction unit tests: `PASS`, 31 tests.
- Direct production-validator path-scope probes.
- PatchTransaction `status`, `project`, and `validate`.
- Predecessor validators:
  - `reference-id validate`: `PASS_WITH_WARNINGS`
  - `event-record validate`: `PASS_WITH_WARNINGS`
  - `evidence-packet validate`: `PASS`
  - `workunit validate`: `PASS`
  - `worker-run validate`: `PASS`
  - `test-job validate`: `PASS`
  - `capability-manifest validate`: `PASS_WITH_WARNINGS`
  - `conformance-profile validate`: `PASS_WITH_WARNINGS`
  - `conformance-result validate`: `PASS_WITH_WARNINGS`
- Source task checks:
  - `task inspect --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`: `missing_evidence: 0`
  - `task evidence --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`: no missing evidence
  - `task inspect --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`: `missing_evidence: 0`
  - `task evidence --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`: no missing evidence
  - `task inspect --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: `missing_evidence: 0`
  - `task evidence --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: no missing evidence
- JSON parsing for PatchTransaction, failed-check, and repair JSON reports:
  `PASS`.
- Broad AIDE validation: `PASS`.
- `git diff --check`: `PASS` after restoring unrelated generated report churn.
- `git diff --cached --check`: `PASS`.
- Secret-like scan over changed files: `0` findings.

One ad hoc path-scope probe was first attempted with Bash-style heredoc syntax
in PowerShell and failed before execution. It was rerun with PowerShell here
string syntax and passed.

Follow-up prompt alignment added direct probes for:

- drive-prefix variants;
- duplicate-normalized `allowed_paths`;
- duplicate-normalized `forbidden_paths`;
- duplicate-normalized `declared_changed_paths`;
- duplicate diagnostic content;
- valid distinct normalized paths.

Broad validation refreshed out-of-scope WorkUnit and TestJob reports. Those
generated files were restored before completion.
