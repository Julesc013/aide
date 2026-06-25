# Fixture Matrix

Positive fixtures:

- Principal
- AdmissionRecord
- PolicyDecision
- CapabilityGrant
- DelegationRecord
- RevocationRecord
- AuthorizationEvaluation

Negative authorization fixtures cover every required refusal code listed in
`refusal-code-registry.md`.

The focused test suite verifies the complete matrix through
`trust_authorization.negative_evaluation_matrix()`.
