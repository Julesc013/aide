# Prompt

Create and process `AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01`.

Implement deterministic local authorization evaluation and persistence over the
accepted trust contracts and Local Service.

Evaluate:

```text
Principal
+ AdmissionRecord
+ PolicyDecision
+ CapabilityGrant
+ DelegationRecord
+ RevocationRecord
+ requested operation
-> AuthorizationEvaluation
```

Enforce principal active, exact implementation admission, digest match,
capability admission, policy allow, active grant, no expiry or revocation, use
budget, workspace/resource/mode/effect match, network and secret limits,
delegation bounds, and required features.

Persist the evaluation object, policy/grant refs, evaluation event, and atomic
bounded-use consumption.

Stop at `needs_review` with proposed capability:

```text
local_trust_enforcement_v0
```

Recommended next task:

```text
AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01
```
