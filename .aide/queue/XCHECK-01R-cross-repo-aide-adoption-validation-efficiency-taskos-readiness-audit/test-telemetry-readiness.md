# Test Telemetry Readiness

| Capability | Status | Evidence |
|---|---|---|
| Executor status | partial | existing commands run tests, but no canonical async executor |
| Reducer status | missing | no source AIDE reducer schema for compact summaries |
| AI reasoner summary | missing | no standard failure-family/delta artifact |
| Full-discovery handoff | partial | AIDE and targets have reports, but no common handoff schema |
| Compact summary schema | missing | no `.aide/policies/test-telemetry` or equivalent |
| Stale-summary detection | missing | no cross-repo freshness contract |
| Failure-family registry | missing in AIDE | Dominium has failure-family evidence, not canonical AIDE source |
| Timing/sharding | partial target-local | Dominium has timing/sharding docs; AIDE lacks source model |
| CI artifact policy | advisory only | AIDE GitHub/CI reports are no-apply advisory |

Recommended first telemetry prompt:

`X-TEST-02 - AIDE Async Test Telemetry Summary Schema`

This should follow `X-TEST-00` and can precede target-specific telemetry
adapters. It must remain report-only and must not install CI or run external
jobs by default.
