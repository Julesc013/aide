# Persistence And Event Review

The evidence-local harness used fresh temporary local Service state and
inspected `state.sqlite` directly through `sqlite3`.

Observed persisted object kinds:

```text
AdmissionRecord
AuthorizationEvaluation
CapabilityGrant
DelegationRecord
PolicyDecision
Principal
```

Observed event sequence and types:

```text
1 trust.authorization_evaluated
2 trust.grant_consumed
```

The stored grant version advanced to `2`, status became `consumed`, remaining
uses became `0`, and only one idempotency key was recorded.
