# Trust And Authorization Contract Projection

- status: PASS_WITH_WARNINGS
- task_id: AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
- capability_label: trust_and_authorization_contract_v0
- projection_only: true
- live_identity_implemented: false
- live_policy_engine_implemented: false
- live_grants_implemented: false
- credentials_embedded: false
- secrets_embedded: false
- runtime_enforcement_implemented: false
- provider_or_model_calls: none
- network_calls: none
- recommended_next_task: AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

## Projections Written

- .aide/reports/trust-authorization-contract-v0/projections/principal.json
- .aide/reports/trust-authorization-contract-v0/projections/admission-record.json
- .aide/reports/trust-authorization-contract-v0/projections/policy-decision.json
- .aide/reports/trust-authorization-contract-v0/projections/capability-grant.json
- .aide/reports/trust-authorization-contract-v0/projections/delegation-record.json
- .aide/reports/trust-authorization-contract-v0/projections/revocation-record.json
- .aide/reports/trust-authorization-contract-v0/projections/authorization-evaluation.json

## Refusal Codes

- principal_unknown
- principal_inactive
- implementation_not_admitted
- implementation_digest_mismatch
- capability_not_admitted
- policy_denied
- approval_required
- grant_missing
- grant_inactive
- grant_expired
- grant_revoked
- grant_exhausted
- workspace_scope_mismatch
- resource_scope_mismatch
- execution_mode_not_granted
- effect_not_granted
- network_not_granted
- secret_not_granted
- delegation_not_allowed
- delegation_scope_widening
- delegation_expired
- required_feature_unsupported
