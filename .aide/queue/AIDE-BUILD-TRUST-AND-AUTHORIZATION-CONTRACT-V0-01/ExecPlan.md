# AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01 ExecPlan

## Objective

Build `trust_and_authorization_contract_v0` as a projection-only contract for
principals, exact implementation admission, policy decisions, bounded grants,
delegation, revocation, and deterministic authorization evaluation.

## Scope

This build adds protocol helpers, schemas, AIDE Lite `trust` status/project/
validate commands, focused tests, deterministic reports, and task evidence.

No live enforcement, identity provider, credentials, secret store, Service,
worker execution, transaction approval, provider/model/network behavior,
preview/apply/rollback, repository mutation, GitHub mutation, release, or
promotion is authorized.

## Plan

1. Add projection-only trust and authorization protocol helper.
2. Add seven Draft 2020-12 schema files for the record kinds.
3. Add `trust status`, `trust project`, and `trust validate` command surfaces.
4. Add focused tests for schema/helper alignment, negative authorization matrix,
   no embedded credentials, unknown required capabilities, deterministic
   projections, and parser rejection of live enforcement commands.
5. Generate deterministic reports under `.aide/reports/trust-authorization-contract-v0/`.
6. Materialize queue evidence and route to the independent check.
7. Run focused tests, compile checks, direct CLI checks, regression tests, broad
   validation, diff checks, leak scans, and commit policy.

## Exit Criteria

Stop at `needs_review` with:

```text
result: PASS_WITH_WARNINGS
proposed_capability: trust_and_authorization_contract_v0
missing_evidence: 0
recommended_next_task: AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```
