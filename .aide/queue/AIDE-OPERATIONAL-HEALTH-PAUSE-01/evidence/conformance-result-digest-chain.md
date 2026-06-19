# ConformanceResult Digest Chain

Reviewed files:

- `.aide/queue/AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01/status.yaml`
- `.aide/reports/conformance-result-accept/acceptance-report.json`
- `.aide/reports/conformance-result-repair-check/check-report.json`
- `.aide/reports/conformance-result/validation.json`

Findings:

- Historical failed check is preserved:
  `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01` with `FAILED_VALIDATION`.
- Historical failed recorded digest:
  `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`.
- Historical failed raw-profile digest:
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`.
- Repaired/accepted profile digest:
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`.
- Digest algorithm: `sha256-canonical-json-v1`.
- Repair check independently confirmed the repaired digest binds to the
  pristine accepted ConformanceProfile payload.
- Acceptance remains evidence-projected, runnerless, non-admitting, and
  non-trusting.
