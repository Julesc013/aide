# AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

Create and process `AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01`.

Define portable, projection-only trust and authorization contracts required
before AIDE can authorize non-fixture capabilities or WorkerRuns.

Proposed capability:

```text
trust_and_authorization_contract_v0
```

Required records:

- Principal
- AdmissionRecord
- PolicyDecision
- CapabilityGrant
- DelegationRecord
- RevocationRecord
- AuthorizationEvaluation

Required boundaries:

- no live enforcement
- no identity provider
- no credentials
- no secrets
- no OIDC/IAM
- no Service
- no worker execution
- no transaction approval
- no provider/model/network calls
- no preview/apply/rollback
- no repository, branch/worktree, GitHub, release, or promotion mutation

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```
