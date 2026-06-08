# Drift Detection Checks

Result: `PASS`

Scenario checked:

- `drift-detected`

Expected blocker:

- `BLOCKED_DRIFT_DETECTED`

The generated plan uses report mode, marks the operation as blocked, requires the drifted preimage hash, omits postimage hash requirements, preserves `target_files_mutated=false`, and points to a static expected report with `status=BLOCKED`, `blocked_reason=BLOCKED_DRIFT_DETECTED`, and `files_that_would_change=[]`.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-drift-detection-checks.json`
