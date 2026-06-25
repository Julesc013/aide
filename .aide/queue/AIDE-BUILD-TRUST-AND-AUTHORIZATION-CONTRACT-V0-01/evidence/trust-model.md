# Trust Model

The contract defines projection-only trust records:

- `Principal`
- `AdmissionRecord`
- `PolicyDecision`
- `CapabilityGrant`
- `DelegationRecord`
- `RevocationRecord`
- `AuthorizationEvaluation`

The model separates installed components, conformance evidence, admission,
policy, grants, delegation, revocation, and authorization evaluation.

No live identity provider, credential exchange, secret store, Service, or
runtime enforcement is implemented.
