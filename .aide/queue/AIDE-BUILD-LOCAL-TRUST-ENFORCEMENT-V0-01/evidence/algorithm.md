# Algorithm

1. Build deterministic fixture Principal, AdmissionRecord, PolicyDecision,
   CapabilityGrant, DelegationRecord, no RevocationRecord, and requested
   operation records from the accepted trust contract helpers.
2. Evaluate with `trust_authorization.evaluate_authorization`.
3. Validate the AuthorizationEvaluation record with the accepted trust helper.
4. Persist support records, AuthorizationEvaluation, evaluation event, grant
   consumption event, and idempotency record through a local SQLite transaction.
5. Reopen the local Service state and verify persisted evaluation, events, and
   consumed grant.
6. Replay the same idempotency key and verify no second event is appended.
7. Attempt a different idempotency key after final-use consumption and verify
   `grant_exhausted`.
