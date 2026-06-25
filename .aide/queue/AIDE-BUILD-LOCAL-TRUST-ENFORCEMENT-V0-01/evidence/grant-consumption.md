# Grant Consumption

The fixture persists an allowed AuthorizationEvaluation and consumes the
one-use CapabilityGrant.

Observed fixture facts:

- evaluation result: allowed
- event sequences: `[1, 2]`
- grant consumed: true
- grant remaining uses: 0
- grant status after reopen: consumed
- concurrent final-use replay with a different idempotency key refused as `grant_exhausted`

Evidence: `.aide/reports/local-trust-enforcement-v0/fixture-report.json`.
