# Projection Review

Status:

```text
PASS_WITH_FINDING
```

Generated result projection reports exist and parse:

- `.aide/reports/conformance-result/results.json`
- `.aide/reports/conformance-result/result-index.json`
- `.aide/reports/conformance-result/case-result-index.json`
- `.aide/reports/conformance-result/projection-report.json`
- `.aide/reports/conformance-result/validation.json`

Projection and validation reports state `PASS_WITH_WARNINGS`. The independent
check downgrades the check result to `FAILED_VALIDATION` because the recorded
profile digest does not match the raw accepted profile report payload.
