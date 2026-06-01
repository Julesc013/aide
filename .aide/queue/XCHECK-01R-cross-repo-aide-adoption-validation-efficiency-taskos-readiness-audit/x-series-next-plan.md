# X-Series Next Plan

Readiness verdict: `READY_FOR_X_TEST_00_ONLY`.

Exact first prompt to generate next:

`X-TEST-00 - AIDE Cross-Repo Validation Tier Model`

## Shortlist

| Order | Prompt | Repo | Dependency | Notes |
|---:|---|---|---|---|
| 1 | `X-TEST-00 - AIDE Cross-Repo Validation Tier Model` | AIDE | none | Must define T0/T1/T2/T3/T4 and normal vs promotion lanes |
| 2 | `X-TEST-01 - Eureka Tiered / Impacted / Timed Test Validation` | Eureka | X-TEST-00 | Re-baseline full-suite/branch divergence before more product work |
| 3 | `X-TEST-03 - Dominium Tiered Validation / CTest / RepoX Plan` | Dominium | X-TEST-00 | Target full CTest/RepoX truth labeling |
| 4 | `X-TEST-02 - AIDE Async Test Telemetry Summary Schema` | AIDE | X-TEST-00 | Compact summaries, stale detection, failure families |
| 5 | `X-OS-00 - AIDE Task OS Schemas and Policies` | AIDE | X-TEST-00 | Report-only schemas first |
| 6 | `X-OS-01 - AIDE Task OS Report-Only Commands` | AIDE | X-OS-00 | observe/classify/plan/report only |
| 7 | `X-OS-02 - Capability Reality Ledger v0` | AIDE | X-OS-00 | Prevent docs/code overclaim |
| 8 | `X-SYNC-DOM-01 - Sync AIDE Task OS v0 to Dominium` | Dominium | X-OS-01, reviewed pack | Target preflight only |
| 9 | `X-SYNC-EUR-01 - Sync AIDE Task OS v0 to Eureka` | Eureka | X-OS-01, reviewed pack | Target preflight only |
| 10 | `X-EUR-01 - Eureka Second Fixture Source Slice v0` | Eureka | X-TEST-01 | Product expansion after target test tiering |
| 11 | `X-DOM-01 - Dominium Validator Wrapper Pilot` | Dominium | X-TEST-03 | Preserve/wrap, no deletion |
| 12 | `X-AIDE-01 - Transactional Apply Engine v0` | AIDE | X-OS-01 plus rollback evidence | Still dry-run/report-first initially |

Parallelism notes: X-TEST-01 and X-TEST-03 can be planned after X-TEST-00, but
target execution should remain target-local and avoid branch mutation. Task OS
sync waits for source AIDE canonical records and a reviewed pack.

Blocked: automatic branch dispatch, repair apply, checkpoint promotion, and more
Eureka product expansion before validation tiering.
