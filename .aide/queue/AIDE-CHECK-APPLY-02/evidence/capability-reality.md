# Capability Reality

## Approved Labels

The checkpoint supports these labels for AIDE-APPLY-02:

- implemented
- tested
- fixture-tested
- report-backed
- review-gated
- needs repair

## Prohibited Labels

The checkpoint does not approve:

- production-ready
- release-ready
- target-repo capable
- broad active-repo apply capable
- install-capable
- upgrade-capable
- repair-capable
- rollback/uninstall-capable
- accepted with notes

## Overclaim Review

No material overclaim was found in task status, policy, docs, reports, or evidence. The checked files consistently preserve `production_ready: false`, `release_ready: false`, target repo mutation false, broad active-repo apply false, and forbidden-operation boundaries.

## Remaining Gates

Before acceptance, `AIDE-APPLY-02-REPAIR-01` should address the runnable example validation failure, resolved target safety, apply-mode partial mutation risk, and direct core report self-reference issue. A follow-up checkpoint should then rerun the validation matrix.
