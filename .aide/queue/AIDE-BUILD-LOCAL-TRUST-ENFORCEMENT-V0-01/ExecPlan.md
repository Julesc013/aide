# AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01 ExecPlan

## Objective

Build a deterministic local trust enforcement slice over the accepted trust
contract and accepted local Service foundation.

## Scope

The implementation is limited to a local service module, AIDE Lite fixture
commands, focused tests, generated reports, this task packet, queue index, and
root plan/log updates.

## Design

- Reuse `core.protocol.trust_authorization.evaluate_authorization` for the
  authorization decision.
- Persist Principal, AdmissionRecord, PolicyDecision, CapabilityGrant,
  DelegationRecord, AuthorizationEvaluation, and trust events into the local
  SQLite Service.
- Consume the one-use grant in the same local SQLite transaction as the
  evaluation event and idempotency record.
- Refuse a second final-use attempt once the stored grant is consumed.
- Keep fixture state temporary and uncommitted.

## Validation

Run focused local trust tests, fixture/status/validate commands, trust and
local Service regressions, compileall, task inspect/evidence, broad validation,
diff checks, and path/secret scans.

## Result

PASS_WITH_WARNINGS. The proposed capability is
`local_trust_enforcement_v0`; the next task is
`AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01`.
