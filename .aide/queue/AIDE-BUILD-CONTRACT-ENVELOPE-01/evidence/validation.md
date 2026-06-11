# Validation

## Passed

- `git diff --check`
  - exit code: 0
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
  - exit code: 0
  - result: PASS
  - mutation scope: temp workspace only
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify`
  - exit code: 0
  - result: PASS
  - checks: 48
- `py -3 .aide\scripts\aide_lite.py contract-envelope status`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py contract-envelope project --source lifecycle-fixture-runner`
  - exit code: 0
  - result: PASS
  - projections written: 3
- `py -3 .aide\scripts\aide_lite.py contract-envelope validate`
  - exit code: 0
  - result: PASS
  - backwards compatibility preserved: true
  - destructive migration performed: false
- `py -3 .aide\scripts\aide_lite.py validate`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py test`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-01`
  - exit code: 0
  - status: needs_review
  - classification: complete
  - evidence files: 11
  - missing evidence: 0
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-CONTRACT-ENVELOPE-01`
  - exit code: 0
  - available evidence files: 11
  - missing evidence files: 0
- JSON parse check for `.aide/protocol/aide-envelope.schema.json`,
  `.aide/reports/contract-envelope/validation.json`, and all three projection
  JSON files
  - exit code: 0
  - result: PASS

## Generated Report Validation

- `.aide/reports/contract-envelope/status.md`: generated and read.
- `.aide/reports/contract-envelope/validation.json`: generated, parsed, and status is `PASS`.
- `.aide/reports/contract-envelope/validation.md`: generated.
- `.aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json`: generated and validated.
- `.aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json`: generated and validated.
- `.aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json`: generated and validated.

## Generated Churn Classification

Lifecycle-fixture report churn caused by validation was restored because those
files are read-only sources for this task. Contract-envelope reports were then
regenerated against the restored sources.
