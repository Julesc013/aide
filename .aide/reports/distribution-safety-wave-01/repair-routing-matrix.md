# Repair Routing Matrix

Checks must not silently repair implementation.

| Condition | Route |
| --- | --- |
| material findings | `AIDE-BUILD-<OBJECT>-REPAIR-01` |
| missing evidence only | `AIDE-BUILD-<OBJECT>-EVIDENCE-REPAIR-01` |
| stale queue, index, or root logs only | `AIDE-BUILD-<OBJECT>-BOOKKEEPING-REPAIR-01` |
| predecessor not accepted | `AIDE-UNBLOCK-<OBJECT>-PREDECESSOR-01` |
| policy ambiguity | `AIDE-UNBLOCK-<OBJECT>-POLICY-01` |
| missing fixture authority | `AIDE-UNBLOCK-<OBJECT>-FIXTURE-AUTHORITY-01` |
| validation infrastructure failure | `AIDE-UNBLOCK-<OBJECT>-VALIDATION-INFRA-01` |
| source-output misuse risk | `AIDE-BUILD-<OBJECT>-SOURCE-BOUNDARY-REPAIR-01` |

Repair tasks must have their own task packet, evidence, validation, commit, and independent repair check before acceptance.
