# Next Task Prompt

```text
Create and process AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01.

Accept exactly local_trust_enforcement_v0 after
AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01 and
AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01 both report PASS_WITH_WARNINGS,
material_finding_count: 0, and missing_evidence: 0.

Do not accept external IAM, credentials, secrets, OIDC, remote policy engines,
process launch, worker execution, transaction approval, provider/model calls,
network calls, preview/apply/rollback, repository mutation, GitHub mutation,
release, or promotion.

Stop at needs_review and recommend exactly:
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
```
