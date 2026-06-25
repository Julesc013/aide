# AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01

Acceptance-only.

Accept exactly:

```text
trust_and_authorization_contract_v0
```

Accepted meaning:

```text
AIDE has portable projection-only contracts for principals, exact implementation
admission, policy decisions, bounded capability grants, delegation, revocation,
and deterministic authorization evaluation.
```

Do not accept or claim:

- live identity;
- live policy engine;
- live grants;
- credentials;
- secrets;
- OIDC/IAM;
- runtime enforcement;
- worker execution;
- transaction approval;
- Service/runtime behavior;
- provider/model/network calls;
- preview/apply/rollback;
- repository mutation;
- branch/worktree or GitHub mutation;
- release or promotion.

Stop at `needs_review` with:

```text
result: ACCEPTED_WITH_WARNINGS
accepted_capability: trust_and_authorization_contract_v0
```

Recommend exactly:

```text
AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
```
