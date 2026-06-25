# Authorization Evaluation

`AuthorizationEvaluation` deterministically projects the result of evaluating:

```text
Principal
+ AdmissionRecord
+ PolicyDecision
+ CapabilityGrant
+ DelegationRecord
+ RevocationRecord
+ requested operation
```

The helper fixture checks principal state, exact implementation admission,
implementation digest, capability admission, policy, active grant, expiry,
revocation, use budget, workspace, resources, mode, effects, network, secrets,
delegation, and required features.

This is projection logic for contract fixtures, not live enforcement.
