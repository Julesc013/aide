# Warning Disposition

## Result

`ACCEPTED_WITH_WARNINGS`

The acceptance gate records 11 non-blocking warning dispositions.

| id | source | accepted | rationale | next_task |
| --- | --- | --- | --- | --- |
| DKT-003 | build findings | true | Policy sequence drift is real but does not undermine observer behavior. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-004 | build findings | true | Reference doc sequence drift is documentation debt, not an observer blocker. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-005 | build findings | true | Latest task packet is a stale projection and remains non-canonical. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-006 | build findings | true | OKF next-work staleness is projection debt; OKF regeneration is deferred. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-007 | build findings | true | OKF queue current-state drift is projection debt. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-008 | build findings | true | OKF source-hash drift is evidence-backed and deferred. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-009 | build findings | true | README Reconciler status drift is docs-truth debt. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-010 | build findings | true | DOCUMENTATION status drift is docs-truth debt. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| DKT-011 | build findings | true | Selected path-reference risk is warning-class debt and no references are rewritten here. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| CHECK-DKT-001 | check findings | true | Reduced review independence is recorded; check was mechanical and evidence-based. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |
| QUEUE-CRLF-001 | validation | true | Existing queue-index line-ending warning is non-blocking and not normalized by this task. | AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01 |

No accepted warning blocks B1 wave continuation.
