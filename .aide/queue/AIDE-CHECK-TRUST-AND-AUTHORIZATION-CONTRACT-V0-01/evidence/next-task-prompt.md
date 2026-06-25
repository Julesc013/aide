# Next Task Prompt

```text
Create and process
AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01.

Repo truth outranks this prompt. Read governing queue policy, the trust build
task, the trust check task, all source/check evidence, PLANS.md, IMPLEMENT.md,
and current repository state before writing anything.

This is acceptance-only.

Accept exactly:

trust_and_authorization_contract_v0

Accepted meaning:

AIDE has portable projection-only contracts for principals, exact implementation
admission, policy decisions, bounded capability grants, delegation, revocation,
and deterministic authorization evaluation.

Do not accept or claim:

- live identity
- live policy engine
- live grants
- credentials
- secrets
- OIDC/IAM
- runtime enforcement
- worker execution
- transaction approval
- Service/runtime behavior
- provider/model/network calls
- preview/apply/rollback
- repository mutation
- branch/worktree or GitHub mutation
- release or promotion

Verify source build and independent check both report PASS_WITH_WARNINGS,
material_finding_count 0, missing_evidence 0, scrubbed reports/evidence, and
complete references.

Stop at needs_review with:

result: ACCEPTED_WITH_WARNINGS
accepted_capability: trust_and_authorization_contract_v0

Recommend exactly:

AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01
```
